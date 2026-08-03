import glob
import os

from extraction.pdf_extractor import extract_table_data
from extraction.extraction_error import PDFExtractionError


def find_pdf_files(origin_directory):

    return glob.glob(os.path.join(origin_directory, "*.pdf"))


def process_batch(origin_directory):

    data_batch = []

    file_paths = find_pdf_files(origin_directory)

    if not file_paths:
        print(f"Nenhum arquivo PDF encontrado na pasta: " f"{origin_directory}")

        return data_batch

    for path in file_paths:

        filename = os.path.basename(path)

        print(f"Processando: {filename}...")

        try:

            table_data = extract_table_data(path)

            data_batch.extend(table_data)

            print(f"OK — " f"{len(table_data)} registros extraídos.")

        except PDFExtractionError as error:

            print(f"ERRO — {filename}: {error}")

    return data_batch
