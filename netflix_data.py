import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
import netflix_func as nf
import os


cwd = os.getcwd()
netflix_csv = pd.read_csv("C:\\Users\\Björn\\PythonVenv\\netflix_data\\netflix-report\\CONTENT_INTERACTION\\ViewingActivity.csv") 
name_list = pd.unique(netflix_csv["Profile Name"])
timezone_name = dt.datetime.now(dt.timezone.utc).astimezone().tzinfo
timezone = dt.datetime.utcnow().astimezone().utcoffset().total_seconds()


for name in name_list:
    netflix_csv_partial = netflix_csv[netflix_csv["Profile Name"] == name]
    illegal_character = ["\\", "/", "|", ",", ":", "#", '"', "?", "<", ">", "*"]
    character_list = []
    for character in list(name):
        if character not in illegal_character:
            character_list.append(character)
    name = "".join(character_list)
    name.replace(" ", "_")
    
    #Gets hours from datetime directly from csv and converts from UTC to EST, as well pulls dates
    times = []
    date_of_week = []
    dates = []
    for datetime in netflix_csv_partial['Start Time']:
        date, time = datetime.split(" ")
        time = time - pd.Timedelta(seconds=abs(timezone))
        time = str(time).split(" ")[2]
        time = time.replace("+", "")
        times.append(time)
        date_of_week.append(date)
        date, n = str(date).rsplit("-", 1)
        dates.append(date)
    netflix_data = {"date": dates,
                    "day_of_week":date_of_week, 
                    "time":times,
                    "duration":netflix_csv_partial["Duration"], 
                    "attributes":netflix_csv_partial["Attributes"], 
                    "title":netflix_csv_partial["Title"], 
                    "video_type":netflix_csv_partial["Supplemental Video Type"], 
                    "device_type":netflix_csv_partial["Device Type"]}
    netflix_df = pd.DataFrame(netflix_data)
    

    netflix_df_filtered = netflix_df.loc[(netflix_df["video_type"].isna() == True)]
    netflix_df_shows = netflix_df_filtered[netflix_df_filtered["title"].str.count(":") >= 2]
    netflix_df_movies = netflix_df_filtered[netflix_df_filtered["title"].str.contains("Season|Episode") == False]



    #produces a bar graph for hours both episodes and movies
    bar_time, day_ex = nf.checker(netflix_df_filtered)
    bar_count = pd.Series(bar_time).value_counts()
    hour_df = bar_count.to_frame()
    hour_df = hour_df.sort_index(ascending = True)
    hour_bar = px.bar(hour_df, 
                            title = f"{name}'s Netflix viewed by hour",
                            labels = dict(index = f"Hours in a day in {timezone_name}", 
                            value = "Episodes and movies watched"),
                            text_auto = True,)
    hour_bar.update_layout(showlegend=False)


    #produces a bar graph for days of week both episodes and movies
    day_of_week = []
    for dates in day_ex:
        d = pd.Timestamp(dates)
        day_of_week.append(f"{d.day_of_week} {d.day_name()}")
    date_s = pd.Series(day_of_week).value_counts()
    date_df = date_s.to_frame()
    date_df = date_df.sort_index(ascending = True)
    date_bar = px.bar(date_df, 
                        title = f"{name}'s Netflix viewed by day of the week", 
                        labels = dict(index = "Days of the Week", 
                        value = "Amount viewed"),
                        text_auto = True)
    date_bar.update_layout(showlegend=False)

    #produces a bar graph for only movies for days of week
    bar_time, day_ex = nf.checker(netflix_df_movies)
    day_of_week = []
    for dates in day_ex:
        d = pd.Timestamp(dates)
        day_of_week.append(f"{d.day_of_week} {d.day_name()}")
    date_s = pd.Series(day_of_week).value_counts()
    date_df = date_s.to_frame()
    date_df = date_df.sort_index(ascending = True)
    movie_bar = px.bar(date_df, 
                        title = f"Movies {name} viewed by day of the week", 
                        labels = dict(index = "Days of the Week", 
                        value = "Amount viewed"),
                        text_auto = True)
    movie_bar.update_layout(showlegend=False)


    #Histogram of movies vs shows watched by month
    len_total = netflix_df_filtered["date"].unique()
    watch = pd.DataFrame(columns=['year_month', 'show_amount', 'movie_amount'])
    for year_month in len_total:
        show_count = len(netflix_df_shows[netflix_df_shows["date"] == year_month])
        movie_count = len(netflix_df_movies[netflix_df_movies["date"] == year_month])
        watch_row = {"year_month":year_month, "show_amount":show_count, "movie_amount":movie_count}
        watch_row_df = pd.DataFrame([watch_row])
        watch = pd.concat([watch, watch_row_df], axis = 0, ignore_index = True)
    his_fig = go.Figure(data=[
        go.Bar(name = "Shows watched", x = watch['year_month'], y = watch['show_amount']),
        go.Bar(name = "Movies watched", x=watch['year_month'], y=watch['movie_amount'])])
    his_fig.update_layout(barmode="overlay", title= f"{name}'s watched episodes and movies per month")


    #Find the shows watched in the most watched month
    watch_max = watch[watch["show_amount"] == watch["show_amount"].max()].reset_index()
    shows_max = netflix_df_shows.loc[netflix_df_shows["date"] == str(watch_max["year_month"].iloc[0])]
    shows_max_watched = pd.Series(nf.title_cleaner(shows_max["title"])).value_counts()
    d= f"{dt.datetime.strptime(watch_max['year_month'].iloc[0], '%Y-%m').strftime('%B')} {dt.datetime.strptime(watch_max['year_month'].iloc[0], '%Y-%m').strftime('%Y')}"
    shows_max_par = f"In {d}, {name} watched {sum(shows_max_watched.values)} episodes that breaks down to: <br> {shows_max_watched}"
    shows_max_par = shows_max_par.replace("dtype: int64", "")


    #Find the average of shows and movies watched
    start_d = dt.datetime.strptime(watch['year_month'].iloc[-1], "%Y-%m")
    end_d = dt.datetime.strptime(watch['year_month'].iloc[0], "%Y-%m")
    show_avg = sum(watch["show_amount"])/int((end_d.year - start_d.year) * 12 + (end_d.month - start_d.month))
    show_avg = round(show_avg, 1)
    show_avg_par = f"{name} watched an average of {show_avg} episodes per month"
    movie_avg = sum(watch["movie_amount"])/int((end_d.year - start_d.year) * 12 + (end_d.month - start_d.month))
    movie_avg = round(movie_avg, 2)
    movie_avg_par = f"{name} watched an average of {movie_avg} movies per month"


    #Makes pie graph for top 15 shows
    netflix_df_shows["title_short"] = nf.title_cleaner(netflix_df_shows["title"])
    shows_title = netflix_df_shows["title_short"].value_counts()
    shows_df = pd.DataFrame({"title":shows_title.index, "value":shows_title})
    shows_df = shows_df.reset_index()
    shows_df = shows_df.iloc[:15]
    print(shows_df)
    for show in shows_df.index:
        print(f"A {shows_df['title'][show]}")
        if str(shows_df['title'][show]).endswith(": "):
            show_new= str(shows_df["title"][show]).rsplit(': ', 1)[0]
            shows_df["title"][show] = show_new
            print(shows_df["title"][show])
    show_pie = px.pie(shows_df, values="value", names="title", title=f"{name}'s top 15 watched shows", hole=.6, color_discrete_sequence=px.colors.cyclical.Edge)

    #Save graphs in folder
    graph_cwd = f"{cwd}\\graphs"
    graph_cwd_person = f"{graph_cwd}\\{name}_graphs"
    if os.path.exists(graph_cwd) == False:
        os.mkdir(graph_cwd)
        if os.path.exists(graph_cwd_person) == False:
            os.mkdir(graph_cwd_person)
    else:
        if os.path.exists(graph_cwd_person) == False:
            os.mkdir(graph_cwd_person)
    hour_bar.write_html(f"{graph_cwd_person}\\hour_viewed.html")
    date_bar.write_html(f"{graph_cwd_person}\\day_viewed.html")
    movie_bar.write_html(f"{graph_cwd_person}\\movie_day_viewed.html")
    his_fig.write_html(f"{graph_cwd_person}\\histogram_shows_movies.html")
    show_pie.write_html(f"{graph_cwd_person}\\most_watched_shows.html")


    #creates a new HTML file to run all individual graphs on one page
    html_graphs = open(f"{graph_cwd_person}\\{name}_index.html", "w")
    html_graphs.write(f"<html lang='en'>\n<head>\n<meta charset='utf-8'>\n<link rel='stylesheet' href='{cwd}\\style.css'>\n<title>{name}'s graphs</title>\n</head>\n<body>\n<embed type='text/html' src='day_viewed.html' width='900' height='600'>\n<embed type='text/html' src='movie_day_viewed.html' width='900' height='600'>\n<embed type='text/html' src='hour_viewed.html' width='900' height='600'>\n<embed type='text/html' src='histogram_shows_movies.html' width='900' height='600'>\n<p>\n{shows_max_par}</p>\n<p>\n{movie_avg_par}</p>\n<p>\n{show_avg_par}</p>\n<embed type='text/html' src='most_watched_shows.html' width='900' height='600'>\n</body>\n</html>")
    html_graphs.close()
    os.system(f"{graph_cwd_person}\\{name}_index.html")