"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-21 17:32:37
 * @modify date 2020-08-21 17:32:37
 * @desc [
    Auxiliary functions to "pretty print" data structures.
 ]
 */
"""

##########
# Imports
##########

import numpy as np
import pandas as pd 


##########
# print dataframe
##########

def print_dataframe(df: object) -> None:
    """
    Prints dataframe with appropriate spacing
    """
    return


def print_formatted_dicts() -> None:
    return


def print_formatted_list() -> None:
    """

    """
    return


def _print_headers_colname_singleattr(
    df: object,
    singleattr_header: str,
    max_colname_length: int = None,
    colname_header: str = "Column:",
    spacing = "\t" * 2,
    ) -> None:
    """
    Prints the headers for column names and a single attribute.
    """
    if not max_colname_length:
        max_colname_length = get_max_col_length(df, colname_header= colname_header)
    extra_space = ' ' * (max_colname_length - len(colname_header))
    
    print(f"{colname_header}{extra_space}{spacing}{singleattr_header}")
    print(f"{len(colname_header) * '-'}{extra_space}{spacing}{'-' * len(singleattr_header)}")


def get_max_col_length(df, colname_header: str = "Column:") -> int:
    """
    Returns the longest column name from the dataframe, including the passed colname_header.
    """
    max_coltitle_length: int = len(
        max((df.columns, colname_header), key = len))
    return max_coltitle_length


##########
# Tests
##########

def test_print_headers():
    _print_headers_colname_singleattr(
        None, 
        "Null",
        5
    )
    
##########
# Main
##########

def main():
    test_print_headers()


if __name__ == "__main__":
    main()
