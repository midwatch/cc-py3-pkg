"invoke task definition"

from pathlib import Path

from invoke import Collection
from invoke import task

from mw_dry_invoke import bumpversion
from mw_dry_invoke import git

GITHUB_USERNAME = "midwatch"
GITHUB_SLUG = "cc-py3-pkg"
SOLUTION_SLUG = "cc-py3-pkg"
CC_VERSION = "0.0.0"

ROOT_DIR = Path(__file__).parent
SOURCE_DIR = ROOT_DIR.joinpath(SOLUTION_SLUG)
TEST_DIR = ROOT_DIR.joinpath("tests")
PYTHON_DIRS_STR = " ".join([str(_dir) for _dir in [SOURCE_DIR, TEST_DIR]])


@task
def init_repo(ctx):
    """Initialize freshly cloned repo."""
    git.init(ctx, GITHUB_USERNAME, GITHUB_SLUG, CC_VERSION)

@task
def test(ctx):
    """Test Cookie Cutter."""
    ctx.run('pylint tasks.py "{{cookiecutter.github_slug}}/tasks.py"')


ns = Collection(bumpversion, init_repo, test)

ns.add_collection(git.collection, name="scm")
