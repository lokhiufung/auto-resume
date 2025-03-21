import re
import json


class TextParserMixin:
    def parse_json(self, generated_text: str) -> dict:
        pattern = rf'```json\n(.*?)\n```'
        matches = re.findall(pattern, generated_text, re.DOTALL)
        if matches:
            return json.loads(matches[0])
        return json.loads(generated_text)