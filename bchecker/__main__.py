import asyncio
import sys
from argparse import ArgumentParser
from os import name, system
from textwrap import dedent

from .api import EmailChecker, PassChecker
from .http_client import HttpClient
from .utils import Banner


class BreachChecker(Banner, EmailChecker, PassChecker):
    LOGO = r"""
        ▄▄▄▄· ▄▄▄  ▄▄▄ . ▄▄▄·  ▄▄·  ▄ .▄   ▄▄·  ▄ .▄▄▄▄ . ▄▄· ▄ •▄ ▄▄▄ .▄▄▄
        ▐█ ▀█▪▀▄ █·▀▄.▀·▐█ ▀█ ▐█ ▌▪██▪▐█  ▐█ ▌▪██▪▐█▀▄.▀·▐█ ▌▪█▌▄▌▪▀▄.▀·▀▄ █·
        ▐█▀▀█▄▐▀▀▄ ▐▀▀▪▄▄█▀▀█ ██ ▄▄██▀▀█  ██ ▄▄██▀▀█▐▀▀▪▄██ ▄▄▐▀▀▄·▐▀▀▪▄▐▀▀▄
        ██▄▪▐█▐█•█▌▐█▄▄▌▐█▪ ▐▌▐███▌██▌▐▀  ▐███▌██▌▐▀▐█▄▄▌▐███▌▐█.█▌▐█▄▄▌▐█•█▌
        ·▀▀▀▀ .▀  ▀ ▀▀▀  ▀  ▀ ·▀▀▀ ▀▀▀ ·  ·▀▀▀ ▀▀▀ · ▀▀▀ ·▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀▀"""

    @classmethod
    def display_logo_and_author(cls):
        print(cls.center(cls.faded_text(cls.LOGO)))
        print(cls.center(f"BY: {cls.LYELLOW}══ᵂʰᵒᴬᴹ!{cls.END}"))
        print(
            f"\n{cls.RED}>> {cls.LPURPLE}Type {cls.BYELLOW}!s{cls.LPURPLE} to STOP|EXIT{cls.END}"
        )

    @classmethod
    async def start_program(cls) -> None:
        parser = ArgumentParser(
            description="Email and password checker for leaked data breaches!"
        )
        parser.add_argument(
            "-pu",
            "--proxy_url",
            default=None,
            type=str,
            help="Proxy URL. Example: (http://username:password@host:port or socks5://username:password@host:port)",
        )
        parser.add_argument(
            "-e", "--email", default=None, type=str, help="Email that should be checked!"
        )
        parser.add_argument(
            "-m",
            "--mode",
            default=None,
            type=str,
            choices=["1", "2"],
            help="(1) Email Checker (2) Password Checker",
        )
        parser.add_argument(
            "-t",
            "--task_type",
            default=None,
            type=str,
            choices=["1", "2"],
            help="(1) Single Check (2) Mass Check",
        )
        parser.add_argument(
            "-p",
            "--password",
            default=None,
            type=str,
            help="Password that should be checked!",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            default=False,
            action="store_true",
            help="Get breaches details!",
        )
        parser.add_argument(
            "-f",
            "--filename",
            default=None,
            type=str,
            help="List of passwords for mass checking!",
        )

        args = parser.parse_args()
        cls.display_logo_and_author()

        async with HttpClient(args.proxy_url) as client:
            while True:
                if args.mode is None:
                    print(
                        dedent(
                            f"""
                        {cls.LBLUE}[1] {cls.GREEN}EMAIL CHECKER{cls.END}
                        {cls.LBLUE}[2] {cls.GREEN}PASSWORD CHECKER{cls.END}
                            """
                        )
                    )
                    args.mode = cls.get_input("Select mode: ")

                if args.mode == "!s":
                    sys.exit()
                elif args.mode == "1":
                    print(f"\nYour email: {args.email}") if args.email else None
                    await cls.run_email(client, args.email, args.verbose)
                elif args.mode == "2":
                    (
                        print(f"\nYour password: {args.password}")
                        if args.password
                        else None
                    )
                    await cls.run_pass(
                        client, args.filename, args.password, args.task_type
                    )
                else:
                    print("Mode is not available! Please check your input!")

                args.mode = cls.get_input("\nSelect mode: ")


if __name__ == "__main__":
    system("cls" if name == "nt" else "clear")
    asyncio.run(BreachChecker.start_program())
