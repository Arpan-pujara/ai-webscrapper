import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup

SBR_WEBDRIVER = "driver_url"

# def scrape_website(website):
#     print("Launching chrome browser...")

#     chrome_driver_path = "./chromedriver"
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

#     try:
#         driver.get(website)
#         print("Successfully scraped website!")
#         print("Page loaded...")
#         html = driver.page_source


#         return html
#     finally:
#         driver.quit()
def scrape_website(website):
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html


def extract_body_content(html_content):
    # Extract the body content of the HTML
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.find("body")
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    # Clean the body content of the HTML
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.split("\n") if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    # Split the DOM tree of the HTML
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]