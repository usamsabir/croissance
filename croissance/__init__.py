import pandas

import croissance.figures.plot

from croissance.estimation import (
    AnnotatedGrowthCurve,
    GrowthEstimationParameters,
    estimate_growth,
)
from croissance.estimation.util import normalize_time_unit


__all__ = [
    "plot_processed_curve",
    "process_curve",
]


def format_time(time: str, type: str) -> str:
    """Formats the given time based on the specified type without using datetime."""

    if type == "24_hour":
        # Split time into components (e.g., "10:30 PM" -> ['10:30', 'PM'])
        time_parts = time.strip().split(" ")
        if len(time_parts) != 2 or time_parts[1] not in ['AM', 'PM']:
            return "Invalid"

        # Extract hour and minute
        hour_minute = time_parts[0].split(":")
        if len(hour_minute) != 2:
            return "Invalid"

        try:
            hour = int(hour_minute[0])
            minute = int(hour_minute[1])
        except ValueError:
            return "Invalid"

        # Validate hour and minute
        if hour < 1 or hour > 12 or minute < 0 or minute >= 60:
            return "Invalid"

        # Convert to 24-hour format based on AM/PM
        if time_parts[1] == 'PM' and hour != 12:
            hour += 12
        elif time_parts[1] == 'AM' and hour == 12:
            hour = 0

        # Format hour and minute
        return f"{hour:02d}:{minute:02d}"

    elif type == "ISO":
        # Split date and time for ISO format (assuming "YYYY-MM-DDTHH:MM:SS" format)
        try:
            date, time = time.split('T')
            # Validate date part (YYYY-MM-DD)
            year, month, day = map(int, date.split('-'))
            if not (1 <= month <= 12 and 1 <= day <= 31):
                return "Invalid"

            # Validate time part (HH:MM:SS)
            time_parts = time.split(':')
            hour, minute, second = map(int, time_parts)
            if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
                return "Invalid"

            return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"
        except Exception:
            return "Invalid"

    else:
        return "Invalid"


def process_curve(
    curve: "pandas.Series",
    segment_log_n0: bool = False,
    constrain_n0: bool = False,
    n0: float = 0.0,
    unit: str = "hours",
    time: str="11:20 PM",
    type: str="24_hour",
):
    curve = normalize_time_unit(curve, unit)
    if curve.isnull().all():
        return AnnotatedGrowthCurve(curve, [], [])

    result_time = format_time(time,type)
    params = GrowthEstimationParameters()
    params.segment_log_n0 = segment_log_n0
    params.constrain_n0 = constrain_n0
    params.n0 = n0

    return estimate_growth(curve, params=params)


def plot_processed_curve(curve: AnnotatedGrowthCurve, yscale="both"):
    return croissance.figures.plot.plot_processed_curve(curve=curve, yscale=yscale)
