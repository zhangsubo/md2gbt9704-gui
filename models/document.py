from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Paragraph:
    text: str
    paragraph_type: str
    font_name: Optional[str] = None
    font_size: Optional[int] = None
    is_bold: bool = False
    alignment: str = 'left'

@dataclass
class Table:
    rows: List[List[str]]
    has_header: bool = True

@dataclass
class DocumentModel:
    title: str
    paragraphs: List[Paragraph]
    tables: List[Table]
    file_path: Optional[str] = None
