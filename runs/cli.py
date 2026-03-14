from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import Any

from hydra import compose, initialize_config_dir
from omegaconf import OmegaConf

from core.jobs import AbstractJob


_SUPPORTED_CONFIG_EXTENSIONS = (".yaml", ".yml")


def list_available_runs() -> list[str]:
	runs_root = Path(__file__).resolve().parent
	return sorted(
		path.name
		for path in runs_root.iterdir()
		if path.is_dir() and (path / "__init__.py").exists()
	)


def _resolve_concrete_job_class_from_module(module: Any) -> type[AbstractJob] | None:
	job_class = getattr(module, "JOB_CLASS", None)
	if inspect.isclass(job_class) and issubclass(job_class, AbstractJob):
		if inspect.isabstract(job_class):
			raise ValueError("JOB_CLASS is abstract; expose a concrete class.")
		return job_class

	return None


def resolve_job_class(run_name: str) -> type[AbstractJob]:
	run_name = run_name.strip().lower()
	try:
		module = importlib.import_module(f"runs.{run_name}")
	except ModuleNotFoundError as exc:
		raise ValueError(f"Run '{run_name}' was not found.") from exc

	resolved = _resolve_concrete_job_class_from_module(module)
	if resolved is not None:
		return resolved

	for _, cls in inspect.getmembers(module, inspect.isclass):
		if cls.__module__ != module.__name__:
			continue
		if cls is AbstractJob:
			continue
		if issubclass(cls, AbstractJob) and not inspect.isabstract(cls):
			return cls

	raise ValueError(
		f"Run '{run_name}' does not expose a concrete job class. "
		"Export JOB_CLASS = YourConcreteJob in runs/<run>/__init__.py."
	)


def load_config(run_name: str, config_name: str) -> dict[str, Any]:
	run_name = run_name.strip().lower()
	config_name = config_name.strip()
	run_dir = Path(__file__).resolve().parent / run_name
	if not run_dir.exists():
		raise FileNotFoundError(f"Run folder was not found: {run_dir}")

	config_dir = run_dir / "configs"
	if not config_dir.exists():
		raise FileNotFoundError(f"Config folder was not found: {config_dir}")

	config_path = Path(config_name)
	if config_path.suffix and config_path.suffix not in _SUPPORTED_CONFIG_EXTENSIONS:
		raise ValueError(
			"Only YAML configs are supported. Use .yaml/.yml or pass the config name without extension."
		)

	config_stem = config_path.stem if config_path.suffix else config_name
	candidates = [config_dir / f"{config_stem}{ext}" for ext in _SUPPORTED_CONFIG_EXTENSIONS]

	resolved_config_path = next((path for path in candidates if path.exists()), None)
	if resolved_config_path is None:
		looked_up = ", ".join(path.name for path in candidates)
		raise FileNotFoundError(
			f"Config '{config_name}' was not found for run '{run_name}'. Looked for: {looked_up}"
		)

	with initialize_config_dir(version_base=None, config_dir=str(config_dir.resolve())):
		config = compose(config_name=config_stem)

	config = OmegaConf.to_container(config, resolve=True)

	if not isinstance(config, dict):
		raise ValueError(f"Config must be a dictionary: {resolved_config_path}")
	return config


def run_named_job(run_name: str, config_name: str) -> None:
	job_class = resolve_job_class(run_name)
	config = load_config(run_name, config_name)
	job = job_class(config=config)
	job.run()
