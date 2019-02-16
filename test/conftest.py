from click.testing import CliRunner
import pytest


@pytest.fixture(scope="session")
def runner():
    return CliRunner()
