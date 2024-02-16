import os
import re
import fitz
from PIL import Image
from reportlab.pdfgen import canvas

class PDFMerger:
    def get_unique_number(self, pdf_name):
        unique_number_match = re.search(r'\d{9}', pdf_name)
        return unique_number_match.group() if unique_number_match else None

    def convert_image_to_pdf(self, image_path, pdf_path):
        img = Image.open(image_path)
        pdf_path_with_extension = pdf_path if pdf_path.lower().endswith('.pdf') else pdf_path + '.pdf'
        c = canvas.Canvas(pdf_path_with_extension, pagesize=img.size)
        c.drawImage(image_path, 0, 0, width=img.size[0], height=img.size[1])
        c.save()
        return pdf_path_with_extension

    def convert_tif_to_pdf(self, tif_path, pdf_path):
        image = Image.open(tif_path)
        pdf_path_with_extension = pdf_path if pdf_path.lower().endswith('.pdf') else pdf_path + '.pdf'
        image.save(pdf_path_with_extension, 'PDF', resolution=100.0)
        return pdf_path_with_extension

    def extract_document_type(self, file_name, document_type_order):
        for doc_type in document_type_order:
            if doc_type.lower() in file_name.lower():
                return doc_type
        return None

    def is_skipped_file(self, file_name):
        skipped_extensions = ['.eml', '.htm', '.xlsx']
        return any(file_name.lower().endswith(ext) for ext in skipped_extensions)

    def merge_pdfs(self, input_folder, output_folder):
        document_type_order = [
            "Account File",
            "Contract_Note_Acct Agr",
            "Truth in Lending",
            "Bill Statement - CHARGE OFF",
            "Bill Statement",
            "Pay History"
        ]

        pdf_dict = {}

        for root, _, files in os.walk(input_folder):
            for file in files:
                if self.is_skipped_file(file):
                    continue  # Skip files with specific extensions

                if file.lower().endswith(('.pdf', '.tif', '.tiff', '.jpg', '.jpeg')):
                    unique_number = self.get_unique_number(file)
                    if unique_number:
                        document_type = self.extract_document_type(file, document_type_order)
                        file_path = os.path.join(root, file)

                        if file.lower().endswith(('.tif', '.tiff')):
                            pdf_path = self.convert_tif_to_pdf(file_path, file_path.replace('.tif', '_converted.pdf').replace('.tiff', '_converted.pdf'))
                            pdf_dict.setdefault(unique_number, []).append((document_type, pdf_path))
                        elif file.lower().endswith(('.jpg', '.jpeg')):
                            pdf_path = self.convert_image_to_pdf(file_path, file_path.replace('.jpg', '_converted.pdf').replace('.jpeg', '_converted.pdf'))
                            pdf_dict.setdefault(unique_number, []).append((document_type, pdf_path))
                        else:
                            pdf_dict.setdefault(unique_number, []).append((document_type, file_path))

        for unique_number, document_list in pdf_dict.items():
            document_list.sort(key=lambda x: document_type_order.index(x[0]) if x[0] in document_type_order else float('inf'))

            merged_pdf = fitz.open()

            for _, document_path in document_list:
                pdf_document = fitz.open(document_path)
                merged_pdf.insert_pdf(pdf_document)

            output_filename = os.path.join(output_folder, f"{unique_number}.pdf")

            if merged_pdf.page_count > 0:
                merged_pdf.save(output_filename)
                merged_pdf.close()
                print(f"PDF {output_filename} merged successfully.")
            else:
                print(f"No pages found for {unique_number}.pdf. Skipping.")

if __name__ == "__main__":
    input_folder = r"P:\Departments\Pre-Jmt\Evan PreJMT\Documents\RSG\Docs Extracted\2024\02\Docs\ONB"
    output_folder = r"P:\Departments\Staging\RSG\02.15.24\New folder"

    pdf_merger = PDFMerger()
    pdf_merger.merge_pdfs(input_folder, output_folder)
    print("PDFs merged successfully.")
