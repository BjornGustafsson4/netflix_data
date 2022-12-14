# netflix_data



Issues:
The solution for netflix_df_shows works for almost all shows, some exceptions will have to be made for shows that treat seasons differently then other shows:
1. Shows that call seasons as "book", "Part", "Volume", or "Stranger Things *" (Avatar: The Last Airbender:)
2. One Piece which doesn't use any pattern to naming seasons but uses phrases instead
    Luckily all shows contain "Episode", either in the title somewhere or in parentheses at the end
Going by only "Episode" to find a show could bring up issues, what if a movie has "Episode" in the name 