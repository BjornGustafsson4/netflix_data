import pandas as pd
import matplotlib.pyplot as plt
import collections


netflix_csv = pd.read_csv("C:\\Users\\Björn\\PythonVenv\\netflix_data\\netflix-report\\CONTENT_INTERACTION\\ViewingActivity.csv", usecols = ['Profile Name', 'Start Time']) 
#Gets hours from datetime directly from csv and converts from UTC to EST, as well pulls dates
hours = []
dates = []
for datetime in netflix_csv["Start Time"]:
    date, time = datetime.split(" ")
    time = time - pd.Timedelta(hours=5)
    hour, minute, second = str(time).split(":")
    n, days, hour = hour.split(" ")
    hour = hour.replace("+", "")
    hours.append(hour)
    d = pd.Timestamp(date)
    dates.append(f"{d.day_of_week} {d.day_name()}")


#counts, organizes, and turns hours into percentages
hour_dict = collections.Counter(hours)
hour_dict = collections.OrderedDict(sorted(hour_dict.items()))
for key, value in hour_dict.items():
    hour_dict[key] = (value/len(netflix_csv["Start Time"]))*100



hour_keys = hour_dict.keys()
hour_values = hour_dict.values()
plt.title("Probability of watching Netflix based on time")
plt.xlabel("Hours in a day (24 hour clock)")
plt.ylabel("Probability of watching Netflix")
plt.bar(hour_keys, hour_values)
plt.show()


dates_dict = collections.Counter(dates)
dates_dict = collections.OrderedDict(sorted(dates_dict.items()))
for key, value in dates_dict.items():
    dates_dict[key] = (value/len(netflix_csv["Start Time"]))*100


date_keys = dates_dict.keys()
date_values = dates_dict.values()
plt.title(f"Percentage of all Netflix viewed by day of the Week")
plt.xlabel("Days of the Week")
plt.ylabel("Percentage viewed")
plt.bar(date_keys, date_values)
plt.show()