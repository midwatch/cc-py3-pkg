#!/usr/bin/env python
"""Tests for `{{ cookiecutter.solution_slug }}` package."""
# pylint: disable=redefined-outer-name

import pytest

from click.testing import CliRunner

from {{ cookiecutter.solution_slug }} import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert '{{ cookiecutter.solution_slug }}.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
