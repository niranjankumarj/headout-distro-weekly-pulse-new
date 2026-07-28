import pandas as pd

from metrics import MetricEngine


class TotalCalculator:

    def __init__(self):

        pass

    # --------------------------------------------------
    # Build Total DataFrame
    # --------------------------------------------------

    def dataframe(self, *datasets):

        total = datasets[0][["Period"]].copy()

        total["Current Period"] = 0

        for df in datasets:

            merged = total.merge(
                df,
                on="Period",
                how="outer",
                suffixes=("", "_new"),
            )

            merged["Current Period"] = (
                merged["Current Period"].fillna(0)
                +
                merged["Current Period_new"].fillna(0)
            )

            merged.drop(
                columns=["Current Period_new"],
                inplace=True,
            )

            total = merged

        total.sort_values(
            "Period",
            inplace=True,
        )

        total.reset_index(
            drop=True,
            inplace=True,
        )

        return total

    # --------------------------------------------------
    # Weekly
    # --------------------------------------------------

    def weekly(
        self,
        datasets,
        week_start,
        week_end,
        prev_week_start,
        prev_week_end,
        prev_month_week_start,
        prev_month_week_end,
        prev_year_week_start,
        prev_year_week_end,
    ):

        engine = MetricEngine(
            self.dataframe(*datasets)
        )

        wow = engine.compare(
            week_start,
            week_end,
            prev_week_start,
            prev_week_end,
        )

        mom = engine.compare(
            week_start,
            week_end,
            prev_month_week_start,
            prev_month_week_end,
        )

        yoy = engine.compare(
            week_start,
            week_end,
            prev_year_week_start,
            prev_year_week_end,
        )

        wow.mom = mom.growth
        wow.yoy = yoy.growth

        return wow

    # --------------------------------------------------
    # MTD
    # --------------------------------------------------

    def mtd(
        self,
        datasets,
        mtd_start,
        mtd_end,
        prev_mtd_start,
        prev_mtd_end,
        yoy_start,
        yoy_end,
    ):

        engine = MetricEngine(
            self.dataframe(*datasets)
        )

        mom = engine.compare(
            mtd_start,
            mtd_end,
            prev_mtd_start,
            prev_mtd_end,
        )

        yoy = engine.compare(
            mtd_start,
            mtd_end,
            yoy_start,
            yoy_end,
        )

        mom.yoy = yoy.growth

        return mom