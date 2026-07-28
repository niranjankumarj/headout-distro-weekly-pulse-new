from dataclasses import dataclass


@dataclass
class Projection:

    actual: float
    projected: float
    goal: float
    gap: float
    gap_percent: float


class ProjectionEngine:

    def build(
        self,
        actual,
        goal,
        elapsed_days,
        total_days,
    ):

        if elapsed_days == 0:
            projected = 0
        else:
            projected = (actual / elapsed_days) * total_days

        gap = goal - projected

        if goal == 0:
            gap_percent = 0
        else:
            gap_percent = ((projected - goal) / goal) * 100

        return Projection(
            actual=actual,
            projected=projected,
            goal=goal,
            gap=gap,
            gap_percent=gap_percent,
        )