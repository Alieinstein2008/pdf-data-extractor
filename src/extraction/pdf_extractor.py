import pdfplumber

def locate_table_columns(page):
    return {
        "initial": page.search("NºFA"),
        "intermediate": page.search("Consumidor"),
        "final": page.search("Fornecedor"),
    }

def locate_metadata(page):
    return {
        "unit": page.search("Unidade:")[0],
        "date": page.search("Data:")[0],
        "issuer": page.search("Por:")[0],
        "delivery_note": page.search("Guia Nº:")[0],
        "procedure": page.search("Trâmite:")[0],
        "complement": page.search("Complemento:")[0],
    }

def validate_table_columns(columns):
    required_columns = [
        "initial",
        "intermediate",
        "final",
    ]

    return all(columns[column] for column in required_columns)

def extract_page_rows(
    page,
    first_page,
    columns,
    metadata,
    path,
    page_num,
):
    rows = []

    end_of_table_marker = page.search(r"Total de FA´s:\s\d+")

    final_table_height = (
        page.height * 0.93 if not end_of_table_marker else end_of_table_marker[0]["top"]
    )

    dynamic_table_width = page.width * 0.910

    matches = page.search(
        r"\d{2}.\d{3}.\d{3}.\d{2}-\d{7}",
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
        unit_locale_locator["bottom"] + 0.5,
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
        delivery_note_locator["top"] - 1,
        first_page.width,
        delivery_note_locator["bottom"] + 1,
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
            next_match_top - 0.1,
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
    table_data = []

    with pdfplumber.open(path) as pdf:

        first_page = pdf.pages[0]

        columns = locate_table_columns(first_page)

        if not validate_table_columns(columns):
            print("Documento invalido")
            return []

        metadata = locate_metadata(first_page)

        for page_num, page in enumerate(pdf.pages, start=1):

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