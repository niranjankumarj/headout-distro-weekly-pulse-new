from datetime import date

from config import DASHBOARDS
from dates import DateEngine
from goals import GoalEngine
from loaders import load_dashboard
from metrics import MetricEngine
from omni import OmniClient
from projection import ProjectionEngine
from story import StoryEngine
from slack_formatter import SlackFormatter
from mobile_slack_formatter import MobileSlackFormatter
from totals import TotalCalculator
from slack import SlackClient
from report_image import ReportImageGenerator



def main():

    # --------------------------------------------------
    # Report Date
    # --------------------------------------------------

    # Development
    #report_date = date(2026, 6, 29)

    # Production
    report_date = date.today()

    dates = DateEngine(report_date)

    # --------------------------------------------------
    # Weekly Dates
    # --------------------------------------------------

    week_start, week_end = dates.previous_week()

    prev_week_start, prev_week_end = dates.week_before()

    prev_month_week_start, prev_month_week_end = dates.previous_month_week()

    prev_year_week_start, prev_year_week_end = dates.previous_year_week()


    # --------------------------------------------------
    # MTD Dates
    # --------------------------------------------------

    mtd_start, mtd_end = dates.current_mtd()

    prev_mtd_start, prev_mtd_end = dates.previous_mtd()

    yoy_start, yoy_end = dates.previous_year_mtd()

    print("=" * 60)
    print("DISTRO PARTNERSHIP WEEKLY PULSE")
    print("=" * 60)

    # --------------------------------------------------
    # Download latest dashboards
    # --------------------------------------------------

    client = OmniClient()

    client.download_dashboard(
        DASHBOARDS["affiliate"],
        "affiliate",
    )

    client.download_dashboard(
        DASHBOARDS["api_agent"],
        "api_agent",
    )

    # --------------------------------------------------
    # Load dashboards
    # --------------------------------------------------

    print("\nLoading dashboards...")

    affiliate = load_dashboard(
    "downloads/affiliate"
)

    api_agent = load_dashboard(
    "downloads/api_agent"
)

        # --------------------------------------------------
    # Weekly Metrics
    # --------------------------------------------------

    metric_map = [
    ("Affiliate GBV", affiliate, "GBV"),
    ("API GBV", api_agent, "API GBV"),
    ("Agent GBV", api_agent, "Agent GBV"),
    ("Affiliate CM2", affiliate, "Affiliate CM2"),
    ("API+Agent CM2", api_agent, "CM2"),
    ]

    weekly = {}

    for display_name, dashboard, dataset in metric_map:

        engine = MetricEngine(
            dashboard[dataset]
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

        weekly[display_name] = wow

        # --------------------------------------------------
    # Computed Totals
    # --------------------------------------------------

    calculator = TotalCalculator()

    weekly["Total GBV"] = calculator.weekly(
        [
            affiliate["GBV"],
            api_agent["API GBV"],
            api_agent["Agent GBV"],
        ],
        week_start,
        week_end,
        prev_week_start,
        prev_week_end,
        prev_month_week_start,
        prev_month_week_end,
        prev_year_week_start,
        prev_year_week_end,
    )

    weekly["Total CM2"] = calculator.weekly(
        [
            affiliate["Affiliate CM2"],
            api_agent["CM2"],
        ],
        week_start,
        week_end,
        prev_week_start,
        prev_week_end,
        prev_month_week_start,
        prev_month_week_end,
        prev_year_week_start,
        prev_year_week_end,
    )
    # --------------------------------------------------
    # MTD Metrics
    # --------------------------------------------------

    mtd = {}

    for display_name, dashboard, dataset in metric_map:

        engine = MetricEngine(
            dashboard[dataset]
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

        mtd[display_name] = mom

    # --------------------------------------------------
    # Computed Totals
    # --------------------------------------------------

    mtd["Total GBV"] = calculator.mtd(
        [
            affiliate["GBV"],
            api_agent["API GBV"],
            api_agent["Agent GBV"],
        ],
        mtd_start,
        mtd_end,
        prev_mtd_start,
        prev_mtd_end,
        yoy_start,
        yoy_end,
    )

    mtd["Total CM2"] = calculator.mtd(
        [
            affiliate["Affiliate CM2"],
            api_agent["CM2"],
        ],
        mtd_start,
        mtd_end,
        prev_mtd_start,
        prev_mtd_end,
        yoy_start,
        yoy_end,
    )

    # --------------------------------------------------
    # Goal
    # --------------------------------------------------

    goal = GoalEngine(
        "H2 Goal Tracker - Distro - Sheet1.csv"
    ).goal(
        mtd_end
    )

    # --------------------------------------------------
    # Projection
    # --------------------------------------------------

    projection = ProjectionEngine().build(
        actual=mtd["Total GBV"].current,
        goal=goal,
        elapsed_days=dates.elapsed_days(),
        total_days=dates.days_in_month(),
    )

    # --------------------------------------------------
    # Story
    # --------------------------------------------------

    story = StoryEngine().weekly_story(
        weekly["Total GBV"],
        weekly["Total CM2"],
        projection,
        week_end.strftime("%B"),
    )

        # --------------------------------------------------
    # Report
    # --------------------------------------------------

    report = {

        "week_start": week_start,
        "week_end": week_end,

        "weekly": weekly,

        "mtd": mtd,

        "goal": goal,

        "projection": projection,

        "story": story,

        "top_movers": [],

        "needs_attention": [],
    }




    formatter = SlackFormatter()

    message = formatter.build(report)

    print(message)


    # --------------------------------------------------
    # Mobile Message Preview
    # --------------------------------------------------

    mobile_formatter = MobileSlackFormatter()

    mobile_message = mobile_formatter.build(report)

    print("\n" + "=" * 60)
    print("MOBILE MESSAGE PREVIEW")
    print("=" * 60)

    print(mobile_message)

    # --------------------------------------------------
    # Generate Report Image
    # --------------------------------------------------

    image_path = ReportImageGenerator().generate(report)
   

    # --------------------------------------------------
    # Send Desktop Message + Mobile Thread Reply
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("Sending Slack Messages...")
    print("=" * 60)

    slack_client = SlackClient()

    # Send desktop report as the main Slack message
    parent_ts = slack_client.send(message)

    # Upload image version of report as a thread reply
    slack_client.upload_image_to_thread(
        image_path,
        parent_ts,
    )


if __name__ == "__main__":
    main()