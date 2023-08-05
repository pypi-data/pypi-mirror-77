from typing import List

import xlsxwriter
import pandas as pd
import numpy as np

from .commons import run_requests, structure_sheets, structure_sheet
from .consts import RED_TO_GREEN_GRADIENT
from ..services.services import Services


def convert_to_xlsx(
    input_path: str,
    services: Services,
    workers: int = 1,
    output_path: str = None,
    normalize: bool = None,
):
    """Sends requests to defined Hypatos services for every invoice found in given
    directory. Merges results off all services into one Excel file and writes to
    project directory. Every key, value pair from Invoice Extractor will flattened
    into the following tuple:

        key = (value, probability, validation[optional])

    Arguments:
        path {str} -- Path to the directory containing invoices, uses rglob.
        extractor_endpoint {str} -- Url of Hypatos extractor service.

    Keyword Arguments:
        vat_validator_endpoint {str} -- Url of vat_validator. (default: {None})
        validation_endpoint {str} -- Url of validation. (default: {None})
        token {str} -- API token. (default: {None})
        workers {int} -- Amount of multithread. (default: {1})
    """
    # Get requests result
    response, vat_validation_result = run_requests(workers, input_path, services)

    # Structure response into sheets (dict) containing records [{...}, {...}]
    sheets = structure_sheets(response)

    # Normalize probability
    if normalize and (services.headers.get("probabilities") == "true"):
        for sheet in sheets.copy():
            sheets[sheet] = normalize_probability(sheets[sheet])

    # Write sheets into workbook
    write_workbook(
        output_path, sheets, vat_validation_result, bool(services.validation_endpoint),
    )


def write_workbook(
    output_path: str,
    sheets: List[dict],
    vat_validation=None,
    validation: bool = False,
    progress_reporter: object = None,
):
    # Init workbook/sheets
    workbook = xlsxwriter.Workbook(output_path)

    # Add progress counter
    if progress_reporter:
        progress_reporter.max += sum([len(*sheet.values()) for sheet in sheets])

    # Styling
    header = workbook.add_format({"bold": True})
    probability_format = [
        workbook.add_format({"bold": True, "bg_color": color})
        for color in RED_TO_GREEN_GRADIENT
    ]

    for sheet in sheets:
        workbook.add_worksheet(sheet)
        write_sheet(
            workbook.get_worksheet_by_name(sheet),
            structure_sheet(sheets[sheet]),
            header,
            probability_format,
            validation,
            progress_reporter,
        )

    if vat_validation:
        write_vat_validation(vat_validation, workbook)

    workbook.close()


def write_sheet(
    worksheet,
    records: list,
    bold_header,
    red_to_green_formats: list,
    validation: bool,
    progress_reporter: object = None,
):
    """Write items to workbook sheet.

    Arguments:
        worksheet {[type]} -- [description]
        records {[type]} -- [description]
        bold_header {[type]} -- [description]
        red_to_green_formats {[type]} -- [description]
        validation {[type]} -- [description]
    """
    for idx, row in enumerate(records):
        count = 0
        for key, value in row.copy().items():
            worksheet.write(0, count, key, bold_header)
            if not isinstance(value, tuple):
                records[idx][key] = (value, None, None)

            column_value, probability, validation_errors = records[idx][key]

            if pd.notna(probability):
                color_idx = int((len(red_to_green_formats) - 1) * probability)
                color = red_to_green_formats[color_idx]
                worksheet.write(idx + 1, count, column_value, color)
            else:
                worksheet.write(idx + 1, count, column_value)

            if validation and key not in ["file_name", "error_message", "row_number"]:
                validation_errors = validation_errors if validation_errors else 0
                count += 1
                worksheet.write(0, count, f"{key}ValidationErrors", bold_header)
                if validation_errors == 0:
                    worksheet.write(idx + 1, count, validation_errors)
                else:
                    worksheet.write(idx + 1, count, len(validation_errors))
                    worksheet.write_comment(idx + 1, count, str(validation_errors))

            count += 1

        if progress_reporter:
            progress_reporter.current += 1

    for i, width in enumerate(get_col_widths(pd.DataFrame.from_records(records))):
        worksheet.set_column(i, i, width)


def get_col_widths(invoices, max_col_width=70):
    """ Get max length for every column and below max_column_width """
    return [
        min(
            max(
                [len(str(s[0])) for s in invoices[col].values if s is not np.nan]
                + [len(col)]
            ),
            max_col_width,
        )
        for col in invoices.columns
    ]


def write_vat_validation(result, workbook):
    workbook.add_worksheet("vat_validation")
    worksheet = workbook.get_worksheet_by_name("vat_validation")

    for idx, row in result.items():
        count = 0
        for key, value in row.items():
            worksheet.write(0, count, key)
            worksheet.write(idx + 1, count, value)
            count += 1


def normalize_probability(records: list):
    """ Normalize the probabilities for every column inbetween range(min, max) of
    particulair column.

    Args:
        invoices ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Read
    probabilities = {}
    for idx, invoice in enumerate(records):
        probabilities[idx] = {k: v[1] for k, v in invoice.items()}

    # Normalize
    df = pd.DataFrame.from_dict(probabilities, orient="index")
    for col in df.columns:
        if not df[col].isnull().all():
            min_value, max_value = (
                df[col].min(),
                df[col].max(),
            )
            if min_value == max_value:
                df[col] = pd.Series([np.nan] * len(df[col]))
            else:
                df[col] = (df[col] - min_value) / (max_value - min_value)

    # Write
    normalized = df.to_dict("records")
    for idx, invoice in enumerate(records.copy()):
        for col in invoice:
            if invoice[col]:
                triplet = list(records[idx][col])
                triplet[1] = normalized[idx][col]
                records[idx][col] = tuple(triplet)

    return records
