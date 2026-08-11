import math
import re

from django.core.management import call_command
from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer

from companies.models import CompanyEmbedding
from news.models import ArticleCategory, ArticleEmbedding, RawArticle


class Command(BaseCommand):
    help = "Generate article embeddings and categorize articles by company."

    def add_arguments(self, parser):
        parser.add_argument(
            "--threshold",
            type=float,
            default=0.55,
            help="Minimum final score required to create a company category.",
        )
        parser.add_argument(
            "--embedding-floor",
            type=float,
            default=0.45,
            help="Minimum raw embedding similarity to consider at all.",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--debug-company",
            type=str,
            default=None,
        )
        parser.add_argument(
            "--sample",
            type=int,
            default=0,
        )

    def handle(self, *args, **options):
        threshold = options["threshold"]
        embedding_floor = options["embedding_floor"]
        debug = options["debug"]
        debug_company = (options["debug_company"] or "").lower()
        sample = options["sample"]

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        if not CompanyEmbedding.objects.exists():
            call_command("generate_company_embeddings")

        company_embeddings = list(
            CompanyEmbedding.objects.select_related("company")
        )

        if not company_embeddings:
            self.stdout.write(
                self.style.WARNING("No company embeddings available.")
            )
            return

        articles = RawArticle.objects.all()
        if sample:
            articles = articles[:sample]

        created_embeddings = 0
        created_categories = 0

        stats = {
            "below_floor": 0,
            "no_match_below_threshold": 0,
            "headline_symbol": 0,
            "headline_name": 0,
            "headline_alias": 0,
            "body_symbol_name": 0,
            "body_alias": 0,
            "embedding_only": 0,
        }

        for article in articles:
            source_text = self.build_article_text(article)
            article_vector = model.encode(source_text).tolist()

            ArticleEmbedding.objects.update_or_create(
                article=article,
                defaults={
                    "embedding": article_vector,
                    "source_text": source_text,
                },
            )
            created_embeddings += 1

            ArticleCategory.objects.filter(article=article).delete()

            for company_embedding in company_embeddings:
                company = company_embedding.company
                company_key = (
                    f"{company.symbol or ''} {company.name or ''}"
                ).lower()
                show_debug = (
                    debug
                    and (not debug_company or debug_company in company_key)
                )

                result = self.calculate_company_score(
                    article=article,
                    company_embedding=company_embedding,
                    article_vector=article_vector,
                    threshold=threshold,
                    embedding_floor=embedding_floor,
                )

                if show_debug:
                    self._log_debug(article, company, result)

                if result["rejected"]:
                    reason = result["reject_reason"]
                    if reason == "below_floor":
                        stats["below_floor"] += 1
                    elif reason == "below_threshold":
                        stats["no_match_below_threshold"] += 1
                    continue

                ArticleCategory.objects.create(
                    article=article,
                    company=company,
                    confidence=result["score"],
                    method=result["method"],
                )
                created_categories += 1

                method = result["method"]
                if method == "hybrid_headline_symbol":
                    stats["headline_symbol"] += 1
                elif method == "hybrid_headline_name":
                    stats["headline_name"] += 1
                elif method == "hybrid_headline_alias":
                    stats["headline_alias"] += 1
                elif method == "hybrid_body":
                    stats["body_symbol_name"] += 1
                elif method == "hybrid_body_alias":
                    stats["body_alias"] += 1
                else:
                    stats["embedding_only"] += 1

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("CATEGORIZATION SUMMARY")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Articles processed: {created_embeddings}")
        self.stdout.write(f"Categories created: {created_categories}")
        self.stdout.write(f"  - Headline symbol match: {stats['headline_symbol']}")
        self.stdout.write(f"  - Headline name match:   {stats['headline_name']}")
        self.stdout.write(f"  - Headline alias match:  {stats['headline_alias']}")
        self.stdout.write(f"  - Body symbol/name match:{stats['body_symbol_name']}")
        self.stdout.write(f"  - Body alias match:      {stats['body_alias']}")
        self.stdout.write(f"  - Embedding only:        {stats['embedding_only']}")
        self.stdout.write(f"Rejected (below floor):    {stats['below_floor']}")
        self.stdout.write(f"Rejected (below threshold):{stats['no_match_below_threshold']}")

        if created_categories == 0:
            self.stdout.write(
                self.style.WARNING(
                    "\nZero categories created. Try lowering --threshold or "
                    "--embedding-floor."
                )
            )

    def _log_debug(self, article, company, result):
        self.stdout.write(
            f"\n--- {article.headline[:50] if article.headline else '(no headline)'}... "
            f"| {company.symbol or company.name} ---"
        )
        self.stdout.write(f"  embedding: {result['embedding']:.3f}")
        self.stdout.write(f"  boost:     {result['boost']:.2f}")
        self.stdout.write(f"  final:     {result['score']:.3f}")
        self.stdout.write(f"  method:    {result['method']}")
        if result["rejected"]:
            self.stdout.write(f"  → REJECTED: {result['reject_reason']}")

    def build_article_text(self, article):
        return (
            f"{article.headline or ''}\n\n"
            f"{article.body[:4000] if article.body else ''}"
        )

    def calculate_company_score(
        self,
        article,
        company_embedding,
        article_vector,
        threshold,
        embedding_floor,
    ):
        company = company_embedding.company
        headline = (article.headline or "").lower()
        body = (article.body or "").lower()

        symbol = (company.symbol or "").strip()
        name = (company.name or "").strip()

        # Exact match detection
        symbol_headline = bool(symbol) and self.contains_term(headline, symbol)
        symbol_body = bool(symbol) and self.contains_term(body, symbol)
        name_headline = bool(name) and self.contains_term(headline, name)
        name_body = bool(name) and self.contains_term(body, name)

        alias_terms = [
            term.strip()
            for term in (company.aliases or [])
            if term and term.strip()
            and term.strip().lower() != symbol.lower()
            and term.strip().lower() != name.lower()
        ]
        alias_headline = any(
            self.contains_term(headline, term) for term in alias_terms
        )
        alias_body = any(
            self.contains_term(body, term) for term in alias_terms
        )

        # Embedding score
        embedding_score = self.cosine_similarity(
            article_vector,
            list(company_embedding.embedding),
        )

        # Hard floor: completely unrelated articles get rejected immediately
        if embedding_score < embedding_floor:
            return {
                "embedding": embedding_score,
                "score": 0.0,
                "method": "embedding",
                "boost": 1.0,
                "rejected": True,
                "reject_reason": "below_floor",
            }

        # Determine boost and method
        if symbol_headline:
            boost = 1.20
            method = "hl_sym"
        elif name_headline:
            boost = 1.15
            method = "hl_name"
        elif alias_headline:
            boost = 1.10
            method = "hl_alias"
        elif symbol_body or name_body:
            boost = 1.05
            method = "body"
        elif alias_body:
            boost = 1.02
            method = "body_alias"
        else:
            boost = 1.0
            method = "embedding"

        final_score = min(1.0, embedding_score * boost)

        # Penalize weak embeddings even with exact match
        # (prevents "Apple pie" from matching Apple Inc.)
        if embedding_score < 0.45 and method.startswith("hybrid_body"):
            final_score = final_score * 0.8

        if final_score < threshold:
            return {
                "embedding": embedding_score,
                "score": final_score,
                "method": method,
                "boost": boost,
                "rejected": True,
                "reject_reason": "below_threshold",
            }

        return {
            "embedding": embedding_score,
            "score": final_score,
            "method": method,
            "boost": boost,
            "rejected": False,
            "reject_reason": None,
        }

    def contains_term(self, text, term):
        if not term:
            return False
        pattern = rf"\b{re.escape(term.strip().lower())}\b"
        return bool(re.search(pattern, text, re.IGNORECASE))

    def cosine_similarity(self, first, second):
        dot_product = sum(a * b for a, b in zip(first, second))
        first_norm = math.sqrt(sum(a * a for a in first))
        second_norm = math.sqrt(sum(b * b for b in second))
        if not first_norm or not second_norm:
            return 0.0
        return dot_product / (first_norm * second_norm)