import re
from typing import List, Optional

import bs4
import langdetect


class TextAnalyzer:
    def __init__(self, keywords: Optional[List[str]] = None, lang: Optional[str] = None, remove_html: bool = False):
        self.keywords_re = None
        if keywords is not None:
            self.keywords_re = re.compile(r"({})".format('|'.join(keywords)), flags=re.IGNORECASE)
        self.lang = lang
        self.remove_html = remove_html

    def preprocess(self, text: str) -> str:
        if self.remove_html:
            return bs4.BeautifulSoup(text, 'html.parser').get_text(' ', strip=True)
        return text

    def detect_keywords(self, text: str) -> List[str]:
        return self.keywords_re.findall(self.preprocess(text))

    def detect_lang(self, text: str) -> str:
        return langdetect.detect(self.preprocess(text))

    def contains_lang(self, text: str) -> bool:
        return self.lang is None or self.detect_lang(text) == self.lang

    def contains_keywords(self, text: str) -> bool:
        return self.keywords_re is None or len(self.detect_keywords(text)) > 0
