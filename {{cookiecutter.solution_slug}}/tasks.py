from pathlib import Path

from invoke import Collection
from invoke import task
from invoke.exceptions import Failure

GITHUB_USERNAME = "{{ cookiecutter.github_username }}"
GITHUB_SLUG = "{{ cookiecutter.github_slug }}"
SOLUTION_SLUG = "{{ cookiecutter.solution_slug }}"
CC_VERSION = "{{ cookiecutter.version }}"


@task
def clean_build(ctx):
    """
    Clean up files from package building
    """
    ctx.run(ctx, "rm -fr build/")
    ctx.run(ctx, "rm -fr dist/")
    ctx.run(ctx, "rm -fr .eggs/")
    ctx.run(ctx, "find . -name '*.egg-info' -exec rm -fr {} +")
    ctx.run(ctx, "find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(ctx):
    """
    Clean up python file artifacts
    """
    ctx.run(ctx, "find . -name '*.pyc' -exec rm -f {} +")
    ctx.run(ctx, "find . -name '*.pyo' -exec rm -f {} +")
    ctx.run(ctx, "find . -name '*~' -exec rm -f {} +")
    ctx.run(ctx, "find . -name '__pycache__' -exec rm -fr {} +")


@task
def scm_init(ctx):
    """Init scm repo (if required).

    Raises:
        Failure: .gitignore does not exist

    Returns:
        None
    """
    if not Path('.gitignore').is_file():
        raise Failure('.gitignore does not exist')

    if not Path('.git').is_dir():
        uri_remote = 'git@github.com:{}/{}.git'.format(GITHUB_USERNAME,
                                                       GITHUB_SLUG
                                                      )

        ctx.run('git init')
        ctx.run('git add .')
        ctx.run('git commit -m "new package from midwatch/cc-py3-pkg ({})"'.format(CC_VERSION))
        ctx.run('git branch -M main')
        ctx.run('git remote add origin {}'.format(uri_remote))
        ctx.run('git tag -a "v_0.0.0" -m "cookiecutter ref"')


@task
def scm_push(ctx):
    """Push all branches and tags to origin."""

    for branch in ('develop', 'main'):
        ctx.run('git push origin {}'.format(branch))

    ctx.run('git push --tags')


@task
def scm_status(ctx):
    """Show status of remote branches."""
    ctx.run('git for-each-ref --format="%(refname:short) %(upstream:track)" refs/heads')


@task(help={'part': "major, minor, or patch"})
def bumpversion(ctx, part):
    """Bump project version

    Raises:
        Failure: part not in [major, minor, patch]
    """
    if part not in ['major', 'minor', 'patch']:
        raise Failure('Not a valid part')

    ctx.run(f'poetry run bump2version {part}')


@task(pre=[clean_build, clean_python])
def clean(ctx):
    """
    Runs all clean sub-tasks
    """
    pass


@task(clean)
def build(ctx):
    """
    Build source and wheel packages
    """
    ctx.run(ctx, "poetry build")


@task
def init(ctx):
    """Initialize freshly cloned repo"""
    ctx.run('poetry install')

    scm_init(ctx)

    ctx.run('git flow init -d')
    ctx.run('git flow config set versiontagprefix v_')

    scm_push(ctx)


@task(pre=[clean, build])
def release(ctx):
    """
    Make a release of the python package to pypi
    """
    ctx.run(ctx, "poetry publish")


@task
def test(ctx):
    """Run tests"""
    ctx.run('poetry run pytest')


scm = Collection()
scm.add_task(scm_push, name="push")
scm.add_task(scm_status, name="status")

ns = Collection(build, bumpversion, clean, init, test)
ns.add_collection(scm, name="scm")
