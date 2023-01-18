from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)
browser.get("https://www.indeed.com/jobs?q=python&l=Remote")


def get_page_count(keyword):
    base_url = "https://indeed.com/jobs?q="
    browser.get(f"{base_url}{keyword}")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    navigation = soup.find("nav", class_="ecydgvn0")
    pages = navigation.find_all("div", recursive=False)
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    results = []
    for page in range(pages):
        base_url = "https://indeed.com/jobs?"
        final_url = browser.get(f"{base_url}q={keyword}&start={page*10}")

        soup = BeautifulSoup(browser.page_source, "html.parser")

        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                link = anchor["href"]
                title = anchor["aria-label"]
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    "link": f"http://indeed.com{link}",
                    "company": company.string,
                    "location": location.string,
                    "position": title,
                }
                results.append(job_data)

    return results
