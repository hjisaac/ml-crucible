import logging

from core.jobs import AbstractGDTrainerJob
from core.models.mlp import MLP


logger = logging.getLogger(__name__)


class MLPTrainerJob(AbstractGDTrainerJob):
    def setup_data(self) -> None:
        self.train_data = None

    def setup_model(self) -> None:
        self.model = MLP()

    def setup_optimizer(self) -> None:
        self.optimizer = None

    def setup_lr_scheduler(self) -> None:
        self.lr_scheduler = None

    def setup_metrics(self) -> None:
        self.metrics = {}

    def setup_tracker(self) -> None:
        self.tracker = None

    def train(self) -> dict[str, str]:
        logger.info("MLP training placeholder executed.")
        return {"status": "ok", "phase": "train"}

    def evaluate(self) -> dict[str, str]:
        logger.info("MLP evaluation placeholder executed.")
        return {"status": "ok", "phase": "eval"}


JOB_CLASS = MLPTrainerJob