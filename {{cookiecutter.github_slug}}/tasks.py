"invoke task definition"
from pathlib import Path

from invoke import Collection
from invoke import task

from mw_dry_invoke import bumpversion
from mw_dry_invoke import git

GITHUB_USERNAME = "{{ cookiecutter.github_username }}"
GITHUB_SLUG = "{{ cookiecutter.github_slug }}"
SOLUTION_SLUG = "{{ cookiecutter.solution_slug }}"
CC_VERSION = "0.4.0"

ROOT_DIR = Path(__file__).parent
SOURCE_DIR = ROOT_DIR.joinpath(SOLUTION_SLUG)
TEST_DIR = ROOT_DIR.joinpath("tests")
PYTHON_DIRS_STR = " ".join([str(_dir) for _dir in [SOURCE_DIR, TEST_DIR]])


@task
def clean_build(ctx):
    """
    Clean up files from package building
    """
    ctx.run("rm -fr build/")
    ctx.run("rm -fr dist/")
    ctx.run("rm -fr .eggs/")
    ctx.run("find . -name '*.egg-info' -exec rm -fr {} +")
    ctx.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(ctx):
    """
    Clean up python file artifacts
    """
    ctx.run("find . -name '*.pyc' -exec rm -f {} +")
    ctx.run("find . -name '*.pyo' -exec rm -f {} +")
    ctx.run("find . -name '*~' -exec rm -f {} +")
    ctx.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def lint_pycodestyle(ctx):
    """Lint code with pycodestyle"""
    ctx.run(f'poetry run pycodestyle --max-line-length=120 {SOURCE_DIR}')


@task
def lint_pydocstyle(ctx):
    """Lint code with pydocstyle"""
    ctx.run(f'poetry run pydocstyle {SOURCE_DIR}')


@task
def lint_pylint(ctx):
    """Lint code with pylint"""
    ctx.run(f'poetry run pylint {PYTHON_DIRS_STR}')


@task
def lint_similar(ctx):
    """Run pylint test for duplicate code."""
    ctx.run(f'poetry run pylint --disable=all --enable=similarities {PYTHON_DIRS_STR}')


@task(pre=[clean_build, clean_python])
def clean(ctx):     # pylint: disable=unused-argument
    """Runs all clean sub-tasks."""


@task(clean)
def build(ctx):
    """
    Build source and wheel packages
    """
    ctx.run("poetry build")


@task()
def format_yapf(ctx):
    """Format code"""
    ctx.run(f'poetry run yapf --in-place {PYTHON_DIRS_STR}')
    ctx.run(f'poetry run isort {PYTHON_DIRS_STR}')


@task
def init_repo(ctx):
    """Initialize freshly cloned repo."""
    ctx.run('poetry install')
    git.init(ctx, GITHUB_USERNAME, GITHUB_SLUG, CC_VERSION)


@task(lint_pylint, lint_pycodestyle, lint_pydocstyle)
def lint(ctx):  # pylint: disable=unused-argument
    """Run all linters"""


@task(pre=[clean, build])
def release(ctx):
    """Release package to pypi."""
    ctx.run("poetry publish")


@task(clean)
def test_accept(ctx):   # pylint: disable=unused-argument
    "Run acceptance tests."


@task
def test_pytest(ctx):   # pylint: disable=unused-argument
    """Run pytest tests"""
    ctx.run('poetry run pytest')

@task
def test_typing(ctx):
    """Run mypy typing test."""
    ctx.run('poetry run mypy --disallow-untyped-defs python_boilerplate/')

@task(test_pytest, test_accept)
def test(ctx):  # pylint: disable=unused-argument
    """Run tests"""


ns = Collection(build, bumpversion, clean, init_repo, lint, lint_similar,
    release, test, test_typing)
ns.add_task(format_yapf, name="format")

ns.add_collection(git.collection, name="scm")
