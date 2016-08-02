# TI6 Predictions 

Inspired by [this](https://yasp.co/ti6predictions) I wanted to make something similar.

Why?

Yasp did a great job, but considered too much games(games before 6.88b and some non-pro games too).

This a work in progress and it's currently missing a lot of stuff, code is messy and could be buggy too.

## Requirements

I used a lot of libraries like **Requests** and **BeautifulSoup**.

If you want to try this out you'll also need a Steam Api Key, you can find it [here](https://steamcommunity.com/dev/apikey).

## Explanation

**matches.py** : I selected the series I wanted and I got the match ids I wanted to work with first.

**get_data_.py** : Using the Steam Web Api I got the data I needed.

**heroes.json** : I made a single call to [GetHeroes](https://wiki.teamfortress.com/wiki/WebAPI/GetHeroes) to get the heroes name

**stats.py** : Sorted the data I had and made the output in **finals.txt** , Players names are missing because I was getting encoding errors
