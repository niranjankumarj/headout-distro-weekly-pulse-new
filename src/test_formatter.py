from datetime import date
from collections import namedtuple

from slack_formatter import SlackFormatter


Comparison = namedtuple(
    "Comparison",
    [
        "current",
        "previous",
        "growth",
        "yoy",
    ]
)

weekly_gbv = Comparison(
    current=91125,
    previous=135136,
    growth=-32.57,
    yoy=18.4,
)

weekly_cm2 = Comparison(
    current=21400,
    previous=20600,
    growth=3.88,
    yoy=26.8,
)

story = [
    "📉 GBV declined *32.6% WoW*, while CM2 increased *3.9% WoW*.",
    "🎯 Current run rate projects *97%* achievement of the July goal.",
    "🚀 API Partners remained the strongest-performing channel (+42.8% YoY).",
]

formatter = SlackFormatter()

message = formatter.build(
    week_start=date(2026, 6, 22),
    week_end=date(2026, 6, 28),
    story=story,
    weekly_gbv=weekly_gbv,
    weekly_cm2=weekly_cm2,
    projected=1261493,
    goal=1300000,
)

print(message)