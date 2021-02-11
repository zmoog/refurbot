#!/usr/bin/env python

import click

from refurbot.domain import commands
from refurbot import bootstrap


@click.command()
@click.option(
    '--country',
    required=True,
    help='The country ID')
@click.option(
    '--product',
    required=True,
    help='The product ID')
def run_command(country: str, product: str):
    """Check the product availability in a given country"""

    cmd = commands.SearchDeals(
        country=country,
        product=product,
    )

    messagebus = bootstrap.for_cli()
    messagebus.handle(cmd, {})


if __name__ == '__main__':
    run_command()
