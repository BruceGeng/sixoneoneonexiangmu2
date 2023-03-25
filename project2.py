__author_1__ = "Yipeng Geng, yg2913"
__author_2__ = "Yufei Liu, yl5099"

import pprint
import sys
from googleapiclient.discovery import build
import numpy as np
import spacy
from spanbert import SpanBERT
import requests

def google_search(query, google_api_key, google_engine_id):
    service = build(
        "customsearch", "v1", developerKey=google_api_key
    )

    res = (
        service.cse()
            .list(
            q=query,
            cx=google_engine_id,
        )
            .execute()
    )
    return res

def main():
    method = sys.argv[1]
    google_api_key = sys.argv[2]
    google_engine_id = sys.argv[3]
    openai_key = sys.argv[4]
    r = sys.argv[5]
    t = float(sys.argv[6])
    q = sys.argv[7]
    k = int(sys.argv[8])
    relations = {'1': 'Schools_Attended', '2': 'Work_For', '3': 'Live_In', '4': 'Top_Member_Employees'}

    print("Parameters:")
    print("Client key      =", google_api_key)
    print("Engine key      =", google_engine_id)
    print("OpenAI key      =", openai_key)
    print("Method  =",      method[1:])
    print("Relation        =", relations[r])
    print("Threshold       =", t)
    print("Query           =", q)
    print("# of Tuples     =", k)
    print("Loading necessary libraries; This should take a minute or so ...)\n")

    nlp = spacy.load("en_core_web_lg")
    spanbert = SpanBERT("./pretrained_spanbert")
    goal_check = False
    first_iter = True
    iter = -1
    vis = set() # visited url
    while not goal_check:
        iter += 1
        print('=========== Iteration: {} - Query: {} ===========\n\n'.format(iter, q))
        retrieved = google_search(q, google_api_key, google_engine_id)['items']
        retrieved = retrieved[:min(10, len(retrieved))]
        cnt = 0
        for r in retrieved:
            cnt += 1

            url = r['formattedUrl']
            print(url)
            print("URL ( {} / {}): {}".format(cnt, len(retrieved), url))
            if url not in vis:
                vis.add(url)
                print('Fetching text from url ...')
                try:
                    webpage = requests.get(url)
                except:
                    print('if you cannot retrieve the webpage (e.g., because of a timeout), just skip it and move on')
                    continue
            else:
                print("you should skip already-seen URLs")
                continue
            print(webpage.text)

        goal_check = True


















if __name__ == "__main__":
    main()
