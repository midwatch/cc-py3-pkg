"""Console script for {{cookiecutter.solution_name}}."""

import typer

app = typer.Typer()


@app.command()
def main() -> None:
    """Console script for python_boilerplate."""
    typer.echo("Replace this message by putting your code into "
               "python_boilerplate.cli.main")
    typer.echo("See click documentation at https://click.palletsprojects.com/")


if __name__ == "__main__":
    # sys.exit(main())  # pragma: no cover
    app()
