from flask import Flask, jsonify, request
from pytrends.request import TrendReq
import pandas as pd
import re
import random
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

MAX_CONNECTIONS = 5

class TrendReqPool:
    def __init__(self):
        self.connection_pool = []

    def get_connection(self):
        if not self.connection_pool:
            pytrends = TrendReq(hl='en-US', tz=360)
            return pytrends
        else:
            return self.connection_pool.pop()

    def return_connection(self, pytrends):
        self.connection_pool.append(pytrends)

trendreq_pool = TrendReqPool()

def extract_arrays(list_of_items):
  """Extracts the arrays and their values from a list and returns a new list with the arrays as separate items.

  Args:
    list_of_items: A list of items, some of which are arrays.

  Returns:
    A new list with the arrays as separate items.
  """

  new_list = []
  for item in list_of_items:
    if isinstance(item, list):
      new_list.extend(item)
    elif "," not in item:
      new_list.append(item)

  return new_list

def remove_non_english(data):
  """Removes all non-English characters from a string.

  Args:
    data: The string to be modified.

  Returns:
    The modified string.
  """

  non_english_regex = re.compile(r'[^\x00-\x7F]')
  modified_data = non_english_regex.sub('', data)
  return modified_data


@cache.memoize(timeout=60*60)  # Cache the response for 1 hour
def fetch_suggestions(keyword, pytrends):
    return pytrends.suggestions(keyword=keyword)

@app.route('/', methods=['GET'])
def get_search_trends():
    pytrends_pool = trendreq_pool

    with ThreadPoolExecutor(max_workers=MAX_CONNECTIONS) as executor:
        pytrends = pytrends_pool.get_connection()

        trending_searches_df = pytrends.trending_searches(pn='united_states')
        trending_searches_df_canada = pytrends.trending_searches(pn='canada')
        realtime_trending_searches_df = pytrends.realtime_trending_searches(pn='US')

        realtime_trending_searches = extract_arrays(realtime_trending_searches_df.values.flatten().tolist())
        realtime_trending_searches = [remove_non_english(item) for item in realtime_trending_searches if not isinstance(item, list)]

        trending_searches = trending_searches_df.values.flatten().tolist()
        trending_searches2 = trending_searches_df_canada.values.flatten().tolist()

        suggested_keywords = []
        futures = [executor.submit(partial(fetch_suggestions, keyword, pytrends)) for keyword in trending_searches]
        results = [future.result() for future in futures]
        suggested_keywords.extend([item for sublist in results for item in sublist])

        max_iterations = min(30, len(realtime_trending_searches))
        futures = [executor.submit(partial(fetch_suggestions, keyword, pytrends)) for keyword in realtime_trending_searches[:max_iterations]]
        results = [future.result() for future in futures]
        suggested_keywords.extend([item for sublist in results for item in sublist])

        pytrends_pool.return_connection(pytrends)

    df = pd.DataFrame(suggested_keywords)
    combined_array = realtime_trending_searches + trending_searches + trending_searches2 + df['title'].tolist()

    random_param = request.args.get('random')

    if random_param is not None:
        try:
            n = int(random_param)
            if n > 0:
                random.shuffle(combined_array)
                combined_array = combined_array[:n]
        except ValueError:
            return jsonify({"error": "Invalid 'random' parameter value. Must be a positive integer."}), 400

    return jsonify(combined_array)

if __name__ == '__main__':
    app.run(debug=True)
