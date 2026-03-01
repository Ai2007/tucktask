"""
seed.py – One-time script to populate the database from input.json.

Run this before starting the API server:
    python seed.py
"""

import database
import parser

JSON_PATH = "input.json"


def seed() -> None:
    database.init_db()
    content = parser.parse_gpt_output(JSON_PATH)
    database.set_content(content)
    print(f"Database seeded successfully ({len(content):,} characters written).")


if __name__ == "__main__":
    seed()
