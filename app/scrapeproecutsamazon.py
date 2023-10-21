import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
pd.options.mode.chained_assignment = None
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Function to delay some process
def delay():
    time.sleep(random.randint(3, 10))