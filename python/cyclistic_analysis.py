import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path

raw_data_folder = Path("Raw_Data")
csv_files = sorted(raw_data_folder.glob("*.csv"))

print("Number of CSV files found:", len(csv_files))

for file in csv_files:
    print(file.name)
    
dataframes = []

for file in csv_files:
    print("Reading:", file.name)
    df = pd.read_csv(file)
    dataframes.append(df)

full_year = pd.concat(dataframes, ignore_index=True)

print("Total rows in full-year dataset:", len(full_year))
print("Columns:")
print(full_year.columns.tolist())

full_year["started_at"] = pd.to_datetime(full_year["started_at"])
full_year["ended_at"] = pd.to_datetime(full_year["ended_at"])

full_year["ride_length"] = full_year["ended_at"] - full_year["started_at"]

full_year["day_of_week"] = full_year["started_at"].dt.day_name()

print(full_year[["started_at", "ended_at", "ride_length", "day_of_week"]].head())

print("Missing started_at:", full_year["started_at"].isna().sum())
print("Missing ended_at:", full_year["ended_at"].isna().sum())
print("Missing start station:", full_year["start_station_name"].isna().sum())
print("Missing end station:", full_year["end_station_name"].isna().sum())
print("Duplicate ride IDs:", full_year["ride_id"].duplicated().sum())

short_rides = (full_year["ride_length"] <= pd.Timedelta(seconds=1)).sum()
long_rides = (full_year["ride_length"] >= pd.Timedelta(hours=24)).sum()

print("Rides 1 second or less:", short_rides)
print("Rides 24 hours or more:", long_rides)

# Save the original number of rows
before_cleaning = len(full_year)

# Remove duplicate ride IDs
full_year = full_year.drop_duplicates(subset="ride_id")

# Keep only rides longer than 1 second and shorter than 24 hours
full_year = full_year[
    (full_year["ride_length"] > pd.Timedelta(seconds=1)) &
    (full_year["ride_length"] < pd.Timedelta(hours=24))
]

# Count rows after cleaning
after_cleaning = len(full_year)

print("Rows before cleaning:", before_cleaning)
print("Rows after cleaning:", after_cleaning)
print("Rows removed:", before_cleaning - after_cleaning)

average_ride_length = (
    full_year
    .groupby("member_casual")["ride_length"]
    .mean()
)

print("\nAverage ride length by rider type:")
print(average_ride_length)

rides_by_day = (
    full_year
    .groupby(["member_casual", "day_of_week"])
    .size()
    .unstack()
)

print("\nRide counts by day of week:")
print(rides_by_day)

full_year["month"] = full_year["started_at"].dt.to_period("M")

full_year = full_year[
    (full_year["started_at"] >= "2025-09-01") &
    (full_year["started_at"] < "2026-09-01")
]

rides_by_month = (
    full_year
    .groupby(["month", "member_casual"])
    .size()
    .unstack()
)

print("\nRide counts by month:")
print(rides_by_month)

bike_type_counts = (
    full_year
    .groupby(["member_casual", "rideable_type"])
    .size()
    .unstack()
)

print("\nBike type usage by rider type:")
print(bike_type_counts)

avg_ride_by_day = (
    full_year
    .groupby(["member_casual", "day_of_week"])["ride_length"]
    .mean()
    .unstack()
)

print("\nAverage ride length by day of week:")
print(avg_ride_by_day)

rides_by_rider_type = full_year["member_casual"].value_counts()

print("\nTotal rides by rider type:")
print(rides_by_rider_type)

ride_share = (
    full_year["member_casual"]
    .value_counts(normalize=True)
    * 100
)

print("\nRide share by rider type (%):")
print(ride_share)

from matplotlib.ticker import FuncFormatter

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

# -----------------------------
# CHART 1: RIDES BY DAY
# -----------------------------

rides_by_day = rides_by_day[day_order]

ax = rides_by_day.T.plot(
    kind="bar",
    figsize=(11, 6),
    width=0.75
)

plt.title(
    "Members Lead on Weekdays, Casual Riders on Weekends",
    fontsize=15,
    fontweight="bold",
    pad=18
)

plt.xlabel("")
plt.ylabel("Number of Rides")
plt.xticks(rotation=0)

ax.yaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"{x/1000:.0f}K")
)

ax.grid(axis="y", alpha=0.25, linestyle="--")
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.legend(title="Rider Type", frameon=False)

plt.tight_layout()
plt.savefig("charts/rides_by_day.png", dpi=300, bbox_inches="tight")
plt.close()


# -----------------------------
# CHART 2: MONTHLY TRENDS
# -----------------------------

rides_by_month.index = rides_by_month.index.strftime("%b")

ax = rides_by_month.plot(
    kind="line",
    marker="o",
    linewidth=2.5,
    figsize=(11, 6)
)

plt.title(
    "Cyclistic Ridership Shows Strong Seasonal Patterns",
    fontsize=16,
    fontweight="bold",
    pad=18
)

plt.xlabel("")
plt.ylabel("Number of Rides")

plt.xticks(rotation=0)

ax.yaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"{x/1000:.0f}K")
)

ax.grid(axis="y", alpha=0.25, linestyle="--")
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.legend(title="Rider Type", frameon=False)

plt.tight_layout()

plt.savefig(
    "charts/monthly_ride_trends.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# -----------------------------
# CHART 3: AVERAGE RIDE LENGTH
# -----------------------------

avg_minutes = average_ride_length.dt.total_seconds() / 60

ax = avg_minutes.plot(
    kind="bar",
    figsize=(8, 5),
    width=0.55
)

plt.title(
    "Casual Riders Take Longer Trips on Average",
    fontsize=16,
    fontweight="bold",
    pad=18
)

plt.xlabel("")
plt.ylabel("Average Ride Length (Minutes)")
plt.xticks(rotation=0)

ax.grid(axis="y", alpha=0.25, linestyle="--")
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.1f min",
        padding=5,
        fontweight="bold"
    )

plt.tight_layout()
plt.savefig("charts/average_ride_length.png", dpi=300, bbox_inches="tight")
plt.close()


# -----------------------------
# CHART 4: RIDE SHARE
# -----------------------------

ax = ride_share.plot(
    kind="pie",
    autopct="%1.1f%%",
    figsize=(7, 7),
    startangle=90,
    ylabel=""
)

plt.title(
    "Members Account for Nearly Two-Thirds of All Rides",
    fontsize=15,
    fontweight="bold",
    pad=18
)

plt.tight_layout()

plt.savefig(
    "charts/ride_share.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()