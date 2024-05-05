from __future__ import annotations

import json
from io import StringIO

import click
import yaml


@click.command()
@click.argument("log_file", type=click.File("r"))
@click.option("output_file", "--output", "-o", type=click.File("w"), help="Output file")
@click.option(
    "--format",
    type=click.Choice(["json", "yaml"]),
    default="json",
    help="Output format",
)
def parse_quake_log(log_file: StringIO, output_file: StringIO | None, format: str):
    """Parse a Quake 3 Arena log file."""
    from quake_log_parser.parser import Parser

    parser = Parser()
    parser.parse(log_file)

    out = output_file or StringIO()
    (json if format == "json" else yaml).dump(parser.results, out, indent=2)

    if not output_file:
        click.echo(out.getvalue())
