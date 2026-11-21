from decimal import Decimal
from sqlalchemy import select
from backend.database import SessionLocal
from backend.models import Food

SAMPLE_FOODS = [
    {
        "name": "Phở bò tái (Rare Beef Pho)",
        "portion_desc": "1 medium bowl (~450g)",
        "calories": Decimal("430.00"),
        "protein_g": Decimal("24.00"),
        "carbs_g": Decimal("58.00"),
        "fat_g": Decimal("11.00"),
        "price_vnd": 45000,
        "meal_slot": "breakfast,lunch,dinner",
        "preference_tags": "no-pork",
        "nutrition_source": "Vietnam National Institute of Nutrition (NIN)",
        "price_source": "Hanoi street food average 2026",
    },
    {
        "name": "Cơm tấm sườn bì chả (Broken Rice with Pork Chop)",
        "portion_desc": "1 standard plate (~400g)",
        "calories": Decimal("620.00"),
        "protein_g": Decimal("28.00"),
        "carbs_g": Decimal("75.00"),
        "fat_g": Decimal("22.00"),
        "price_vnd": 45000,
        "meal_slot": "lunch,dinner",
        "preference_tags": "high-calorie",
        "nutrition_source": "Vietnam National Institute of Nutrition (NIN)",
        "price_source": "Local restaurant average 2026",
    },
    {
        "name": "Ức gà luộc (Boiled Chicken Breast)",
        "portion_desc": "150g lean meat",
        "calories": Decimal("248.00"),
        "protein_g": Decimal("46.50"),
        "carbs_g": Decimal("0.00"),
        "fat_g": Decimal("5.40"),
        "price_vnd": 20000,
        "meal_slot": "lunch,dinner",
        "preference_tags": "high-protein,low-carb,no-pork",
        "nutrition_source": "USDA FoodData Central / NIN",
        "price_source": "Supermarket retail 2026",
    },
]


def seed_foods() -> int:
    with SessionLocal() as db:
        added = 0
        for item in SAMPLE_FOODS:
            exists = db.execute(
                select(Food).where(Food.name == item["name"])
            ).scalar_one_or_none()
            if not exists:
                db.add(Food(**item))
                added += 1
        db.commit()
        print(f"Seeded {added} new food items.")
        return added


if __name__ == "__main__":
    seed_foods()