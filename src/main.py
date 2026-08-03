import os

from processing.batch_processor import process_batch
from output.excel_writer import write_excel


def main():

    input_directory = "./data/input"
    output_file = "./output/tabela.xlsx"

    os.makedirs(input_directory, exist_ok=True)
    os.makedirs("./output", exist_ok=True)

    data = process_batch(input_directory)

    write_excel(data, output_file)


if __name__ == "__main__":
    main()