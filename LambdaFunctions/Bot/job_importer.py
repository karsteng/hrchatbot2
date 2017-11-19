import requests
from enum import Enum
from bs4 import BeautifulSoup


base_url = "https://recruitingapp-2388.umantis.com/Jobs/All"


headers = {
    "accept": "text/html"
}


class Position(Enum):
    none = None
    professional = "1000148"
    young_talent = "1000150"


def get_html_jobs(search_job_title=None,
                  full_search_text=None,
                  position=Position.none,
                  url=base_url,
                  headers=headers):
    """Sends a post request to the umantis job search engine."""

    data = {
        "Search": "Suchen",
        "token": 0,
        "MultiActionUID": "",
        "searchFullPositionsConfExtPubAll":
            full_search_text if full_search_text else "",
        "searchJobTitleExtPub": search_job_title if search_job_title else "",
        "searchPosition": position.value if position and position != Position.none else "",
        "searchSkill1005": ""
    }

    r = requests.post(url, data, headers=headers)
    return r.text


def parse_jobs(html_job_response):
    """Parses the html response from the search request for jobs."""

    soup = BeautifulSoup(html_job_response, "html.parser")

    job_table = soup.find("table", class_="tableaslist")
    if not job_table:
        return

    jobs = job_table.find_all("div", class_="tableaslist_cell")
    for job in jobs:
        for span_element in job.find_all("span"):
            for class_ in span_element["class"]:
                if "tableaslist_element_1152488" in class_:
                    title_ = span_element.a

                    job_id = title_["id"]
                    job_title = title_.text
                    job_link = title_["href"]
                elif "tableaslist_element_1152487" in class_:
                    online_since = span_element.text
                elif "tableaslist_element_1152491" in class_:
                    contract_type = span_element.text
                elif "tableaslist_element_1152492" in class_:
                    contract_duration = span_element.text
                elif "tableaslist_element_1152496" in class_:
                    job_location = span_element.text
                elif "tableaslist_element_1152497" in class_:
                    job_area = span_element.text

        yield {
            "job_id": job_id,
            "job_title": job_title,
            "job_link": job_link,
            "job_location": job_location,
            "job_area": job_area,
            "online_since": online_since,
            "contract_type": contract_type,
            "contract_duration": contract_duration
        }
