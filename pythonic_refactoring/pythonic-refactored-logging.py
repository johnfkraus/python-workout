# https://www.youtube.com/watch?v=bsU7AFjh4m8
# "import this" at terminal to get python philosophy

from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers = [
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

FOOD_CSV = Path("food.csv")
ACTIVITIES_CSV = Path("activities.csv")

def today() -> str:
    return datetime.now().strftime('%Y-%m-%d')

@dataclass
class Entry:
    description: str
    calories: int
    date: str = field(default_factory=today)


def append_entry(filename: Path, entry: Entry) -> None:
    with open(filename, 'a') as f:
        f.write(f'{entry.date},{entry.description},{entry.calories}\n')
    logging.info(f'Appended entry {entry.description} ({entry.calories} kcal) on {entry.date}.')


def read_entries(filename: Path) -> Iterator:
    with open(filename) as f:
        for line in f:
            parts = line.strip().split(',')
            yield Entry(description = parts[1], calories = int(parts[2]), date = parts[0])


def run_day_summary(date: str) -> None:
    logging.info(read_entries(FOOD_CSV))
    logging.debug(f"{len(list(read_entries(FOOD_CSV)))=}")
    logging.warning(f"{len(list(read_entries(ACTIVITIES_CSV)))=}")
    food = list(read_entries(FOOD_CSV))
    activity = list(read_entries(ACTIVITIES_CSV))

    food_total = sum(entry.calories for entry in food if entry.date == date)
    activity_total = sum(entry.calories for entry in activity if entry.date == date)
    logging.error(f"{activity_total=}")

    net = food_total - activity_total
    print(f"Summary for {date}")
    print(f"  Food total:       {food_total}")
    print(f"  Activity total:   {activity_total}")
    print(f"  Net               {net} kcal")


def main() -> None:
    append_entry(FOOD_CSV, Entry("Banana", 100))
    append_entry(ACTIVITIES_CSV, Entry("Running", 50))
    run_day_summary(today())  # "2025-11-23")

if __name__ == "__main__":
    main()