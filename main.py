from scraper import Scrape_this
from gcalendar import save_calendar

import json
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(prog="PROG", allow_abbrev=False)

parser.add_argument("--headless", action="store_true")
parser.add_argument("--no-update", action="store_true")
parser.add_argument("--save-sched", action="store_true")
parser.add_argument(
    "--time",
    type=int,
    default=0,
    help="for time adjustment, \
                                                for example my tz is behind by 1hr \
                                                compared to japan so time is 1",
)

args = parser.parse_args()

if not args.no_update:
    scrape = Scrape_this(
        headless=args.headless,
        url=f"https://www.nogizaka46.com/s/n46/media/list?ima=2046&dy={datetime.now().year}{datetime.now().month}",
    )
    sched = scrape.get_sched()
    if args.save_sched:
        with open("schedule.json", "w", encoding="utf-8") as json_file:
            json.dump(sched, json_file, ensure_ascii=False, indent=2)
else:
    with open("schedule.json", "r", encoding="utf-8") as file:
        sched = json.load(file)

save_calendar(sched, args.time)
