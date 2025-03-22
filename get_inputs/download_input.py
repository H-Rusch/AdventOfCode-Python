import requests
import os
from dotenv import load_dotenv
import logging

SESSION_KEY = "session"
NOT_LOGGED_IN_TEXT = (
    "Puzzle inputs differ by user.  Please log in to get your puzzle input."
)
USER_AGENT_HEADER_BODY = "https://github.com/H-Rusch/AdventOfCode-Python contact @ https://github.com/H-Rusch/AdventOfCode-Python/issues/new"


class AocDownloadException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def download_input(year: int, day: int) -> str:
    logging.info(f"Downloading input for year {year} day {day}...")

    url = build_url(year, day)
    cookies = build_cookies()
    headers = build_headers()

    response = requests.get(url, cookies=cookies, headers=headers)

    if not response.text.startswith(NOT_LOGGED_IN_TEXT):
        logging.info("Download finished successfully.")

        return response.text
    else:
        raise AocDownloadException(
            "Session to the website has expired. Please log in again and update the session value."
        )


def build_url(year: int, day: int) -> str:
    return f"https://adventofcode.com/{year}/day/{day}/input"


def build_cookies() -> dict:
    return {SESSION_KEY: get_session_cookie()}


def build_headers() -> dict:
    return {"User-Agent": USER_AGENT_HEADER_BODY}


def get_session_cookie() -> str:
    load_dotenv()

    if SESSION_KEY in os.environ:
        return os.environ[SESSION_KEY]
    else:
        raise AocDownloadException(
            f"Key {SESSION_KEY} not present in this environment. Make sure you set it either as an env variable or through a .env file."
        )
