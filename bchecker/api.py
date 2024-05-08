import asyncio
import sys
from hashlib import sha1
from html import unescape
from json import dumps
from re import sub
from time import time

import httpx

from .utils import Colors, Config, UserInput


class EmailChecker(Colors, Config, UserInput):
    MAIL_URL = "https://webapi.namescan.io/v1/freechecks/email/breaches"

    @classmethod
    async def __make_request(
        cls, client: httpx.AsyncClient, email: str
    ) -> httpx.Response:
        return await client.post(
            cls.MAIL_URL,
            json={
                "email": email,
                "g-recaptcha-response": None,
            },
        )

    @staticmethod
    def __handle_response(response: httpx.Response, email: str) -> dict:
        response_json = response.json()
        return {
            "count": response_json.get("count", 0),
            "email": email,
            "breaches": [
                {
                    "name": breach.get("name", ""),
                    "breachDate": breach.get("breachDate", ""),
                    "description": unescape(
                        sub("<.*?>", "", breach.get("description", ""))
                    ),
                    "compromised": breach.get("dataClasses", ""),
                }
                for breach in response_json.get("breaches", [])
            ],
        }

    @classmethod
    async def run_email(
        cls, client: httpx.AsyncClient, email: str = None, verbose=False
    ) -> None:
        while True:
            email = email or cls.get_input("\nYour email: ")
            if email == "!s":
                sys.exit()
            response = await cls.__make_request(client, email)
            result = cls.__handle_response(response, email)
            if count := result.get("count"):
                verbose = verbose or cls.get_verbose("Verbose mode? (y/n): ")
                if verbose:
                    print(dumps(result, indent=4, ensure_ascii=False))
                    if cls.get_verbose("\nDo you want to save to file? (y/n): "):
                        cls.save_results(result, "mailleaks.json")
                else:
                    print(
                        f"{cls.RED}Oh no — pwned!{cls.END} Your {cls.BYELLOW}{email}{cls.END} pwned in {cls.WHITE}{count}{cls.END} data breaches!"
                    )
            else:
                print(
                    f"{cls.BGREEN}Good news — no pwnage found!{cls.END} No breaches account for {cls.BYELLOW}{email}{cls.END}"
                )

            email, verbose = None, False


class PassChecker(Colors, Config, UserInput):
    PASS_URL = "https://api.pwnedpasswords.com/range"

    @classmethod
    async def __make_request(
        cls, client: httpx.AsyncClient, head: str
    ) -> httpx.Response:
        return await client.get(f"{cls.PASS_URL}/{head}")

    @staticmethod
    def __leaks_count(response: httpx.Response, tail: str) -> int:
        hashes = {
            hash_value: int(count)
            for hash_value, count in (
                line.split(":") for line in response.text.splitlines()
            )
        }
        return hashes.get(tail, 0)

    @staticmethod
    def __hashes_password(password: str) -> tuple:
        sha1password = sha1(bytes(password, "utf-8")).hexdigest().upper()
        head, tail = sha1password[:5], sha1password[5:]
        return head, tail

    @classmethod
    async def __single_pass(cls, client: httpx.AsyncClient, password: str) -> None:
        while True:
            password = password or cls.get_input("\nYour password: ")
            if password == "!s":
                sys.exit()
            head, tail = cls.__hashes_password(password)
            response = await cls.__make_request(client, head)
            if count := cls.__leaks_count(response, tail):
                print(
                    f"{cls.RED}Oh no — pwned!{cls.END} This password {cls.BYELLOW}{password}{cls.END} has been seen {cls.WHITE}{count}{cls.END} times!"
                )
            else:
                print(
                    f"{cls.BGREEN}Good news — no pwnage found!{cls.END} No breaches password for {cls.BYELLOW}{password}{cls.END}"
                )

            password = None

    @classmethod
    async def __mass_pass(cls, client: httpx.AsyncClient, filename: str) -> dict:
        result = {}
        passwords = cls.load_file(filename)
        heads, tails = zip(*(cls.__hashes_password(password) for password in passwords))
        tasks = [cls.__make_request(client, head) for head in heads]
        completed_tasks = await asyncio.gather(*tasks)
        for index, response in enumerate(completed_tasks):
            if count := cls.__leaks_count(response, tails[index]):
                result[passwords[index]] = (
                    f"Oh no — pwned! This password has been seen {count} times!"
                )
            else:
                result[passwords[index]] = (
                    "Good news — no pwnage found! No breaches password!"
                )

        return result

    @classmethod
    async def run_pass(
        cls,
        client: httpx.AsyncClient,
        filename: str = None,
        password: str = None,
        task_type: str = None,
    ) -> None:
        while True:
            task_type = task_type or cls.get_input(
                "\nEnter task type (1.Single or 2.Mass): "
            )
            if task_type == "!s":
                sys.exit()

            if task_type == "1":
                await cls.__single_pass(client, password)
            elif task_type == "2":
                filename = filename or cls.get_input("\nEnter filename: ")
                started_mass = time()
                result = await cls.__mass_pass(client, filename)
                print(dumps(result, indent=4, ensure_ascii=False))
                print(f"\nTime taken: {cls.time_taken(started_mass)}")
                cls.save_results(result, "passleaks.json")

            task_type, filename = None, None
