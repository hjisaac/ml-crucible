from .base_export import BaseExperiment

class MuonExperiment(BaseExperiment):
    def track(self):
        raise NotImplementedError