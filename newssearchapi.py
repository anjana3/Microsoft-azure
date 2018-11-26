import requests
from IPython.display import HTML
import csv, json, sys

import pdb


subscription_key = "2a58ab684d28436e880b0f5a4fa749d5"
assert subscription_key
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
search_term = "Foot ball"

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()
print("\nRelevant HTTP Headfders:\n")
print("\n".join(headers))
print("\nJSON Response:\n")
with open("output_news.csv", "w") as f:
    f.write(json.dumps(search_results, indent=4))


# descriptions = [article["description"] for article in search_results["value"]]


# rows = "\n".join(["<tr><td>{0}</td></tr>".format(desc) for desc in descriptions])
# HTML("<table>" + rows + "</table>")

