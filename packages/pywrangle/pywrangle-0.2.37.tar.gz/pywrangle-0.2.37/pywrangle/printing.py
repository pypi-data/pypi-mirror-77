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

from typing import (
    Tuple, 
    Any, 
    List,
)


import numpy as np
import pandas as pd 


try:
    import aux_functions
    import df_changes

except (ModuleNotFoundError):
    from pywrangle import aux_functions


##########
# Max col length
##########

def get_max_colname_length(df, colname_header: str = "Column:") -> int:
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
        max_colname_length = get_max_colname_length(df, colname_header= colname_header)
    extra_spaces = ' ' * (max_colname_length - len(colname_header))
    
    print(f"{colname_header}{extra_spaces}{spacing}{singleattr_header}")
    print(f"{len(colname_header) * '-'}{extra_spaces}{spacing}{'-' * len(singleattr_header)}")


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
            val2,
        )
    return 


##########
# Print formatted dict
##########

def print_formatted_dict(
    df_dicts: List[dict], 
    spacing: str = "\t" * 2,
    ) -> None:
    """
    Prints dictionaries for proper formatting.
    """
    
    def get_df_dict_headers() -> dict:
        """
        Returns dictionary with information abou the dataframes to be printed.

        NOTE: func should specify df_change_headers
        """
        key_info = (
            ('name', 'df'),
            ('columns', 'Num columns'),
            ('size', 'df.size'),
            ('shape', 'df.shape')
        )
        return aux_functions.create_dict(key_info)
    

    def get_key_max_charlength(df_dicts: List[dict]) -> dict:
        """
        Returns dictionary with max character length for all values.
        """
        max_charlength_dict = dict()

        for k in df_dicts[0].keys():
            max_char_length = 0

            for df_dict in df_dicts:
                val = aux_functions.to_str(df_dict[k])
                if len(val) > max_char_length:
                    max_char_length = len(val)

            max_charlength_dict[k] = max_char_length
        
        return max_charlength_dict
    

    ## Headers
    df_headers: dict = get_df_dict_headers()

    ## Get max char length dict
    max_char_length: dict = get_key_max_charlength(df_dicts + [df_headers])

    ## TODO: Refactor into funcs to print each for readability & reduction?
    ## Print headers:
    for k in df_headers.keys():
        header = df_headers[k]
        num_extra_spaces = max_char_length[k] - len(header)
        print(
            header, 
            ' ' * num_extra_spaces,
            spacing,
            end = '')
    print('')

    ## Print header dashes
    for k in df_headers.keys():
        header_dashes = len( df_headers[k]) * '-'
        num_extra_spaces = max_char_length[k] - len(header_dashes)
        print(
            header_dashes, 
            ' ' * num_extra_spaces,
            spacing,
            end = '')
    print('')

    ## Print values
    for df_dict in df_dicts:
        for k in df_dicts[0].keys():
            
            value = df_dict[k]
            num_extra_spaces = max_char_length[k] - len(str(df_dict[k]))
            print(value, 
            ' ' * num_extra_spaces,
            spacing, 
            end = ''
            )
        print('')



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
