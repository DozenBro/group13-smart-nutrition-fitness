import csv
from decimal import Decimal
from pathlib import Path
from sqlalchemy import select
from backend.database import SessionLocal
from backend.models import Food

DEFAULT_CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "vietnamese_foods.csv"


def load_foods_from_csv(csv_path: Path = DEFAULT_CSV_PATH) -> list[dict]:
    items = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                "name": row["name"].strip(),
                "portion_desc": row["portion_desc"].strip(),
                "calories": Decimal(row["calories"]),
                "protein_g": Decimal(row["protein_g"]),
                "carbs_g": Decimal(row["carbs_g"]),
                "fat_g": Decimal(row["fat_g"]),
                "price_vnd": int(row["price_vnd"]),
                "meal_slot": row["meal_slot"].strip(),
                "preference_tags": row["preference_tags"].strip() or None,
                "nutrition_source": row["nutrition_source"].strip(),
                "price_source": row["price_source"].strip(),
            })
    return items


def seed_foods(csv_path: Path = DEFAULT_CSV_PATH) -> int:
    items = load_foods_from_csv(csv_path)
    with SessionLocal() as db:
        added = 0
        for item in items:
            exists = db.execute(
                select(Food).where(Food.name == item["name"])
            ).scalar_one_or_none()
            if not exists:
                db.add(Food(**item))
                added += 1
        db.commit()
        print(f"Seeded {added} new food items from {csv_path.name}.")
        return added


if __name__ == "__main__":
    seed_foods()