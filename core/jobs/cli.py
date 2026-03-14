import logging

import typer

from runs.cli import list_available_runs, run_named_job


logger = logging.getLogger(__name__)


standalone_job_cli = typer.Typer(
    help="Standalone jobs (non-training workflows).",
    pretty_exceptions_enable=False,
)

trainer_job_cli = typer.Typer(
    help="Trainer jobs (fit/eval workflows).",
    pretty_exceptions_enable=False,
)


@standalone_job_cli.command("list")
def list_standalone_jobs() -> None:
    """List currently wired standalone jobs."""
    typer.echo("No standalone jobs are registered yet.")


@standalone_job_cli.command("run")
def run_standalone_job(name: str) -> None:
    """Run a standalone job by name (placeholder)."""
    raise typer.BadParameter(f"Standalone job '{name}' is not implemented yet.")


@trainer_job_cli.command("list")
def list_trainer_jobs() -> None:
    """List currently wired trainer jobs."""
    runs = list_available_runs()
    typer.echo(f"Available trainer jobs: {', '.join(runs) if runs else 'none'}")


@trainer_job_cli.command("run")
def run_trainer_job(
    name: str,
    config: str = typer.Option(
        "default",
        "--config",
        "-c",
        help="YAML config name under runs/<name>/configs (without extension).",
    ),
) -> None:
    """Run a trainer job by name."""
    try:
        run_named_job(name.lower(), config)
    except (FileNotFoundError, ValueError, TypeError) as exc:
        logger.exception("Failed to run trainer job '%s' with config '%s'.", name, config)
        raise typer.Exit(code=1) from exc
