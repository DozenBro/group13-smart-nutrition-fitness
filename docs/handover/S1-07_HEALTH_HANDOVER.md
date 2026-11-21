# S1-07 Health Calculation Handover

**21 November 2026 · Proposal for D-02 · Awaiting team review**

Tracking: [task issue #1](https://github.com/DozenBro/group13-smart-nutrition-fitness/issues/1) · [review PR #2](https://github.com/DozenBro/group13-smart-nutrition-fitness/pull/2).

Prepared with AI assistance at the user's request for Tá Anh's health-module handover. Tuấn Anh reviews the integration contract; Thắng reviews the arithmetic and tests. This records a proposed implementation, not either member's approval or a completed user story.

## Start Here

1. Tuấn Anh: read the input contract and integration steps below before designing profile fields.
2. Thắng: reproduce the two worked examples independently, then run the unit tests.
3. The group: resolve the D-02 checklist before adding the calculation to the API and UI.

The existing demo already calculates BMI, saves measurements, and lists shared history. This handover adds a standalone TDEE function. Account/profile APIs, authentication, ownership, database changes, and UI integration remain separate Sprint 1 tasks.

## Proposed Inputs

All five arguments are required for this calculation. The function has no implicit defaults.

- `weight_kg`: Python `Decimal`, kilograms, greater than 0 and no more than 500; at most two significant fractional places. Reuses the demo's software limits, which still need team confirmation.
- `height_cm`: Python `Decimal`, centimetres, 50 through 250 inclusive; at most two significant fractional places. Reuses the demo's software limits.
- `age_years`: Python `int`, whole years, 19 through 78 inclusive. This proposed sample scope follows the age range in the original study; it is not a claim of individual suitability within that range. The team must decide how profile age is stored and kept current.
- `sex_for_equation`: exactly `male` or `female`, selecting the corresponding published equation coefficient. Do not infer this value from a name or silently map another/missing value to either equation. The profile/UI must explain what the input selects; if unavailable, show no estimate.
- `activity_level`: exactly one of the proposed codes below. The backend owns the mapping; the browser should send the selected code rather than an arbitrary multiplier.

Proposed activity mapping, following the labels in source 2:

- `sedentary`: 1.2.
- `lightly_active`: 1.375.
- `moderately_active`: 1.55.
- `active`: 1.725.
- `very_active`: 1.9.

These are proposed software choices for review. The original Mifflin paper supplies the resting-energy equation, not this activity-code mapping. Source 2 is a reference for the multiplier set; its clinical context does not establish validation for this project's users.

## Formulas and Rounding

Let `W` be kilograms, `H` be centimetres, and `A` be age in years.

```text
BMI = W / (H / 100)^2

Resting energy estimate (REE), kcal/day:
male:   REE = 10*W + 6.25*H - 5*A + 5
female: REE = 10*W + 6.25*H - 5*A - 161

Estimated TDEE = REE * activity factor
```

The resting equation is the simplified Mifflin–St Jeor equation from source 1. An activity multiplier is a separate estimation step. Keep full `Decimal` precision through the multiplication. Round the final TDEE to two decimal places with `ROUND_HALF_UP`, matching the existing BMI display convention. Do not round REE first. Reject a non-positive REE instead of returning an invalid energy estimate.

The UI should label the result **Estimated TDEE (kcal/day)**. This handover defines a software estimate, with no weight-loss/gain calorie adjustment or meal target policy.

## Independently Worked Examples

These are fictional software fixtures. Expected results are arithmetic written out here, not values obtained by calling the implementation.

**Example H-01:** 70 kg, 175 cm, 25 years, `male`, `moderately_active`.

```text
BMI = 70 / 1.75^2 = 22.857142... -> 22.86
REE = 700 + 1093.75 - 125 + 5 = 1673.75
TDEE = 1673.75 * 1.55 = 2594.3125 -> 2594.31 kcal/day
```

**Example H-02:** 60 kg, 165 cm, 30 years, `female`, `lightly_active`.

```text
REE = 600 + 1031.25 - 150 - 161 = 1320.25
TDEE = 1320.25 * 1.375 = 1815.34375 -> 1815.34 kcal/day
```

**Rounding fixture H-03:** 70 kg, 175.01 cm, 25 years, `male`, `sedentary` gives REE 1673.8125 and TDEE 2008.575 -> **2008.58**. Rounding REE first would incorrectly produce 2008.57.

## Python Contract for Tuấn Anh

The implementation lives in `backend/health.py`:

```python
def calculate_tdee(
    *,
    weight_kg: Decimal,
    height_cm: Decimal,
    age_years: int,
    sex_for_equation: str,
    activity_level: str,
) -> Decimal:
    ...
```

Example call from the repository root, after implementation:

```python
from decimal import Decimal
from backend.health import calculate_tdee

result = calculate_tdee(
    weight_kg=Decimal('70'),
    height_cm=Decimal('175'),
    age_years=25,
    sex_for_equation='male',
    activity_level='moderately_active',
)
assert result == Decimal('2594.31')
```

Returns a two-decimal `Decimal` in kcal/day. Invalid, missing (`None`), non-finite, unsupported, or out-of-scope inputs raise `ValueError`. A missing keyword argument is a Python call error; the API should validate request/profile completeness before calling the function. The function performs no database access and does not choose an account, timestamp, or measurement.

## Integration Steps for Tuấn Anh and Bảo

1. Resolve D-02 and agree the profile schema and field names with Tá Anh and Bảo. The age field here is a calculation input; storing birth date instead requires an agreed age-at-calculation policy.
2. Obtain account identity from the backend session. Read that account's profile and the measurement being displayed. Never accept a submitted owner ID as authorization.
3. Validate required fields and convert numeric inputs using the API's Decimal validation. Reuse the stored measurement values; do not parse already-rounded display text.
4. Call `calculate_tdee` with the inputs above. Handle `ValueError` according to the agreed API contract. A proposed convention is HTTP 422 for invalid submitted data; an incomplete stored profile should identify missing fields and leave the estimate unavailable, not substitute zero.
5. Agree request/response examples and error states with Bảo before UI integration. This handover creates no endpoint or response schema.
6. Decide whether historical TDEE uses a profile snapshot or the current profile. Do not silently recalculate historical results with new profile values and call them original estimates.
7. Add API/database tests for own-account calculation, missing data, and cross-account denial. These remain outside the pure calculation tests.

Tuấn Anh can implement account/session foundations while D-02 is reviewed. Avoid finalizing profile-specific migrations or API contracts on unreviewed assumptions.

## Verification and Review

Run calculation tests without PostgreSQL:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/test_health.py
```

Run the complete suite against the isolated project test database:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

- [ ] Tuấn Anh confirms parameter names, field storage, and error handling for integration.
- [ ] Thắng checks H-01/H-02 independently and reviews rounding, boundaries, and rejected inputs.
- [ ] The group accepts or revises the equation, activity mapping, age scope, and measurement limits in D-02/S1-R01.
- [ ] The group resolves age updates and historical-profile policy before integrating history.
- [ ] Actual human review and acceptance results are recorded in the issue/PR and Sprint 1 log.

## Sources

1. Mifflin et al. (1990), *A new predictive equation for resting energy expenditure in healthy individuals*, simplified equations and study age range. [PubMed, PMID 2305711](https://pubmed.ncbi.nlm.nih.gov/2305711/). DOI: `10.1093/ajcn/51.2.241`.
2. Texas Health and Human Services, *Common Comparative Standards for RDs in LTC Settings*, revised October 2022, page 2, "Estimating Energy Needs", item 2: resting equations and five activity multipliers. [Official PDF](https://www.hhs.texas.gov/sites/default/files/documents/common-comparative-standards-for-rds-ltc-settings.pdf).

Sources checked 21 November 2026. The project-specific choices remain proposals until the named team members review them.
