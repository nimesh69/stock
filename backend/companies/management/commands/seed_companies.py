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
    "name": "Nerude Mirmire Laghubitta Bittiya Sanstha Limited",
    "sector": "Microfinance",
    "aliases": [
        "NMLBBL",
        "Nerude Mirmire Laghubitta",
        "Nerude Mirmire Laghubitta Bittiya Sanstha",
        "Nerude Mirmire Laghubitta Bittiya Sanstha Limited",
    ],
    "description": (
        "Microfinance company in Nepal providing "
        "microfinance and financial services."
    ),
},
{
        "symbol": "EBL",
        "name": "Everest Bank Limited",
        "sector": "Commercial Bank",
        "aliases": [
            "Everest",
            "Everest Bank",
            "Everest Bank Limited",
            "EBL",
        ],
        "description": (
            "Leading commercial bank in Nepal known for steady dividend "
            "payouts and joint venture with Punjab National Bank."
        ),
    },
    {
        "symbol": "NICA",
        "name": "NIC Asia Bank Limited",
        "sector": "Commercial Bank",
        "aliases": [
            "NIC Asia",
            "NIC Asia Bank",
            "NIC Asia Bank Limited",
            "NICA",
        ],
        "description": (
            "One of Nepal's largest commercial banks by branch network and asset size."
        ),
    },
    {
        "symbol": "SCB",
        "name": "Standard Chartered Bank Nepal Limited",
        "sector": "Commercial Bank",
        "aliases": [
            "Standard Chartered",
            "Standard Chartered Bank",
            "Standard Chartered Nepal",
            "SCB",
        ],
        "description": (
            "International commercial bank in Nepal with strong capital position and consistent returns."
        ),
    },
    {
        "symbol": "SHL",
        "name": "Soaltee Hotel Limited",
        "sector": "Hotels And Tourism",
        "aliases": [
            "Soaltee",
            "Soaltee Hotel",
            "Soaltee Hotel Limited",
            "SHL",
        ],
        "description": (
            "Premier five-star hotel and hospitality company listed on NEPSE."
        ),
    },
    {
        "symbol": "HDL",
        "name": "Himalayan Distillery Limited",
        "sector": "Manufacturing And Processing",
        "aliases": [
            "Himalayan Distillery",
            "Himalayan Distillery Limited",
            "HDL",
        ],
        "description": (
            "Top alcoholic beverage manufacturer in Nepal known for high retail investor demand."
        ),
    },
    {
        "symbol": "NTC",
        "name": "Nepal Doorsanchar Company Limited",
        "sector": "Others",
        "aliases": [
            "Nepal Telecom",
            "NTC",
            "Nepal Doorsanchar",
            "Nepal Doorsanchar Company Limited",
        ],
        "description": (
            "State-owned telecommunications giant, one of the largest market cap stocks in NEPSE."
        ),
    },
    {
        "symbol": "SAHAS",
        "name": "Sahas Urja Limited",
        "sector": "Hydro Power",
        "aliases": [
            "Sahas",
            "Sahas Urja",
            "Sahas Urja Limited",
            "SAHAS",
        ],
        "description": (
            "Prominent hydropower project developer trading actively in NEPSE."
        ),
    },
    {
        "symbol": "CBBL",
        "name": "Chhimek Laghubitta Bittiya Sanstha Limited",
        "sector": "Microfinance",
        "aliases": [
            "Chhimek",
            "Chhimek Laghubitta",
            "Chhimek Microfinance",
            "CBBL",
        ],
        "description": (
            "One of Nepal's leading microfinance institutions with strong financial health."
        ),
    },
    {
        "symbol": "CIT",
        "name": "Citizen Investment Trust",
        "sector": "Investment",
        "aliases": [
            "CIT",
            "Citizen Investment Trust",
            "Nagarik Lagani Kosh",
        ],
        "description": (
            "Statutory institutional investment manager in Nepal offering retirement funds and capital market services."
        ),
    },
    {
        "symbol": "MNBBL",
        "name": "Muktinath Bikas Bank Limited",
        "sector": "Development Bank",
        "aliases": [
            "Muktinath",
            "Muktinath Bikas Bank",
            "Muktinath Bikas Bank Limited",
            "MNBBL",
        ],
        "description": (
            "Largest national-level development bank in Nepal by market presence and deposit base."
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
