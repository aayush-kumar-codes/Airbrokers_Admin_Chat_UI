import os
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from  .form_elements import FormElementDetector
from .config import Config

class FormProcessor:
    def __init__(self, output_folder=Config.DEFAULT_OUTPUT_FOLDER):
        self.output_folder = output_folder
        self.detector = FormElementDetector()

    def process_pdf(self, pdf_path):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        images = convert_from_path(pdf_path)
        results = []

        for i, image in enumerate(images):
            image_path = os.path.join(self.output_folder, f"page_{i + 1}.png")
            image.save(image_path, "PNG")
            
            # Convert PIL Image to OpenCV format for visualization
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            # debug_image = opencv_image.copy()
            # debug_dir = os.path.join(self.output_folder, "debug")
            # if not os.path.exists(debug_dir):
            #     os.makedirs(debug_dir)
            # debug_image_path = os.path.join(debug_dir, f"page_{i + 1}_debug.png")
            # cv2.imwrite(debug_image_path, debug_image)
            
            print(f"\nProcessing page {i + 1}...")
            try:
                # Detect form elements
                checkboxes = self.detector.detect_checkboxes(opencv_image)
                horizontal_lines = self.detector.detect_horizontal_lines(opencv_image)

                ocr_data = pytesseract.image_to_data(opencv_image, output_type=pytesseract.Output.DICT)
                text_boxes = self._create_text_boxes(ocr_data)

                processed_checkboxes = self._process_checkboxes(checkboxes, text_boxes)
                line_results = self._process_horizontal_lines(horizontal_lines, text_boxes)

                results.append({
                    'page_number': i + 1,
                    'checkboxes': processed_checkboxes,
                    'line_results': line_results
                })

            except Exception as e:
                print(f"Error processing page {i + 1}: {e}")

        return results

    def _create_text_boxes(self, ocr_data):
        return [
            {
                'text': ocr_data['text'][i],
                'x': ocr_data['left'][i],
                'y': ocr_data['top'][i],
                'width': ocr_data['width'][i],
                'height': ocr_data['height'][i]
            }
            for i in range(len(ocr_data['text']))
            if ocr_data['text'][i].strip()
        ]

    def _process_checkboxes(self, checkboxes, text_boxes):
        processed_checkboxes = []
        for checkbox in checkboxes:
            x, y, w, h = checkbox['coordinates']
            checkbox_center_y = y + h / 2

            # Create checkbox info with default empty text first
            checkbox_info = {
                'coordinates': (x, y, w, h),
                'line_text': '',  # Default empty text
                'has_text': False,
                'position': {'x': x, 'y': y},
                'area': checkbox.get('area', 0),
                'aspect_ratio': checkbox.get('aspect_ratio', 0)
            }

            # Find associated text boxes
            line_text_boxes = [
                box for box in text_boxes
                if box['y'] <= checkbox_center_y <= (box['y'] + box['height'])
            ]

            # Update with text if found
            if line_text_boxes:
                line_text_boxes.sort(key=lambda b: b['x'])
                checkbox_info.update({
                    'line_text': ' '.join([box['text'] for box in line_text_boxes]),
                    'has_text': True
                })
            
            processed_checkboxes.append(checkbox_info)
            print(f"Found checkbox at ({x},{y}), text: {checkbox_info['line_text']}")

        return processed_checkboxes

    def _process_horizontal_lines(self, horizontal_lines, text_boxes):
        line_results = []
        for x, y, w, h in horizontal_lines:
            horizontal_center_y = y + h / 2

            left_text_boxes = [
                box for box in text_boxes
                if (box['y'] <= horizontal_center_y <= (box['y'] + box['height']) and
                    box['x'] + box['width'] <= x)
            ]

            # Save line regardless of text presence
            line_info = {
                'horizontal_line': (x, y, w, h),
                'left_text': '',  # Default empty text
                'has_text': False,
                'position': {'x': x, 'y': y}
            }

            if left_text_boxes:
                left_text_boxes.sort(key=lambda b: b['x'])
                line_info.update({
                    'left_text': ' '.join([box['text'] for box in left_text_boxes]),
                    'has_text': True
                })
            
            line_results.append(line_info)
            print(f"Found line at ({x},{y}), text: {line_info['left_text']}")

        return line_results
