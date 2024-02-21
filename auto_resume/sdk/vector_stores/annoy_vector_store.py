import os
import json

from annoy import AnnoyIndex
from tqdm import tqdm

from auto_coder.sdk.core.vector_stores.base_vector_store import BaseVectorStore
from auto_coder.sdk import utils


class AnnoyVectorStore(BaseVectorStore):
    INDEX_FILE_NAME = 'index.ann'
    DOCS_FILE_NAME = 'docs.txt'
    CONFIG_FILE_NAME = 'config.json'
    DEFAULT_CONFIG = {
        'dim': 128,
        'metric': 'angular',
        'n_trees': 10,
    }
    def __init__(self, docs, embedding_model, vector_store_config):
        super().__init__(docs, embedding_model, vector_store_config)

        self.index = AnnoyIndex(
            f=self.vector_store_config['dim'],
            metric=self.vector_store_config['metric']
        )
        self.index_file_path = os.path.join(self.vector_store_config['store_path'], self.INDEX_FILE_NAME)
        self.docs_file_path = os.path.join(self.vector_store_config['store_path'], self.DOCS_FILE_NAME)
        self.config_file_path = os.path.join(self.vector_store_config['store_path'], self.CONFIG_FILE_NAME) 

        if not os.path.exists(self.vector_store_config['store_path']):
            os.makedirs(self.vector_store_config['store_path'])
            self._build_index()
        else:
            # load the vector store
            self.index.load(self.index_file_path)
        
        self.idx_to_doc = {doc['id']: doc for doc in self.docs}
    
    @classmethod
    def from_store_path(cls, embedding_model, store_path):
        docs_file_path = os.path.join(store_path, cls.DOCS_FILE_NAME)
        config_file_path = os.path.join(store_path, cls.CONFIG_FILE_NAME)
        # load docs
        docs = []
        with open(docs_file_path, 'r') as f:
            for line in f:
                docs.append(json.loads(line))
        # load config
        with open(config_file_path, 'r') as f:
            config = json.load(f)
        return cls(docs, embedding_model, config)

    def _add_default_config(self):
        for k, v in self.DEFAULT_CONFIG.items():
            if k not in self.vector_store_config:
                self.vector_store_config[k] = v

    def _build_index(self):
        # { "id": 1, "content": "...", "metadata": {""}}
        # assign doc id to docs if there is no id
        if 'id' not in self.docs:
            self.docs = [{'id': i, **doc} for i, doc in enumerate(self.docs)]
        # create embeddings
        batches = utils.make_batches(self.docs, 10)
        for batch in tqdm(batches):
            vectors = self.embedding_model.batch_vectorize([doc['content'] for doc in batch])
            for vector, doc in zip(vectors, batch):
                self.index.add_item(doc['id'], vector)

        # paths
        # index_file_path = os.path.join(self.vector_store_config['store_path'], self.INDEX_FILE_NAME)
        # docs_file_path = os.path.join(self.vector_store_config['store_path'], self.DOCS_FILE_NAME)
        # config_file_path = os.path.join(self.vector_store_config['store_path'], self.CONFIG_FILE_NAME) 
        self.index.build(self.vector_store_config['n_trees'])
        # save the index
        self.index.save(self.index_file_path)
        # save the docs
        with open(self.docs_file_path, 'w') as f:
            for doc in self.docs:
                f.write(json.dumps(doc) + '\n')
        # save the config
        with open(self.config_file_path, 'w') as f:
            json.dump(self.vector_store_config, f)

    def _vector_search(self, vector, n_neighbors):
        indexes, distances = self.index.get_nns_by_vector(vector, n=n_neighbors, include_distances=True)
        docs = []
        for index, distance in zip(indexes, distances):
            docs.append({
                'score': distance,
                **self.idx_to_doc[index]                
            })
        return docs

    def normalize_score(self, scores):
        if self.vector_store_config['metric'] == 'angular':
            return [(2 - score) / 2 for score in scores ]
        else:
            raise ValueError('Do not support normalization for metric={self.metric}')
        
