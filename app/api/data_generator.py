from dataclasses import dataclass
from typing import Literal, Optional, Tuple
import numpy as np

from app.helpers.iterable_class import IterableClass
from app.helpers.utils import (
    NpDateTimeUnitCode,
    get_np_datetime_from_date_string,
    timearray_to_string,
)

GeneratorTypes = Literal[
    "brownian", "constant", "dates", "gaussian", "pattern", "uniform"
]

TimeUnits = Literal["second", "minute", "hour", "day", "week", "month", "year"]


@dataclass
class PatternConfig(IterableClass):
    base: float | int = 0
    delta: float | int = 0


@dataclass
class GaussConfig(IterableClass):
    mean: float | int = 1
    std: float | int = 1


@dataclass
class DateTimeConfig(IterableClass):
    start_date_time: str = ""
    interval: int = 1
    time_unit: TimeUnits = "day"
    time_format: str = "%Y-%m-%d"


class DataGenerator:
    # Number of data points to generate
    count = 10

    # Default type = uniform
    type: GeneratorTypes = "uniform"

    # Min and max value
    # Normalization range for normal/uniform distributions
    range: Tuple[float | int, float | int] = (0, 10)

    # Round numbers, set to -1 to disable
    decimals: int = -1

    # Mean and standard deviation for normal distributions
    gauss_config: GaussConfig = (
        GaussConfig()
    )  # Tuple[Optional[float|int], Optional[float|int]] = (None, None)

    # Configuration for time/date series. Note: Start date must use ISO format
    date_time_config: DateTimeConfig = DateTimeConfig()

    # Pattern generator config - not initialized!
    __pattern_config: PatternConfig

    # Set the seed to reproduce the same values - disabled by default
    # seed: Optional[int] = None
    rng: np.random.Generator
    seed: Optional[int] = None
    __seed = None
    __saved_seeds: set[int]

    @property
    def saved_seeds(self):
        seeds = list(self.__saved_seeds)
        seeds.reverse()  # FIFO order
        return seeds

    @property
    def pattern_config(self) -> PatternConfig:
        return self.__pattern_config

    @pattern_config.setter
    def pattern_config(self, value: Tuple[float | int, float | int]):
        self.__pattern_config = PatternConfig(*value)

    @property
    def single(self):
        return self.values[0]

    @property
    def values(self):
        values = []
        match self.type:
            case "brownian":
                values = self.__generate_brownian()

            case "constant":
                values = self.__generate_constant()

            case "dates":
                values = self.__generate_date_sequence()

            case "exponential":
                values = self.__generate_exponential()

            case "gaussian":
                values = self.__generate_gaussian()

            case "pattern":
                values = self.__generate_pattern()

            case "uniform":
                values = self.__generate_uniform()

        if self.decimals >= 0:
            values = np.round(values, self.decimals)

        return values

    def __init__(
        self,
        type: GeneratorTypes = "uniform",
        generate_int=False,
        count=None,
        value_range=None,
        decimals=-1,
        gauss_config: Optional[GaussConfig] = None,
        date_time_config: Optional[DateTimeConfig] = None,
    ):
        if value_range:
            self.range = value_range
        if count:
            self.count = count
        if decimals > -1:
            self.decimals = decimals
        if type:
            self.type = type
        if generate_int:
            self.generate_int = generate_int
        if gauss_config:
            self.gauss_config = gauss_config
        if date_time_config:
            self.date_time_config = date_time_config

        self.__saved_seeds = set([])

    def __setup_generator(self):
        if not self.seed:
            bytes = np.random.bytes(10)
            self.__seed = int.from_bytes(bytes, "little")
            self.__saved_seeds.add(self.__seed)
        else:
            self.__seed = self.seed

        rng = np.random.default_rng(self.__seed)
        self.rng = rng
        return rng

    def __generate_random(self):
        rng = self.__setup_generator()

        if self.decimals <= 0:
            return self.rng.integers(0, 1, self.count)

        return rng.random(self.count)

    def __generate_brownian(self):
        self.__setup_generator()
        arr = np.arange(0, self.count - 1)
        values = np.array([0])

        for x in arr:
            sigma = x + 1 - x  # std
            randomNumber = self.rng.normal(0, sigma)
            v = values[x] + randomNumber
            values = np.append(values, v)

        return self.__normalize_values(values, rescale=True)

    def __generate_constant(self):
        self.__setup_generator()
        value = None
        if self.decimals > 0:
            value = round(self.rng.uniform(
                self.range[0], self.range[1]), self.decimals)
        elif self.decimals == 0:
            value = self.rng.integers(
                self.range[0], self.range[1])  # type: ignore
        return np.full(self.count, value)

    def __generate_exponential(self):
        x_range = np.arange(0, self.count)
        # values = [np.power(0.95, x) for x in x_range]
        # noise = self.__generate_gaussian()
        # values = values + noise
        coeff = 0.95
        values = np.vectorize(lambda x: np.power(coeff, x))(x_range)
        return self.__normalize_values(values)

    def __generate_gaussian(self):
        self.__setup_generator()
        mean, std = self.gauss_config

        # if mean == None or std == None:
        #     raise Exception('Invalid configuration data in `gauss_config`.')
        values = self.rng.normal(mean, std, self.count)  # type: ignore
        return self.__normalize_values(values)

    def __generate_pattern(self):
        delta = self.pattern_config.delta
        data = {"value": self.pattern_config.base}
        mod = self.count
        limit = mod // 2

        def generate(x):
            increment = x % mod
            if increment >= limit:
                data["value"] += delta
            else:
                data["value"] -= delta

            return data["value"]

        values = np.arange(self.count)
        return np.vectorize(generate)(values)

    def __generate_uniform(self):
        values = self.__generate_random()
        return self.__normalize_values(values)

    def __generate_date_sequence(self):
        dt_conf = self.date_time_config

        if not dt_conf:
            raise ValueError(
                "\nError! Required date_time_config has not been provided."
            )

        start, interval, unit, time_format = (
            dt_conf.start_date_time,
            dt_conf.interval,
            dt_conf.time_unit,
            dt_conf.time_format,
        )

        if any(not x for x in dt_conf):
            raise ValueError(
                "\nError! Encountered empty configuration values in date_time_config."
            )

        if unit in ["second", "minute", "hour"]:
            # NP time parser only supports ISO string - add a random date that will be discarded later
            start = f"1900-01-01 {start}"

        unit_code = NpDateTimeUnitCode[unit]

        time_span = self.count * interval
        date_diff = np.timedelta64(time_span, unit_code)
        start_date = get_np_datetime_from_date_string(start)
        end_date = start_date + date_diff

        timearray = np.arange(
            start_date,
            end_date,
            np.timedelta64(interval, unit_code),
            dtype="datetime64",
        )

        timestrings = timearray_to_string(timearray, time_format)
        return timestrings

    def __normalize_values(self, values, rescale=False):
        lower, upper = self.range
        vmin, vmax = values.min(), values.max()
        coeff = upper - lower

        # If required, first rescale values between 0 and 1
        intermediate_values = values
        if rescale:
            intermediate_values = np.interp(values, (vmin, vmax), (0, 1))
            # scaled = (values - vmin)/(vmax - vmin)

        # Apply y = mx + c
        normalized = intermediate_values * coeff + lower

        return normalized
