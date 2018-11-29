import requests
import urllib.parse
import json
import pandas as pd
from math import ceil
import pdb
import time
import argparse


subscriptionKey = "83956de883a5473dad3dfaaf00252f47"

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"


class Test(object):
    def __init__(self, term, site, freshness):
        self.term = term
        self.site = site
        self.freshness = freshness

    def BingnewsSearch(self, count=10, offset=0, mkt="en-US"):
        "Performs a Bing Web search and returns the results."

        print("searching term:", self.term)
        print("searching site:", self.site)
        print("searching freshness:", self.freshness)
        headers = {"Ocp-Apim-Subscription-Key": subscriptionKey, "Pragma": "no-cache"}
        params = {
            "q": "{} (site:{})".format(self.term, self.site),
            "mkt": "en-US",
            "count": count,
            "offset": offset,
            "responseFilter": "News",
            "freshness": self.freshness,
        }
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        return response
        # pdb.set_trace()

    def bingnew(self):

        if len(subscriptionKey) == 32:

            print("Searching the news for: ")
            results_count = 50
            scraped_domains = []

            response = self.BingnewsSearch()
            result = response.json()
            totalEstimatedMatches = result["totalEstimatedMatches"]
            n = (
                200
                if totalEstimatedMatches > 10000
                else ceil(totalEstimatedMatches / results_count)
            )

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
                offset = results_count * page_number
                max_limit = totalEstimatedMatches - results_count
                if max_limit > 0 and offset > max_limit:
                    print(
                        "Offset Value is greater than totalEstimatedMatches: {}".format(
                            totalEstimatedMatches - results_count
                        )
                    )
                    break

                response = self.BingnewsSearch(count=results_count, offset=offset)
                data = response.json()
                import pdb

                pdb.set_trace()
                totalEstimatedMatches = data.get("totalEstimatedMatches", 0)
                # print("\nJSON Response:\n")
                # with open("output.json", "w") as f:
                #     f.write(json.dumps(json.loads(result), indent=4))

                final_data = []
                skipped_domains = 0
                print(
                    "PageNumber: {}, Offset: {}, ResultsCOunt: {}, totalEstimatedMatches: {}".format(
                        page_number + 1,
                        offset,
                        len(data["value"]),
                        totalEstimatedMatches,
                    )
                )
                for i in data["value"]:
                    domain = i["url"]
                    if domain in scraped_domains:
                        # print("Filtered Duplicate domain: {}".format(domain))
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
            print("Len of scraped domains: {}".format(len(scraped_domains)))
            if final_data:
                df = df.append(final_data, ignore_index=True)
            print("Scraped Results: {}".format(len(df)))
            # print(df.head())
            time.sleep(5)
            df.to_csv("output_DATA_NEWS_22.csv", index=False)
        else:

            print("Invalid Bing Search API subscription key!")
            print("Please paste yours into the source code.")


# session.close()
#         df = df.append(final_data, ignore_index=True)

#     df.to_csv("output_data_us_200_drp_3.csv", index=False)
# else:

#     print("Invalid Bing Search API subscription key!")
#     print("Please paste yours into the source code.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    required_args = parser.add_argument_group()
    required_args.add_argument("-t", "--term", dest="term", required=True)
    required_args.add_argument("-s", "--site", dest="site", default="", required=True)
    required_args.add_argument(
        "-f", "--freshness", dest="freshness", default="Month", required=True
    )
    arguments = parser.parse_args()
    tr_obj = Test(arguments.term, arguments.site, arguments.freshness)
    tr_obj.bingnew()

