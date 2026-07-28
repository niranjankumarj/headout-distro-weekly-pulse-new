from utils import (
    format_number,
    format_percent,
)


class SlackFormatter:

    def divider(self):
        return "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    def header(self, report):

        return [
            "📊 *DISTRO PARTNERSHIP WEEKLY PULSE*",
            "",
            f"*Reporting Week:* {report['week_start']:%d %b} – {report['week_end']:%d %b %Y}",
            "",
        ]

    # --------------------------------------------------
    # Story
    # --------------------------------------------------

    def story(self, report):

        rows = []

        rows.append("🔦 *Spotlight*")
        rows.append("")

        for line in report["story"]:
            rows.append(f"• {line}")

        rows.append("")

        return rows

    # --------------------------------------------------
    # KPI Strip
    # --------------------------------------------------

    def kpi_strip(self, report):

        gbv = report["weekly"]["Total GBV"]
        cm2 = report["weekly"]["Total CM2"]
        projection = report["projection"]

        achievement = 0

        if projection.goal != 0:
            achievement = (
                projection.projected /
                projection.goal
            ) * 100

        gbv_icon = "🟢" if gbv.growth >= 0 else "🔴"
        cm2_icon = "🟢" if cm2.growth >= 0 else "🔴"

        return [
            f"📌 WoW GBV {gbv_icon} {format_percent(gbv.growth)} | "
            f"WoW CM2 {cm2_icon} {format_percent(cm2.growth)} | "
            f"Target 🎯 {achievement:.0f}%",
            "",
            self.divider(),
            "",
        ]

    # --------------------------------------------------
    # Weekly Performance
    # --------------------------------------------------

    def weekly(self, report):

        metrics = report["weekly"]

        rows = []

        rows.append("1️⃣ *Weekly Performance*")
        rows.append("")
        rows.append("```")

        rows.append(
            f"{'Metric':<18}"
            f"{'This Week':>12}"
            f"{'WoW':>9}"
            f"{'MoM':>9}"
            f"{'YoY':>9}"
        )

        rows.append("-" * 60)

        ordered_metrics = [
            "Affiliate GBV",
            "API GBV",
            "Agent GBV",
            "Affiliate CM2",
            "API+Agent CM2",
            "Total GBV",
            "Total CM2",
        ]

        for name in ordered_metrics:

            metric = metrics[name]

            rows.append(
                f"{name:<18}"
                f"{format_number(metric.current):>12}"
                f"{format_percent(metric.growth):>9}"
                f"{format_percent(metric.mom):>9}"
                f"{format_percent(metric.yoy):>9}"
            )

        rows.append("```")
        rows.append("")
        rows.append(self.divider())
        rows.append("")

        return rows

    # --------------------------------------------------
    # MTD Performance
    # --------------------------------------------------

    def mtd(self, report):

        metrics = report["mtd"]
        projection = report["projection"]

        achievement = 0

        if projection.goal != 0:
            achievement = (
                projection.projected /
                projection.goal
            ) * 100

        rows = []

        rows.append("2️⃣ *MTD Performance*")
        rows.append("")
        rows.append("```")

        rows.append(
            f"{'Metric':<18}"
            f"{'MTD':>12}"
            f"{'MoM':>9}"
            f"{'YoY':>9}"
            f"{'Target':>10}"
        )

        rows.append("-" * 70)

        ordered_metrics = [
            "Affiliate GBV",
            "API GBV",
            "Agent GBV",
            "Affiliate CM2",
            "API+Agent CM2",
            "Total GBV",
            "Total CM2",
        ]

        for name in ordered_metrics:

            metric = metrics[name]

            target = ""

            if name == "Total GBV":
                target = f"{achievement:.0f}%"

            rows.append(
                f"{name:<18}"
                f"{format_number(metric.current):>12}"
                f"{format_percent(metric.growth):>9}"
                f"{format_percent(metric.yoy):>9}"
                f"{target:>10}"
            )

        rows.append("```")
        rows.append("")

        return rows

    # --------------------------------------------------
    # Build
    # --------------------------------------------------

    def build(self, report):

        message = []

        message.extend(
            self.header(report)
        )

        message.extend(
            self.story(report)
        )

        message.extend(
            self.kpi_strip(report)
        )

        message.extend(
            self.weekly(report)
        )

        message.extend(
            self.mtd(report)
        )

        return "\n".join(message)