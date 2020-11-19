# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 22:10:18 2020

@author: Pishikaka

This is a job scraper
"""
from selenium import webdriver
import time


def scrape(link,job,city,radius,pages,pagestart):
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window() #GOLD!!
    num = 1007
    for p in range(pagestart-1,pages+1):
        
        #input the job type, city, pagestart, mile range as url elementa
        url = link + '?q='+job +'&l=' + city +'&radius=' + str(radius) +'&start=' + str(p*10)
        print('searching page '+ str(p) +' ...')
        driver.get(url)  
        #remove popover box
        try:
            time.sleep(1.5)
            driver.find_element_by_css_selector('div[id="popover-foreground"]')
            print("pop-out found and eliminated")
            driver.find_element_by_css_selector('div[id="popover-x"]').click()
        except:
            print('continue')
        isbox = 0
        
        #find and click job box, then follow link in the next div,
        for i in driver.find_elements_by_css_selector('div[class="jobsearch-SerpJobCard unifiedRow row result clickcard"]'):
            
            
            try:
                isbox = driver.find_element_by_css_selector('iframe[id="vjs-container-iframe"]')
                
            except:
                isbox = 0

            
            if isbox:
                driver.switch_to_default_content
                frame = driver.find_element_by_css_selector('iframe[id="vjs-container-iframe"]')
                driver.switch_to.frame(frame) #GOLD!!
                try:
                    html =driver.find_element_by_css_selector('html[dir="ltr"]').get_attribute('innerHTML')
                
                except:
                    print('one mistake')
                    driver.switch_to.parent_frame()
                    continue
                driver.switch_to.parent_frame()
                fname = job+'/' +job+str(num)+'.html'
                num += 1
                print(num)
                
                fw=open(fname,'w',encoding='utf8')
                fw.write(html)
                fw.close()
                
                
            
            
            i.click()
            time.sleep(1)
        
        #if last page, quit the search
        try:
            driver.find_element_by_css_selector('a[aria-label="Next"]')
        except:
            print('Finished all job ads, total of ' + str(num-1) + ' '+ job + ' jobs found' )
            break
            
            
            
            
        
        #go to the link and find the text block for html file
        
    
    
    
    
    
    
    
    

    

#locate the html link for each job ad

#download the html file from the job untill the number 
#reaches 1000 or the end

if __name__ == "__main__" :
    job1 = 'Software Engineer'
    city = 'New York, NY'
    radius = 100
    link = 'https://www.indeed.com/jobs'
    pages = 200
    pagestart = 74
    scrape(link,job1,city,radius,pages,pagestart)
    '''
    job2 = 'Data Engineer'
    scrape(link,job2,city,radius,pages)
    
    job3 = 'Software Engineer'

    scrape(link,job3,city,radius,pages)
    '''
