"""Tests for input validators."""

import pytest

from weldfatigue.utils.validators import (
    validate_positive,
    validate_non_negative,
    validate_range,
    validate_fat_class,
)


class TestValidatePositive:

    def test_positive(self):
        assert validate_positive(10.0, "test") == 10.0

    def test_zero_raises(self):
        with pytest.raises(ValueError):
            validate_positive(0.0, "test")

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            validate_positive(-5.0, "test")


class TestValidateNonNegative:

    def test_positive(self):
        assert validate_non_negative(10.0, "test") == 10.0

    def test_zero_ok(self):
        assert validate_non_negative(0.0, "test") == 0.0

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            validate_non_negative(-1.0, "test")


class TestValidateRange:

    def test_within_range(self):
        assert validate_range(5.0, 0.0, 10.0, "test") == 5.0

    def test_at_lower_bound(self):
        assert validate_range(0.0, 0.0, 10.0, "test") == 0.0

    def test_at_upper_bound(self):
        assert validate_range(10.0, 0.0, 10.0, "test") == 10.0

    def test_below_range_raises(self):
        with pytest.raises(ValueError):
            validate_range(-1.0, 0.0, 10.0, "test")

    def test_above_range_raises(self):
        with pytest.raises(ValueError):
            validate_range(11.0, 0.0, 10.0, "test")


class TestValidateFATClass:

    def test_valid_fat_71(self):
        assert validate_fat_class(71) == 71

    def test_valid_fat_225(self):
        assert validate_fat_class(225) == 225

    def test_invalid_fat_raises(self):
        with pytest.raises(ValueError):
            validate_fat_class(72)

    def test_all_valid_classes(self):
        valid = [36, 40, 45, 50, 56, 63, 71, 80, 90, 100, 112, 125, 140, 160, 225]
        for fc in valid:
            assert validate_fat_class(fc) == fc
