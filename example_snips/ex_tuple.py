# -*- coding: utf-8 -*-
#>>>>>python example for tuples including named ones

""""
What:   basic tuple and named_tuple  stuff
Status: draft, ok draft but possibly useful
Refs:


Notes:

    can add more to this

    you can slice

    Search on:
        named

        collections
        *args

"""


#A  tuple is defined in the same way as a list, except that the whole set of elements is enclosed in parentheses instead of square brackets.
#2	The elements of a tuple have a defined order, just like a list. Tuples indices are zero-based, just like a list, so the first element of a non-empty tuple is always t[0].
#3	Negative indices count from the end of the tuple, just as with a list.
#4	Slicing works too, just like a list. Note that when you slice a list, you get a new list; when you slice a tuple, you get a new tuple.


import collections


# ---------------- helper function
def a_function( a, b, c ):
    print( a )
    print( b )
    print( c )

# ==========================================================
def ex_star_args():
    print( """
    ----------------ex_star_args() call like  a_function( *args ) ---------------------------
    """ )
    args   = ( 1, 2, 3)
    a_function( *args )   # not * fixes what else would be error

#ex_star_args()


# ==========================================================
def ex_literal_tuples():
    print( """
    ----------------------- ex_literal_tuples() ------------
    """ )
    print( ( 1,2,3 ) )
    print( ( 1, ) )
    print( ( 1 ) )
    print ( (  ) )
    print( ( 1,2,3 ) )

    x       = 1     # 1 is just a number
    print( x )
    x       = 2,    # watch out not a number but a tuple
    print( x )

#ex_literal_tuples()


# ==========================================================
def ex_unpack():
    print( """
    ----------------ex_unpack ---------------------------
    """ )
    args   = ( 1, 2, 3)

    a,b,c  = args
    print( a,b,c )

    print( args[2], args[1], args[0], )

    a_tuple   = ( ["list_c_0", "list_0_1"], ["list_1_0", "list_1_1"] )

    print( f"a_tuple[0] = {a_tuple[0]}" )

#ex_unpack()



# ==========================================================
def ex_named_tuples():
    print( """\n\n
    ----------------------- ex_named_tuples()   ------------

    """ )
    Person = collections.namedtuple( 'PersonTuple', 'name age gender')

    print(( 'Type of Person:', type(Person) ))

    bob = Person( name='Bob', age=30, gender='male' )
    print( '\nRepresentation of bob:', bob )

    jane = Person( name='Jane', age=29, gender='female' )
    print(  '\nField by name for jane.name:', jane.name )

    print( '\nFields by index:' )
    for p in [ bob, jane ]:
        print( '%s is a %d year old %s' % p )

#ex_named_tuples()

# ==========================================================
def ex_named_tuples_dbader():
    print( """\n\n
    ----------------------- ex_named_tuples_dbader()   ------------
    more at:
    Writing Clean Python With Namedtuples – dbader.org
    *>url  https://dbader.org/blog/writing-clean-python-with-namedtuples
    plus a few russ additions
    """ )

#    args  collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)
#    Car = collections.namedtuple(  'color mileage')  # missing firs arg

    Car = collections.namedtuple('Car' , 'color mileage')
#    # or
#    Car = collections.namedtuple('Car', ['color', 'mileage'])
#    collections.namedtuple('Car', ['color', 'mileage'])   # name Car is not defined
#    Car  = collections.namedtuple( 'Boat', ['color', 'mileage'])   # mismatch  name seems to be use by str and repl

    my_car = Car('red', 3812.4)
    print( my_car.color )
    print( my_car.mileage )
    print( my_car )

    # like functions with named args
    my_car = Car( color = 'green', mileage = 3812.4 )
    print( my_car )

    # need not be in order
    my_car = Car( mileage = 3812.4, color = 'blue', )
    print( my_car )

    print( f"my_car._asdict()  >>{my_car._asdict()}<<" )
    new_car      = my_car._replace( color='blue' )
    print( new_car )
    #Lastly, the _make() classmethod can be used to create new instances of a namedtuple from a sequence or iterable:

    newest_car = Car._make(['red', 999])
    print( newest_car )

#ex_named_tuples_dbader()


# ===== might want to experiment with variations on this
# ------------- helper -------------------

def three_args( arg1, arg2, arg3, arg4 = 0):
    ret  = arg1 + arg2 + arg3 + arg4
    print( ret )
    return ret


# ==========================================================
def ex_un_pack_for_function():
    print( """\n\n
    ----------------------- ex_un_pack_for_function()   ------------

    """ )

    three_args( 1, 2, 3 )         # function call
    unpack_me   = ( 5, 6, 7 )
    three_args( *unpack_me )      # function call

#ex_un_pack_for_function()







