from enum import Enum
from loguru import logger


class SizeUnit(Enum):
    KB = 1, "1 KB is an average 100 default tables"
    MB = 2, "1 MB is an average 100 default tables"
    GB = 3, "1 GB is an average 1000 default tables"
    TB = 4, "1 TB is an average 10000 default tables"

    def __init__(self, value: int, description: str = None):
        self._value_ = value
        self._description_ = description

    @property
    def description(self):
        return self._description_

    @classmethod
    def is_valid_unit(cls, unit: str) -> bool:
        return unit.upper() in [x.name for x in SizeUnit]

    @classmethod
    def find_by_name(cls, unit_name: str):
        for unit in SizeUnit:
            if unit.name == unit_name:
                return unit
        logger.error(
            f"Size unit {unit_name} is not allowed. You can use only {', '.join([unit.name for unit in SizeUnit])}")
        exit(1)
