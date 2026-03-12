from abc import ABCMeta, abstractmethod

from core.mixins.deep_learning import GradientDescentMixin


class AbstractJobber(metaclass=ABCMeta):
    """Base class for all jobber classes (e.g. trainers, analysers)."""
    
    def __init__(self, config) -> None:
        self.config = config
        
    @abstractmethod
    def setup_data(self) -> None:
        pass
    
    def setup(self) -> None:
        self.setup_data()
        
    
    @abstractmethod
    def setup_tracker(self) -> None:
        pass
    
    @abstractmethod
    def run(self) -> None:
        pass
    
class AbstractTrainerJob(AbstractJobber):
    """Base class for all trainer jobbers, regardless of the optimization strategy."""

    def __init__(self, config) -> None:
        self.config = config

    def setup(self) -> None:
        super().setup()
        self.setup_model()
        self.setup_metrics()
        self.setup_tracker()


    @abstractmethod
    def setup_model(self) -> None:
        pass

    @abstractmethod
    def setup_metrics(self) -> None:
        pass

    @abstractmethod
    def train(self) -> None:
        pass

    @abstractmethod
    def evaluate(self) -> None:
        pass

    @abstractmethod
    def run(self):
        return self.train()


class AbstractGDTrainerJob(AbstractTrainerJob, GradientDescentMixin):
    """Trainer jobber that assumes gradient-descent-based optimization."""

    def setup(self) -> None:
        super().setup()
        self.setup_optimizer()
        self.setup_lr_scheduler()