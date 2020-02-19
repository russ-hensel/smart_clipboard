# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 16:15:24 2018

@author: Russ    gui_snippets
"""


import tkinter as Tk
import tkinter.ttk
from   subprocess import Popen   #, PIPE  #

from   app_global import AppGlobal



#============ class =================

class DropDownWidget( Tk.Frame, ):

    def __init__(self, parent, label_text = "Choose", direct_edit = False, width = 15 ):
        """
        Args:
               parent -- must have
               label_text = "Choose", direct_edit = False

               ??width = 10
        Args:  ??thinking about -- but do some with sets
               read only
               add new to drop down ??
               set_list  ( actually a tuple )
               color
               height
               width    of what
               default text --- no just set it
               button text
               border
               for label drop down arrangement

        """
        super( DropDownWidget, self).__init__( parent, width = 20, height=20, bg ="red")

        labelTop = Tk.Label( self, text = label_text )
        labelTop.grid(column = 0, row = 0)

        self.lister       = ["list one","list two"]   # more for tests
        self.a_string_var = Tk.StringVar()

#        self.cbox = Tk.ttk.Combobox( parent, values=["one", "two" ], ) # ok # width = 10, postcommand = self.updtcblist )
#        self.cbox = Tk.ttk.Combobox( parent, values=["one"],  width = 10, postcommand = self.updtcblist )

         #postcommand = self.updtcblist )   runs at time ddarrow is pressed i think
        self.cbox = Tk.ttk.Combobox( self, values=self.lister,  width = width, textvariable = self.a_string_var, postcommand = self.updtcblist )

        if not direct_edit:
            self.cbox.state(['readonly'])   #  can drop down but no entry

#        self.cbox.bind('<<cbox.bind ComboboxSelected>>', callback_2 ) #binding of user selection with a custom callback callback when?

        self.cbox.grid( column = 1, row=0 )
#        self.cbox.current(1)    # not if box is empty

#        self.cbox.bind("<<ComboboxSelected>>", callbackFunc )
        self.cbox.bind( "<<ComboboxSelected>>", self.selected )   # "<<ComboboxSelected>>" is a virtual event are ther others
        self.counter              = 100
        self.selected_function    = None

    # -----------------------------------------
    def selected( self, event ):
        """
        call function with  selected text ?? add index ?
        """
#        AppGlobal.print_debug( f"ddw selected {event}" )
        if  self.selected_function == None:
            return

    # -----------------------------------------
    def set_selected_function( self, a_function ):
#        msg   = "set_selected_function) "
#        AppGlobal.print_debug( msg )
        self.selected_function    = a_function
#        msg   = "set_text() done "
#        AppGlobal.print_debug( msg )

    def xtra_bcb( self, ):
        pass  # think for debug ... check and delete
        msg   = f"xtra_bcb self.counter = >>{self.counter}<<"
        print( msg, flush = True )

    # -----------------------------------------
    def updtcblist( self ):
        """
        this seems to work but of what use
        """
        self.add_to_dd( "from updtcblist" )

    # -----------------------------------------
    def add_to_dd( self, new_string  ):
        """
        Purpose: see name
        Args: change to pass in new item -- still need to fix
        """
        #!! pass back index
        # add trims for spaces !!
        # works to make sure what is entered is in the drop down, but adds dups
        # need to search or have a shadow set -- what about oreder in dd, by
        # perhaps run when a get is called
#        print( "add_to_dd", flush = True )
        current          = self.a_string_var.get(  )
#        print( self.cbox['values'] )
        current_list     = list( self.cbox['values'] )
#        print( f"current_list {current_list}")

        if current in current_list:
            pass
        else:
            current_list.append( current )
            new_list         = current_list
#            print( f"current >>{current}<< append:    new_list {new_list}")
            self.cbox['values'] = new_list

#        AppGlobal.print_debug( "add_to_dd done"   )

    def set_text( self, a_string ):
#        msg   = f"set_text( >>a_string<< ) "
#        AppGlobal.print_debug( msg )
        self.a_string_var.set( a_string )
#        msg   = "set_text() done "
#        AppGlobal.print_debug( msg )

    # -----------------------------------------
    def get_text( self, ):
        #print( "get text " )
        a_string    =  self.a_string_var.get(  )
        msg         = f"get_text done a_string >>>{a_string}<<<"
        print( msg, flush = True )
        return( a_string )

    def get_list( self, ):
        #print( "get_list" )
        ret   =  self.cbox['values']
        #print( f"get_list done ret >>>{ret}<<<", flush = True )
        return( ret )

    # -----------------------------------------
    def set_list( self, a_list ):
        #print( "set_list" )
        self.cbox['values'] = a_list
        #print( f"get_list done ret >>>{ret}<<<", flush = True )
        return

    def get_index( self, ):
#        print( "get_index" )
        a_index  = self.cboxc.current()
        #print( f"get text done a_string >>>{a_string}<<<" , flush = True )
        return a_index

    # -----------------------------------------
    def set_index( self, a_index ):
#        print( "set_index" )
        self.cbox.current( a_index )
        #print( f"get text done a_string >>>{a_string}<<<" , flush = True)
        return


#============ class =================

class SnippetFilesDialog():

    def __init__(self, mutuable_dict = {} ):

        self.win   = Tk.Toplevel()
        Tk.Label( self.win, text='Modal Dialog')
        #Button( self.win, )

        a_button = Tk.Button( self.win , width = 30, height= 1, text = "Edit Snippet File", command = self._edit_snippet_file_ )
        a_button.grid( row = 1, column = 4, )

#        a_button = Tk.Button( self.win , width=10, height=2, text = "Ed Log" )
#        a_button.grid( row = 0, column = 1, )
#
#        a_button = Tk.Button( self.win , width=10, height=2, text = "Ed Log" )
#        a_button.grid( row = 0, column = 2, )

        self.ddw_snippet_list   = DropDownWidget( self.win, label_text = "Files", direct_edit = False, width = 30 )
        snippet_list            = mutuable_dict[ "snippet_list" ]
        self.ddw_snippet_list.set_list( snippet_list )
        #self.ddw_format.set_text( "input" )  # seems fine or set the index
        self.ddw_snippet_list.set_text( snippet_list[ 0 ] )
        self.ddw_snippet_list.grid( row = 1, column = 1, )


        self.win.geometry( '500x400+300+200'  )
        self.win.transient(self.win.master)
        self.win.focus_set()
        self.win.grab_set()
        self.win.wait_window()

    def _edit_snippet_file_( self, ):


         snippet_fn    = self.ddw_snippet_list.get_text()
         proc = Popen( [ AppGlobal.parameters.ex_editor, snippet_fn ] )
         self.win.destroy()

#  ==================================



