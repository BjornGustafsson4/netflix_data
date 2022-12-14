import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
from datetime import datetime as datetimes
import plotly
import os


cwd = os.getcwd()
netflix_csv = pd.read_csv("C:\\Users\\Björn\\PythonVenv\\netflix_data\\netflix-report\\CONTENT_INTERACTION\\ViewingActivity.csv") 
name_list = pd.unique(netflix_csv["Profile Name"])
timezone_name = dt.datetime.now(dt.timezone.utc).astimezone().tzinfo
timezone = datetimes.utcnow().astimezone().utcoffset().total_seconds()


for name in name_list:
    netflix_csv_partial = netflix_csv[netflix_csv["Profile Name"] == name]
    #Gets hours from datetime directly from csv and converts from UTC to EST, as well pulls dates
    hours = []
    date_of_week = []
    dates = []
    for datetime in netflix_csv_partial['Start Time']:
        date, time = datetime.split(" ")
        time = time - pd.Timedelta(seconds=abs(timezone))
        hour, minute, second = str(time).split(":")
        n, days, hour = hour.split(" ")
        hour = hour.replace("+", "")
        hours.append(hour)
        date, n = str(date).rsplit("-", 1)
        dates.append(date)
        d = pd.Timestamp(date)
        date_of_week.append(f"{d.day_of_week} {d.day_name()}")
    netflix_data = {"date": dates,
                    "date of week":date_of_week, 
                    "hour":hours, 
                    "attributes":netflix_csv_partial["Attributes"], 
                    "title":netflix_csv_partial["Title"], 
                    "video type":netflix_csv_partial["Supplemental Video Type"], 
                    "device type":netflix_csv_partial["Device Type"]}
    netflix_df = pd.DataFrame(netflix_data)
    

    #filters netflix_df into movies&show, movies, shows.  This isn't perfect refer to README for further details
    netflix_df_filtered = netflix_df.loc[(netflix_df["video type"].isna() == True)]
    netflix_df_shows = netflix_df_filtered[netflix_df_filtered["title"].str.contains("Season|Episode")]
    netflix_df_movies = netflix_df_filtered[netflix_df_filtered["title"].str.contains("Season|Episode") == False]


    #produces a bar graph for hours
    hour_s = netflix_df["hour"].value_counts()
    hour_df = hour_s.to_frame()
    hour_df = hour_df.sort_index(ascending = True)
    hour_bar = px.bar(hour_df, 
                            title = f"{name}'s Netflix viewed by hour",
                            labels = dict(index = f"Hours in a day in {timezone_name}", 
                            value = "Shows and movies watched"))
    hour_bar.show()


    #produces a bar graph for days of week
    date_s = netflix_df["date of week"].value_counts()
    date_df = date_s.to_frame()
    date_df = date_df.sort_index(ascending = True)
    date_bar = px.bar(date_df, 
                        title = f"{name}'s Netflix viewed by day of the week", 
                        labels = dict(index = "Days of the Week", 
                        value = "Amount viewed"))
    date_bar.show()


    #Histogram of movies vs shows watched by month
    len_total = netflix_df_filtered["date"].unique()
    watch = pd.DataFrame(columns=['year month', 'show amount', 'movie amount'])
    for year_month in len_total:
        show_count = len(netflix_df_shows[netflix_df_shows["date"] == year_month])
        movie_count = len(netflix_df_movies[netflix_df_movies["date"] == year_month])
        watch_row = {"year month":year_month, "show amount":show_count, "movie amount":movie_count}
        watch_row_df = pd.DataFrame([watch_row])
        watch = pd.concat([watch, watch_row_df], axis = 0, ignore_index = True)
    his_fig = go.Figure(data=[
        go.Bar(name = "Shows watched", x = watch['year month'], y = watch['show amount']),
        go.Bar(name = "Movies watched", x=watch['year month'], y=watch['movie amount'])
    ])
    his_fig.update_layout(barmode="overlay", title= f"{name}'s watched shows and movies per month")
    his_fig.show()


    #Makes pie graph for top 15 shows Pie graph issue see README for details
    title_list=[]
    for title_name in netflix_df_shows["title"]:
        title_short = title_name.split("Season", 1)
        title_list.append(title_short[0])
    netflix_df_shows["title short"] = title_list 
    shows_title = netflix_df_shows["title short"].value_counts()
    shows_data = {"title":shows_title.index, "value":shows_title}
    shows_df = pd.DataFrame(shows_data)
    shows_df = shows_df.reset_index()
    shows_df = shows_df.iloc[:15]
    show_pie = px.pie(shows_df, values="value", names="title", title=f"{name}'s top 15 watched showes", hole=.6)
    show_pie.show()

    
    #auto open crashes my VSCode for no reason
    #TODO Save all graphs somehow to put into an html page
    #hour_bar.write_html(f"{cwd}\\{name}_hour_bar.html")
    #date_bar.write_html(f"{cwd}\\{name}_date_bar.html")
    #his_fig.write_html(f"{cwd}\\{name}_his_fig.html")
    #show_pie.write_html(f"{cwd}\\{name}_show_pie.html")