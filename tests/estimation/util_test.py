import pandas

from croissance.estimation.util import normalize_time_unit
from croissance import format_time


def test_normalize_time_unit():
    curve = pandas.Series(index=[0, 15, 30, 60], data=[1, 2, 3, 4])

    assert pandas.Series(index=[0.0, 0.25, 0.5, 1.0], data=[1, 2, 3, 4]).equals(
        normalize_time_unit(curve, "minutes")
    )


def test_format_time_24_hour_valid_am():
    # Test valid 12-hour AM time to 24-hour conversion
    assert format_time("10:30 AM", "24_hour") == "10:30"


def test_format_time_24_hour_valid_pm():
    # Test valid 12-hour PM time to 24-hour conversion
    assert format_time("10:30 PM", "24_hour") == "22:30"


def test_format_time_24_hour_invalid_format():
    # Test invalid time format for 24-hour conversion
    assert format_time("25:00 PM", "24_hour") == "Invalid"


def test_format_time_iso_invalid():
    # Test invalid time format for ISO conversion
    assert format_time("09/09/2024 15:45", "ISO") == "Invalid"


def test_format_time_invalid_type():
    # Test unsupported type
    assert format_time("10:30 AM", "12_hour") == "Invalid"


def test_format_time_empty_time():
    # Test empty time input
    assert format_time("", "24_hour") == "Invalid"


def test_format_time_iso_edge_case():
    # Test valid edge case with midnight ISO format
    assert format_time("2024-09-09T00:00:00", "ISO") == "2024-09-09T00:00:00"
