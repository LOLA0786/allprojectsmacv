from setuptools import setup, find_packages

setup(
    name="aifinops-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "click",
        "boto3",
        "google-cloud-monitoring",
        "azure-mgmt-monitor",
    ],
    entry_points={
        "console_scripts": [
            "aifinops=aifinops_agent.cli.main:cli"
        ]
    },
)
