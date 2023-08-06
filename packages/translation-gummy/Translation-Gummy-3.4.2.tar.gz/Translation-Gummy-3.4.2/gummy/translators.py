# coding: utf-8
import re
import time
import json
import urllib
import warnings
from abc import ABCMeta, abstractmethod, abstractproperty, abstractstaticmethod
from bs4 import BeautifulSoup

from .utils.coloring_utils import toBLUE, toGREEN
from .utils.driver_utils import get_driver
from .utils.generic_utils import (handleKeyError, handleTypeError,
                                  mk_class_get, splitted_query_generator)
from .utils.monitor_utils import ProgressMonitor
from .utils.soup_utils import find_text

class GummyAbstTranslator(metaclass=ABCMeta):
    def __init__(self, driver=None, maxsize=5000, interval=1, trials=30, verbose=False):
        """ Translator
        @params en2ja_url_fmt : (str) Format of the query. English will be assigned to {english}.
        @params find_ja_func  : (function) Takes only one argument (bs4.BeautifulSoup)
                                           and find translated Japanese text.
        @params driver        : (WebDriver)
        @params maxsize       : (int) Number of English characters that we can send a request at one time.
        @params interval      : (int) Trial interval.
        @params trials        : (int) How many times to try.
        @params verbose       : (bool)
        """
        self.name  = self.__class__.__name__
        self.name_ = re.sub(r"([a-z])([A-Z])", r"\1_\2", self.name).lower()
        self.driver = driver
        self.maxsize = maxsize
        self.interval = interval
        self.trials = trials
        self.verbose = verbose
        self.cache_ja = ""

    @abstractproperty
    def en2ja_url_fmt(self):
        return "https://domain/english2japanese/?query={english}"

    @abstractstaticmethod
    def find_ja(soup):
        return find_text(soup=soup, name="japanese")

    def is_ja_enough(self, ja):
        return (len(ja)>0) and (not self.cache_ja.startswith(ja))

    @property
    def driver_info(self):
        info = {}
        driver = self.driver
        if driver is not None:
            info["session_id"] = driver.session_id
            info["browserName"] = driver.capabilities.get("browserName")
        return info

    def check_en2ja(self):
        # en2ja format.
        if not isinstance(self.en2ja_url_fmt, str):
            raise TypeError(f"`self.en2ja_url_fmt` must be str not {type(self.en2ja_url_fmt)}")
        if self.en2ja_url_fmt.find("{english}") == -1:
            raise ValueError("Please include {english} in `self.en2ja_url_fmt`")

    def check_driver(self, driver=None):
        driver = driver or self.driver
        if driver is None:
            driver = get_driver()
        self.driver = driver
        if self.verbose: print(f"Driver info:\n{json.dumps(self.driver_info, indent=2)}")
        return driver

    def en2ja(self, query, driver=None, barname=None):
        self.check_en2ja()
        driver = self.check_driver(driver=driver)
        maxsize = self.maxsize
        interval = self.interval
        trials = self.trials
        verbose = self.verbose
        barname = barname if barname is not None else self.name
        
        japanese = []
        gen = splitted_query_generator(query=query, maxsize=maxsize)
        for i,q in enumerate(gen):
            url = self.en2ja_url_fmt.format(english=urllib.parse.quote(q))
            driver.refresh()
            driver.get(url)
            monitor = ProgressMonitor(max_iter=trials, verbose=verbose, barname=f"{barname} (query{i+1})")
            for i in range(trials):
                time.sleep(interval)
                html = driver.page_source.encode("utf-8")
                soup = BeautifulSoup(html, "lxml")
                ja = self.find_ja(soup)
                monitor.report(i, japanese=ja)
                if self.is_ja_enough(ja):
                    break
            monitor.remove()
            japanese.append(ja)
            self.cache_ja = ja
            time.sleep(1)
        
        japanese = "".join(japanese)
        return japanese

class DeepLTranslator(GummyAbstTranslator):
    def __init__(self, driver=None, maxsize=5000, interval=1, trials=30, verbose=False):
        super().__init__(driver=driver, maxsize=maxsize, interval=interval, trials=trials, verbose=verbose)

    @property
    def en2ja_url_fmt(self):
        return "https://www.deepl.com/en/translator#en/ja/{english}"

    @staticmethod
    def find_ja(soup):
        return find_text(soup=soup, name="button", class_="lmt__translations_as_text__text_btn")

    def is_ja_enough(self, ja):
        return super().is_ja_enough(ja) and (not ja.endswith("[...]"))

class GoogleTranslator(GummyAbstTranslator):
    def __init__(self, driver=None, maxsize=5000, interval=1, trials=30, verbose=False):
        super().__init__(driver=driver, maxsize=maxsize, interval=interval, trials=trials, verbose=verbose)

    @property
    def en2ja_url_fmt(self):
        return "https://translate.google.co.jp/#en/ja/{english}"

    @staticmethod
    def find_ja(soup):
        return find_text(soup=soup, name="span", class_="tlid-translation translation", attrs={"lang": "ja"})

all = TranslationGummyTranslators = {
    "google" : GoogleTranslator,
    "deepl"  : DeepLTranslator,
}

get = mk_class_get(
    all_classes=TranslationGummyTranslators,
    gummy_abst_class=[GummyAbstTranslator],
    genre="translators"
)