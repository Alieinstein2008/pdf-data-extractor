import pdfplumber

from extraction.extraction_config import (
    FA_NUMBER_PATTERN,
    LAST_ROW_BOTTOM_OFFSET,
    TABLE_COLUMNS,
    TABLE_END_PATTERN,
    TABLE_HEIGHT_RATIO,
    TABLE_WIDTH_RATIO,
    METADATA_LABELS,
    DELIVERY_NOTE_TOP_OFFSET,
    DELIVERY_NOTE_BOTTOM_OFFSET,
    UNIT_BOTTOM_OFFSET,
)

from extraction.extraction_error import PDFExtractionError


def locate_table_columns(page):
    return {key: page.search(label) for key, label in TABLE_COLUMNS.items()}


def locate_metadata(page):

    metadata = {}

    for key, label in METADATA_LABELS.items():

        matches = page.search(label)

        if not matches:
            raise PDFExtractionError(f"Metadado não encontrado: {label}")

        metadata[key] = matches[0]

    return metadata


def validate_table_columns(columns):

    required_columns = [
        "initial",
        "intermediate",
        "final",
    ]

    missing_columns = [column for column in required_columns if not columns[column]]

    if missing_columns:
        raise PDFExtractionError(
            "Colunas obrigatórias não encontradas: " + ", ".join(missing_columns)
        )


def extract_page_rows(
    page,
    first_page,
    columns,
    metadata,
    path,
    page_num,
):
    rows = []

    end_of_table_marker = page.search(TABLE_END_PATTERN, regex=True)

    final_table_height = (
        page.height * TABLE_HEIGHT_RATIO
        if not end_of_table_marker
        else end_of_table_marker[0]["top"]
    )

    dynamic_table_width = page.width * TABLE_WIDTH_RATIO

    matches = page.search(
        FA_NUMBER_PATTERN,
        regex=True,
    )

    if not matches:
        return rows

    opening_match = matches[0]

    table_area = (
        opening_match["x0"],
        opening_match["top"],
        dynamic_table_width,
        final_table_height,
    )

    table = page.crop(table_area)

    number_of_matches = len(matches)

    unit_locale_locator = metadata["unit"]
    date_locator = metadata["date"]
    issuer_locator = metadata["issuer"]
    delivery_note_locator = metadata["delivery_note"]
    procedure_locator = metadata["procedure"]
    complement_locator = metadata["complement"]

    unit_locale_text_area = (
        unit_locale_locator["x1"],
        unit_locale_locator["top"],
        first_page.width,
        unit_locale_locator["bottom"] + UNIT_BOTTOM_OFFSET,
    )

    date_text_area = (
        date_locator["x1"],
        date_locator["top"],
        first_page.width,
        date_locator["bottom"],
    )

    issuer_text_area = (
        issuer_locator["x1"],
        issuer_locator["top"],
        first_page.width,
        issuer_locator["bottom"],
    )

    delivery_note_text_area = (
        delivery_note_locator["x1"],
        delivery_note_locator["top"] - DELIVERY_NOTE_TOP_OFFSET,
        first_page.width,
        delivery_note_locator["bottom"] + DELIVERY_NOTE_BOTTOM_OFFSET,
    )

    procedure_text_area = (
        procedure_locator["x1"],
        procedure_locator["top"],
        date_locator["x0"],
        procedure_locator["bottom"],
    )

    complement_text_area = (
        complement_locator["x1"],
        complement_locator["top"],
        first_page.width,
        complement_locator["bottom"],
    )

    intermediate_column = columns["intermediate"]
    final_column = columns["final"]

    for match_num, match in enumerate(matches):

        next_match_top = (
            matches[match_num + 1]["top"]
            if match_num < number_of_matches - 1
            else final_table_height
        )

        text_area_1 = (
            match["x0"],
            match["top"],
            intermediate_column[1]["x0"],
            next_match_top - LAST_ROW_BOTTOM_OFFSET,
        )

        text_area_2 = (
            intermediate_column[1]["x0"],
            match["top"],
            final_column[0]["x0"],
            next_match_top,
        )

        text_area_3 = (
            final_column[0]["x0"],
            match["top"],
            dynamic_table_width,
            next_match_top,
        )

        rows.append(
            {
                "Nº FA": table.within_bbox(text_area_1).extract_text(),
                "Consumidor": table.within_bbox(text_area_2).extract_text(),
                "Fornecedor": table.within_bbox(text_area_3).extract_text(),
                "Guia Nº": first_page.within_bbox(
                    delivery_note_text_area
                ).extract_text(),
                "Trâmite": first_page.within_bbox(procedure_text_area).extract_text(),
                "Complemento": first_page.within_bbox(
                    complement_text_area
                ).extract_text(),
                "Unidade": first_page.within_bbox(unit_locale_text_area).extract_text(),
                "Data": first_page.within_bbox(date_text_area).extract_text(),
                "Impresso Por": first_page.within_bbox(issuer_text_area).extract_text(),
                "Caminho": path,
                "Pagina": page_num,
                "Linha": match_num,
            }
        )

    return rows


def extract_table_data(path):

    try:

        with pdfplumber.open(path) as pdf:

            if not pdf.pages:
                raise PDFExtractionError("Documento não possui páginas.")

            first_page = pdf.pages[0]

            columns = locate_table_columns(first_page)

            validate_table_columns(columns)

            metadata = locate_metadata(first_page)

            table_data = []

            for page_num, page in enumerate(
                pdf.pages,
                start=1,
            ):

                rows = extract_page_rows(
                    page=page,
                    first_page=first_page,
                    columns=columns,
                    metadata=metadata,
                    path=path,
                    page_num=page_num,
                )

                table_data.extend(rows)

            return table_data

    except PDFExtractionError:
        raise

    except Exception as error:
        raise PDFExtractionError(f"Falha ao processar o PDF: {error}") from error
