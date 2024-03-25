import re
import json


class TextParserMixin:
    def parse_json(self, generated_text: str) -> dict:
        pattern = rf'```json\n(.*?)\n```'
        matches = re.findall(pattern, generated_text, re.DOTALL)
        return json.loads(matches[0])