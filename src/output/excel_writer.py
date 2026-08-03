import pandas as pd


REQUIRED_COLUMNS = [
    "Nº FA",
    "Consumidor",
    "Fornecedor",
    "Guia Nº",
    "Trâmite",
    "Complemento",
    "Unidade",
    "Data",
    "Impresso Por",
    "Caminho",
    "Pagina",
    "Linha",
]


def write_excel(data, output_file):

    if not data:
        print("Nenhum dado válido foi extraído dos PDFs.")
        return

    data_frame = pd.DataFrame(data)

    for column in REQUIRED_COLUMNS:
        if column not in data_frame.columns:
            data_frame[column] = None

    columns = REQUIRED_COLUMNS + [
        column
        for column in data_frame.columns
        if column not in REQUIRED_COLUMNS
    ]

    data_frame = data_frame[columns]

    data_frame.to_excel(
        output_file,
        index=False,
        engine="openpyxl",
    )

    print(
        f"Sucesso! Planilha gerada em: {output_file}"
    )