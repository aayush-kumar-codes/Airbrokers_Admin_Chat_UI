# # import PyPDF2
# # import yaml

# # # Load your PDF file

# # pdf = PyPDF2.PdfReader(pdf_path)

# # # Extract form fields

# # acro_fields = pdf.get_fields()

# # print(acro_fields)

# # # Compile all detected fields into a dictionary
# # fields_data = {name: {'question': value} for name, value in acro_fields.items()}


# # print(fields_data)
# # # Output to a YAML file
# # with open('output.yaml', 'w') as file:
# #     yaml.dump(fields_data, file, default_flow_style=False)


# import fitz  # PyMuPDF

# input_pdf = '/home/local/Airbrokers_Admin_Chat_UI/form-4-T-6.pdf'

# def replace_underscores_in_pdf(input_pdf, output_pdf):
#     doc = fitz.open(input_pdf)
    
#     for page_num, page in enumerate(doc):
#         text = page.get_text("text")
#         print(f"Original Text (Page {page_num + 1}):")
#         print(text)
        
#         # Search for the pattern of underscores
#         underscored_positions = page.search_for("_ _ _ _ _ _")  # Adjust for your underscore pattern

#         # Print bounding box coordinates
#         for rect in underscored_positions:
#             print(f"Underscore Field Found at: {rect}")

#         # Replace the underscores in the text and keep their positions
#         modified_text = text.replace("_ _ _ _ _ _", "______________")  # Adjust for different underscore patterns
#         if text != modified_text:
#             page.clean_contents()  # Clear old content
#             page.insert_text((50, 50), modified_text)  # Insert modified text at (x, y)

#     doc.save(output_pdf)
#     print(f"Processed PDF saved as: {output_pdf}")

# # Usage
# replace_underscores_in_pdf(input_pdf, "output.pdf")




import cv2
import numpy as np
from pdf2image import convert_from_path

# Convert PDF to Image
pages = convert_from_path('/home/local/Airbrokers_Admin_Chat_UI/form-4-T-6.pdf', 300)
image = np.array(pages[0])  # Assuming we work with the first page

# Convert to grayscale and then to binary
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Detect horizontal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
detected_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

# Dilate the lines to fill gaps
dilated_lines = cv2.dilate(detected_lines, horizontal_kernel, iterations=1)

# Optionally combine with the original image to see the result
result = cv2.bitwise_or(image, image, mask=dilated_lines)

cv2.imwrite('filled_lines_output.png', result)
