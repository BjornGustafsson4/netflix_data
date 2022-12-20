def title_cleaner(titles):
    title_list=[]
    for title_name in titles:
        if title_name.find("Season") > -1:
            title_short = title_name.split("Season", 1)[0]
        else:
            title_short = title_name.split(":")[0]
        title_list.append(title_short)
    return title_list