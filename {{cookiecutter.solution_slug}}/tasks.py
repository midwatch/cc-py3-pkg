from pathlib import Path

from invoke import Collection
from invoke import task
from invoke.exceptions import Failure

GITHUB_USERNAME = "{{ cookiecutter.github_username }}"
SOLUTION_SLUG = "{{ cookiecutter.solution_slug }}"
CC_VERSION = "{{ cookiecutter.version }}"


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
                                                       SOLUTION_SLUG
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


@task
def init(ctx):
    """Initialize freshly cloned repo."""
    ctx.run('poetry install')

    scm_init(ctx)

    ctx.run('git flow init -d')
    ctx.run('git flow config set versiontagprefix v_')

    scm_push(ctx)


scm = Collection()
scm.add_task(scm_push, name="push")
scm.add_task(scm_status, name="status")

ns = Collection(init)
ns.add_collection(scm, name="scm")