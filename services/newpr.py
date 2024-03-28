from typing import Self
import requests
import logging

from utils.botconfig import BotConfig


class NewPrService:
    """Submit new PR to Google Form"""

    HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

    MALE_CATEGORIES = ["-66", "-73", "-80", "-87", "-94", "-104", ">104"]
    FEMALE_CATEGORIES = ["-52", "-57", "-63", "-70", ">70"]

    def __init__(
        self,
        url: str,
        entry_username: str,
        entry_category: str,
        entry_mu: str,
        entry_pull: str,
        entry_dips: str,
        entry_squat: str,
    ) -> None:
        self.__url = url
        self.__entry_username = entry_username
        self.__entry_category = entry_category
        self.__entry_mu = entry_mu
        self.__entry_pull = entry_pull
        self.__entry_dips = entry_dips
        self.__entry_squat = entry_squat
        self.__data = {}

    def new_pr(
        self,
        username: str,
        category: str,
        mu: float = None,
        pull: float = None,
        dips: float = None,
        squat: float = None,
    ) -> Self:
        self.__data = {
            self.__entry_username: username,
            self.__entry_category: category,
            self.__entry_mu: mu,
            self.__entry_pull: pull,
            self.__entry_dips: dips,
            self.__entry_squat: squat,
        }
        return self

    def submit(
        self,
    ) -> requests.Response:
        logging.info("Data to be submitted: " + self.__url)
        logging.info(self.__data)
        response = requests.post(self.__url, headers=self.HEADERS, data=self.__data)
        logging.info(response.status_code)
        return response

    @classmethod
    def categories(cls) -> list[str]:
        return cls.MALE_CATEGORIES + cls.FEMALE_CATEGORIES

    @classmethod
    def guess_gender_from_category(cls, category: str) -> str | None:
        if category in cls.MALE_CATEGORIES:
            return "MALE"
        if category in cls.FEMALE_CATEGORIES:
            return "FEMALE"
        return None
