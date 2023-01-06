import pandas as pd
import datetime as dt

#Edits titles to be useful
def title_cleaner(titles):
    title_list=[]
    for title_name in titles:
        if title_name.find("Season") > -1:
            title_short = title_name.split("Season", 1)[0]
        else:
            title_short = title_name.split(":")[0]
        title_list.append(title_short)
    return title_list


#Checks each entry for duration over hour and day
def checker(new_df):
    bar_time = []
    day_ex = []
    for row in new_df.index:
        bt = str(new_df["time"][row]).split(":")[0]
        bar_time.append(bt)
        t = pd.to_timedelta(new_df["duration"][row])
        check = new_df["time"][row] + t 
        day, check = str(check).rsplit(" ", 1)
        check = check.split(":")[0]
        check = check.replace("+", "")
        day_ex.append(new_df["day_of_week"][row])
        if check != bt:
            bar_time.append(check)
        if day != "0 days":
            day_ex.append(dt.datetime.date((dt.datetime.strptime(new_df['day_of_week'][row], '%Y-%m-%d') + pd.to_timedelta(day))))
    return bar_time, day_ex