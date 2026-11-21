from decimal import Decimal, ROUND_HALF_UP


ACTIVITY_FACTORS = {
    'sedentary': Decimal('1.2'),
    'lightly_active': Decimal('1.375'),
    'moderately_active': Decimal('1.55'),
    'active': Decimal('1.725'),
    'very_active': Decimal('1.9'),
}


def calculate_bmi(weight_kg: Decimal, height_cm: Decimal) -> Decimal:
    height_m = height_cm / Decimal('100')
    return (weight_kg / (height_m * height_m)).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )


def calculate_tdee(
    *,
    weight_kg: Decimal,
    height_cm: Decimal,
    age_years: int,
    sex_for_equation: str,
    activity_level: str,
) -> Decimal:
    """Estimate kcal/day using the proposed S1-07 rules; D-02 awaits review."""
    for name, value in (('weight_kg', weight_kg), ('height_cm', height_cm)):
        if not isinstance(value, Decimal) or not value.is_finite():
            raise ValueError(f'{name} must be a finite Decimal.')
    if not Decimal('0') < weight_kg <= Decimal('500'):
        raise ValueError('weight_kg must be greater than 0 and no more than 500.')
    if not Decimal('50') <= height_cm <= Decimal('250'):
        raise ValueError('height_cm must be between 50 and 250.')
    for name, value in (('weight_kg', weight_kg), ('height_cm', height_cm)):
        if value != value.quantize(Decimal('0.01')):
            raise ValueError(f'{name} must have at most 2 decimal places.')
    if type(age_years) is not int or not 19 <= age_years <= 78:
        raise ValueError('age_years must be an integer from 19 to 78.')
    if not isinstance(sex_for_equation, str) or sex_for_equation not in ('male', 'female'):
        raise ValueError('sex_for_equation must be male or female.')
    if not isinstance(activity_level, str) or activity_level not in ACTIVITY_FACTORS:
        raise ValueError('activity_level must be one of the documented activity codes.')
    coefficient = {'male': Decimal('5'), 'female': Decimal('-161')}[sex_for_equation]
    resting_energy = (
        Decimal('10') * weight_kg + Decimal('6.25') * height_cm
        - Decimal('5') * age_years + coefficient
    )
    if resting_energy <= 0:
        raise ValueError('Profile produces non-positive resting energy; review the inputs.')
    return (resting_energy * ACTIVITY_FACTORS[activity_level]).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP,
    )

