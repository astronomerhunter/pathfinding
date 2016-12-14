# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------- #
# This module houses simple functions.  A user of the code shouldn't touch it.
# -------------------------------------------------------------------------------------- #
import os


# --- simple functions ----------------------------------------------------------------- #
def get_path_to_this_file():
    # This function returns a string that represents the absolute filepath of this 
    # file.
    # 
    return os.path.abspath(__file__)

    
def filepath_string_to_list(inString):
    # This function converts a filepath string (with '/' separating folders) into
    # a list.  Keeping a filepath as a list allows us to modify it easily.  
    # To convert a list to a string filepath, use filepath_list_to_string().
    #
    assert type(inString) == type('')
    # split path into list
    return inString.split('/')
    
    
def filepath_list_to_string(inList):
    # This function converts a filepath list (entries = strings of folder/file
    # names) into a string.  inverse of filepath_string_to_list().
    #
    assert type(inList) == type([])
    # join list with '/'s, making sure to put a leading '/'
    return '/'+os.path.join(*inList)
