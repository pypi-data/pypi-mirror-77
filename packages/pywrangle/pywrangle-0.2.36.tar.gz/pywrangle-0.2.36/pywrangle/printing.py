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

from typing import Tuple, Any, List


import numpy as np
import pandas as pd 


##########
# Max col length
##########

def get_max_col_length(df, colname_header: str = "Column:") -> int:
    """
    Returns the longest column name from the dataframe, including the passed colname_header.
    """
    max_coltitle_length: int = len(
        max((df.columns, colname_header), key = len))
    return max_coltitle_length


##########
# Single Header
##########

def _print_headers_colname_singleattr(
    df: object,
    singleattr_header: str,
    max_colname_length: int = None,
    colname_header: str = "Column:",
    spacing: str = "\t" * 2,
    ) -> None:
    """
    Prints the headers for column names and a single attribute.
    """
    if not max_colname_length:
        max_colname_length = get_max_col_length(df, colname_header= colname_header)
    extra_space = ' ' * (max_colname_length - len(colname_header))
    
    print(f"{colname_header}{extra_space}{spacing}{singleattr_header}")
    print(f"{len(colname_header) * '-'}{extra_space}{spacing}{'-' * len(singleattr_header)}")


def _print_tuple_with_spacing(
    two_val_tuple: Tuple[ str, Any],
    max_colname_length: int = None,
    spacing: str = "\t" * 2
    ) -> None:
    """
    Prints tuple of values with spacing between two values.
    """
    for val1, val2 in two_val_tuple:
        extra_spaces = ' ' * (max_colname_length - len(val1))
        print(
            val1,
            extra_spaces,
            spacing,
            val2
        )
    return 


##########
# Print dataframe
##########
def print_formatted_df(df, spacing: str = "\t" * 1) -> None:
    """Prints dataframe with meta information for proper formatting."""

    def get_list_columns_max_charlength(df) -> List[int]:
        """Returns a list of each columns max character length."""

        max_col_charlengths: List[int] = list()

        for col in df.columns:
            max_col_len = len(max( [ df[[col]], str(col)], key = len))
            max_col_charlengths.append( max_col_len)
        return max_col_charlengths
    

    df = df.astype(str)
    max_col_charlengths = get_list_columns_max_charlength(df)

    ## print headers
    for _, row in df.iterrows():
        for i in range(len(df.columns)):

            max_space = max_col_charlengths[i]
            col = df.columns[i]
            val =  row[col]

            print(max_space, col, val)

            print(
                val,
                ' ' * max_space - len(str(val)),    # padding space
                spacing,
                end = ''
            )
        print('')
    return

    


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
