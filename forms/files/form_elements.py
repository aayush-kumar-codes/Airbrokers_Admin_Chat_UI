import cv2
import numpy as np
from typing import List, Dict

from .config import Config


class FormElementDetector:
    @staticmethod
    def _is_dashed_line(binary_image, x: int, y: int, width: int) -> bool:
        """Check if the line is dashed by analyzing pixel distribution."""
        line_region = binary_image[y:y+3, x:x+width]

        # Check for gaps in the line
        horizontal_profile = np.sum(line_region, axis=0)
        horizontal_profile = (horizontal_profile > 0).astype(np.int32)

        # Count transitions between 0 and 1
        transitions = np.abs(np.diff(horizontal_profile))
        transition_count = np.sum(transitions)

        # If there are multiple transitions, it's likely a dashed line
        return transition_count > 4  # Adjust this threshold based on your needs

    @staticmethod
    def _is_underline(binary_image, x: int, y: int, width: int) -> bool:
        """Check if the line is likely an underline by looking for text above it."""
        params = Config.LINE_PARAMS

        # Check the region above the line for text
        text_region = binary_image[
            max(0, y - params['TEXT_CHECK_HEIGHT']):y,
            x:x+width
        ]

        if text_region.size == 0:
            return False

        # Calculate text density in the region
        text_density = np.sum(text_region > 0) / text_region.size

        # If there's significant text above the line, it's likely an underline
        return text_density > 0.05  # Adjust threshold based on your needs

    @staticmethod
    def _is_solid_line(binary_image, x: int, y: int, width: int) -> bool:
        """Verify if the line is solid (not dashed or dotted)."""
        params = Config.LINE_PARAMS
        line_region = binary_image[y:y+3, x:x+width]

        # Calculate horizontal density profile
        horizontal_profile = np.sum(line_region, axis=0) > 0

        # Count continuous segments
        gaps = np.where(horizontal_profile == 0)[0]
        if len(gaps) == 0:
            return True

        # Check gap sizes
        gap_sizes = np.diff(gaps)
        max_gap = np.max(gap_sizes) if len(gap_sizes) > 0 else 0

        # Calculate density
        density = np.sum(horizontal_profile) / width

        return (max_gap <= params['MAX_GAP_SIZE'] and
                density >= params['MIN_DENSITY'])

    @staticmethod
    def detect_horizontal_lines(image):
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # # Apply Gaussian blur to reduce noise
        # gray = cv2.GaussianBlur(gray,
        #                        Config.PREPROCESSING_PARAMS['GAUSSIAN_BLUR_KERNEL'],
        #                        Config.PREPROCESSING_PARAMS['GAUSSIAN_BLUR_SIGMA'])

        # Create binary image
        _, binary = cv2.threshold(gray,
                                Config.LINE_PARAMS['THRESHOLD_VALUE'],
                                255,
                                cv2.THRESH_BINARY_INV)

        # Create horizontal kernel
        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (Config.LINE_PARAMS['KERNEL_LENGTH'], 1)
        )

        detect_horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)

        contours, _ = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        horizontal_lines = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if (Config.LINE_PARAMS['MIN_WIDTH'] <= w <= Config.LINE_PARAMS['MAX_WIDTH'] and
                Config.LINE_PARAMS['MIN_LINE_THICKNESS'] <= h <= Config.LINE_PARAMS['MAX_LINE_THICKNESS']):

                # Skip if it's a dashed line
                if FormElementDetector._is_dashed_line(binary, x, y, w):
                    continue

                # Skip if it's an underline
                if FormElementDetector._is_underline(binary, x, y, w):
                    continue

                # Skip if it's not a solid line
                if not FormElementDetector._is_solid_line(binary, x, y, w):
                    continue

                new_y = y - (Config.LINE_PARAMS['EXTENDED_HEIGHT'] - h)
                horizontal_lines.append((x, new_y, w, Config.LINE_PARAMS['EXTENDED_HEIGHT']))

        return horizontal_lines

    @staticmethod
    def _is_checkbox_empty(image, x: int, y: int, w: int, h: int) -> bool:
        """Check if a checkbox is empty using the configured threshold."""
        checkbox_region = image[y:y+h, x:x+w]

        # Use configured threshold value
        _, binary = cv2.threshold(checkbox_region,
                                Config.CHECKBOX_PARAMS['THRESHOLD_VALUE'],
                                255,
                                cv2.THRESH_BINARY_INV)

        total_pixels = w * h
        filled_pixels = np.count_nonzero(binary)
        fill_percentage = (filled_pixels / total_pixels) * 100

        return fill_percentage < Config.CHECKBOX_PARAMS['FILL_THRESHOLD']

    @staticmethod
    def _is_valid_checkbox(x, y, w, h, area, aspect_ratio, solidity, contour, existing_checkboxes):
        """Enhanced checkbox validation using additional parameters."""
        params = Config.CHECKBOX_PARAMS

        # Basic size and shape checks
        if not (params['MIN_AREA'] <= area <= params['MAX_AREA']):
            return False
        if not (params['MIN_ASPECT_RATIO'] <= aspect_ratio <= params['MAX_ASPECT_RATIO']):
            return False
        if not (solidity > params['MIN_SOLIDITY']):
            return False
        if not (w >= params['MIN_DIMENSION'] and h >= params['MIN_DIMENSION']):
            return False

        # Check contour complexity
        if not (params['MIN_CONTOUR_POINTS'] <= len(contour) <= params['MAX_CONTOUR_POINTS']):
            return False

        # Check perimeter
        perimeter = cv2.arcLength(contour, True)
        if not (params['MIN_PERIMETER'] <= perimeter <= params['MAX_PERIMETER']):
            return False

        # Check for approximate rectangle shape
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        if len(approx) != 4:  # Should have 4 corners
            return False

        # Verify corners are roughly 90 degrees
        for i in range(4):
            pt1 = approx[i][0]
            pt2 = approx[(i+1)%4][0]
            pt3 = approx[(i+2)%4][0]

            # Calculate angle
            v1 = pt1 - pt2
            v2 = pt3 - pt2
            angle = abs(np.degrees(np.arctan2(np.cross(v1, v2), np.dot(v1, v2))))

            if abs(angle - 90) > params['CORNER_ANGLE_TOLERANCE']:
                return False

        # Check for duplicates
        for existing in existing_checkboxes:
            ex_x, ex_y, _, _ = existing['coordinates']
            if abs(x - ex_x) < params['DUPLICATE_THRESHOLD'] and abs(y - ex_y) < params['DUPLICATE_THRESHOLD']:
                return False

        return True

    @staticmethod
    def detect_checkboxes(image):
        """Enhanced checkbox detection with preprocessing."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # # Apply Gaussian blur
        # gray = cv2.GaussianBlur(gray,
        #                        Config.PREPROCESSING_PARAMS['GAUSSIAN_BLUR_KERNEL'],
        #                        Config.PREPROCESSING_PARAMS['GAUSSIAN_BLUR_SIGMA'])

        # Apply adaptive threshold
        binary = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            Config.PREPROCESSING_PARAMS['ADAPTIVE_BLOCK_SIZE'],
            Config.PREPROCESSING_PARAMS['ADAPTIVE_C']
        )

        # Remove noise
        kernel = np.ones(Config.CHECKBOX_PARAMS['NOISE_REMOVAL_KERNEL'], np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        empty_checkboxes = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            aspect_ratio = float(w) / h

            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            solidity = float(area) / hull_area if hull_area > 0 else 0

            if FormElementDetector._is_valid_checkbox(x, y, w, h, area, aspect_ratio, solidity, contour, empty_checkboxes):
                if FormElementDetector._is_checkbox_empty(gray, x, y, w, h):
                    checkbox_info = {
                        'coordinates': (x, y, w, h),
                        'area': area,
                        'aspect_ratio': aspect_ratio,
                        'y_position': y
                    }
                    empty_checkboxes.append(checkbox_info)

        empty_checkboxes.sort(key=lambda x: x['y_position'])
        return empty_checkboxes