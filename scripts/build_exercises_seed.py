import csv
import json
import urllib.request
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
OUT_JSON = Path("data/exercises_seed.json")
OUT_CSV = Path("data/exercises_seed.csv")

# Map raw category to (app category, goal tags, MET value)
CATEGORY_MAP = {
    "cardio": ("Cardio", ["weight_loss", "maintenance"], 8.0),
    "plyometrics": ("Cardio", ["weight_loss", "muscle_gain"], 8.5),
    "strength": ("Strength", ["muscle_gain", "maintenance"], 5.0),
    "powerlifting": ("Strength", ["muscle_gain"], 6.0),
    "olympic weightlifting": ("Strength", ["muscle_gain"], 6.5),
    "strongman": ("Strength", ["muscle_gain"], 6.5),
    "stretching": ("Core & Mobility", ["maintenance"], 2.5),
}

LEVEL_MAP = {
    "beginner": "beginner",
    "intermediate": "intermediate",
    "expert": "advanced",
}

# Static/timed exercises measured in seconds
HOLD_KEYWORDS = ("plank", "hold", "stretch", "bridge", "wall sit", "hang", "balance")


def infer_unit(name: str, raw_category: str) -> str:
    lower = name.lower()
    if raw_category in ("cardio", "stretching") or any(k in lower for k in HOLD_KEYWORDS):
        return "seconds"
    return "reps"


def build_dataset(per_category: int = 50) -> list[dict]:
    req = urllib.request.urlopen(SOURCE_URL, timeout=30)
    raw_items = json.loads(req.read().decode("utf-8"))

    buckets: dict[str, list[dict]] = {
        "Cardio": [],
        "Strength": [],
        "Core & Mobility": [],
    }
    seen_names: set[str] = set()

    for item in raw_items:
        name = (item.get("name") or "").strip()
        if not name or len(name) > 150 or name.lower() in seen_names:
            continue

        raw_cat = (item.get("category") or "strength").lower()
        category, goal_tags, met = CATEGORY_MAP.get(
            raw_cat, ("Strength", ["muscle_gain", "maintenance"], 4.5)
        )

        # Reclassify abdominal/lower-back strength moves into Core & Mobility
        primary_muscles = [m.lower() for m in (item.get("primaryMuscles") or [])]
        if any(m in primary_muscles for m in ("abdominals", "lower back")) and category == "Strength":
            category = "Core & Mobility"
            goal_tags = ["weight_loss", "muscle_gain", "maintenance"]
            met = 3.8

        if len(buckets[category]) >= per_category:
            if all(len(v) >= per_category for v in buckets.values()):
                break
            continue

        steps = item.get("instructions") or []
        if not steps:
            continue

        difficulty = LEVEL_MAP.get((item.get("level") or "").lower(), "beginner")
        equipment = (item.get("equipment") or "body only").strip()[:100]
        unit = infer_unit(name, raw_cat)

        # Estimate calorie burn for a 65kg person over 10 minutes (Compendium MET formula)
        kcal_10min_65kg = round(met * 65 * (10 / 60))
        muscles_label = ", ".join(item.get("primaryMuscles") or ["full body"])
        meta_note = (
            f"[Target: {muscles_label} | Intensity: {met} MET (~{kcal_10min_65kg} kcal / 10 min for 65kg)]\n"
        )
        instructions = meta_note + " ".join(s.strip() for s in steps)

        seen_names.add(name.lower())
        buckets[category].append({
            "name": name,
            "category": category,
            "equipment": equipment,
            "difficulty": difficulty,
            "instructions": instructions,
            "activity_unit": unit,
            "goal_tags": goal_tags,
            "source": "Free Exercise DB (yuhonas/free-exercise-db) + Compendium MET",
            "review_status": "approved",
        })

    return buckets["Cardio"] + buckets["Strength"] + buckets["Core & Mobility"]


def main():
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    exercises = build_dataset(per_category=50)

    # Export JSON payload for POST /api/admin/exercises/import
    OUT_JSON.write_text(
        json.dumps({"exercises": exercises}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Export CSV for inspection and documentation
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name", "category", "equipment", "difficulty",
                "activity_unit", "goal_tags", "source", "review_status", "instructions",
            ],
        )
        writer.writeheader()
        for row in exercises:
            csv_row = {**row, "goal_tags": ",".join(row["goal_tags"])}
            writer.writerow(csv_row)

    print(f"Exported {len(exercises)} exercises -> {OUT_JSON} & {OUT_CSV}")


if __name__ == "__main__":
    main()