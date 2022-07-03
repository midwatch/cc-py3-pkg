from pathlib import Path

from invoke import Collection
from invoke import task
from invoke.exceptions import Failure

GITHUB_USERNAME = "{{ github_username }}"
GITHUB_SLUG = "{{ github_slug }}"
SOLUTION_SLUG = "{{ solution_slug }}"
CC_VERSION = "0.0.0"

ROOT_DIR = Path(__file__).parent
SOURCE_DIR = ROOT_DIR.joinpath(SOLUTION_SLUG)
TEST_DIR = ROOT_DIR.joinpath("tests")
PYTHON_DIRS_STR = " ".join([str(_dir) for _dir in [SOURCE_DIR, TEST_DIR]])


def scm_init(ctx, gitflow=True):
    """Init scm repo (if required).

    Raises:
        Failure: .gitignore does not exist

    Returns:
        None
    """
    if not Path('.gitignore').is_file():
        raise Failure('.gitignore does not exist')

    is_new_repo = not Path('.git').is_dir()
    uri_remote = f'git@github.com:{GITHUB_USERNAME}/{GITHUB_SLUG}.git'
    commit_msg = f'new package from midwatch/cc-py3-pkg ({CC_VERSION})'
    branches = ['main']

    if is_new_repo:
        ctx.run('git init')
        ctx.run('git add .')
        ctx.run('git commit -m "{commit_msg}"')
        ctx.run('git branch -M main')
        ctx.run('git remote add origin {}'.format(uri_remote))
        ctx.run('git tag -a "v_0.0.0" -m "cookiecutter ref"')

    if gitflow:
        ctx.run('git flow init -d')
        ctx.run('git flow config set versiontagprefix v_')
        branches.append('develop')

    if is_new_repo:
        for branch in branches:
            ctx.run(f'git push -u origin {branch}')

        ctx.run('git push --tags')

@task
def scm_push(ctx):
    """Push all branches and tags to origin."""

    ctx.run('git push --all')
    ctx.run('git push --tags')


@task
def scm_status(ctx):
    """Show status of remote branches."""
    ctx.run('git for-each-ref --format="%(refname:short) %(upstream:track)" refs/heads')


@task
def init_repo(ctx):
    """Initialize freshly cloned repo."""
    scm_init(ctx)

scm = Collection()
scm.add_task(scm_push, name="push")
scm.add_task(scm_status, name="status")

ns = Collection(init_repo)

ns.add_collection(scm, name="scm")
