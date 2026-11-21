from decimal import Decimal

import pytest

from backend import health


def valid_profile(**overrides):
    return {
        'weight_kg': Decimal('70'),
        'height_cm': Decimal('175'),
        'age_years': 25,
        'sex_for_equation': 'male',
        'activity_level': 'moderately_active',
        **overrides,
    }


@pytest.mark.parametrize(('activity_level', 'expected'), [
    ('sedentary', '2008.50'),
    ('lightly_active', '2301.41'),
    ('moderately_active', '2594.31'),
    ('active', '2887.22'),
    ('very_active', '3180.13'),
])
def test_male_worked_example_for_each_activity(activity_level, expected):
    result = health.calculate_tdee(**valid_profile(activity_level=activity_level))
    assert result == Decimal(expected)
    assert isinstance(result, Decimal)
    assert result.as_tuple().exponent == -2


def test_female_worked_example():
    assert health.calculate_tdee(**valid_profile(
        weight_kg=Decimal('60'), height_cm=Decimal('165'), age_years=30,
        sex_for_equation='female', activity_level='lightly_active',
    )) == Decimal('1815.34')


def test_round_only_after_applying_activity_factor():
    # REE 1673.8125 * 1.2 = 2008.575; rounding REE first gives the wrong 2008.57.
    assert health.calculate_tdee(**valid_profile(
        height_cm=Decimal('175.01'), activity_level='sedentary',
    )) == Decimal('2008.58')


@pytest.mark.parametrize(('age_years', 'expected'), [(19, '2044.50'), (78, '1690.50')])
def test_proposed_age_scope_includes_both_boundaries(age_years, expected):
    assert health.calculate_tdee(**valid_profile(
        age_years=age_years, activity_level='sedentary',
    )) == Decimal(expected)


@pytest.mark.parametrize(('field', 'value'), [
    ('weight_kg', None),
    ('weight_kg', Decimal('0')),
    ('weight_kg', Decimal('-1')),
    ('weight_kg', Decimal('500.01')),
    ('weight_kg', Decimal('70.001')),
    ('weight_kg', Decimal('NaN')),
    ('weight_kg', Decimal('sNaN')),
    ('weight_kg', Decimal('Infinity')),
    ('weight_kg', Decimal('-Infinity')),
    ('weight_kg', 70.0),
    ('weight_kg', '70'),
    ('height_cm', None),
    ('height_cm', Decimal('0')),
    ('height_cm', Decimal('49.99')),
    ('height_cm', Decimal('250.01')),
    ('height_cm', Decimal('175.001')),
    ('height_cm', Decimal('NaN')),
    ('height_cm', Decimal('Infinity')),
    ('height_cm', 175),
    ('age_years', None),
    ('age_years', 18),
    ('age_years', 79),
    ('age_years', 25.5),
    ('age_years', True),
    ('age_years', '25'),
    ('sex_for_equation', None),
    ('sex_for_equation', ''),
    ('sex_for_equation', 'MALE'),
    ('sex_for_equation', 'unspecified'),
    ('sex_for_equation', []),
    ('activity_level', None),
    ('activity_level', ''),
    ('activity_level', 'unknown'),
    ('activity_level', Decimal('1.55')),
    ('activity_level', []),
])
def test_reject_invalid_or_missing_profile_input(field, value):
    with pytest.raises(ValueError, match=field):
        health.calculate_tdee(**valid_profile(**{field: value}))


def test_reject_profile_that_produces_non_positive_resting_energy():
    with pytest.raises(ValueError, match='resting energy'):
        health.calculate_tdee(**valid_profile(
            weight_kg=Decimal('0.01'), height_cm=Decimal('50'), age_years=78,
            sex_for_equation='female',
        ))


def test_accept_measurements_at_upper_software_limits():
    assert health.calculate_tdee(**valid_profile(
        weight_kg=Decimal('500'), height_cm=Decimal('250'), activity_level='sedentary',
    )) == Decimal('7731.00')


def test_accept_trailing_zeros_without_changing_the_value():
    assert health.calculate_tdee(**valid_profile(
        weight_kg=Decimal('70.000'), height_cm=Decimal('175.000'),
    )) == Decimal('2594.31')
