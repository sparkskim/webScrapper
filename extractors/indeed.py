from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)
browser.get(
    "https://www.simplyhired.com/search?q=python&l=remote&job=dJ7x56EJlUrxRQxUxCd7_orlhHl8ddXnkSlMSi-x4TdDzBistjaDSg"
)


def get_page_count(keyword):
    base_url = "https://www.simplyhired.com/search?q="
    browser.get(f"{base_url}{keyword}")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    navigation = soup.find("a", class_="Pagination-link")
    pages = navigation.find_all("a", recursive=False)
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    results = []
    for page in range(pages):
        base_url = "https://www.simplyhired.com/search?"
        final_url = browser.get(f"{base_url}q={keyword}&start={page*10}")

        soup = BeautifulSoup(browser.page_source, "html.parser")

        job_list = soup.find("ul", class_="viewjob-jobTitle h2")
        jobs = job_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                # anchor = job.select_one("h2 a")
                link = job.find("class", class_="SerpJob-simplyApplyLabel")
                title = job.find("class", class_="viewjob-jobTitle h2")
                company = job.find("class", class_="viewjob-labelWithIcon")
                location = job.find("div", class_="viewjob-labelWithIcon-icon")
                job_data = {
                    "link": f"http://www.simplyhired.com{link}",
                    "company": company.string,
                    "location": location.string,
                    "position": title,
                }
                results.append(job_data)

    return results
