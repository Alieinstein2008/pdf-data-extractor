TABLE_WIDTH_RATIO = 0.910
TABLE_HEIGHT_RATIO = 0.93

LAST_ROW_BOTTOM_OFFSET = 0.1
DELIVERY_NOTE_TOP_OFFSET = 1.0
DELIVERY_NOTE_BOTTOM_OFFSET = 1.0
UNIT_BOTTOM_OFFSET = 0.5

FA_NUMBER_PATTERN = r"\d{2}\.\d{3}\.\d{3}\.\d{2}-\d{7}"

TABLE_END_PATTERN = r"Total de FA´s:\s\d+"

TABLE_COLUMNS = {
    "initial": "NºFA",
    "intermediate": "Consumidor",
    "final": "Fornecedor",
}

METADATA_LABELS = {
    "unit": "Unidade:",
    "date": "Data:",
    "issuer": "Por:",
    "delivery_note": "Guia Nº:",
    "procedure": "Trâmite:",
    "complement": "Complemento:",
}
