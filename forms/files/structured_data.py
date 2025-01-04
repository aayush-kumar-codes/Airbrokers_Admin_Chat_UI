from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Rectangle:
    x0: float
    y0: float
    x1: float
    y1: float

@dataclass
class Field:
    question: str
    type: str
    page: int
    rect: Rectangle
    value: Optional[List[str]] = None
    possible_answers: Optional[List[Dict]] = None

@dataclass
class DocumentMetadata:
    timestamp: str
    filename: str
    document_title: str
    number_of_pages: int
    versions: Dict
    summary: str

@dataclass
class Summary:
    total_fields: int
    fields_by_type: Dict[str, int]
    fields_by_page: Dict[str, int]
