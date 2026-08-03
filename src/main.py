from processing.batch_processor import process_batch


def main():

    input_directory = "./data/input"

    data = process_batch(input_directory)

    print(f"Registros extraídos: {len(data)}")


if __name__ == "__main__":
    main()