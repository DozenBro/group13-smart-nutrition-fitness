# Data Sources & Collection Methodology

This document tracks the authoritative open datasets, reference pricing benchmarks, and standardization rules used to populate the **Foods** and **Exercises** tables in the **Smart Nutrition & Fitness** project.

---

## 1. Nutrition & Food Datasets

To ensure accurate macronutrient calculations (calories, protein, carbohydrates, and fat) for Vietnamese daily meals while maintaining clean, auditable records, data is compiled from three primary sources:

| Source | Type | URL / Endpoint | Data Extracted | Usage in Project |
| :--- | :--- | :--- | :--- | :--- |
| **Vietnam National Institute of Nutrition (NIN)** | Official Food Composition Table | `https://viendinhduong.vn` | Calories (`kcal`), Protein (`g`), Glucid/Carbs (`g`), Lipid/Fat (`g`) per 100g of traditional Vietnamese ingredients and cooked dishes. | Primary reference for cooked Vietnamese staples (e.g., *Phở*, *Bún chả*, *Cơm tấm*, stir-fried vegetables, tofu). |
| **Open Food Facts (Vietnam)** | Open REST API & Crowd-sourced DB | `https://world.openfoodfacts.org/api/v2/search?countries_tags_en=vietnam` | Product names, serving sizes, and macro values per 100g (`energy-kcal_100g`, `proteins_100g`, `carbohydrates_100g`, `fat_100g`). | Used via automated Python scripts to collect packaged supermarket foods, dairy, yogurt, and snacks available in Vietnam. |
| **USDA FoodData Central** | Open Government Dataset (CSV/JSON/API) | `https://fdc.nal.usda.gov` | Standardized raw ingredient nutrition profiles per 100g. | Secondary verification for fitness-focused whole foods (e.g., chicken breast, eggs, sweet potatoes, oats, bananas). |

### Reference Pricing (`price_vnd`)
International and academic nutrition databases do not include local Vietnamese retail prices. Reference prices in VND are estimated based on **2026 Hanoi average consumer pricing**:
* **Street food & casual eateries:** ~20,000 – 55,000 VND per standard serving (e.g., *Bánh mì*, *Phở*, *Cơm bình dân*).
* **Supermarket retail (WinMart / Bach Hoa Xanh):** Pro-rated by portion weight (e.g., 150g chicken breast, 2 chicken eggs, 100g rolled oats).
* Every record explicitly logs its provenance in the `nutrition_source` and `price_source` columns.

---

## 2. Exercise & Physical Activity Datasets

For workout recommendations and calorie expenditure estimation, exercises are sourced from open fitness repositories:

| Source | Type | URL | Data Extracted | Usage in Project |
| :--- | :--- | :--- | :--- | :--- |
| **Free Exercise DB** | Open GitHub Repository (JSON) | `https://github.com/yuhonas/free-exercise-db` | 800+ exercises with `name`, `level` (beginner/intermediate/expert), `equipment`, `primaryMuscles`, `category`, and step-by-step `instructions`. | Core catalog for bodyweight, dumbbell, and gym workout routines. |
| **Compendium of Physical Activities** | Scientific Reference Table | `https://pacompendium.com` | Metabolic Equivalent of Task (**MET**) values per activity intensity. | Used to calculate estimated calories burned: $\text{Calories} = \text{MET} \times \text{weight\_kg} \times \text{duration\_hours}$. |

---

## 3. Data Standardization & Seeding Pipeline

Instead of scraping unstructured HTML pages at runtime, all curated data is stored as version-controlled CSV files inside the `data/` directory and loaded into PostgreSQL via idempotent Python scripts.

```text
Open APIs / Official Tables  ──>  data/vietnamese_foods.csv  ──>  backend/seed_foods.py  ──>  PostgreSQL (foods)
```

### CSV Schema Rules (`data/vietnamese_foods.csv`)
1. **Encoding:** UTF-8 (to preserve Vietnamese diacritics alongside English translations, e.g., `Phở bò tái (Rare Beef Pho)`).
2. **Portion Normalization:** All macro values and `price_vnd` must correspond to a single practical serving described in `portion_desc` (e.g., `1 medium bowl (~450g)`), rather than raw 100g values, so the meal planner can sum meals directly.
3. **Allowed Tags:**
   * `meal_slot`: Comma-separated subset of `breakfast`, `lunch`, `dinner`, `snack`.
   * `preference_tags`: Comma-separated dietary tags such as `high-protein`, `low-carb`, `vegetarian`, `no-pork`, `budget`, `high-calorie`.
4. **Idempotency:** `backend/seed_foods.py` checks existing records by `name` before inserting, ensuring repeated runs never create duplicate rows.

---

## 4. Collection Checklist & Progress

- [x] Define `Food` SQLAlchemy schema with `nutrition_source` and `price_source` audit fields.
- [x] Create initial seed script (`backend/seed_foods.py`) and verify idempotency via unit tests.
- [ ] Expand `data/vietnamese_foods.csv` to **60+ curated Vietnamese dishes** covering all meal slots and budget tiers.
- [ ] Refactor `backend/seed_foods.py` to ingest records directly from `data/vietnamese_foods.csv`.
- [ ] (Optional / Next Task) Curate `data/exercises.csv` (~40 exercises with MET values) from Free Exercise DB.