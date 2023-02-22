import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

# Define date parser function
def date_parser(date_str):
    return pd.datetime.strptime(date_str, '%d/%m/%Y')

# Read data from CSV file
df = pd.read_csv("data.csv", parse_dates=["Enter start date", "Enter end date"], date_parser=date_parser)

# Extract columns from DataFrame
start_dates = df["Enter start date"]
end_dates = df["Enter end date"]
names = df["First Name"]

# Convert dates to datetime objects
start_datetimes = start_dates.values.astype('datetime64[D]')
end_datetimes = end_dates.values.astype('datetime64[D]')

# Compute time range
min_datetime = np.min(start_datetimes)
max_datetime = np.max(end_datetimes)
days = (max_datetime - min_datetime).astype(int) + 1

# Create list of date strings for tick labels
date_strings = [(min_datetime + np.timedelta64(i, 'D')).astype(datetime.datetime).strftime('%d/%m/%Y') for i in range(days)]

# Create empty availability matrix
availability = np.zeros((len(names), days))

# Fill availability matrix
for i in range(len(names)):
    start_index = (start_datetimes[i] - min_datetime).astype(int)
    end_index = (end_datetimes[i] - min_datetime).astype(int) + 1
    availability[i, start_index:end_index] = 1

# Compute availability for each time slot
availability_sum = np.sum(availability, axis=0)

# Find time range with maximum availability
best_start_index = np.argmax(availability_sum)
availability_sum_reversed = np.flip(availability_sum)
best_end_index = days - np.argmax(availability_sum_reversed) - 1
best_time_range = (min_datetime + np.timedelta64(best_start_index, 'D'), min_datetime + np.timedelta64(best_end_index, 'D'))

# Print best time range to console
print("Best time range:", best_time_range)

# Plot availability
plt.figure(figsize=(10, 5))
plt.title('Time Availability Mini UN Montpellier Reunion')
plt.xlabel('Date')
plt.ylabel('Person')
plt.yticks(np.arange(len(names)), names)
plt.imshow(availability, cmap='Greys', aspect='auto', extent=[0, days, len(names), 0])
plt.axvspan(best_start_index, best_end_index + 1, color='green', alpha=0.8)
plt.xticks([best_start_index, best_end_index], 
           [np.datetime_as_string(best_time_range[0], unit='D'), np.datetime_as_string(best_time_range[1], unit='D')], 
           rotation=0)
plt.show()
