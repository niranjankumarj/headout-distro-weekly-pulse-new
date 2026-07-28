from datetime import date

from dates import DateEngine
from goals import GoalEngine


dates = DateEngine(date(2026, 7, 4))

goal_engine = GoalEngine("H2 Goal Tracker - Distro - Sheet1.csv")

goal = goal_engine.goal("July")

actual = 122080

projection = goal_engine.projected(
    actual,
    dates.elapsed_days(),
    dates.days_in_month()
)

gap = goal_engine.gap(
    projection,
    goal
)

gap_percent = goal_engine.gap_percent(
    projection,
    goal
)

print("=" * 60)
print("Goal Engine")
print("=" * 60)

print()

print(f"Elapsed Days : {dates.elapsed_days()}")

print(f"Days in Month: {dates.days_in_month()}")

print()

print(f"Actual MTD   : {actual:,.0f}")

print(f"Projected    : {projection:,.0f}")

print(f"Goal         : {goal:,.0f}")

print(f"Gap          : {gap:,.0f}")

print(f"Gap %        : {gap_percent:.2f}%")