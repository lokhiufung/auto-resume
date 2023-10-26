import json


class TextParserMixin:
    def parse_json(self, generated_text: str) -> dict:
        return json.loads(generated_text)