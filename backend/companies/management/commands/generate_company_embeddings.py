from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer

from companies.models import Company, CompanyEmbedding


class Command(BaseCommand):

    help = "Generate embeddings for companies"

    def handle(self, *args, **options):

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        companies = Company.objects.all()

        for company in companies:

            text = self.build_company_text(company)

            vector = model.encode(text).tolist()

            CompanyEmbedding.objects.update_or_create(
                company=company,
                defaults={
                    "embedding": vector,
                    "source_text": text,
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Generated embedding: {company.symbol}"
                )
            )

    def build_company_text(self, company):

        aliases = ", ".join(company.aliases)

        return f"""
        Company name: {company.name}
        Stock symbol: {company.symbol}
        Sector: {company.sector}
        Aliases: {aliases}
        Description: {company.description}
        """