from abc import abstractmethod

from .jobber import AbstractJobber

class AbstractTrainerJob(AbstractJobber):
    """Base class for all trainer jobber classes."""
    
    def __init__(self, config) -> None:
        self.config = config
        
    def setup(self) -> None:
        self.setup_data()
        self.setup_model()
        self.setup_optimizer()
        self.setup_lr_scheduler()
        self.setup_metrics()
        self.setup_tracker()
        
    def setup_data(self) -> None:
        pass
        
    @abstractmethod
    def setup_model(self) -> None:
        pass
    
    @abstractmethod
    def setup_optimizer(self) -> None:
        pass
    
    @abstractmethod
    def setup_lr_scheduler(self) -> None:
        pass
    
    @abstractmethod
    def setup_metrics(self) -> None:
        pass
    
    @abstractmethod
    def train(self) -> None:
        pass

    @abstractmethod
    def setup_tracker(self) -> None:
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