import http.client, urllib.parse, json
import pandas as pd
from math import ceil
import pdb

subscriptionKey = "2a58ab684d28436e880b0f5a4fa749d5"

host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/news/search"

term = "data"


def BingnewsSearch(search, count=10, offset=0, mkt="en-US"):
    "Performs a Bing Web search and returns the results."

    headers = {"Ocp-Apim-Subscription-Key": subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request(
        "GET",
        path
        + "?q="
        + query
        + "&count="
        + str(count)
        + "&offset="
        + str(offset)
        + "&mkt="
        + str(mkt),
        headers=headers,
    )
    response = conn.getresponse()
    headers = [
        k + ": " + v
        for (k, v) in response.getheaders()
        if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")
    ]
    return headers, response.read().decode("utf8")


if len(subscriptionKey) == 32:

    print("Searching the news for: ", term)

    headers, result = BingnewsSearch(term)
    result = json.loads(result)
    # pdb.set_trace()
    totalEstimatedMatches = result["totalEstimatedMatches"]
    n = 200 if totalEstimatedMatches > 10000 else ceil(totalEstimatedMatches / 50)

    df = pd.DataFrame(
        columns=[
            "Name",
            "Description",
            "URL",
            "Image",
            "Provider",
            "Date Published",
            "Category",
        ]
    )
    for page_number in range(n):
        headers, result = BingnewsSearch(term, 50, (50 * page_number))
        # print("\nRelevant HTTP Headers:\n")
        # print("\n".join(headers))
        # print("\nJSON Response:\n")
        # with open("output.json", "w") as f:
        #     f.write(json.dumps(json.loads(result), indent=4))

        data = json.loads(result)
        final_data = [
            {
                "Name": i["name"],
                "Description": i.get("description"),
                "URL": i.get("url"),
                "Image": i.get("image"),
                "Provider": i.get("provider"),
                "Date Published": i.get("datePublished"),
                "Category": i.get("category"),
                "contentUrl": i.get("contentUrl"),
            }
            for i in data["value"]
        ]

        df = df.append(final_data, ignore_index=True)
        # print(df.head())
    df.to_csv("output_data_us.csv", index=False)
else:

    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")
