# -*- coding: utf-8 -*-
#
#plan is to have helper objects and functions to aid in building of gui's
from   app_global import AppGlobal
import app_global
import tkinter as Tk

class PlaceInGrid( object ):
    """
    called sequentially to help layout grids in a row and column format
    columnspan=2, rowspan=2
    add columnspan to place  make it increment in direction we are moving ....??
    """
    def __init__(self,  max, by_rows ):

        #self.parent   = parent
        self.max      = max
        self.ix_row   =  0
        self.ix_col   =  0
        self.by_rows  = by_rows
        if by_rows:
            self.function =  self._place_down_row_
        else:
            self.function =  self._place_across_col_

    def place( self, a_widget, delta = 1 ):
        """
        move row or column by delta grid spacings after pacing control
        """
        #app_global.print_debug( f"row,co = {self.ix_row}, {self.ix_col}" )
        self.function( a_widget, delta )
#
    def _place_down_row_( self, a_widget, delta ):
        """
        one of the value intended for self.function
        does its name
        """

#        print( f"_place_down_row_ row = {self.ix_row} col = {self.ix_col}"  )
        a_widget.grid( row = self.ix_row, column = self.ix_col, rowspan = delta   )

        self.ix_row += delta
        if self.ix_row >= self.max:
            print( f"hit max row {self.max}"  )
            self.ix_col += 1
            self.ix_row = 0

    # -----------------------------------
#    delta_row_col( delta_row, delta_col )
#    add a span argument
    # -----------------------------------
    def set_row( self, row,  ):
        """
        what if beyond max
        """
        self.ix_row = row

    # -----------------------------------
    def set_col( self,  col ):
        self.ix_col = col

    # -----------------------------------
    def _place_across_col_( self, a_widget, delta ):
        """
        one of the value intended for self.function
        does its name
        """
#        print( f"_place_across_col_ row = {self.ix_row} col = {self.ix_col}"  )
        a_widget.grid( row = self.ix_row, column = self.ix_col, columnspan = delta, sticky = Tk.W + Tk.E  + Tk.N + Tk.S  )   # sticky = Tk.W + Tk.E  + Tk.N + Tk.S

        self.ix_col += delta
        if self.ix_col >= self.max:
            print( f"hit max row {self.max}"  )
            self.ix_row += 1
            self.ix_col  = 0

        #print("_place_across_col_",  self.ix_row, self.ix_col  )


# =========================== eof =========================






