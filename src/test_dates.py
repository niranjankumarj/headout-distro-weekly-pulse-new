from datetime import date

from dates import DateEngine

engine = DateEngine(date(2026, 6, 29))

print("=" * 60)
print("DATE ENGINE TEST")
print("=" * 60)

print()

print("Weekly")
print(engine.weekly_label())

print()

print("WoW")
print(engine.wow_label())

print()

print("MTD")
print(engine.mtd_label())

print()

print("MoM")
print(engine.mom_label())