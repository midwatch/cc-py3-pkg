from pathlib import Path

if __name__ == '__main__':

    if '{{ cookiecutter.enable_cli|lower }}' != 'y':
        (Path.cwd() / '{{ cookiecutter.solution_slug }}' / 'cli.py').unlink()
