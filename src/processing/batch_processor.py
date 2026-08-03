import glob
import os

from extraction.pdf_extractor import extract_table_data


def find_pdf_files(origin_directory):

    return glob.glob(os.path.join(origin_directory, "*.pdf"))


def process_batch(origin_directory):

    data_batch = []

    file_paths = find_pdf_files(origin_directory)

    if not file_paths:
        print(f"Nenhum arquivo PDF encontrado na pasta: " f"{origin_directory}")

        return data_batch

    for path in file_paths:

        print(f"Processando: " f"{os.path.basename(path)}...")

        table_data = extract_table_data(path)

        data_batch.extend(table_data)

    return data_batch
