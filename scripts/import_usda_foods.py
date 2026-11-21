import csv
from pathlib import Path

USDA_DIR = Path(r"D:\HUST\2026A\Software\FoodData_Central_sr_legacy_food_csv_2018-04")
OUTPUT_CSV = Path(__file__).resolve().parents[1] / "data" / "vietnamese_foods.csv"

# USDA SR Legacy nutrient IDs
NUTRIENT_MAP = {
    "1008": "calories",
    "1003": "protein_g",
    "1005": "carbs_g",
    "1004": "fat_g",
}

# Select practical everyday categories and map to meal_slot, tags, and estimated VND per 100g
CATEGORY_RULES = {
    "1": ("breakfast,snack", "vegetarian,no-pork", 12000),            # Dairy and Egg Products
    "5": ("lunch,dinner", "high-protein,low-carb,no-pork", 18000),    # Poultry Products
    "9": ("breakfast,snack", "vegetarian,vegan,low-fat,no-pork", 10000), # Fruits and Fruit Juices
    "10": ("lunch,dinner", "high-protein,low-carb", 18000),           # Pork Products
    "11": ("lunch,dinner", "vegetarian,vegan,low-calorie,no-pork", 8000), # Vegetables
    "12": ("snack", "vegetarian,vegan,no-pork", 15000),               # Nut and Seed Products
    "13": ("lunch,dinner", "high-protein,low-carb,no-pork", 30000),   # Beef Products
    "15": ("lunch,dinner", "high-protein,low-carb,no-pork,seafood", 25000), # Finfish and Shellfish
    "16": ("lunch,dinner", "vegetarian,vegan,high-protein,no-pork", 10000), # Legumes
    "20": ("breakfast,lunch,dinner", "vegetarian,vegan,no-pork", 8000), # Cereal Grains and Pasta
}

# Keep common, clean items (avoid baby food, obscure organ meats, raw game, etc.)
INCLUDE_KEYWORDS = (
    "chicken", "turkey", "beef", "pork", "salmon", "tuna", "shrimp", "tilapia", "cod", "mackerel",
    "egg", "milk", "yogurt", "cheese", "rice", "oats", "oatmeal", "bread", "pasta", "noodles",
    "potato", "sweet potato", "corn", "broccoli", "spinach", "cabbage", "carrot", "tomato",
    "cucumber", "lettuce", "onion", "garlic", "mushroom", "asparagus", "cauliflower", "pumpkin",
    "banana", "apple", "orange", "mango", "pineapple", "watermelon", "papaya", "guava", "avocado",
    "strawberry", "blueberry", "grape", "pear", "tofu", "soybeans", "lentils", "chickpeas",
    "black beans", "kidney beans", "peanuts", "almonds", "walnuts", "cashew", "chia seeds",
)

EXCLUDE_KEYWORDS = (
    "babyfood", "infant", "raw", "uncooked", "fat only", "separable fat", "skin only",
    "giblets", "liver", "kidney", "brain", "heart", "tongue", "tripe", "chitterlings",
    "canned", "frozen", "fast foods", "restaurant", "mcdonald", "burger king", "kfc",
    "candies", "frosting", "gravy", "imitation", "simulated", "enriched", "unprepared",
)


def main():
    if not USDA_DIR.exists():
        raise FileNotFoundError(f"USDA directory not found: {USDA_DIR}")

    # 1. Load existing food names so we never duplicate
    existing_names = set()
    if OUTPUT_CSV.exists():
        with OUTPUT_CSV.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                existing_names.add(row["name"].strip().lower())

    # 2. Filter candidate foods from food.csv
    candidates = {}
    with (USDA_DIR / "food.csv").open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            cat_id = row["food_category_id"].strip()
            if cat_id not in CATEGORY_RULES:
                continue

            desc = row["description"].strip()
            desc_lower = desc.lower()

            if any(bad in desc_lower for bad in EXCLUDE_KEYWORDS):
                continue
            if not any(good in desc_lower for good in INCLUDE_KEYWORDS):
                continue

            # Keep concise descriptions
            if len(desc) > 65:
                continue

            candidates[row["fdc_id"]] = (desc, cat_id)

    # 3. Read macros from food_nutrient.csv for candidate fdc_ids
    nutrients_by_id = {fdc_id: {} for fdc_id in candidates}
    with (USDA_DIR / "food_nutrient.csv").open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            fdc_id = row["fdc_id"]
            if fdc_id not in nutrients_by_id:
                continue
            n_id = row["nutrient_id"]
            if n_id in NUTRIENT_MAP and row["amount"]:
                nutrients_by_id[fdc_id][NUTRIENT_MAP[n_id]] = float(row["amount"])

    # 4. Build normalized rows (cap at 240 new items -> total ~300 items)
    new_rows = []
    seen_descriptions = set()

    for fdc_id, (desc, cat_id) in candidates.items():
        macros = nutrients_by_id.get(fdc_id, {})
        if not all(k in macros for k in ("calories", "protein_g", "carbs_g", "fat_g")):
            continue

        clean_name = f"{desc} (USDA)"
        if clean_name.lower() in existing_names or clean_name.lower() in seen_descriptions:
            continue

        meal_slot, base_tags, base_price = CATEGORY_RULES[cat_id]
        tags = [t for t in base_tags.split(",") if t]
        if macros["protein_g"] >= 20.0 and "high-protein" not in tags:
            tags.append("high-protein")
        if macros["carbs_g"] <= 5.0 and "low-carb" not in tags:
            tags.append("low-carb")
        if macros["calories"] <= 80.0 and "low-calorie" not in tags:
            tags.append("low-calorie")

        seen_descriptions.add(clean_name.lower())
        new_rows.append([
            clean_name,
            "100g edible portion",
            f"{macros['calories']:.2f}",
            f"{macros['protein_g']:.2f}",
            f"{macros['carbs_g']:.2f}",
            f"{macros['fat_g']:.2f}",
            base_price,
            meal_slot,
            ",".join(dict.fromkeys(tags)),
            f"USDA FoodData Central SR Legacy (fdc_id={fdc_id})",
            "Hanoi retail estimate per 100g (2026)",
        ])

        # Limitation if necessary
        # if len(new_rows) >= 240:
        #    break

    # 5. Append to data/vietnamese_foods.csv
    with OUTPUT_CSV.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(new_rows)

    print(f"Appended {len(new_rows)} USDA items. Total rows in {OUTPUT_CSV.name}: {len(existing_names) + len(new_rows)}")


if __name__ == "__main__":
    main()