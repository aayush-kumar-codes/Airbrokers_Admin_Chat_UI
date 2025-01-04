import json
import fitz  # PyMuPDF
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import black

def get_image_files_from_folder(folder_path):
    # Get all image files from the folder and sort them numerically
    image_extensions = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp')
    image_files = [f for f in os.listdir(folder_path)
                   if f.lower().endswith(image_extensions)]

    # Sort files numerically (assuming names contain numbers)
    image_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

    # Return full paths
    return [os.path.join(folder_path, f) for f in image_files]

def create_acroform_from_images(image_files, form_data_file, output_pdf, page_dimensions=None):
    # Load form data
    with open(form_data_file, 'r') as f:
        form_data = json.load(f)

    # Get page dimensions
    pdf_width = page_dimensions['width'] if page_dimensions else 612  # default letter width
    pdf_height = page_dimensions['height'] if page_dimensions else 792  # default letter height
    
    # Create PDF with dynamic page size
    pagesize = (pdf_width, pdf_height)
    c = canvas.Canvas(output_pdf, pagesize=pagesize)

    # Update scaling factors
    scale_x = pagesize[0] / pdf_width
    scale_y = pagesize[1] / pdf_height

    # Process each page
    for page_num, image_file in enumerate(image_files, 1):
        try:
            print(f"Processing page {page_num} - {image_file}")

            # Add image as background
            c.drawImage(image_file, 0, 0, width=pagesize[0], height=pagesize[1])

            # Add form fields for current page
            for field_name, field_info in form_data['fields'].items():
                if field_info['page'] == page_num:
                    # Extract coordinates
                    x0 = field_info['rect']['x0']
                    y0 = field_info['rect']['y0']
                    x1 = field_info['rect']['x1']
                    y1 = field_info['rect']['y1']

                    # Scale coordinates from original PDF to letter size
                    scaled_x0 = x0 * scale_x
                    scaled_y0 = y0 * scale_y
                    scaled_x1 = x1 * scale_x
                    scaled_y1 = y1 * scale_y

                    width = scaled_x1 - scaled_x0
                    height = scaled_y1 - scaled_y0

                    # Get tooltip text from question
                    tooltip = field_info.get('question', '')

                    # Create form field based on type
                    if field_info['type'] == 'checkbox':
                        c.acroForm.checkbox(
                            name=field_name,
                            x=scaled_x0,
                            y=pagesize[1] - scaled_y1,  # Flip Y coordinate
                            buttonStyle='check',
                            size=min(width, height),
                            borderWidth=0,  # No border
                            tooltip=tooltip  # Add tooltip
                        )
                    elif field_info['type'] == 'text':
                        c.acroForm.textfield(
                            name=field_name,
                            x=scaled_x0,
                            y=pagesize[1] - scaled_y1,  # Flip Y coordinate
                            width=width,
                            height=height,
                            fontSize=10,
                            borderWidth=0,  # No border
                            textColor=black,
                            tooltip=tooltip  # Add tooltip
                        )

            c.showPage()

        except Exception as e:
            print(f"Error processing page {page_num} - {image_file}: {str(e)}")
            continue

    try:
        c.save()
        print(f"PDF form saved as: {output_pdf}")
    except Exception as e:
        print(f"Error saving PDF: {str(e)}")

def main():
    # Path configurations
    output_folder = "output"  # Your folder containing the images
    form_data_file = 'output/normalized_form_data.json'
    output_pdf = 'output/final_form.pdf'

    # Get image files from output folder
    image_files = get_image_files_from_folder(output_folder)

    if not image_files:
        print("No image files found in the output folder!")
        return

    print(f"Found {len(image_files)} images in the output folder")
    print("Processing images:", *image_files, sep='\n')

    create_acroform_from_images(image_files, form_data_file, output_pdf)

if __name__ == "__main__":
    main()
