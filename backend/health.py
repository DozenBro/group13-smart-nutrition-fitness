from decimal import Decimal, ROUND_HALF_UP


def calculate_bmi(weight_kg: Decimal, height_cm: Decimal) -> Decimal:
    height_m = height_cm / Decimal('100')
    return (weight_kg / (height_m * height_m)).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )

