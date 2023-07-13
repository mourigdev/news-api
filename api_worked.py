from flask import Flask, jsonify
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_search_trends():
    # Set up pytrends
    pytrends = TrendReq(hl='en-US', tz=360)

    # Get daily search trends for the United States
    trending_searches_df = pytrends.trending_searches(pn='united_states')
    trending_searches_df_canada = pytrends.trending_searches(pn='canada')

    # Process the retrieved data
    trending_searches = trending_searches_df.values.flatten().tolist()
    trending_searches2 = trending_searches_df_canada.values.flatten().tolist()

    # Get top charts for a specific year
    top_charts_df = pytrends.top_charts(2022, hl='en-US', tz=300, geo='US')

    # Process the retrieved data
    top_charts = top_charts_df["title"].tolist()

    # Fetch suggestions for trending searches
    suggested_keywords = []
    for keyword in trending_searches:
        suggestions = pytrends.suggestions(keyword=keyword)
        suggested_keywords.extend(suggestions)

    for keyword in trending_searches2:
        suggestions = pytrends.suggestions(keyword=keyword)
        suggested_keywords.extend(suggestions)

    # Create a DataFrame from the suggested keywords
    df = pd.DataFrame(suggested_keywords)

    # Combine all the search trends and suggested keywords into a single array
    combined_array = trending_searches + trending_searches2 +  top_charts + df['title'].tolist()

    return jsonify(combined_array)

if __name__ == '__main__':
    app.run(debug=True)
