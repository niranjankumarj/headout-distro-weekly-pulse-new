from utils import (
    format_number,
    format_percent,
)


class MobileSlackFormatter:

    # --------------------------------------------------
    # Short Metric Names
    # --------------------------------------------------

    def short_name(self, name):

        aliases = {
            "Affiliate GBV": "Aff GBV",
            "API GBV": "API GBV",
            "Agent GBV": "Agent GBV",
            "Affiliate CM2": "Aff CM2",
            "API+Agent CM2": "API+Ag CM2",
            "Total GBV": "Total GBV",
            "Total CM2": "Total CM2",
        }

        return aliases.get(name, name)

    # --------------------------------------------------
    # Weekly Performance
    # --------------------------------------------------

    def weekly(self, report):

        metrics = report["weekly"]

        rows = []

        rows.append("📱 *Mobile-Friendly View*")
        rows.append("")
        rows.append("1️⃣ *Weekly Performance*")
        rows.append("")

        rows.append("```")

        rows.append(
            f"{'Metric':<11}"
            f"{'Week':>8}"
            f"{'WoW':>8}"
            f"{'MoM':>8}"
            f"{'YoY':>8}"
        )

        rows.append("-" * 43)

        for name, metric in metrics.items():

            display_name = self.short_name(name)

            rows.append(
                f"{display_name:<11}"
                f"{format_number(metric.current):>8}"
                f"{format_percent(metric.growth):>8}"
                f"{format_percent(metric.mom):>8}"
                f"{format_percent(metric.yoy):>8}"
            )

        rows.append("```")
        rows.append("")

        return rows

    # --------------------------------------------------
    # MTD Performance
    # --------------------------------------------------

    def mtd(self, report):

        metrics = report["mtd"]
        projection = report["projection"]

        rows = []

        rows.append("2️⃣ *MTD Performance*")
        rows.append("")

        rows.append("```")

        rows.append(
            f"{'Metric':<11}"
            f"{'MTD':>8}"
            f"{'MoM':>8}"
            f"{'YoY':>8}"
        )

        rows.append("-" * 35)

        for name, metric in metrics.items():

            display_name = self.short_name(name)

            rows.append(
                f"{display_name:<11}"
                f"{format_number(metric.current):>8}"
                f"{format_percent(metric.growth):>8}"
                f"{format_percent(metric.yoy):>8}"
            )

        rows.append("```")
        rows.append("")

        # Calculate projected target achievement
        achievement = (
            (projection.projected / projection.goal) * 100
            if projection.goal
            else 0
        )

        rows.append(
            f"🎯 *Projected Target Achievement:* "
            f"{achievement:.0f}%"
        )

        rows.append("")

        return rows

    # --------------------------------------------------
    # Build Mobile Report
    # --------------------------------------------------

    def build(self, report):

        message = []

        message.extend(
            self.weekly(report)
        )

        message.extend(
            self.mtd(report)
        )

        return "\n".join(message)