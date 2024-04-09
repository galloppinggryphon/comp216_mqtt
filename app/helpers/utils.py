from datetime import datetime
from enum import StrEnum
from typing import Literal, Optional, Tuple
import numpy as np


class NpDateTimeUnitCode(StrEnum):
    second = "s"
    minute = "m"
    hour = "h"
    day = "D"
    week = "W"
    month = "M"
    year = "Y"


def get_np_datetime_from_date_string(date_str: str):
    try:
        datetime = np.datetime64(date_str)
    except ValueError:
        raise ValueError(
            f"\nError! Invalid date-time format.\nDate-time string could not be parsed: {date_str}"
        )

    return datetime


# Use Python datetime string formatting
def timearray_to_string(time_array, format="%Y-%m-%d"):
    def convert(x):
        t = x.astype(datetime)
        return t.strftime(format)

    values = [convert(i) for i in time_array]
    return values
