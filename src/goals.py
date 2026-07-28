import pandas as pd


class GoalEngine:

    def __init__(self, csv_path):

        self.df = pd.read_csv(csv_path)

    def goal(
        self,
        report_date,
        partnership="Overall",
    ):

        month = report_date.strftime("%B")

        row = self.df[
            self.df["Month"].str.lower()
            == month.lower()
        ]

        if row.empty:
            raise ValueError(
                f"Goal not found for month: {month}"
            )

        return float(
            row.iloc[0][partnership]
        )