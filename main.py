from sec_api import RenderApi
from utils import download_filings, get_filings_url

sec_api_key=""

get_filings_url(sec_api_key)
download_filings(sec_api_key, "./filing_urls.txt")
