"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-21 22:18:13
 * @modify date 2020-08-21 22:18:13
 * @desc [
    Auxiliary functions for pywrangle.
 ]
 */
"""
##########
# Imports
##########

from typing import (
    Any,
    Tuple,
    Union
)

import numpy as np
import pandas as pd


##########
# To string
##########
   
def to_str(var):
    """
    Aux method to transform NP arrays into string type.

    Credit: https://stackoverflow.com/a/25085806/14122026
    """
    if type(var) is list:
        return str(var)[1:-1] # list
    if type(var) is np.ndarray:
        try:
            return str(list(var[0]))[1:-1] # numpy 1D array
        except TypeError:
            return str(list(var))[1:-1] # numpy sequence
    return str(var) # everything else


##########
# Create dictionary
##########
   
def create_dict( key_info: Tuple[ str, Any]) -> dict:
    """Returns dictionary from key_info tuple."""
    if not isinstance(key_info, tuple):       # note: can change to tuple, list generic"
        raise Exception("Must pass tuple of keys and information")

    new_dict = dict()
    for key, info in key_info:
        new_dict[key] = info
    return new_dict


##########
# Print new lines
##########

def print_lines(num_new_lines: int = 2) -> None:
    """Prints number of new_line characters."""
    print(
        "\n" * num_new_lines,
        end = '')
    return


##########
# Max col length
##########

def get_max_colname_length(df, colname_header: str = "Column:") -> int:
    """
    Returns the the length of the longest column name in dataframe the dataframe, including passed colname_header.
    """
    max_coltitle_length: int = len(
        max((df.columns, colname_header), key = len))
    return max_coltitle_length


##########
# Rounded %
##########
def get_percent( number: float, digits: int = 4) -> str:
    """Returns percentage of number to digits significant digits."""
    return str(
        round(number, digits) * 100) + "%"


##########
# Is negative
##########

def is_negative(number: Union[int, float]) -> bool:
    """Returns boolean if the number is negative."""
    return number < 0


##########
# Count whole digits
##########
def count_whole_digits(number: Union[int, float]) -> int:
    """Returns integer representing the number of non-decimal digits."""
    num_digits = 0
    while number >= 1:
        number /= 10
        num_digits += 1
    return num_digits


