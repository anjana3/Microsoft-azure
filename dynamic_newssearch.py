""" Dynamic application to search the given "search term",site (Domain) and Freshness "Day, Month,Year"  """

import argparse
import json
import time
import sys
import urllib.parse

import pandas as pd
import requests

from math import ceil

""" Get subscriptionKey and search_url from Microsoft Azure Account by creating new service of bing """

subscriptionKey = "83956de883a5473dad3dfaaf00252f47"
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"

session = requests.Session()


class NewsSearch(object):
    def __init__(self, term: str, site: str, freshness: str):
        """ To call the Bing API to get the search results
            Args:
                term(str): search term
                site(str): particular domain
                freshness(str): Results for Day,month,year
            Returns:
        """
        self.term = term
        self.site = site
        self.freshness = freshness

    def bing_news_search(
        self,
        count: int = 10,
        offset: int = 0,
        mkt: str = "en-US",
        clientid: str = None,
        traceid: str = None,
    ):
        """ To call count,offset,clientid,traceid
            Args:
                count(int):Result per page.
                offset(int):Page next result to skip the count of page results.
                clientid(str) : Behaviour while making API calls
                traceid(str) : Trace id captures the error occurs
            Returns:
                response(HTTP Response): Search results for the search term
        """

        print("searching term:", self.term)
        print("searching site:", self.site)
        print("searching freshness:", self.freshness)

        headers = {
            "Ocp-Apim-Subscription-Key": subscriptionKey,
            "Host": "api.cognitive.microsoft.com",
            "BingAPIs-Market": "en-US",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
        }

        if clientid:
            headers["X-MSEdge-ClientID"] = clientid

        if traceid:
            headers["BingAPIs-TraceId"] = traceid

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

    def bingnew(self, clientid=None, traceid=None):
        """ Function set the count and offset parameters to set
            the page next results and load into csv file.

            Args:
                clientid(str) : Behaviour while making API calls.
                traceid(str) : Trace id captures the error occurs.

            Returns:
                df(DataFrame): Pandas DataFrame with sheet data.
             """
        if len(subscriptionKey) == 32:
            results_count = 50
            scraped_domains = []

            response = self.bing_news_search()
            result = response.json()
            if not "totalEstimatedMatches" in result or not result.get("value", []):
                print("No results found in the response")
                sys.exit()
            totalEstimatedMatches = result["totalEstimatedMatches"]

            # To set the page numbers to append the page next results.
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
                    # To check the results from the total estimated matches from the offset.
                    print(
                        "Offset Value is greater than totalEstimatedMatches: {}".format(
                            totalEstimatedMatches - results_count
                        )
                    )
                    break

                response = self.bing_news_search(
                    count=results_count,
                    offset=offset,
                    clientid=clientid,
                    traceid=traceid,
                )

                if not clientid:
                    clientid = response.headers["X-MSEdge-ClientID"]
                if not traceid:
                    traceid = response.headers.get("BingAPIs-TraceId")
                final_data = []
                skipped_domains = 0
                data = response.json()
                totalEstimatedMatches = data.get("totalEstimatedMatches", 0)
                print(
                    "PageNumber: {}, Offset: {}, ResultsCOunt: {}, EstimatedMatches: {}".format(
                        page_number + 1,
                        offset,
                        len(data["value"]),
                        totalEstimatedMatches,
                    )
                )

                for i in data["value"]:
                    domain = i["url"]
                    if domain in scraped_domains:
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
                print(
                    "Total skipped domains in this offset: {}".format(skipped_domains)
                )

                if final_data:
                    df = df.append(final_data, ignore_index=True)
                print("Scraped Results: {}".format(len(df)))

                time.sleep(5)

            df.to_csv("final_result_newsearch_day.csv", index=False)
        else:
            print("Invalid Bing Search API subscription key!")
            print("Please paste yours into the source code.")
        session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    required_args = parser.add_argument_group()
    required_args.add_argument(
        "-t", "--term", dest="term", required=True, help="search term"
    )
    required_args.add_argument(
        "-s",
        "--site",
        dest="site",
        default="",
        required=True,
        help="Domain eg: www.CNN.com",
    )
    required_args.add_argument(
        "-f",
        "--freshness",
        dest="freshness",
        default="Month",
        required=True,
        help="eg:Day,month,year",
    )
    arguments = parser.parse_args()
    tr_obj = NewsSearch(arguments.term, arguments.site, arguments.freshness)
    tr_obj.bingnew()

