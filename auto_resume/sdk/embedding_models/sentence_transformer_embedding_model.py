from sentence_transformers import SentenceTransformer

from auto_resume.sdk.embedding_models.base_embedding_model import BaseEmbeddingModel


class SentenceTransformerEmbeddingModel(BaseEmbeddingModel):
    DEFAULT_CONFIG = {
        'model_name': 'all-MiniLM-L12-v2',  # dim = 384
        'device': None
    }

    def __init__(self, model_config):
        super().__init__(model_config)
        self.model_config = {**self.DEFAULT_CONFIG, **self.model_config}
        self.model = SentenceTransformer(
            model_name_or_path=self.model_config['model_name'],
            device=self.model_config['device']
        )
    def vectorize(self, query: str):
        vector = self.model.encode([query])
        return vector[0]

    def batch_vectorize(self, queries: list[str]):
        vectors = self.model.encode(queries)
        return vectors
    

