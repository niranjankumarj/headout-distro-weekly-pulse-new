from utils import format_number


class StoryEngine:

    def weekly_story(
        self,
        weekly_gbv,
        weekly_cm2,
        projection,
        month_name,
    ):

        story = []

        # ------------------------------
        # Weekly GBV
        # ------------------------------

        if weekly_gbv.growth >= 0:

            story.append(
                f"📈 Weekly GBV rose from "
                f"{format_number(weekly_gbv.previous)} "
                f"to {format_number(weekly_gbv.current)} "
                f"({weekly_gbv.growth:.1f}% WoW)."
            )

        else:

            story.append(
                f"📉 Weekly GBV fell from "
                f"{format_number(weekly_gbv.previous)} "
                f"to {format_number(weekly_gbv.current)} "
                f"(-{abs(weekly_gbv.growth):.1f}% WoW)."
            )

        # ------------------------------
        # Weekly CM2
        # ------------------------------

        if weekly_cm2.growth >= 0:

            story.append(
                f"💰 Weekly CM2 rose from "
                f"{format_number(weekly_cm2.previous)} "
                f"to {format_number(weekly_cm2.current)} "
                f"({weekly_cm2.growth:.1f}% WoW)."
            )

        else:

            story.append(
                f"💰 Weekly CM2 fell from "
                f"{format_number(weekly_cm2.previous)} "
                f"to {format_number(weekly_cm2.current)} "
                f"(-{abs(weekly_cm2.growth):.1f}% WoW)."
            )

        # ------------------------------
        # Monthly Projection
        # ------------------------------

        achievement = (
            projection.projected
            / projection.goal
        ) * 100

        if achievement >= 100:

            story.append(
                f"🎯 At the current run rate, Distribution is projected to exceed the {month_name} target ({achievement:.0f}% achieved)."
            )

        elif achievement >= 95:

            story.append(
                f"🟡 At the current run rate, Distribution is projected to achieve {achievement:.0f}% of the {month_name} target."
            )

        else:

            story.append(
                f"🔴 At the current run rate, Distribution is projected to achieve {achievement:.0f}% of the {month_name} target."
            )

        return story