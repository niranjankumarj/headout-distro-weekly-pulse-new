from collections import namedtuple

from story import StoryEngine


Comparison = namedtuple(
    "Comparison",
    [
        "current",
        "previous",
        "growth",
    ]
)

weekly_gbv = Comparison(
    91125,
    135136,
    -32.57,
)

weekly_cm2 = Comparison(
    21400,
    20600,
    3.88,
)

story = StoryEngine()

lines = story.weekly_story(
    weekly_gbv=weekly_gbv,
    weekly_cm2=weekly_cm2,
    projected=1261493,
    goal=1300000,
    best_channel="API Partners",
    best_channel_yoy=42.8,
)

print("=" * 60)
print("Story of the Week")
print("=" * 60)

print()

for line in lines:
    print(line)