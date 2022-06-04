#!/usr/bin/env python

from abc import ABC, abstractmethod
from typing import List

import requests
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Provider(ABC):
    """Base class for providing language support table for a translation API"""
    
    @abstractmethod
    def fetch(self) -> List[str]:
        """Return the list of supported languages as ISO language codes."""
        pass
    
    @abstractmethod
    def url(self) -> str:
        """URL where a human-readable support list can be found."""
        pass

    def name(self) -> str:
        """Name of provider to use in table"""
        return self.__class__.__name__

    def _get_soup(self):
        r = requests.get(self.url())
        r.raise_for_status()
        html = r.text
        soup = BeautifulSoup(html, features='html.parser')
        return soup

    def _get_dynamic_soup(self, load_condition = None):
        logging.getLogger('WDM').disabled = True
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--silent')
        options.add_argument('--log-level=OFF')
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get(self.url())
        if load_condition:
            WebDriverWait(driver, 3).until(load_condition)
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        return soup
