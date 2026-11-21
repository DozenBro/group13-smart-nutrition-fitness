# Data Sources, ETL Pipeline & Database Seeding Guide

This document records the authoritative sources, data processing pipeline, and local setup instructions for the **Foods** dataset in the **Smart Nutrition & Fitness** project. It also serves as an onboarding guide for team members to seed, inspect, and test the database locally.

---

## 1. Food & Nutrition Data Sources

The current dataset (`data/vietnamese_foods.csv`) combines **60 manually curated Vietnamese daily dishes** with **hundreds of filtered whole foods and basic ingredients** extracted from the USDA database (~700+ total food items).

| Source | Type | URL / Reference | Scope & Usage in Project |
| :--- | :--- | :--- | :--- |
| **Vietnam National Institute of Nutrition (NIN)** | Official Food Composition Table | `https://viendinhduong.vn` | Reference values (`kcal`, `protein_g`, `carbs_g`, `fat_g`) for traditional Vietnamese cooked dishes (e.g., *Phở bò*, *Bún chả*, *Cơm tấm*, stir-fried dishes). |
| **USDA FoodData Central (SR Legacy 2018-04)** | Open Government CSV Dataset | `https://fdc.nal.usda.gov` | Filtered raw and minimally processed ingredients (poultry, beef, pork, seafood, eggs, dairy, grains, vegetables, fruits, legumes, nuts) standardized per `100g edible portion`. |
| **Open Food Facts (Vietnam)** | Open REST API | `https://world.openfoodfacts.org/api/v2/search?countries_tags_en=vietnam` | Secondary reference for packaged Vietnamese dairy and retail snacks. |

### Reference Pricing (`price_vnd`)
International nutrition datasets do not include Vietnamese currency pricing. All prices are standardized in **VND** based on **2026 Hanoi average consumer benchmarks**:
* **Vietnamese street food & casual meals:** ~20,000 – 55,000 VND per practical serving (e.g., *1 medium bowl (~450g)*).
* **USDA whole ingredients:** Estimated Hanoi retail price per `100g edible portion` (ranging from 8,000 VND for grains/vegetables to 30,000 VND for beef).
* Every record tracks its exact provenance via the `nutrition_source` (including USDA `fdc_id`) and `price_source` columns.

---

## 2. ETL & Data Standardization Pipeline

Instead of storing raw multi-table dumps in Git, raw datasets are processed locally and stored in a single, version-controlled UTF-8 CSV file:

```text
[NIN Reference + Curated VN Dishes (60)] ──┐
                                           ├──> data/vietnamese_foods.csv ──> backend/seed_foods.py ──> PostgreSQL (foods)
[USDA SR Legacy CSV] ─> import_usda_foods.py ┘
```

### Key Files
* `data/vietnamese_foods.csv`: Master UTF-8 CSV dataset containing all normalized food records.
* `scripts/import_usda_foods.py`: Local ETL script that joins `food.csv` and `food_nutrient.csv` (`nutrient_id`: `1008` Energy, `1003` Protein, `1005` Carbs, `1004` Fat), filters out baby food, organ meats, fast foods, and overly verbose entries, auto-assigns `meal_slot` and `preference_tags`, and appends clean records without duplicates.
* `backend/seed_foods.py`: Idempotent database seeder using `csv.DictReader` and SQLAlchemy. It checks existing rows by `Food.name` so repeated runs safely insert only new items.

### CSV Schema Conventions
* **Encoding:** UTF-8 (`encoding="utf-8"`). *(Note: If opening directly in Windows Excel, use **Data → From Text/CSV → File Origin: 65001: Unicode (UTF-8)** to display Vietnamese diacritics properly).*
* **Allowed `meal_slot` values:** Comma-separated subset of `breakfast`, `lunch`, `dinner`, `snack`.
* **Allowed `preference_tags` values:** Comma-separated tags such as `high-protein`, `low-carb`, `low-calorie`, `vegetarian`, `vegan`, `no-pork`, `seafood`, `budget`, `high-calorie`.

---

## 3. Team Guide: How to Seed, Inspect & Test the Database

Because the isolated local PostgreSQL instance runs on port `55432` and is managed by `manage.py`, follow these steps after pulling the latest code:

### Step 1: Start Local PostgreSQL & Application Server
Open **Terminal 1** in the project root and run:
```powershell
.\.venv\Scripts\python.exe manage.py run
```
Wait until the isolated PostgreSQL instance (`127.0.0.1:55432`) and FastAPI server (`http://127.0.0.1:8013`) are up and running.

### Step 2: Seed the Food Dataset into PostgreSQL
Open **Terminal 2**, load the local database credentials, and run the seeder:
```powershell
$db = Get-Content .local\database.json | ConvertFrom-Json
$env:DATABASE_URL = "postgresql+psycopg://fitness:$($db.password)@127.0.0.1:55432/fitness_demo"
.\.venv\Scripts\python.exe -m backend.seed_foods
```
Expected output:
```text
Seeded <N> new food items from vietnamese_foods.csv. Total foods in database: <TOTAL>.
```
*(Running this command multiple times is completely safe; duplicate names are automatically skipped).*

### Step 3: Verify & Inspect Data
You can verify the seeded records in three ways:
1. **Interactive API Docs (Swagger UI):** Open `http://127.0.0.1:8013/docs` in your browser and test `GET /api/foods` with filters (`meal_slot`, `max_price_vnd`, `tag`).
2. **Quick PowerShell Check:**
   ```powershell
   $foods = Invoke-RestMethod http://127.0.0.1:8013/api/foods
   "Total foods via API: $($foods.Count)"
   $foods | Select-Object -First 5 id, name, calories, protein_g, price_vnd | Format-Table
   ```
3. **Direct Database Row Count:**
   ```powershell
   .\.venv\Scripts\python.exe -c "from sqlalchemy import func, select; from backend.database import SessionLocal; from backend.models import Food; db=SessionLocal(); print('Total DB:', db.execute(select(func.count(Food.id))).scalar_one())"
   ```

### Step 4: Run Automated Tests
Stop the server in Terminal 1 (`Ctrl + C`) if needed, then run the full test suite (including `tests/test_foods.py`, which verifies CRUD endpoints, filtering, soft-deactivation, and CSV seed idempotency):
```powershell
.\.venv\Scripts\python.exe manage.py test
```
*(Optional: To shut down the background PostgreSQL process when finished working, run `.\.venv\Scripts\python.exe manage.py stop-db`).*

---

## 4. Future Expansion (Exercises Dataset)

For upcoming workout recommendation features (`exercises` table), the recommended open datasets are:
* **Free Exercise DB** (`https://github.com/yuhonas/free-exercise-db`): 873 structured exercises with muscle groups, equipment, difficulty levels, and instructions.
* **Compendium of Physical Activities** (`https://pacompendium.com`): Scientific **MET** values for calorie burn calculation ($\text{Calories} = \text{MET} \times \text{weight\_kg} \times \text{duration\_hours}$).