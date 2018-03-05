# Senelyzing-4G-Reactions

## Background:
For last couple of weeks, the telecommunication operators in Bangladesh are promoting their clients to avail 4G internet connection enabled sim cards. All these operators are fighting head to head in the world of marketing and advertisement. In the meantime, the actual situation may be a little bit different as I went through the comments in their facebook pages. People are having mixed reactions and even trolls to the operators. So, I just wanted to scrape all the comments and reactions related to 4G posts. It is a fun project to learn about facebook scrapping using python and sentiment analyzing posts and comments.

## Phases:
This experiment is divided in to two phases. They are -

1. Scrape facebook page of GrameenPhone, Robi and Balnglalink and dump 4G related posts and their comments and reactions into CSV file.

2. Analyze the posts and comments and check anything interesting is there for us. (I may plug-in my Banglish sentiment analysis code for fun :) .)

## Weapon of choice and techniques:
- Python
- Facebook Graph API
- Threading
- Recursion to crawl comments

## Code structure:
I have used python as my language of choice here to cover up some basics and getting my hands dirty. I wanted to experiment the graph api also to know how facebook scrapping works. I crawled for 100 posts from the pages as I saw all the 4G related posts were published recently and crawling 100 recent posts are quite enough. Also, there are some goos, nice, stable facebook-sdk libraries online for python, but I wanted to do it by myself.

Initialize the code with your facebook access token first in the code -

    # graph api constants
    graph_api_version = 'v2.12'
    access_token = 'YOUR_ACCESS_TOKEN'

Facebook page ids are hardcoded inside -

    # Facebook page ids [Grameenphone.net, RobiFanz4G, banglalinkmela]
    page_id_list = [['121148644629531', 'gp', False],
    ['681794701899631', 'robi', False],
    ['250144108362888', 'bl', False]]

I took some keywords to search inside the posts and hard-coded those. (yes!!! not to be astonished, but we have 4.5G in Bangldesh as per show and published in numerous media :) )

    keywords = ['4g', '4G', 'ফোরজি', '৪জি', '4.5g', '4.5G']

My data of interest is as -

    reaction_header = ['operator', 'post_id', 'message', 'created_time', 'comments', 'likes', 'love', 'haha', 'sad', 'angry']

I also tried to make the scraping faster with the help of basic threading -

    _thread.start_new_thread(get_post_thread, ("Thread-1", page_id_list[0:1], ))
    _thread.start_new_thread(get_post_thread, ("Thread-2", page_id_list[1:2], ))
    _thread.start_new_thread(get_post_thread, ("Thread-3", page_id_list[2:3], ))

## License
> MPL 2.0

## Result:
I was able to generate 3 CSV files containing the posts, comments and reactions for 3 different operators. The files are -

- gp.csv
- robi.csv
- bl.csv

## To-do:
A lot can be done to improve the code also to visualize and analyze the grabbed data. It's actually a fun project, so codes are a bit raw. Major focus was to grab the comments and analyze if there is something interesting in it.

## Necessary links:
- https://developers.facebook.com/tools/accesstoken/
- https://developers.facebook.com/tools/explorer/
- https://facebook-sdk.readthedocs.io/en/latest/
