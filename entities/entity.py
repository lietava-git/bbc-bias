from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup as bs
from ratelimit import limits, sleep_and_retry

ONE_MINUTE = 60


@sleep_and_retry
@limits(calls=5, period=ONE_MINUTE)
def call_api(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response


class Entity(ABC):
    def __init__(self, url: str):
        response = call_api(url)
        self.soup = bs(response.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()

    @abstractmethod
    def get_body(self) -> list:
        return

    @abstractmethod
    def get_title(self) -> str:
        return
