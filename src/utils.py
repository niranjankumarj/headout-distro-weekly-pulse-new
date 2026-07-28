def format_number(value):
    if value is None:
        return "-"

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value/1_000:.1f}K"

    return f"{value:.0f}"


def format_percent(value):

    if value is None:
        return "-"

    if value > 0:
        return f"+{value:.1f}%"

    return f"{value:.1f}%"


def trend_icon(value):

    if value > 0:
        return "🟢"

    if value < 0:
        return "🔻"

    return "⚪"