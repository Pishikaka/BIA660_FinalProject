import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getJobs(title: str, location: str):

    # open url in chrome and wait 2 second to load
    url = 'https://www.indeed.com'
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'text-input-what'))
    )

    try:
        jobfield = driver.find_element_by_id('text-input-what')
    except:
        print('job title input field not found')
    
    try:
        locationfield = driver.find_element_by_id('text-input-where')
    except:
        print('job location input field not found')

    jobfield.clear()
    jobfield.send_keys(title)

    # clear the location field
    for i in range(20):
        locationfield.send_keys(Keys.BACK_SPACE)

    locationfield.send_keys(location)

    jobfield.submit()

    go = True
    currentPage = 0
    res = set()
    while go:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'resultsBodyContent'))
        )
        currentPage+=1
        print(f'page = {currentPage}')
        try:
            jobs = driver.find_elements_by_css_selector("div.jobsearch-SerpJobCard.unifiedRow.row.result.clickcard")
        except:
            print("job card element not found")
        else:
            print(f'{len(jobs)} jobs found')

        
        jname, jdescription = None, None

        for j in jobs:
            try:
                jname = j.find_element_by_css_selector('a[data-tn-element="jobTitle"]').text
            except:
                print("job name element not found")

            j.find_element_by_css_selector('h2.title').click()
            
            WebDriverWait(driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, 'vjs-container-iframe'))
            )
            
            try:
                jdescription = driver.find_element_by_id('jobDescriptionText').text
            except:
                print('job description not found')
            else:
                jdescription.replace('\n', ' ')
                jdescription.replace('\r', ' ')

            if jname and jdescription:
                res.add((jname, jdescription))

            driver.switch_to.default_content()
        
        try:
            driver.find_element_by_css_selector(f'a[aria-label="{currentPage+1}"]')
        except:
            go = False
        else:
            driver.find_element_by_css_selector(f'a[aria-label="{currentPage+1}"]').click()

    if res:      
        with open('indeed.txt', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, lineterminator='\n')
            for i in res:
                writer.writerow(i)
                
    
    print(f'total {len(res)} job record written successfully')
    driver.close()

if __name__ == "__main__":
    getJobs('data scientist', 'houston')