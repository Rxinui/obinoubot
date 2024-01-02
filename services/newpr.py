import requests
import json
import logging

with open("bot.json") as properties_fp:
    URL_FORM = json.load(properties_fp)["properties"]["GOOGLE_FORM_PR_POST"]


class NewPrService:
    """Submit new PR to Google Form"""

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

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

    @staticmethod
    def submit_new_mu(mu: float):
        data = NewPrService.__build_form_data("48405377","-80",mu=mu)
        logging.debug(data)
        r = requests.post(URL_FORM, headers=NewPrService.headers, data=data)
        logging.info(r.status_code)
        return r
