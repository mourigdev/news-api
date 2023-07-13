import requests

api_key = '4d17e96415874d12abf24c932f459fed'
url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

response = requests.get(url)
data = response.json()
titles = [article["title"] for article in data["articles"]]

# Process the retrieved data
print(titles)


# ===============API=================
# from flask import Flask, jsonify
# import requests

# app = Flask(__name__)


# @app.route('/api/articles/titles', methods=['GET'])
# def get_article_titles():
#     api_key = '4d17e96415874d12abf24c932f459fed'
#     url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

#     response = requests.get(url)
#     data = response.json()
#     titles = [article["title"] for article in data["articles"]]

#     return jsonify(titles)


# if __name__ == '__main__':
#     app.run()
# ================================================


# from pytrends.request import TrendReq
# import pandas as pd
# import numpy as np

# # Set up pytrends
# pytrends = TrendReq(hl='en-US', tz=360)

# # Get daily search trends for the United States
# trending_searches_df = pytrends.trending_searches(pn='united_states')

# # Process the retrieved data
# trending_searches = trending_searches_df.values.flatten().tolist()

# print(trending_searches)

# # Get top charts for a specific year
# top_charts_df = pytrends.top_charts(2022, hl='en-US', tz=300, geo='US')

# # Process the retrieved data
# top_charts = top_charts_df["title"].tolist()

# print(top_charts)

# # Fetch suggestions for trending searches
# suggested_keywords = []
# for keyword in trending_searches:
#     suggestions = pytrends.suggestions(keyword=keyword)
#     suggested_keywords.extend(suggestions)

# # Create a DataFrame from the suggested keywords
# df = pd.DataFrame(suggested_keywords)

# # Get the keywords as an array
# keyword_array = df['title'].values

# print(np.array2string(keyword_array, separator=', '))


# # Combine all the search trends and suggested keywords into a single array
# combined_array = trending_searches + top_charts + df['title'].tolist()
# print(combined_array)
