"""
companies/management/commands/seed_companies.py

Run with: python manage.py seed_companies

Picks 5 companies across distinct sectors (satisfies the assignment's
"mix of sectors" requirement) using real symbols confirmed to exist on
sharesansar.com's today-share-price table.
"""

from django.core.management.base import BaseCommand
from companies.models import Company
WATCHLIST = [
    {
        "symbol": "NABIL",
        "name": "Nabil Bank Limited",
        "sector": "Commercial Bank",
        "aliases": [
            "Nabil",
            "Nabil Bank",
            "Nabil Bank Limited",
            "NABIL",
        ],
        "description": (
            "Commercial bank in Nepal providing banking "
            "and financial services."
        ),
    },
    {
        "symbol": "CHCL",
        "name": "Chilime Hydropower Company Limited",
        "sector": "Hydropower",
        "aliases": [
            "Chilime",
            "Chilime Hydropower",
            "Chilime Hydropower Company",
            "Chilime Hydropower Company Limited",
            "CHCL",
        ],
        "description": (
            "Hydropower company in Nepal involved in "
            "electricity generation."
        ),
    },
    {
        "symbol": "NLIC",
        "name": "Nepal Life Insurance Company Limited",
        "sector": "Life Insurance",
        "aliases": [
            "Nepal Life",
            "Nepal Life Insurance",
            "Nepal Life Insurance Company",
            "Nepal Life Insurance Company Limited",
            "NLIC",
        ],
        "description": (
            "Life insurance company in Nepal providing "
            "life insurance services."
        ),
    },
    {
        "symbol": "SHIVM",
        "name": "Shivam Cements Limited",
        "sector": "Manufacturing and Processing",
        "aliases": [
            "Shivam",
            "Shivam Cement",
            "Shivam Cements",
            "Shivam Cements Limited",
            "SHIVM",
        ],
        "description": (
            "Cement manufacturing company in Nepal."
        ),
    },
    {
        "symbol": "ICFC",
        "name": "ICFC Finance Limited",
        "sector": "Finance",
        "aliases": [
            "ICFC",
            "ICFC Finance",
            "ICFC Finance Limited",
        ],
        "description": (
            "Finance company in Nepal providing "
            "financial services."
        ),
    },
    {
        "symbol": "MLBSL",
        "name": "Mithila Laghubitta Bittiya Sanstha Limited",
        "sector": "Microfinance",
        "aliases": [
            "MLBSL",
            "Mithila Laghubitta",
            "Mithila Laghubitta Bittiya Sanstha",
            "Mithila Laghubitta Bittiya Sanstha Limited",
        ],
        "description": (
            "Microfinance company in Nepal providing "
            "microfinance and financial services."
        ),
    },
    {
        "symbol": "SGHL",
        "name": "Sanigad Hydro Limited",
        "sector": "Hydropower",
        "aliases": [
            "SGHL",
            "Sanigad Hydro",
            "Sanigad Hydropower",
            "Sanigad Hydro Limited",
        ],
        "description": (
            "Hydropower company in Nepal involved in "
            "hydroelectricity generation."
        ),
    },
    {
        "symbol": "NMLBBL",
        "name": "NMB Laghubitta Bittiya Sanstha Limited",
        "sector": "Microfinance",
        "aliases": [
            "NMLBBL",
            "NMB Laghubitta",
            "NMB Laghubitta Bittiya Sanstha",
            "NMB Laghubitta Bittiya Sanstha Limited",
        ],
        "description": (
            "Microfinance company in Nepal providing "
            "microfinance and financial services."
        ),
    },
]


class Command(BaseCommand):
    help = "Seeds the 5-company watchlist used across crawling, categorization, and analysis."

    def handle(self, *args, **options):
        created_count = 0

        for entry in WATCHLIST:
            _, created = Company.objects.update_or_create(
                symbol=entry["symbol"],
                defaults={
                    "name": entry["name"],
                    "sector": entry["sector"],
                    "aliases": entry["aliases"],
                    "description": entry["description"],
                },
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created_count} new companies "
                f"(watchlist total: {len(WATCHLIST)})."
            )
        )
