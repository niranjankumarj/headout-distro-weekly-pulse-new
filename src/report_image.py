from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

from utils import (
    format_number,
    format_percent,
)


class ReportImageGenerator:

    def __init__(self):

        # --------------------------------------------------
        # Layout
        # --------------------------------------------------

        # Canvas width is now computed automatically from the
        # longest rendered line (see generate()). This is just
        # a safety ceiling so a single absurdly long line can't
        # blow the image up.
        self.max_width = 1600

        self.padding_x = 40
        self.padding_y = 36
        self.line_height = 34

        # Maximum characters per Spotlight line (wrapping is
        # character-based, independent of font size)
        self.spotlight_wrap_width = 78

        self.font, self.bold_font, self.title_font = self._load_fonts()

    # --------------------------------------------------
    # Font loading
    # --------------------------------------------------
    #
    # Table columns in this report are aligned using fixed-width
    # string formatting (f"{name:<18}..."), so the font MUST be
    # monospaced or columns will visually drift out of alignment.
    #
    # We try, in order:
    #   1. A font shipped inside this repo (most reliable —
    #      identical on every machine, no install step needed)
    #   2. Common Linux paths (GitHub Actions ubuntu-latest, if
    #      `apt-get install fonts-dejavu-core` has been run)
    #   3. Common Windows paths (local dev machine)
    #   4. Common macOS paths
    #   5. Pillow's built-in scalable font as an absolute last
    #      resort (Pillow >= 10.1 supports a `size` argument here,
    #      so even the fallback is legible instead of 10px tall —
    #      but note it is NOT monospaced, so table columns will
    #      lose alignment if this path is ever hit).

    def _repo_font_dir(self):
        return Path(__file__).resolve().parent / "fonts"

    def _candidate_paths(self):

        repo_fonts = self._repo_font_dir()

        return {
            "regular": [
                repo_fonts / "DejaVuSansMono.ttf",
                Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
                Path("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"),
                Path("C:/Windows/Fonts/consola.ttf"),
                Path("/System/Library/Fonts/Menlo.ttc"),
                Path("/Library/Fonts/Menlo.ttc"),
            ],
            "bold": [
                repo_fonts / "DejaVuSansMono-Bold.ttf",
                Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
                Path("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"),
                Path("C:/Windows/Fonts/consolab.ttf"),
                Path("/System/Library/Fonts/Menlo.ttc"),
                Path("/Library/Fonts/Menlo.ttc"),
            ],
        }

    def _first_existing(self, paths):
        for path in paths:
            if Path(path).exists():
                return str(path)
        return None

    def _load_fonts(self):

        candidates = self._candidate_paths()

        regular_path = self._first_existing(candidates["regular"])
        bold_path = self._first_existing(candidates["bold"])

        # Sizes: bumped up noticeably from the original (28/30/38)
        body_size = 34
        bold_size = 34
        title_size = 46

        if regular_path and bold_path:

            font = ImageFont.truetype(regular_path, body_size)
            bold_font = ImageFont.truetype(bold_path, bold_size)
            title_font = ImageFont.truetype(bold_path, title_size)

            return font, bold_font, title_font

        # --------------------------------------------------
        # Fallback: no monospace font found on this machine.
        # Use Pillow's bundled scalable font so text is at least
        # readable, and warn loudly so it gets noticed/fixed.
        # --------------------------------------------------

        print(
            "\n⚠️  WARNING: No monospace font found (checked repo /fonts, "
            "Linux, Windows, macOS paths). Falling back to Pillow's default "
            "font. Table columns will NOT align correctly. Install a "
            "monospace font (e.g. `apt-get install fonts-dejavu-core` in "
            "CI) or add DejaVuSansMono.ttf / DejaVuSansMono-Bold.ttf to a "
            "'fonts/' folder next to this script.\n"
        )

        try:
            # Pillow >= 10.1 lets load_default take a size
            font = ImageFont.load_default(size=body_size)
            bold_font = ImageFont.load_default(size=bold_size)
            title_font = ImageFont.load_default(size=title_size)
        except TypeError:
            # Older Pillow: no size support at all
            font = ImageFont.load_default()
            bold_font = font
            title_font = font

        return font, bold_font, title_font

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
            ("title", "DISTRO PARTNERSHIP WEEKLY PULSE")
        )

        lines.append(("body", ""))

        lines.append(
            (
                "body",
                f"Reporting Week: "
                f"{report['week_start']:%d %b} - "
                f"{report['week_end']:%d %b %Y}",
            )
        )

        lines.append(("body", ""))
        lines.append(("bold", "SPOTLIGHT"))
        lines.append(("body", ""))

        # --------------------------------------------------
        # Spotlight
        # --------------------------------------------------

        for story_line in report["story"]:

            wrapped_lines = self.wrap_story_line(
                story_line
            )

            for wrapped in wrapped_lines:
                lines.append(("body", wrapped))

        lines.append(("body", ""))
        lines.append(("body", "-" * 70))
        lines.append(("body", ""))

        # --------------------------------------------------
        # Weekly Performance
        # --------------------------------------------------

        lines.append(("bold", "1. WEEKLY PERFORMANCE"))
        lines.append(("body", ""))

        lines.append(
            (
                "body",
                f"{'Metric':<20}"
                f"{'This Week':>12}"
                f"{'WoW':>10}"
                f"{'MoM':>10}"
                f"{'YoY':>10}",
            )
        )

        lines.append(("body", "-" * 62))

        for name, metric in report["weekly"].items():

            lines.append(
                (
                    "body",
                    f"{name:<20}"
                    f"{format_number(metric.current):>12}"
                    f"{format_percent(metric.growth):>10}"
                    f"{format_percent(metric.mom):>10}"
                    f"{format_percent(metric.yoy):>10}",
                )
            )

        lines.append(("body", ""))
        lines.append(("body", "-" * 70))
        lines.append(("body", ""))

        # --------------------------------------------------
        # MTD Performance
        # --------------------------------------------------

        lines.append(("bold", "2. MTD PERFORMANCE"))
        lines.append(("body", ""))

        lines.append(
            (
                "body",
                f"{'Metric':<20}"
                f"{'MTD':>12}"
                f"{'MoM':>10}"
                f"{'YoY':>10}",
            )
        )

        lines.append(("body", "-" * 52))

        for name, metric in report["mtd"].items():

            lines.append(
                (
                    "body",
                    f"{name:<20}"
                    f"{format_number(metric.current):>12}"
                    f"{format_percent(metric.growth):>10}"
                    f"{format_percent(metric.yoy):>10}",
                )
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

        lines.append(("body", ""))

        lines.append(
            (
                "bold",
                f"Projected Target Achievement: "
                f"{achievement:.0f}%",
            )
        )

        return lines

    # --------------------------------------------------
    # Font lookup helper
    # --------------------------------------------------

    def _font_for(self, style):

        if style == "title":
            return self.title_font

        if style == "bold":
            return self.bold_font

        return self.font

    # --------------------------------------------------
    # Measure required canvas width
    # --------------------------------------------------

    def _measure_width(self, lines):

        # Use a throwaway 1x1 image purely to get a drawing
        # context capable of measuring text extents.
        probe = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(probe)

        max_line_width = 0

        for style, text in lines:

            if not text:
                continue

            font = self._font_for(style)

            bbox = draw.textbbox((0, 0), text, font=font)
            line_width = bbox[2] - bbox[0]

            max_line_width = max(max_line_width, line_width)

        width = max_line_width + (self.padding_x * 2)

        return min(width, self.max_width)

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

        width = self._measure_width(lines)

        height = (
            len(lines) * self.line_height
            + (self.padding_y * 2)
        )

        image = Image.new(
            "RGB",
            (width, height),
            "white",
        )

        draw = ImageDraw.Draw(
            image
        )

        y = self.padding_y

        for style, text in lines:

            font = self._font_for(style)

            draw.text(
                (
                    self.padding_x,
                    y,
                ),
                text,
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
            f"\n✓ Report image generated: {output} ({width}x{height})"
        )

        return str(
            output
        )