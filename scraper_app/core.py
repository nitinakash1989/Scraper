import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re


def get_data_from_server(url):
    """
    core function to initialize the selenium drivar and set the value for form property of the site.
    Parameters:
        input: None
        out: cleaned scraped dataframe containing detail building address, suite number, suite name, area, size of suit and rent.
    """
    driver = webdriver.Firefox(executable_path=r'C:\Users\nitin\Documents\geckodriver.exe')
    
    # Grab the web page
    driver.get(url)
    
    #set the values for property type, province and Market
    dropdown = Select(driver.find_element_by_name("ddSearchPropertyType"))
    dropdown.select_by_value("Office")
    
    dropdown = Select(driver.find_element_by_name("ddSearchProvince"))
    dropdown.select_by_value("ON")
    
    dropdown = Select(driver.find_element_by_name("ddSearchMarket"))
    dropdown.select_by_value("Greater Toronto Area")
    
    
    # Now we can grab the search button and click it
    search_button = driver.find_element_by_id("butSearch")
    search_button.click()
    
    # Instead of using requests.get, we just look at .page_source of the driver
    #print(driver.page_source)
    
    # We can feed that into Beautiful Soup
    doc = BeautifulSoup(driver.page_source, "html.parser")
    
    # It's a tricky table, but this grabs the linked names inside of the A
    #rows = doc.select("#datagrid_results tr")
    rows = doc.find('table', id='tblSearchResults').find_all('tr', attrs={'class': None})
    
    records = []
    
    for row in rows:
        # print(row.attrs)
        # Find the ones that don't have 'style' as an attribute
        cells = row.find_all("td")
        
        if len(cells)==0:
            continue
        prop_spec = data_cleaning(row)
        records.append(prop_spec)
    # Close the webdriver
    driver.close()
    
    driver.quit()
    prop_df = pd.DataFrame(records)
    
    
    
    return prop_df


def data_cleaning(row):
    """
    
    This function is used to clean the html data and return a dictionary.
    Parameters:
        input 1: html table row
        out: dictionary containing detail building address, suite number, suite name, area, size of suit and rent.
        
    """
    cells = row.find_all("td")
    
    #for building address
    try:
        building_address =  cells[1].contents[1].text.strip().split(',')[0].upper()
    except:
        building_address =  cells[1].contents[1].text.strip().upper()
        

    #for suite name    
    if len(cells[1].contents) == 7:
        try:
            suite_name = cells[1].contents[3].strip().upper()
        except:
            suite_name = None
    
    #for suite number
    try:
        suite_number =  cells[1].contents[1].text.strip().split(',')[1].strip().split(' ')[1]
    except:
        suite_number =  None
    
    #for rent
    try:
        rent =  re.findall(r'-?\d+\.?\d*', cells[4].contents[0])[0].replace(',', '')
    except:
        rent =  None
    
    #for size of suite
    try:
        size_of_suite =  cells[3].contents[0].strip().split(' ')[0]
    except:
        size_of_suite=None
    
    #for area
    try:
        area= cells[2].contents[0].strip().split(',')[0].upper()
    except:
        area = None
    
    return { 
            'building_address': building_address, 
            'suite_number': suite_number,
            'suite_name':suite_name,
            'area': area,
            'size_of_suite(sq_ft)':size_of_suite,
            'rent': rent
            }

