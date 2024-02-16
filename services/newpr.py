import requests
import logging


class NewPrService:
    """Submit new PR to Google Form"""

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    CATEGORIES = ["-66", "-73", "-80", "-87", "-94", "-104", ">104"]

    def __init__(self, url: str) -> None:
        self.url = url

    @staticmethod
    def __build_form_data(
        user_id: str,
        category: str,
        mu: str = None,
        pull: str = None,
        dips: str = None,
        squat: str = None,
    ) -> str:
        entries = {
            "entry.742237483": f"{user_id}",
            "entry.1509725706": f"{category}",
            "entry.2038241630": mu,
            "entry.1321964420": pull,
            "entry.620889826": dips,
            "entry.1205398535": squat,
        }
        return entries

    def submit_new_pr(
        self,
        user_id: str,
        category: str,
        mu: float = None,
        pull: float = None,
        dips: float = None,
        squat: float = None,
    ) -> requests.Response:
        data = NewPrService.__build_form_data(user_id, category, mu, pull, dips, squat)
        logging.debug(data)
        r = requests.post(self.url, headers=self.headers, data=data)
        logging.info(r.status_code)
        return r
