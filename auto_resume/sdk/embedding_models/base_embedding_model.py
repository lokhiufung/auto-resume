from abc import ABC, abstractmethod


class BaseEmbeddingModel(ABC):
    
    def __init__(self, model_config):
        self.model_config = model_config

    @abstractmethod
    def vectorize(self):
        pass

    @abstractmethod
    def batch_vectorize(self):
        pass
