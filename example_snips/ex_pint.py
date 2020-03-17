# -*- coding: utf-8 -*-
#>>>>>python example unit registry numbers with constants


"""
this is physical units and perhaps constants
What about joule = newton * meter
https://pint.readthedocs.io/en/0.8.1/index.html



"""

from pint import UnitRegistry
ureg = UnitRegistry()

uc   =  ureg

# ------------------------- helper -----------------
def print_info( a_item, title ):
    """
    print some info ( see code ) about a_item, give it a title
    """

    print( "\n" )
    print((     "-----" +   title + "-----" ))
    print(        a_item )
    print(( "str:  " + str(  a_item ) ))
    print(( "type: " + str(  type(  a_item ) ) ))
    print(( "repr: " + repr( a_item ) ))
#    print( repr ( speed.dimensionality ) )


# ----------------------------------------
def ex_unit_registry(  ):
    print("""\n\n
    ================ ex_unit_registry(): properties of distance ===============
    """)
    distance = 24.0 * ureg.meter
    #print(distance)
    #24.0 meter

    ret =  str( distance.magnitude )
#    print ret
    ret =  str( distance.units )

    print((        distance.dimensionality ))
    print(( type(  distance.dimensionality ) ))
    print(( str(   distance.dimensionality ) ))
    print(( repr ( distance.dimensionality ) ))

    ret =  str( distance.dimensionality )

    print ( "high" )


#ex_unit_registry()


# ----------------------------------------
def ex_speed(  ):
    print("""\n\n
    ================ ex_speed(): properties of speed ===============
    """)
    distance = 25.0 * uc.meter
    time     = 5.   * uc.sec
    speed    = distance/time

    print(        speed )
    print(( type(  speed ) ))
    print(( str(   speed ) ))
    print(( repr ( speed ) ))

    print((        speed.dimensionality ))
    print(( "str:  " + str(   speed.dimensionality ) ))
    print(( "type: " + str( type(  speed.dimensionality ) ) ))

    print(( repr ( speed.dimensionality ) ))

#ex_speed(  )


# ----------------------------------------
def ex_speed_and_aceleration(  ):
    print("""\n\n
    ================ ex_speed_and_aceleration(): properties of speed acc dimensionality ===============
    """)
    distance = 25.0 * uc.meter
    time     = 5.   * uc.sec
    speed    = distance/time
    acc      = speed/time
#    print(        speed )
#    print( type(  speed ) )
#    print( str(   speed ) )
#    print( repr ( speed ) )

    print_info( speed.dimensionality, "speed.dimensionality" )
    print_info( acc.dimensionality,   "acc.dimensionality" )

    return

ex_speed_and_aceleration(  )


# ----------------------------------------
def ex_compound_units(  ):
    print("""\n\n
    ================ ex_compound_units(): use compound units ===============
    """)
    f_x_d = ( 5.0 * uc.meter ) * ( 4. * uc.newton )

    e_as_joule = ( 20.0 * uc.joule )
    print(        e_as_joule )


ex_compound_units()

# ----------------------------------------
def ex_conversion(  ):
    print("""
    ================ ex_conversion(): conversion  ===============
    """)

    distance     =  20. * uc.meter

    time         =  5. * uc.second

    speed        = distance/time

    speed.ito( ureg.inch / ureg.minute )

    print( speed )

ex_conversion()

# ----------------------------------------
def   ex_5(  ):
    print("""
    ================ ex_5(): conversion compound  ===============
    """)

    f_x_d = ( 5.0 * uc.meter ) * ( 4. * uc.newton )

    e_as_joule = ( 20.0 * uc.joule )

    what       = f_x_d.ito( uc.joule )

    what       = e_as_joule  #.ito( uc.joule )

   # what = 5

    print(        what )


#    distance     =  20. * uc.meter
#
#    time         =  5. * uc.second
#
#    speed        = distance/time
#
#    speed.ito( ureg.inch / ureg.minute )
#
#    print( speed )


# ----------------------------------------
def ex_property_relation(  ):
    print("""
    ================ ex_property_relation(): properties ureg. and its relations ===============
    """)

#    print(        speed )
#    print( type(  speed ) )
#    print( str(   speed ) )
#    print( repr ( speed ) )

    print_info( ureg.meter, "ureg.meter" )

    print_info( ureg.meter * ureg.sec, "ureg.meter * ureg.sec" )

    print_info( 5.0 * ureg.meter * ureg.sec, "5.0 * ureg.meter * ureg.sec" )

    print_info( ( 5.0 * ureg.meter * ureg.sec ).dimensionality, "5.0 * ureg.meter * ureg.sec ).dimensionality" )


    # print_info( acc.dimensionality,   "acc.dimensionality" )


ex_property_relation()



