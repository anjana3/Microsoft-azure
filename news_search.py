import http.client, urllib.parse, json
import pandas as pd
from math import ceil
import pdb

subscriptionKey = "83956de883a5473dad3dfaaf00252f47"

host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/news/search"

term = "foot ball"


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
    scraped_domains = []

    headers, result = BingnewsSearch(term)
    result = json.loads(result)
    import pdb

    # pdb.set_trace()
    # pdb.set_trace()
    totalEstimatedMatches = result["totalEstimatedMatches"]
    # n = 200 if totalEstimatedMatches > 10000 else ceil(totalEstimatedMatches / 50)

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
    n = 20
    for page_number in range(n):
        headers, result = BingnewsSearch(term, 50, (50 * page_number))
        # print("\nRelevant HTTP Headers:\n")
        # print("\n".join(headers))
        # print("\nJSON Response:\n")
        # with open("output.json", "w") as f:
        #     f.write(json.dumps(json.loads(result), indent=4))

        data = json.loads(result)
        final_data = []
        skipped_domains = 0
        print(
            "Count: {}, Offset: {}, ResultsCOunt: {}".format(
                50, 50 * page_number, len(data["value"])
            )
        )
        for i in data["value"]:
            domain = i["url"]
            if domain in scraped_domains:
                print("Filtered Duplicate domain: {}".format(domain))
                skipped_domains += 1
                continue

            scraped_domains.append(domain)
            final_data.append(
                {
                    "Name": i["name"],
                    "Description": i.get("description"),
                    "URL": i.get("url"),
                    "Image": i.get("image"),
                    "Provider": i.get("provider"),
                    "Date Published": i.get("datePublished"),
                    "Category": i.get("category"),
                }
            )

        print("Total skipped domains in this offset: {}".format(skipped_domains))
        if final_data:
            df = df.append(final_data, ignore_index=True)
        print("Scraped Results: {}".format(len(df)))
        # print(df.head())
    df.to_csv("output_data_500_2_football.csv", index=False)
else:

    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")


#         df = df.append(final_data, ignore_index=True)

#     df.to_csv("output_data_us_200_drp_3.csv", index=False)
# else:

#     print("Invalid Bing Search API subscription key!")
#     print("Please paste yours into the source code.")
