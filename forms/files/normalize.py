import json
import fitz  # PyMuPDF
from PIL import Image

def get_image_dimensions(image_path):
    """Get width and height of the image."""
    with Image.open(image_path) as img:
        return img.size[0], img.size[1]

def normalize_rect(image_width, image_height, pdf_path, page_num, rect):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pdf_width, pdf_height = page.rect.width, page.rect.height
    width_factor = pdf_width / image_width
    height_factor = pdf_height / image_height
    normalized_rect = {
        "x0": rect["x0"] * width_factor,
        "y0": rect["y0"] * height_factor,
        "x1": rect["x1"] * width_factor,
        "y1": rect["y1"] * height_factor
    }
    return normalized_rect

def normalize_form_data(image_path, pdf_path, form_data):
    """Normalize form data using actual image dimensions."""
    image_width, image_height = get_image_dimensions(image_path)
    for field_key, field_value in form_data["fields"].items():
        page_num = field_value["page"] - 1
        rect = field_value["rect"]
        field_value["rect"] = normalize_rect(image_width, image_height, pdf_path, page_num, rect)
    return form_data

def main():
    with open('output/form_data.json', 'r') as f:
        form_data = json.load(f)

    pdf_path = form_data["metadata"]["filename"]
    image_path = form_data["metadata"]["image_path"]  # Assuming image path is stored in metadata
    
    normalized_form_data = normalize_form_data(image_path, pdf_path, form_data)

    with open('output/normalized_form_data.json', 'w') as f:
        json.dump(normalized_form_data, f, indent=2)

    print("Normalization complete. Data saved to 'normalized_form_data.json'.")

if __name__ == "__main__":
    main()
