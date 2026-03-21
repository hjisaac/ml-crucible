from abc import ABCMeta, abstractmethod


class GradientDescentMixin(metaclass=ABCMeta):
    """Mixin for gradient-descent-based training: optimizer and lr scheduler setup."""

    @abstractmethod
    def setup_optimizer(self) -> None:
        """Initialize the optimizer (e.g. SGD, Adam, Muon)."""
        pass

    @abstractmethod
    def setup_lr_scheduler(self) -> None:
        """Initialize the learning rate scheduler (e.g. cosine, step)."""
        pass
