"""Input validation helpers."""


def validate_positive(value: float, name: str) -> float:
    """Validate that a value is positive."""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def validate_non_negative(value: float, name: str) -> float:
    """Validate that a value is non-negative."""
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    return value


def validate_range(value: float, low: float, high: float, name: str) -> float:
    """Validate that a value is within a range."""
    if not (low <= value <= high):
        raise ValueError(f"{name} must be between {low} and {high}, got {value}")
    return value


def validate_fat_class(fat_class: int) -> int:
    """Validate that a FAT class is in the standard IIW set."""
    valid_classes = {36, 40, 45, 50, 56, 63, 71, 80, 90, 100, 112, 125, 140, 160, 225}
    if fat_class not in valid_classes:
        raise ValueError(
            f"FAT class {fat_class} not in standard IIW set: {sorted(valid_classes)}"
        )
    return fat_class
