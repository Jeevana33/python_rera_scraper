import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def get_project_details(driver, url):
    """Extracts project and promoter details from a project's detail page."""
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
      
        rera_no = soup.find("span", id="ctl00_ContentPlaceHolder1_lblReraNo").text.strip()
        project_name = soup.find("span", id="ctl00_ContentPlaceHolder1_lblProjectName").text.strip()

        # Navigate to Promoter Details tab
        promoter_tab = driver.find_element(By.LINK_TEXT, "Promoter Details")
        promoter_tab.click()
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

    
        promoter_name = soup.find("span", id="ctl00_ContentPlaceHolder1_lblPromoterName").text.strip()
        promoter_address = soup.find("span", id="ctl00_ContentPlaceHolder1_lblRegisteredOfficeAdd").text.strip()
        gst_no = soup.find("span", id="ctl00_ContentPlaceHolder1_lblGSTIN").text.strip()

        return {
            "RERA Regd. No": rera_no,
            "Project Name": project_name,
            "Promoter Name": promoter_name,
            "Promoter Address": promoter_address,
            "GST No": gst_no
        }

    except Exception as e:
        print(f"Error scraping {url}:\n{e}")
        return None

def main():
    """Main function to launch the browser, navigate the site, and scrape data."""
    print("Launching Chrome WebDriver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    print("Opening RERA Odisha project list page...")
    driver.get("https://rera.odisha.gov.in/projects/project-list")
    time.sleep(3)

    print("Switching to 'Projects Registered' tab...")
    try:
        tab = driver.find_element(By.XPATH, "//a[text()='Projects Registered']")
        tab.click()
        time.sleep(3)
    except Exception as e:
        print("Could not switch to Projects Registered tab:", e)
        driver.quit()
        return

    print("Collecting project detail links...")
    view_links = driver.find_elements(By.LINK_TEXT, "View Details")[:6]
    project_urls = [link.get_attribute("href") for link in view_links]

    results = []

    print("\nScraping project details...\n")
    for i, url in enumerate(project_urls, start=1):
        print(f"Scraping Project {i}...")
        data = get_project_details(driver, url)
        if data:
            results.append(data)
        else:
            print(f"Failed to retrieve details for Project {i}.\n")
        print("-" * 40)

    driver.quit()

    print("\n--- Scraped Project Details ---\n")
    for i, project in enumerate(results, 1):
        print(f"Project {i}")
        for key, value in project.items():
            print(f"{key}: {value}")
        print("-" * 40)

if __name__ == "__main__":
    main()
