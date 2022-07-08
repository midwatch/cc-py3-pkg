#!/usr/bin/env python
"""Tests for `{{ cookiecutter.solution_slug }}` package."""
# pylint: disable=redefined-outer-name

# import pytest

from typer.testing import CliRunner

from {{ cookiecutter.solution_slug }}.cli import app

runner = CliRunner()

def test_cli():
    """Test the CLI."""

    result = runner.invoke(app)
    assert result.exit_code == 0
