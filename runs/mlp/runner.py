from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

if __package__ is None or __package__ == "":
	# Supports direct execution: python runs/mlp/runner.py
	sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.jobs import AbstractJob


logger = logging.getLogger(__name__)


class IdentityJob(AbstractJob):
	"""Minimal concrete job used to validate the run pipeline."""

	def setup_data(self) -> None:
		self.data = {"status": "ready"}

	def run(self) -> dict[str, str]:
		self.setup()
		logger.info("Identity task executed with data status: %s", self.data["status"])
		return {"status": "ok", "task": "identity"}


def build_default_config() -> dict[str, Any]:
	return {
		"log_dir": "logs",
		"log_console_level": "INFO",
		"log_file_level": "DEBUG",
	}


def main() -> None:
	parser = argparse.ArgumentParser(description="Run the first minimal task.")
	parser.parse_args()

	job = IdentityJob(config=build_default_config())
	result = job.run()
	print(result)


if __name__ == "__main__":
	main()
