#!/usr/bin/python3
import sys
import asyncio
import argparse
import logging
from web.client import Client

logging.basicConfig(level=logging.INFO)


def add_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numeric', type=str, help='Numeric currency code')
    parser.add_argument('--alpha', type=str, help='Alpha currency code')

    return parser


async def app():
    parser = add_parser()
    namespace = parser.parse_args(sys.argv[1:])
    data = await Client().get_cur_base(numeric=namespace.numeric, alpha=namespace.alpha)
    print(data)


def main():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(app())

    except Exception as err:
        logging.error(err)


if __name__ == '__main__':
    main()
