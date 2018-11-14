import http.client, urllib.parse, json
import pandas as pd

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "9f5502ecfbf14208b2420ef72d368ea6"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"

term = "box manufacturer Bobst"


def BingWebSearch(search, count=10, offset=0):
    "Performs a Bing Web search and returns the results."

    headers = {"Ocp-Apim-Subscription-Key": subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request(
        "GET",
        path + "?q=" + query + "&count=" + str(count) + "&offset=" + str(offset),
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

    print("Searching the Web for: ", term)

    headers, result = BingWebSearch(term)
    result = json.loads(result)
    totalEstimatedMatches = result["webPages"]["totalEstimatedMatches"]
    n = 200 if totalEstimatedMatches > 10000 else totalEstimatedMatches / 50

    df = pd.DataFrame(columns=["Url", "Description"])

    for page_number in range(n):
        headers, result = BingWebSearch(term, 50, (50 * page_number))
        # print("\nRelevant HTTP Headers:\n")
        # print("\n".join(headers))
        # print("\nJSON Response:\n")
        # with open("output.json", "w") as f:
        #     f.write(json.dumps(json.loads(result), indent=4))

        data = json.loads(result)
        final_data = [
            {"Url": i["url"], "Description": i.get("snippet", i.get("description"))}
            for i in data["webPages"]["value"]
        ]

        df = df.append(final_data, ignore_index=True)
        # print(df.head())
    df.to_csv("output.csv", index=False)
else:

    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")

