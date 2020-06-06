from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic

from geopy.geocoders import Nominatim

from bs4 import BeautifulSoup



address = ""
keyword = ""


# b = 180

class Browser:

    def __init__ (self):

        self.driver = webdriver.Chrome(executable_path = "/Users/augustinechang/Desktop/chromedriver")
        self.domain = "https://www.google.com/maps"
        self.d = 10/12*1609.34

    def get_geopoints(self, address, query):
        
        # Get lat and long for input address
        geolocator = Nominatim(user_agent="a")
        location = geolocator.geocode(address)
        lat1 = location.latitude
        lon1 = location.longitude

        # Generate 13 x 13 endpoints, 169 total
        geod = Geodesic(Constants.WGS84_a, Constants.WGS84_f)
        lst = [(lat1, lon1)]
        for b in [0, 90, 180, 170]:

            for x in range(0, 6):

                d = geod.Direct(lat1, lon1, b, self.d)
                lst.append((d['lat2'], d['lon2']))
                lat1, lon1 = d['lat2'], d['lon2']
                lat2, lon2 = d['lat2'], d['lon2']

                for y in range(0, 6):

                    d = geod.Direct(lat2, lon2, b+90, self.d)
                    lst.append((d['lat2'], d['lon2']))
                    lat2 = d['lat2']
                    lon2 = d['lon2']

        print(lst)

        # Input lat and long points
        self.driver.get(self.domain)

        for latlon in lst:

            WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH, "(//input[@class='tactile-searchbox-input'])[1]"))).send_keys(str(latlon))
            time.sleep(1)

            self.driver.find_element_by_xpath("//div[@class='searchbox-searchbutton-container']/button").click()
            time.sleep(3)

            WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH, "(//input[@class='tactile-searchbox-input'])[1]"))).clear()
            time.sleep(1)

            # input query, click, zoom in 3x

            WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH, "(//input[@class='tactile-searchbox-input'])[1]"))).send_keys(query)
            time.sleep(1)

            self.driver.find_element_by_xpath("//div[@class='searchbox-searchbutton-container']/button").click()
            time.sleep(3)

            # self.driver.find_element_by_xpath("//div[@jsaction='blur:zoom.onZoomInOrTooltipBlur']/button").click()
            # time.sleep(1)
            # self.driver.find_element_by_xpath("//div[@jsaction='blur:zoom.onZoomInOrTooltipBlur']/button").click()
            # time.sleep(1)
            # self.driver.find_element_by_xpath("//div[@jsaction='blur:zoom.onZoomInOrTooltipBlur']/button").click()
            # time.sleep(1)

            # # Search this area
            # self.driver.find_element_by_xpath("//div[@class='widget-search-this-area widget-search-this-area-visible']/button").click()
            # time.sleep(3)

            # WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH, "(//input[@class='tactile-searchbox-input'])[1]"))).clear()
            # time.sleep(1)


            a = self.driver.find_element_by_xpath("//div[@class='section-layout section-scrollbox scrollable-y scrollable-show section-layout-flex-vertical']/div")
            vendors = a.find_elements_by_xpath("//h3[@class='section-result-title']")
            for x, y in enumerate(vendors):
                print(x)
                print(y.text)
            time.sleep(10)
            


a = Browser()
a.get_geopoints("5-25 46th Ave, Long Island City, NY 11101", "iPhone")

