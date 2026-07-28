from datetime import date, timedelta
import calendar
from dateutil.relativedelta import relativedelta


class DateEngine:

    def __init__(self, report_date=None):
        self.report_date = report_date or date.today()

    # --------------------------------------------------
    # Weekly
    # --------------------------------------------------

    def previous_week(self):

        weekday = self.report_date.weekday()

        current_week_start = self.report_date - timedelta(days=weekday)

        previous_week_end = current_week_start - timedelta(days=1)

        previous_week_start = previous_week_end - timedelta(days=6)

        return previous_week_start, previous_week_end

    def week_before(self):

        previous_start, _ = self.previous_week()

        end = previous_start - timedelta(days=1)

        start = end - timedelta(days=6)

        return start, end

    # --------------------------------------------------
    # Weekly MoM
    # --------------------------------------------------

    def previous_month_week(self):

        week_start, week_end = self.previous_week()

        previous_start = week_start - relativedelta(months=1)

        duration = week_end - week_start

        previous_end = previous_start + duration

        return previous_start, previous_end

    # --------------------------------------------------
    # Weekly YoY
    # --------------------------------------------------

    def previous_year_week(self):

        week_start, week_end = self.previous_week()

        previous_start = week_start - relativedelta(years=1)

        previous_end = week_end - relativedelta(years=1)

        return previous_start, previous_end

    # --------------------------------------------------
    # Month to Date
    # --------------------------------------------------

    def current_mtd(self):

        yesterday = self.report_date - timedelta(days=1)

        month_start = yesterday.replace(day=1)

        return month_start, yesterday

    def previous_mtd(self):

        current_start, current_end = self.current_mtd()

        previous_start = current_start - relativedelta(months=1)

        days = (current_end - current_start).days

        previous_end = previous_start + timedelta(days=days)

        return previous_start, previous_end

    def previous_year_mtd(self):

        current_start, current_end = self.current_mtd()

        previous_year_start = current_start - relativedelta(years=1)

        previous_year_end = current_end - relativedelta(years=1)

        return previous_year_start, previous_year_end

    # --------------------------------------------------
    # Projection helpers
    # --------------------------------------------------

    def elapsed_days(self):

        _, end = self.current_mtd()

        return end.day

    def days_in_month(self):

        _, end = self.current_mtd()

        return calendar.monthrange(
            end.year,
            end.month
        )[1]

    # --------------------------------------------------
    # Labels
    # --------------------------------------------------

    def format_range(self, start, end):

        return f"{start:%d %b %Y} → {end:%d %b %Y}"

    def weekly_label(self):

        return self.format_range(*self.previous_week())

    def wow_label(self):

        return self.format_range(*self.week_before())

    def weekly_mom_label(self):

        return self.format_range(*self.previous_month_week())

    def weekly_yoy_label(self):

        return self.format_range(*self.previous_year_week())

    def mtd_label(self):

        return self.format_range(*self.current_mtd())

    def mom_label(self):

        return self.format_range(*self.previous_mtd())

    def yoy_label(self):

        return self.format_range(*self.previous_year_mtd())