
# coding: utf-8

# # Public Reactions regarding 4G

# Now days the telecom operator are promoting 4G network to the people so that they get attracted to it. We just wanted to know about the reactions of the people on social media through their comments, likes and smileys.

# libraries
import requests
import _thread
import json
from collections import namedtuple
import csv
import re
import sys

# graph api constants
graph_api_version = 'v2.12'
access_token = 'YOUR_ACCESS_TOKEN'

# Facebook page ids [Grameenphone.net, RobiFanz4G, banglalinkmela]
page_id_list = [['121148644629531', 'gp', False],
                ['681794701899631', 'robi', False],
                ['250144108362888', 'bl', False]]

keywords = ['4g', '4G', 'ফোরজি', '৪জি', '4.5g', '4.5G']  # interesting but true ... we have 4.5G in Bangladesh
words_re = re.compile("|".join(keywords))

reaction_header = ['operator', 'post_id', 'message', 'created_time', 'comments', 'likes', 'love', 'haha', 'sad', 'angry']

url_get_posts_stat = 'https://graph.facebook.com/{0}/{1}/posts?limit=100&fields=message,created_time,likes.limit(0).summary(total_count).as(reactions_like),reactions.type(LOVE).limit(0).summary(total_count).as(reactions_love),reactions.type(HAHA).limit(0).summary(total_count).as(reactions_haha),reactions.type(WOW).limit(0).summary(total_count).as(reactions_wow),reactions.type(SAD).limit(0).summary(total_count).as(reactions_sad),reactions.type(ANGRY).limit(0).summary(total_count).as(reactions_angry),comments.limit(0).summary(total_count).as(reactions_comments)'

url_get_comments_stat = 'https://graph.facebook.com/{0}/{1}?fields=comments.limit(100){{message,created_time,likes.limit(0).summary(total_count).as(reactions_like),reactions.type(LOVE).limit(0).summary(total_count).as(reactions_love),reactions.type(HAHA).limit(0).summary(total_count).as(reactions_haha),reactions.type(WOW).limit(0).summary(total_count).as(reactions_wow),reactions.type(SAD).limit(0).summary(total_count).as(reactions_sad),reactions.type(ANGRY).limit(0).summary(total_count).as(reactions_angry),comments.limit(0).summary(total_count).as(reactions_comments)}}'

# control variables
total_threads = 0
thread_started = False


# convert json to python object
def json2object(json_string):
    return json.loads(json_string, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


# convert fb object (comment/post) to an array to make csv friendly
def reactions2csv(operator_name, reaction_obj_list):
    post_reaction = []
    post_reaction.append(operator_name)
    post_reaction.append(reaction_obj_list.id)
    message = re.sub(",|\n", " ", reaction_obj_list.message)
    post_reaction.append(message)
    post_reaction.append(reaction_obj_list.created_time)
    post_reaction.append(reaction_obj_list.reactions_comments.summary.total_count)
    post_reaction.append(reaction_obj_list.reactions_like.summary.total_count)
    post_reaction.append(reaction_obj_list.reactions_love.summary.total_count)
    post_reaction.append(reaction_obj_list.reactions_haha.summary.total_count)
    post_reaction.append(reaction_obj_list.reactions_sad.summary.total_count)
    post_reaction.append(reaction_obj_list.reactions_angry.summary.total_count)
    return post_reaction


# write a csv file with the input list
def writeList2csvFile(filename, list, mode="w"):
    with open(filename + ".csv", mode, encoding='utf-8') as output:
        writer = csv.writer(output, lineterminator='\n', delimiter=',')
        writer.writerows(list)
    return


# recursive function to crawl the comments (dfs)
def crawl4comments(result_list, operator_name, fb_post_id, is_url=False):  # either id or url
    global graph_api_version, access_token
    url_comments = fb_post_id
    if is_url is False:
        url_comments = url_get_comments_stat.format(graph_api_version, fb_post_id)

    # url_comments = urllib.parse.quote(url_comments)
    # print(url_comments)

    response = requests.get(url_comments, params={'access_token': access_token})
    comment_obj_list = json2object(response.content)

    if not hasattr(comment_obj_list, 'comments'):
        return

    for comment_obj in comment_obj_list.comments.data:
        # print(str(comment_obj.message) + " C: " + str(comment_obj.reactions_comments.summary.total_count))
        result_list.append(reactions2csv(operator_name, comment_obj))
        if comment_obj.reactions_comments.summary.total_count > 0:
            crawl4comments(result_list, operator_name, comment_obj.id)

    if hasattr(comment_obj_list.comments.paging, 'next'):
        crawl4comments(result_list, operator_name, comment_obj_list.comments.paging.next, True)

    # sys.exit(0)
    return


# get the posts from the pages
def get_post_thread(thread_name, fb_object_list):
    global total_threads, thread_started

    result_list = []
    result_list.append(reaction_header)

    total_threads += 1
    thread_started = True

    for fb_object in fb_object_list:
        url_posts = fb_object[0]
        operator_name = fb_object[1]
        if fb_object[2] is False:
            url_posts = url_get_posts_stat.format(graph_api_version, fb_object[0])

        response = requests.get(url_posts, params={'access_token': access_token})
        posts_obj_list = json2object(response.content).data

        for post_obj in posts_obj_list:
            try:
                if not words_re.search(post_obj.message):
                    continue
                result_list.append(reactions2csv(operator_name, post_obj))
                crawl4comments(result_list, operator_name, post_obj.id)
            except Exception as exp:
                continue

    # print(result_list)
    writeList2csvFile(operator_name, result_list)
    print(thread_name + " has finished for: " + operator_name)
    total_threads -= 1
    return


# Create three threads for three pages
try:
    _thread.start_new_thread(get_post_thread, ("Thread-1", page_id_list[0:1], ))
    _thread.start_new_thread(get_post_thread, ("Thread-2", page_id_list[1:2], ))
    _thread.start_new_thread(get_post_thread, ("Thread-3", page_id_list[2:3], ))
except Exception as exp:
    print(exp)

while not thread_started:
    pass
while total_threads > 0:
    pass
