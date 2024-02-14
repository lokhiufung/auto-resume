import typing
import os
import json
from dataclasses import dataclass, asdict


@dataclass
class Company:
    id: int
    name: str
    location: str
    duration: str


@dataclass
class Highlight:
    id: int
    desc: str
    company: Company
    titles: typing.List[str]


class StorageClient:
    DEFAULT_STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage'))
    
    def __init__(self, storage_dir: str=None):
        if storage_dir:
            self.storage_dir = storage_dir
        else:
            self.storage_dir = self.DEFAULT_STORAGE_DIR
        
        self.highlight_file_path = os.path.join(self.storage_dir, 'base/highlight.jsonl')
        self.highlights = {}  # indexed by id
        self.companies = {}

        if os.path.exists(self.highlight_file_path):
            with open(self.highlight_file_path, 'r')as f:
                for line in f:
                    doc = json.loads(line)
                    doc_id = doc['id']
                    del doc['id']
                    self.highlights[doc_id] = self._create_highlight(
                        highlight_id=doc_id,
                        highlight=doc
                    )
                    company = self.highlights[doc_id].company
                    if company.id not in self.companies:
                        self.companies[company.id] = company
        
    def _create_highlight(self, highlight_id, highlight):
        company = highlight['company']
        del highlight['company']
        return Highlight(id=highlight_id, company=Company(**company), **highlight)

    def get_highlight(self, highlight_id: int):
        return self.highlights[highlight_id]

    def add_highlight(self, highlight):
        highlight_id = len(self.highlights)
        assert highlight_id not in self.highlights
        self.highlights[highlight_id] = self._create_highlight(highlight_id, highlight)

    def add_company_highlight(self, company_name, highlight):
        # get company
        company = [company for _, company in self.companies.items() if company.name == company_name][0]
        highlight['company'] = asdict(company)
        highlight_id = len(self.highlights)
        self.highlights[highlight_id] = self._create_highlight(highlight_id, highlight)

    def commit(self):
        with open(os.path.join(self.storage_dir, 'base/highlight.jsonl'), 'w') as f:
            for _, highlight in self.highlights.items():
                f.write(json.dumps(asdict(highlight)) + '\n')
        
    def search_highlights(self, company_name):
        return [highlight for _, highlight in self.highlights.items() if highlight.company.name == company_name]
    
