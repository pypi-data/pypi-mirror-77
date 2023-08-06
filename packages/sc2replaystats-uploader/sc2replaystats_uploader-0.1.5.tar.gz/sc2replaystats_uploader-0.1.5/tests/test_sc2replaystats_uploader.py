#!/usr/bin/env python

"""Tests for `sc2replaystats_uploader` package."""


from click.testing import CliRunner

from sc2replaystats_uploader import sc2replaystats_uploader
from sc2replaystats_uploader import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message and exit." in help_result.output
