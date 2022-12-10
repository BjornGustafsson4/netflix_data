import pandas as pd
import matplotlib.pyplot as plt
import collections

netflix_csv = pd.read_csv("C:\\Users\\Björn\\PythonVenv\\netflix_data\\netflix-report\\CONTENT_INTERACTION\\ViewingActivity.csv", usecols = ['Profile Name', 'Start Time']) 


#Gets hours from datetime directly from csv and converts from UTC to EST
hours = []
for datetime in netflix_csv["Start Time"]:
    date, time = datetime.split(" ")
    time = time - pd.Timedelta(hours=5)
    hour, minute, second = str(time).split(":")
    n, days, hour = hour.split(" ")
    hour = hour.replace("+", "")
    hours.append(hour)


#counts, organizes, and turns hours into percentages
hour_dict = collections.Counter(hours)
hour_dict = collections.OrderedDict(sorted(hour_dict.items()))
for key, value in hour_dict.items():
    hour_dict[key] = (value/len(netflix_csv["Start Time"]))*100


#Makes data into graph
hour_keys = hour_dict.keys()
hour_values = hour_dict.values()
plt.bar(hour_keys, hour_values)
plt.show()