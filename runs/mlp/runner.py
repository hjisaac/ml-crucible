from __future__ import annotations

import logging
import pprint
import sys
from pathlib import Path
from typing import Any

if __package__ is None or __package__ == "":
	# Supports direct execution: python runs/mlp/runner.py
	sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.jobs import AbstractJob


logger = logging.getLogger(__name__)


class Job(AbstractJob):
	"""Minimal concrete job used to validate the run pipeline."""

	def setup_data(self) -> None:
		self.data = {"status": "ready"}

	def run(self) -> dict[str, str]:
		self.setup()
		logger.info("Identity task executed with data status: %s", self.data["status"])
		return {"status": "ok", "task": "identity"}


JOB_CLASS = Job