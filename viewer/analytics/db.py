import sqlite3
from typing import Union, List, Optional
from pathlib import Path

from .text import TextAnalyzer


class JobsDB:
    def __init__(self, path: Union[Path, str], text_analyzer: Optional[TextAnalyzer] = None):
        self.c = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        if text_analyzer:
            self.c.create_function('CONTAINS_LANG', 1, text_analyzer.contains_lang)
            self.c.create_function('CONTAINS_KEYWORDS', 1, text_analyzer.contains_keywords)

