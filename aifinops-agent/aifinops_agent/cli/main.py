import click
from aifinops_agent.core.connect import connect_flow
from aifinops_agent.core.aws_setup import setup_aws

@click.group()
def cli(): pass

@cli.command()
def connect(): connect_flow()

@cli.command()
def setup_aws_cmd(): setup_aws()
