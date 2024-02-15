import os
import re
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through the input folder and its subfolders
    for root, dirs, files in os.walk(input_folder):
        for pdf_name in files:
            # Use regex to extract the first 9 digits from the PDF name
            match = re.match(r'\d{9}', pdf_name)
            
            if match:
                unique_number = match.group()
                input_pdf_path = os.path.join(root, pdf_name)

                # Merge PDFs with the same unique number
                merge_pdfs_with_same_number(input_folder, unique_number, output_folder)

def merge_pdfs_with_same_number(input_folder, unique_number, output_folder):
    pdf_writer = PdfWriter()

    # Iterate through the input folder and its subfolders again
    for root, dirs, files in os.walk(input_folder):
        for pdf_name in files:
            # Use regex to extract the first 9 digits from the PDF name
            match = re.match(r'\d{9}', pdf_name)
            
            if match and match.group() == unique_number:
                input_pdf_path = os.path.join(root, pdf_name)
                with open(input_pdf_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])

    # Write the merged PDF to the output folder
    output_pdf_path = os.path.join(output_folder, f"{unique_number}.pdf")
    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

if __name__ == "__main__":
    input_folder = r"P:\Users\Justin\output_test\merge-o"
    output_folder = r"P:\Users\Justin\output_test\merge-o\merge-o_test"

    merge_pdfs(input_folder, output_folder)
    print("PDFs successfully merged.")
