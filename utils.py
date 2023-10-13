from sec_api import QueryApi
from sec_api import RenderApi

def get_filings_url(api_key_, start_year=2022, end_year=2020):
    queryApi = QueryApi(api_key=api_key_)
    base_query = {
        "query": {
            "query_string": {
                "query": "PLACEHOLDER",  # this will be set during runtime
                "time_zone": "America/New_York"
            }
        },
        "from": "0",
        "size": "200",  # don't change this
        # sort returned filings by the filedAt key/value
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    # open the file we use to store the filing URLs
    log_file = open("filing_urls.txt", "a")

    for year in range(start_year, end_year - 1, -1):
        print("Starting download for year {year}".format(year=year))

        for month in range(1, 13, 1):
            universe_query = "formType:(\"10-K\", \"10-KT\", \"10KSB\", \"10KT405\", \"10KSB40\", \"10-K405\") AND " + \
                "filedAt:[{year}-{month:02d}-01 TO {year}-{month:02d}-31]".format(year=year, month=month)

            base_query["query"]["query_string"]["query"] = universe_query;

            for from_batch in range(0, 400, 200):
                base_query["from"] = from_batch

                response = queryApi.get_filings(base_query)

                if len(response["filings"]) == 0:
                    break

                urls_list = list(map(lambda x: x["linkToFilingDetails"], response["filings"]))
                urls_string = "\n".join(urls_list) + "\n"
                log_file.write(urls_string)

            print("Filing URLs downloaded for {year}-{month:02d}".format(year=year, month=month))

    log_file.close()
    print("All URLs downloaded")

def download_filings(api_key:str, file_path: str, destiny: str = "./filings/"):
    with open(file_path, "r") as filings:
        renderApi = RenderApi(api_key)
        for line in filings:
            download_filing(renderApi, line[:-1], destiny)
            print("downloaded:", line)

def download_filing(renderApi, url:str, destiny:str = "./filings/"):
  try:
    filing = renderApi.get_filing(url)
    file_name = url.split("/")[-2] + "-" + url.split("/")[-1] 
    download_to = destiny + file_name
    with open(download_to, "w") as f:
      f.write(filing)
  except Exception as e:
    print("Problem with {url}".format(url=url))
    print(e)




