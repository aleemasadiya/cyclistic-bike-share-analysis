# Cyclistic Bike-Share Analysis

## Project Overview

This project was completed as part of the Google Data Analytics Professional Certificate capstone case study.

The goal of the analysis was to understand how Cyclistic annual members and casual riders use the bike-share service differently and identify opportunities to convert casual riders into annual members.

## Business Question

How do annual members and casual riders use Cyclistic bikes differently?

## Data

I analyzed 12 months of Cyclistic bike-share trip data from September 2025 through August 2026.

The original combined dataset contained 6,115,982 ride records.

After data cleaning and restricting the analysis to the selected 12-month period, the final dataset contained 6,108,475 rides.

## Tools Used

- Microsoft Excel
- Python
- pandas
- matplotlib

## Data Preparation and Cleaning

I first explored one month of data in Excel to understand the dataset structure, create ride-duration and weekday variables, and practice PivotTable analysis.

Python and pandas were then used to combine and analyze the full 12-month dataset.

The cleaning process included:

- Checking for missing start and end timestamps
- Checking for duplicate ride IDs
- Identifying missing station names
- Removing duplicate ride IDs
- Removing rides lasting 1 second or less
- Removing rides lasting 24 hours or more
- Restricting the dataset to September 2025 through August 2026

Rows with missing station names were retained when the fields needed for the main analysis were still available.

## Key Findings

### 1. Members account for most rides

Annual members accounted for approximately 64.7% of rides, compared with 35.3% for casual riders.

### 2. Casual riders take longer rides

The average casual ride lasted approximately 17.8 minutes, compared with approximately 12.0 minutes for members.

### 3. Rider behavior differs throughout the week

Member activity was strongest during weekdays, while casual rider activity was relatively stronger on weekends.

Casual riders also recorded their longest average ride durations on Saturdays and Sundays.

### 4. Ridership is seasonal

Both member and casual ridership declined significantly during winter and increased through spring and summer.

### 5. Electric bikes were used more frequently

Both casual riders and annual members used electric bikes more frequently than classic bikes.

## Business Recommendations

1. Target frequent weekend casual riders with membership-focused promotions and post-ride conversion offers.

2. Increase membership marketing before and during spring and summer, when casual rider activity rises substantially.

3. Emphasize the financial and convenience benefits of membership to frequent riders who may benefit from switching from repeated casual rides to an annual plan.

## Visualizations

The analysis includes visualizations comparing:

- Ride counts by day of week
- Monthly ridership trends
- Average ride duration by rider type
- Average ride duration by day of week
- Member versus casual ride share

## Conclusion

The analysis suggests that annual members use Cyclistic more frequently and consistently throughout the week, while casual riders take longer rides and show stronger weekend and seasonal usage.

These differences provide opportunities for Cyclistic to target casual riders with more focused membership conversion strategies.