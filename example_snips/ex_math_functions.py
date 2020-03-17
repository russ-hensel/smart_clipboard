# -*- coding: utf-8 -*-
#>>>>>python example for math functions
""""
some quick examples of math functions as a cheat sheet
add to add needed 

    https://docs.python.org/2/library/math.html
    math.sin(x)
    Return the sine of x radians.

"""


import  math

# ==========================================================
def ex_dir_of_math():
    print( """
    ================ ex_dir_of_math() ===============
    """ )

    print( dir(  math ) )
    print( help( math ) )

#ex_dir_of_math()


# ==========================================================
def ex_misc_functions():
    print( """
    ================ ex_misc_functions() ===============
    """ )

    x   = math.pi
    #print( f"math.log( pi) = {math.log(1.)}" )
    print( f"x = math.pi     = {math.pi}" )
    print( f"x               = {x}" )
    print( f"math.log(x)     = {math.log(x)}" )
    print( f"math.log10(x)   = {math.log10(x)}" )
    print( f"math.log2(x)    = {math.log2(x)}" )
    print( f"x**2            = {x**2}" )
    print( f"round( x, 2 )   = {round( x, 2 )}" )


ex_misc_functions()


# ==========================================================
def ex_trig_functions():
    print( """
    ================ ex_trig_functions() ===============
    """ )
    x       = math.pi

    print( f"x = math.pi       = {math.pi}" )
    print( f"x                 = {x}" )
    print( f"math.cos(x)       = {math.cos(x)}" )
    print( f"math.pi           = {math.pi}" )
    print( f"math.cos(x)       = {math.cos(x)}" )


    print( f"math.acos(x/4)    = {math.acos(x/4)}" )
    print( f"math.asin(x/4)    = {math.asin(x/4)}" )
    print( f"math.asinh(x)     = {math.asinh(x)}" )
    print( f"math.atan(x)      = {math.atan(x)}" )
#    print( f"math.atan2(x)   = {math.atan2(x)}" )

    print( f"math.cos(x)       = {math.cos(x)}" )
    print( f"math.cosh(x)      = {math.cosh(x)}" )

    print( f"math.sin(x)       = {math.sin(x)}" )
    print( f"math.sinh(x)      = {math.sinh(x)}" )

    print( f"math.tan(x)       = {math.tan(x)}" )


# ex_trig_functions()

















