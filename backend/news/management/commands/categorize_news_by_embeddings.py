import math

from django.core.management import call_command
from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer

from companies.models import CompanyEmbedding
from news.models import ArticleCategory, ArticleEmbedding, RawArticle


class Command(BaseCommand):
    help = "Generate article embeddings and tag articles by company similarity."

    def add_arguments(self, parser):
        parser.add_argument(
            "--threshold",
            type=float,
            default=0.7,
            help="Minimum cosine similarity required to store a company tag.",
        )

    def handle(self, *args, **options):
        threshold = options["threshold"]
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

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
        created_embeddings = 0
        created_categories = 0

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

            for company_embedding in company_embeddings:
                confidence = self.cosine_similarity(
                    article_vector,
                    list(company_embedding.embedding),
                )

                if confidence < threshold:
                    continue

                ArticleCategory.objects.update_or_create(
                    article=article,
                    company=company_embedding.company,
                    defaults={
                        "confidence": confidence,
                        "method": "embedding",
                    },
                )
                created_categories += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Processed "
                f"{created_embeddings} article embeddings and "
                f"{created_categories} article-company categories."
            )
        )

    def build_article_text(self, article):
        return f"{article.headline}\n\n{article.body[:4000]}"

    def cosine_similarity(self, first, second):
        dot_product = sum(a * b for a, b in zip(first, second))
        first_norm = math.sqrt(sum(a * a for a in first))
        second_norm = math.sqrt(sum(b * b for b in second))

        if not first_norm or not second_norm:
            return 0.0

        return dot_product / (first_norm * second_norm)
