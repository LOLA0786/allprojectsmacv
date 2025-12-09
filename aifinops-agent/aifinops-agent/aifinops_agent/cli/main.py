import click
from aifinops_agent.core.connect import connect_flow
from aifinops_agent.core.aws_setup import setup_aws
from aifinops_agent.core.gcp_setup import setup_gcp
from aifinops_agent.core.azure_setup import setup_azure

@click.group()
def cli():
    pass

@cli.command()
def connect():
    """Register your company + generate API key."""
    connect_flow()

@cli.command()
def setup_aws_cmd():
    setup_aws()

@cli.command()
def setup_gcp_cmd():
    setup_gcp()

@cli.command()
def setup_azure_cmd():
    setup_azure()

