import pdfplumber

def extract_table_data(path):

    table_data = []

    with pdfplumber.open(path) as pdf:

        first_page = pdf.pages[0]

        initial_column = first_page.search("NºFA")
        intermediate_column = first_page.search("Consumidor")
        final_column = first_page.search("Fornecedor")

        unit_locale_locator = first_page.search("Unidade:")[0]
        date_locator = first_page.search("Data:")[0]
        issuer_locator = first_page.search("Por:")[0]
        delivery_note_locator = first_page.search("Guia Nº:")[0]
        procedure_locator = first_page.search("Trâmite:")[0]
        complement_locator = first_page.search("Complemento:")[0]

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

        if (
            len(initial_column) == 0
            and len(intermediate_column) == 0
            and len(final_column) == 0
        ):
            print("Documento invalido")

        else:

            for page_num, page in enumerate(pdf.pages, start=1):

                end_of_table_marker = page.search(r"Total de FA´s:\s\d+")

                final_table_height = (
                    page.height * 0.93
                    if (len(end_of_table_marker) == 0)
                    else end_of_table_marker[0]["top"]
                )

                dynamic_table_width = page.width * 0.910

                matches = page.search(r"\d{2}.\d{3}.\d{3}.\d{2}-\d{7}", regex=True)

                number_of_matches = len(matches)

                opening_match = matches[0]

                table_area = (
                    opening_match["x0"],
                    opening_match["top"],
                    dynamic_table_width,
                    final_table_height,
                )

                table = page.crop(table_area)

                for match_num, match in enumerate(matches, start=0):

                    text_area_1 = (
                        match["x0"],
                        match["top"],
                        intermediate_column[1]["x0"],
                        (
                            matches[match_num + 1]["top"]
                            if (match_num < number_of_matches - 1)
                            else final_table_height - 0.1
                        ),
                    )

                    text_area_2 = (
                        intermediate_column[1]["x0"],
                        match["top"],
                        final_column[0]["x0"],
                        (
                            matches[match_num + 1]["top"]
                            if (match_num < number_of_matches - 1)
                            else final_table_height
                        ),
                    )

                    text_area_3 = (
                        final_column[0]["x0"],
                        match["top"],
                        dynamic_table_width,
                        (
                            matches[match_num + 1]["top"]
                            if (match_num < number_of_matches - 1)
                            else final_table_height
                        ),
                    )

                    table_data.append(
                        {
                            "Nº FA": table.within_bbox(text_area_1).extract_text(),
                            "Consumidor": table.within_bbox(text_area_2).extract_text(),
                            "Fornecedor": table.within_bbox(text_area_3).extract_text(),
                            "Guia Nº": first_page.within_bbox(
                                delivery_note_text_area
                            ).extract_text(),
                            "Trâmite": first_page.within_bbox(
                                procedure_text_area
                            ).extract_text(),
                            "Complemento": first_page.within_bbox(
                                complement_text_area
                            ).extract_text(),
                            "Unidade": first_page.within_bbox(
                                unit_locale_text_area
                            ).extract_text(),
                            "Data": first_page.within_bbox(
                                date_text_area
                            ).extract_text(),
                            "Impresso Por": first_page.within_bbox(
                                issuer_text_area
                            ).extract_text(),
                            "Caminho": path,
                            "Pagina": page_num,
                            "Linha": match_num,
                        }
                    )

        return table_data
