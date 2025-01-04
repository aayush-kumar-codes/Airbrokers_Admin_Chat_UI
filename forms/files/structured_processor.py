from dataclasses import asdict
import datetime
import os
import json
from collections import defaultdict
from typing import List, Dict
import fitz  # PyMuPDF
from .structured_data import DocumentMetadata, Summary, Field, Rectangle

class StructuredFormProcessor:
    def __init__(self):
        self.metadata = None
        self.summary = None
        self.fields = {}
        self.checkbox_count = 0
        self.text_count = 0
        self.form_data = {
            'metadata': {},
            'fields': {},
            'page_dimensions': {}  
        }

    def process_pdf_metadata(self, pdf_path: str) -> None:
        doc = fitz.open(pdf_path)
        self.metadata = DocumentMetadata(
            timestamp=datetime.datetime.now().isoformat(),
            filename=os.path.basename(pdf_path),
            document_title=doc.metadata.get('title', os.path.basename(pdf_path)),
            number_of_pages=len(doc),
            versions={
                'pymupdf': fitz.version
            },
            summary="""This is a document used in real estate transactions to provide potential buyers with essential information about a property."""
        )
        # Store page dimensions
        page = doc[0]
        self.form_data['page_dimensions'] = {
            'width': float(page.rect.width),
            'height': float(page.rect.height)
        }
        doc.close()

    def process_form_data(self, results: List[Dict]) -> None:
        fields_by_page = defaultdict(int)
        fields_by_type = defaultdict(int)

        for page_data in results:
            page_num = page_data['page_number']

            for checkbox in page_data['checkboxes']:
                field = self._create_checkbox_field(checkbox, page_num)
                self.fields[f"checkbox_{self.checkbox_count}"] = field
                self.checkbox_count += 1
                fields_by_page[str(page_num)] += 1
                fields_by_type['checkbox'] += 1

            for line in page_data['line_results']:
                field = self._create_text_field(line, page_num)
                self.fields[f"text_{self.text_count}"] = field
                self.text_count += 1
                fields_by_page[str(page_num)] += 1
                fields_by_type['text'] += 1

        self.summary = Summary(
            total_fields=sum(fields_by_type.values()),
            fields_by_type=dict(fields_by_type),
            fields_by_page=dict(fields_by_page)
        )

    def _create_checkbox_field(self, checkbox: Dict, page: int) -> Field:
        x, y, w, h = checkbox['coordinates']
        return Field(
            question=checkbox.get('line_text', ''),
            type='checkbox',
            page=page,
            rect=Rectangle(
                x0=float(x),
                y0=float(y),
                x1=float(x + w),
                y1=float(y + h)
            ),
            possible_answers=[{'answer': 'Yes'}, {'answer': 'No'}]
        )

    def _create_text_field(self, line: Dict, page: int) -> Field:
        x, y, w, h = line['horizontal_line']
        return Field(
            question=line.get('left_text', ''),
            type='text',
            page=page,
            rect=Rectangle(
                x0=float(x),
                y0=float(y),
                x1=float(x + w),
                y1=float(y + h)
            )
        )

    def to_dict(self) -> Dict:
        return {
            'metadata': asdict(self.metadata),
            'summary': asdict(self.summary),
            'fields': {k: asdict(v) for k, v in self.fields.items()}
        }

    def save_json(self, output_path: str) -> None:
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
