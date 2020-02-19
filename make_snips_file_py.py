# -*- coding: utf-8 -*-
"""
automatically make a snips file ( or part of ) by looking in a directory of .py files

#>>>>>python example class def


>>>>>python example class def
D:\Russ\0000\python00\python3\_examples\ex_class.py
>>>>>python example control of flow
D:\Russ\0000\SpyderP\Template\ex_control_flow.py
>>>>>python example csv
D:\Russ\0000\SpyderP\Template\ex_csv.py
>>>>>end


"""
#import stat
#import time
#import shutil
import os
import os.path
#import queue
#import logging
#import datetime
#import sys

# local
#from   app_global import AppGlobal

#---------------- helper functions --------------------------
def print_list( a_list ):
        for i_name in a_list:
            print( i_name )
            #print( f"{src}{os.sep}{i_name}" )
#----------------
def not_a_dir( name ):
    return not( os.path.isdir( name ))


#----------------
def get_file_list( src ):

    names = os.listdir( src )
    full_names   =[ f"{src}{os.sep}{i_name}" for  i_name in names ]
    # could be done with lambda more efficient??
    file_names   = list( filter( not_a_dir, full_names ) )

    return file_names

#----------------
def snip_file_title( test_file_name ):
    """
    return a title if this is a snip file else ""
    """
    #!! still needs a try adn perhaps context
    #!! still need to strip new line
    file_title  = ""   # not a snip file
    filein      = open( test_file_name, "r" , encoding = "utf8", errors='ignore')   # extra stuff needed for the loop to work
    #print( filein )
    ix_line = -1
    for i_line in filein:     # will the line have a newline... on it yes need to strip off end
    #for ix_line, i_line in enumerate( filein ):
        ix_line += 1
        #i_line = i_line.rstrip('\n')
        #print( i_line )
        if ix_line == 1:
            i_line = i_line.rstrip('\n')
            if i_line.startswith( "#>>>>>" ):

                file_title = i_line[1:]
                break
        if ix_line > 3:
            break
    filein.close( )
    return file_title

#----------------
def is_py( file_name ):       # use a set test for in
    """
    is file_name a python file
    """
    splits = file_name.split( "." )
    ext    =  splits[-1].lower()   # end one, could be several, fix case
    # !! use set and in
    if  ext == "py":
        return True
    return False

# ======================= main function =============
def make_snips():
    print( """ =================== make_snips ===============
    """ )
    # both seem to work
    print( "==================================")

    fileout_name   = "snips_file_auto.txt"

    src            = r"D:\Russ\0000\python00\python3\_examples"
    file_names = get_file_list( src )
    #print_list( file_names )
    output_list   = []

    for i_name in filter( is_py, file_names ):
        #print( i_name, flush = True )
        i_title = ""
        i_title = snip_file_title( i_name )
        if i_title != "":
            print( f" {i_name}", flush = True )
            output_list.append( ( i_title, i_name ) )
        else:
            pass
            #print( "xxx", flush = True )

    #print( output_list )
    fileout      = open( fileout_name, "w" ,  )

    for title, filename in output_list:
        fileout.write( f"{title}\n" )
        fileout.write( f"{filename}\n" )

    fileout.write( ">>>>>end" )
    fileout.close()
    # add a popopen ??


# =============================================================================
make_snips()
# =============================================================================


