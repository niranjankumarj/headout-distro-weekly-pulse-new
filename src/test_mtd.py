from dashboard import DashboardData
from metrics import MetricEngine
from goals import GoalEngine
from dates import DateEngine
from mtd import MTDEngine


# ----------------------------------
# Load Affiliate Dashboard
# ----------------------------------

dashboard = DashboardData("downloads/affiliate")
datasets = dashboard.load()

gbv = datasets["GBV"]

metric = MetricEngine(gbv)

# ----------------------------------
# Dates
# ----------------------------------

dates = DateEngine()

mtd_start, mtd_end = dates.current_mtd()

# ----------------------------------
# Goals
# ----------------------------------

goal_engine = GoalEngine(
    "H2 Goal Tracker - Distro - Sheet1.csv"
)

mtd_engine = MTDEngine(goal_engine)

projection = mtd_engine.build(
    metric_engine=metric,
    month_name="July",
    start_date=mtd_start,
    end_date=mtd_end,
    elapsed_days=dates.elapsed_days(),
    total_days=dates.days_in_month(),
)

print("=" * 60)
print("Affiliate MTD")
print("=" * 60)
print()

print(f"Actual     : {projection.actual:,.0f}")
print(f"Projected  : {projection.projected:,.0f}")
print(f"Goal       : {projection.goal:,.0f}")
print(f"Gap        : {projection.gap:,.0f}")
print(f"Gap %      : {projection.gap_percent:.2f}%")