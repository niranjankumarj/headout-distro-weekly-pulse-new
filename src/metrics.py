from dataclasses import dataclass

import pandas as pd


@dataclass
class Comparison:
    current: float
    previous: float
    growth: float
    mom: float = 0.0
    yoy: float = 0.0


class MetricEngine:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

        self.date_col = "Period"
        self.value_col = "Current Period"

    def total(
        self,
        start_date,
        end_date,
    ):

        mask = (
            (self.df[self.date_col] >= pd.Timestamp(start_date))
            &
            (self.df[self.date_col] <= pd.Timestamp(end_date))
        )

        return self.df.loc[
            mask,
            self.value_col,
        ].sum()

    @staticmethod
    def growth(
        current,
        previous,
    ):

        if previous == 0:
            return 0

        return ((current - previous) / previous) * 100

    def compare(
        self,
        current_start,
        current_end,
        previous_start,
        previous_end,
    ):

        current = self.total(
            current_start,
            current_end,
        )

        previous = self.total(
            previous_start,
            previous_end,
        )

        return Comparison(
            current=current,
            previous=previous,
            growth=self.growth(
                current,
                previous,
            ),
        )