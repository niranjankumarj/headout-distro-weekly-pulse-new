from projection import ProjectionEngine


engine = ProjectionEngine()

projection = engine.build(
    actual=122080,
    goal=1300000,
    elapsed_days=3,
    total_days=31,
)

print("=" * 60)
print("Projection Engine")
print("=" * 60)

print()

print(f"Actual MTD : {projection.actual:,.0f}")
print(f"Projected  : {projection.projected:,.0f}")
print(f"Goal       : {projection.goal:,.0f}")
print(f"Gap        : {projection.gap:,.0f}")
print(f"Gap %      : {projection.gap_percent:.2f}%")