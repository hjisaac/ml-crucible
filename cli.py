import logging

import typer

from core.jobs.cli import standalone_job_cli, trainer_job_cli
from runs.cli import run_named_job


logger = logging.getLogger(__name__)


cli_app = typer.Typer(pretty_exceptions_enable=False)

cli_app.add_typer(
    standalone_job_cli,
    name="standalone",
    help="Run standalone jobs.",
)

cli_app.add_typer(
    trainer_job_cli,
    name="trainer",
    help="Run trainer jobs.",
)


@cli_app.command()
def mlp(
    config: str = typer.Option(
        "default",
        "--config",
        "-c",
        help="YAML config name under runs/mlp/configs (without extension).",
    ),
) -> None:
    """Run the MLP job using a named config."""
    try:
        run_named_job("mlp", config)
    except (FileNotFoundError, ValueError, TypeError) as exc:
        logger.exception("Failed to run mlp with config '%s'.", config)
        raise typer.Exit(code=1) from exc


@cli_app.command("run")
def run_job(
    name: str = typer.Argument(..., help="Run name under runs/ (e.g. mlp)."),
    config: str = typer.Option(
        "default",
        "--config",
        "-c",
        help="YAML config name under runs/<name>/configs (without extension).",
    ),
) -> None:
    """Run any registered job by run name."""
    try:
        run_named_job(name, config)
    except (FileNotFoundError, ValueError, TypeError) as exc:
        logger.exception("Failed to run '%s' with config '%s'.", name, config)
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    cli_app()