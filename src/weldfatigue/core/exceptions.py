"""Custom exception hierarchy for the weldfatigue package."""


class WeldFatigueError(Exception):
    """Base exception for the weldfatigue package."""


class MaterialNotFoundError(WeldFatigueError):
    """Raised when a material grade is not in the database."""


class InvalidFATClassError(WeldFatigueError):
    """Raised when an unsupported FAT class is requested."""


class FEAParsingError(WeldFatigueError):
    """Raised when FEA result parsing fails."""


class InsufficientDataError(WeldFatigueError):
    """Raised when not enough data points are available."""
