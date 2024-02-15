import os
import re
from PyPDF2 import PdfMerger
from PIL import Image

def get_unique_number(pdf_name):
    unique_number_match = re.search(r'\d{9}', pdf_name)
    return unique_number_match.group() if unique_number_match else None

def convert_tif_to_pdf(tif_path, pdf_path):
    image = Image.open(tif_path)
    pdf_path_with_extension = pdf_path if pdf_path.lower().endswith('.pdf') else pdf_path + '.pdf'
    image.save(pdf_path_with_extension, 'PDF')
    return pdf_path_with_extension

def extract_document_type(file_name, document_type_order):
    for doc_type in document_type_order:
        if doc_type.lower() in file_name.lower():
            return doc_type
    return None

def merge_pdfs(input_folder, output_folder):
    document_type_order = [
        "Account File",
        "Contract_Note_Acct Agr",
        "Truth in Lending",
        "Bill Statement - CHARGE OFF",
        "Bill Statement",
        "Pay History"
    ]

    pdf_dict = {}
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.pdf', '.tif', '.tiff')):
                unique_number = get_unique_number(file)
                if unique_number:
                    document_type = extract_document_type(file, document_type_order)
                    file_path = os.path.join(root, file)

                    if file.lower().endswith(('.tif', '.tiff')):
                        pdf_path = convert_tif_to_pdf(file_path, file_path.replace('.tif', '_converted.pdf').replace('.tiff', '_converted.pdf'))
                        pdf_dict.setdefault(unique_number, []).append((document_type, pdf_path))
                    else:
                        pdf_dict.setdefault(unique_number, []).append((document_type, file_path))

    for unique_number, document_list in pdf_dict.items():
        document_list.sort(key=lambda x: document_type_order.index(x[0]) if x[0] in document_type_order else float('inf'))

        merged_pdf = PdfMerger()

        for _, document_path in document_list:
            merged_pdf.append(document_path)

        output_filename = os.path.join(output_folder, f"{unique_number}.pdf")

        if merged_pdf.pages:
            merged_pdf.write(output_filename)
            merged_pdf.close()
            print(f"PDF {output_filename} merged successfully.")
        else:
            print(f"No pages found for {unique_number}.pdf. Skipping.")

if __name__ == "__main__":
    input_folder = r"P:\Users\Justin\output_test\merge-o"
    output_folder = r"P:\Users\Justin\output_test\merge-o\merge-o_test"

    merge_pdfs(input_folder, output_folder)
    print("PDFs merged successfully.")
