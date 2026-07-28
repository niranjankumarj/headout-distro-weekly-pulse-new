from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

from utils import (
    format_number,
    format_percent,
)


class ReportImageGenerator:

    def __init__(self):

        self.width = 1400
        self.padding = 60
        self.line_height = 42

        # Maximum characters per Spotlight line
        self.spotlight_wrap_width = 75

        # Try to use a standard Windows font
        try:
            self.font = ImageFont.truetype(
                "C:/Windows/Fonts/consola.ttf",
                28,
            )

            self.bold_font = ImageFont.truetype(
                "C:/Windows/Fonts/consolab.ttf",
                30,
            )

            self.title_font = ImageFont.truetype(
                "C:/Windows/Fonts/consolab.ttf",
                38,
            )

        except OSError:

            self.font = ImageFont.load_default()
            self.bold_font = ImageFont.load_default()
            self.title_font = ImageFont.load_default()

    # --------------------------------------------------
    # Clean Spotlight Text
    # --------------------------------------------------

    def clean_story_line(self, story_line):

        return (
            story_line
            .replace("📈", "")
            .replace("📉", "")
            .replace("💰", "")
            .replace("🎯", "")
            .replace("🔴", "")
            .replace("🟡", "")
            .strip()
        )

    # --------------------------------------------------
    # Wrap Spotlight Text
    # --------------------------------------------------

    def wrap_story_line(self, story_line):

        cleaned_line = self.clean_story_line(
            story_line
        )

        wrapped_lines = textwrap.wrap(
            cleaned_line,
            width=self.spotlight_wrap_width,
            break_long_words=False,
            break_on_hyphens=False,
        )

        return wrapped_lines

    # --------------------------------------------------
    # Build Report Text
    # --------------------------------------------------

    def build_lines(self, report):

        lines = []

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        lines.append(
            "DISTRO PARTNERSHIP WEEKLY PULSE"
        )

        lines.append("")

        lines.append(
            f"Reporting Week: "
            f"{report['week_start']:%d %b} - "
            f"{report['week_end']:%d %b %Y}"
        )

        lines.append("")
        lines.append("SPOTLIGHT")
        lines.append("")

        # --------------------------------------------------
        # Spotlight
        # --------------------------------------------------

        for story_line in report["story"]:

            wrapped_lines = self.wrap_story_line(
                story_line
            )

            lines.extend(
                wrapped_lines
            )

        lines.append("")
        lines.append("-" * 70)
        lines.append("")

        # --------------------------------------------------
        # Weekly Performance
        # --------------------------------------------------

        lines.append(
            "1. WEEKLY PERFORMANCE"
        )

        lines.append("")

        lines.append(
            f"{'Metric':<20}"
            f"{'This Week':>12}"
            f"{'WoW':>10}"
            f"{'MoM':>10}"
            f"{'YoY':>10}"
        )

        lines.append("-" * 62)

        for name, metric in report["weekly"].items():

            lines.append(
                f"{name:<20}"
                f"{format_number(metric.current):>12}"
                f"{format_percent(metric.growth):>10}"
                f"{format_percent(metric.mom):>10}"
                f"{format_percent(metric.yoy):>10}"
            )

        lines.append("")
        lines.append("-" * 70)
        lines.append("")

        # --------------------------------------------------
        # MTD Performance
        # --------------------------------------------------

        lines.append(
            "2. MTD PERFORMANCE"
        )

        lines.append("")

        lines.append(
            f"{'Metric':<20}"
            f"{'MTD':>12}"
            f"{'MoM':>10}"
            f"{'YoY':>10}"
        )

        lines.append("-" * 52)

        for name, metric in report["mtd"].items():

            lines.append(
                f"{name:<20}"
                f"{format_number(metric.current):>12}"
                f"{format_percent(metric.growth):>10}"
                f"{format_percent(metric.yoy):>10}"
            )

        # --------------------------------------------------
        # Target
        # --------------------------------------------------

        projection = report["projection"]

        achievement = (
            (projection.projected / projection.goal) * 100
            if projection.goal
            else 0
        )

        lines.append("")

        lines.append(
            f"Projected Target Achievement: "
            f"{achievement:.0f}%"
        )

        return lines

    # --------------------------------------------------
    # Generate PNG
    # --------------------------------------------------

    def generate(
        self,
        report,
        output_path="outputs/distro_weekly_pulse.png",
    ):

        lines = self.build_lines(
            report
        )

        # Image height automatically increases
        # if Spotlight text wraps onto additional lines
        height = (
            len(lines) * self.line_height
            + (self.padding * 2)
        )

        image = Image.new(
            "RGB",
            (
                self.width,
                height,
            ),
            "white",
        )

        draw = ImageDraw.Draw(
            image
        )

        y = self.padding

        for index, line in enumerate(lines):

            font = self.font

            # Main title
            if index == 0:

                font = self.title_font

            # Section headings
            elif line in [
                "SPOTLIGHT",
                "1. WEEKLY PERFORMANCE",
                "2. MTD PERFORMANCE",
            ]:

                font = self.bold_font

            draw.text(
                (
                    self.padding,
                    y,
                ),
                line,
                fill="black",
                font=font,
            )

            y += self.line_height

        # --------------------------------------------------
        # Create Output Directory
        # --------------------------------------------------

        output = Path(
            output_path
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # --------------------------------------------------
        # Save Image
        # --------------------------------------------------

        image.save(
            output
        )

        print(
            f"\n✓ Report image generated: {output}"
        )

        return str(
            output
        )