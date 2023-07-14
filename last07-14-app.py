from flask import Flask, jsonify
from pytrends.request import TrendReq
import pandas as pd
import re

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

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_search_trends():
    # Set up pytrends
    pytrends = TrendReq(hl='en-US', tz=360)

    # Get daily search trends for the United States
    trending_searches_df = pytrends.trending_searches(pn='united_states')
    trending_searches_df_canada = pytrends.trending_searches(pn='canada')
    
    # Get real-time search trends
    realtime_trending_searches_df = pytrends.realtime_trending_searches(pn='US')
    realtime_trending_searches = realtime_trending_searches_df.values.flatten().tolist()
    realtime_trending_searches = extract_arrays(realtime_trending_searches)
    realtime_trending_searches = [remove_non_english(item) for item in realtime_trending_searches if not isinstance(item, list)]


    # Process the retrieved data
    trending_searches = trending_searches_df.values.flatten().tolist()
    trending_searches2 = trending_searches_df_canada.values.flatten().tolist()

    # # Get top charts for a specific year
    # top_charts_df = pytrends.top_charts(2022, hl='en-US', tz=300, geo='US')
    # top_charts = top_charts_df["title"].tolist()

    # Fetch suggestions for trending searches
    suggested_keywords = []
    for keyword in trending_searches:
        suggestions = pytrends.suggestions(keyword=keyword)
        suggested_keywords.extend(suggestions)

    # Create a DataFrame from the suggested keywords
    df = pd.DataFrame(suggested_keywords)

    # Combine all the search trends and suggested keywords into a single array
    combined_array = realtime_trending_searches + realtime_trending_searches + trending_searches + trending_searches2 + df['title'].tolist()

    return jsonify(combined_array)

if __name__ == '__main__':
    app.run(debug=True)
