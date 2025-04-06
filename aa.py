from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError
from PIL import Image, ImageDraw
import numpy as np
import cv2  # Import OpenCV

pdf_path = '/home/local/Airbrokers_Admin_Chat_UI/media/output/output/form-4-T-6_1_processed.pdf'

def replace_underscores_with_line(image):
    # Convert the image to grayscale for easier processing
    grayscale_image = image.convert('L')
    np_image = np.array(grayscale_image)

    # Threshold the image to create a binary image (white for characters, black for background)
    _, binary_image = cv2.threshold(np_image, 128, 255, cv2.THRESH_BINARY_INV)

    # Detect horizontal edges to find potential underscores
    edges = cv2.Canny(binary_image, 50, 150, apertureSize=3)

    # Dilate the edges to make them more visible
    dilated_edges = cv2.dilate(edges, (5, 1), iterations=2)

    # Find contours of the detected edges
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Modify the image to replace gaps with a solid line
    draw = ImageDraw.Draw(image)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Identify horizontal gaps (sequences of small underscores)
        if h < 5 and w > 50:  # Adjust this condition based on your use case
            # Draw a solid line over the sequence of underscores
            draw.line([(x, y + h), (x + w, y + h)], fill="black", width=5)

    return image

try:
    # Increase DPI for better quality and use the 'poppler_path' if necessary
    images = convert_from_path(pdf_path, dpi=300)  # Increased DPI for better quality
    for i, image in enumerate(images):
        # Call the function to replace underscores with a continuous line
        modified_image = replace_underscores_with_line(image)

        # Save the modified image
        modified_image.save(f"output_page_{i + 1}_modified.png", "PNG")

    print("Conversion and modification successful!")

except FileNotFoundError:
    print("Error: PDF file not found.")
except PDFInfoNotInstalledError:
    print("Error: pdfinfo not installed.")
except PDFPageCountError:
    print("Error: Unable to get the page count.")
except PDFSyntaxError:
    print("Error: Corrupt PDF file.")
except Exception as e:
    print(f"Unexpected error: {e}")



# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import img2pdf
# from pathlib import Path

# # Input and output paths
# pdf_path = '/home/local/Airbrokers_Admin_Chat_UI/media/output/output/form-4-T-6_1_ZMllFV1.pdf'
# output_pdf_path = '/home/local/Airbrokers_Admin_Chat_UI/media/output/output/form-4-T-6_1_processed.pdf'

# # Convert PDF to images
# images = convert_from_path(pdf_path, dpi=300)

# processed_images = []

# for img in images:
#     # Convert PIL image to OpenCV format
#     open_cv_image = np.array(img)
#     open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

#     # Convert to grayscale
#     gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

#     # Apply edge detection
#     edges = cv2.Canny(gray, 50, 150, apertureSize=3)

#     # Detect lines using Hough Line Transform
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

#     if lines is not None:
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             cv2.line(open_cv_image, (x1, y1), (x2, y2), (0, 0, 0), thickness=2)  # Replace dashed lines with solid

#     # Convert back to PIL Image
#     processed_images.append(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))

# # Save modified images as a PDF
# with open(output_pdf_path, "wb") as f:
#     f.write(img2pdf.convert([cv2.imencode(".png", img)[1].tobytes() for img in processed_images]))

# print(f"Processed PDF saved at {output_pdf_path}")
