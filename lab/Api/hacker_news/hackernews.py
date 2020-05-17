import requests
import json
import datetime
import time


t1 = time.time()
top_url = 'https://hacker-news.firebaseio.com/v0/{0}.json?print=pretty'
item_url = 'https://hacker-news.firebaseio.com/v0/item/{0}.json?print=pretty'

top_stories_url = top_url.format('topstories')
best_stories_url = top_url.format('beststories')
new_stories_url = top_url.format('newstories')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }


category_file_map = {
    top_stories_url : ('extracted_data/top_stories.json',
                        'extracted_data/index/top_stories_index.json'),

    best_stories_url: ('extracted_data/best_stories.json',
                        'extracted_data/index/best_stories_index.json'),

    new_stories_url: ('extracted_data/new_stories.json',
                        'extracted_data/index/new_stories_index.json')
}

for category, file_path in category_file_map.items():
    posts_list = []
    category_response = requests.get(category, headers= headers)
    id_list = category_response.json()
    total_id = len(id_list)

    for index, post_id in enumerate(id_list):
        post_url = item_url.format(post_id)
        post_response = requests.get(post_url)
        post_dict = post_response.json()
        if not post_dict:
            print("no post found. Breaking this loop..")
            break

        user = post_dict.get('by', None)
        upvotes = post_dict.get('score', None)

        #time management: convert secs to min:secs
        unix_timestamp = post_dict.get('time', None)
        if unix_timestamp:
            posted_time = datetime.datetime.utcfromtimestamp(unix_timestamp)
            current_time = datetime.datetime.utcnow()
            ago = current_time - posted_time

            total_seconds = ago.seconds
            minutes, seconds = divmod(total_seconds, 60)
            hours, minutes = divmod(minutes, 60)

            if hours == 0:
                time_str = '{0} minutes and {1} seconds ago'.format(minutes, seconds)
            else:
                time_str = '{0} hours, {1} minutes, {2} seconds ago'.format(
                                                    hours, minutes, seconds)
        else:
            time = None

        title = post_dict.get('title', None)
        story_url = post_dict.get('url', None)

        final_dict = {
            'user' : user,
            'upvotes' : upvotes,
            'time' : time_str,
            'title' : title,
            'url' : story_url
        }
        posts_list.append(final_dict)

        req_dur = post_response.elapsed.total_seconds()
        time.sleep(req_dur)
        print("got", post_url, "in", req_dur, "Stat:", index+1, "of", total_id)

    print("Finishing current..... Starting next source....")
    with open(file_path[1], 'w') as wf:
        json.dump(id_list, wf)

    with open(file_path[0], 'w') as wf:
        json.dump(posts_list, wf, indent=2)


t2 = time.time()
dur = t2 - t1
print("Finished in ", round(dur, 2), "seconds")
