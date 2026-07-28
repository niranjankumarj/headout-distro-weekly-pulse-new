from datetime import date

from parser import DashboardData
from dates import DateEngine
from metrics import MetricEngine


dashboard = DashboardData("downloads/affiliate")

datasets = dashboard.load()

gbv = datasets["GBV"]

dates = DateEngine(date(2026, 7, 6))

current_start, current_end = dates.previous_week()

previous_start, previous_end = dates.week_before()

metric = MetricEngine(gbv)

weekly = metric.compare(
    current_start,
    current_end,
    previous_start,
    previous_end,
)

print("=" * 60)
print("Weekly GBV")
print("=" * 60)

print(f"Current Week : {weekly.current:,.2f}")
print(f"Previous Week: {weekly.previous:,.2f}")
print(f"WoW          : {weekly.growth:.2f}%")