import re
from typing import List, Optional


class TextAnalyzer:
    def __init__(self, keywords: Optional[List[str]] = None):
        self.keywords_re = None
        if keywords is not None:
            self.keywords_re = re.compile(r"({})".format('|'.join(keywords)), flags=re.IGNORECASE)

    def detect_keywords(self, text: str) -> List[str]:
        return self.keywords_re.findall(text)

    def contains_keywords(self, text: str) -> bool:
        return self.keywords_re is None or len(self.detect_keywords(text)) > 0
