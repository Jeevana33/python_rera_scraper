from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")

driver_path = "C:\Users\MY PC\Downloads\chromedriver-win64\chromedriver-win64"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://rera.odisha.gov.in/projects/project-list")
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.LINK_TEXT, "View Details")))


links = driver.find_elements(By.LINK_TEXT, "View Details")
project_links = [link.get_attribute("href") for link in links[:6]]

project_data = []

for link in project_links:
    driver.get(link)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "project-details")))

    def get_text(xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text.strip()
        except:
            return ""

    rera_no = get_text("//td[contains(text(), 'RERA Regd. No')]/following-sibling::td")
    project_name = get_text("//td[contains(text(), 'Project Name')]/following-sibling::td")
    try:
        driver.find_element(By.LINK_TEXT, "Promoter Details").click()
        time.sleep(2)  # Wait for tab to load
    except:
        pass

    promoter_name = get_text("//td[contains(text(), 'Company Name')]/following-sibling::td")
    promoter_address = get_text("//td[contains(text(), 'Registered Office Address')]/following-sibling::td")
    gst_no = get_text("//td[contains(text(), 'GST No')]/following-sibling::td")

    project_data.append({
        "RERA Regd. No": rera_no,
        "Project Name": project_name,
        "Promoter Name": promoter_name,
        "Promoter Address": promoter_address,
        "GST No": gst_no
    })

driver.quit()

# Save data to CSV
df = pd.DataFrame(project_data)
df.to_csv("odisha_rera_projects.csv", index=False)
print("Data saved to odisha_rera_projects.csv")



