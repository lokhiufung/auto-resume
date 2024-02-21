from abc import ABC, abstractmethod


class BaseVectorStore(ABC):

    DEFAULT_CONFIG = {}

    def __init__(self, docs, embedding_model, vector_store_config):
        self.docs = docs
        self.embedding_model = embedding_model
        self.vector_store_config = vector_store_config

        self._add_default_config()

    def _add_default_config(self):
        for k, v in self.DEFAULT_CONFIG.items():
            if k not in self.vector_store_config:
                self.vector_store_config[k] = v
    
    def search(self, query, n_neighbors=1):
        vector = self.embedding_model.vectorize(query)
        return self._vector_search(vector, n_neighbors)

    @classmethod
    def from_embedding_model_config(cls, embedding_model_config, vector_store_config, embedding_model_backend='sentence_transformer', docs=[]):
        if embedding_model_backend == 'sentence_transformer':
            from auto_resume.sdk.embedding_models.sentence_transformer_embedding_model import SentenceTransformerEmbeddingModel

            embedding_model = SentenceTransformerEmbeddingModel(embedding_model_config)
        else:
            raise ValueError(f'{embedding_model_backend} is not supported now')

        vector_store = cls(docs=docs, embedding_model=embedding_model, vector_store_config=vector_store_config)
        return vector_store
    
    @abstractmethod
    def _vector_search(self):
        pass
    
    def update(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError

    def bulk_write(self):
        raise NotImplementedError

    def delete_by_id(self, id_):
        raise NotImplementedError
