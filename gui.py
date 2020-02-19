# -*- coding: utf-8 -*-

#   gui for clip_bard.py


import tkinter as Tk
import logging
# local
import gui_helper
from   app_global import AppGlobal

def  make_check_button( p_frame,  a_text, a_variable, a_function     ):
        """
        make a combination check box and button
        look at command frame
        """
        a_frame = Tk.Frame( p_frame, bd = 2, relief = Tk.SUNKEN, height=2 )

        a_cb = Tk.Checkbutton( a_frame, text="",          variable = a_variable,    ) # value=0 )
        a_cb.grid( row=1,  column=0 )

        a_button = Tk.Button( a_frame , width=10, height=2, text = a_text )
        a_button.config( command = a_function  )
        a_button.grid( row = 0, column = 0 )

        return a_frame

# might make a class which could auto increment, store variables.... maybe??
def make_and_place_transform_buttons_1 ( a_frame,           text = "no text",      ix_row   = 5, ix_col = 5,
                                       button_var = None, button_command = None, rb_index = 1 ):   # make both buttons


        """
        this makes it easy to mess with styles for this part of the gui
        """
#        print( f"for {text} index is { ix_col }, {ix_row}" )
        rbx   =  Tk.Radiobutton( a_frame, text= text,   variable = button_var, value = rb_index )
        rbx.grid( row = ix_row,  column = ix_col, )   # sticky = rb_sticky )

        a_button = Tk.Button( a_frame , width=10, height=2, text = text )
        a_button.config( command = button_command  )
        # placement.place( a_button )
        a_button.grid( row = ix_row - 1, column = ix_col )
        return rbx
# ---------------------------
def make_and_place_transform_buttons ( a_frame,           text = "no text",      ix_row   = 5, ix_col = 5,
                                       button_var = None, button_command = None, rb_index = 1 ):   # make both buttons


        """
        rb below, centered no text
        """
#        print( f"for {text} index is { ix_col }, {ix_row}" )
        rbx   =  Tk.Radiobutton( a_frame, text= "",   variable = button_var, value = rb_index )
        rbx.grid( row = ix_row,  column = ix_col, )   # sticky = rb_sticky )

        a_button = Tk.Button( a_frame , width=10, height=2, text = text )
        a_button.config( command = button_command  )
        # placement.place( a_button )
        a_button.grid( row = ix_row - 1, column = ix_col )
        return rbx

#def  make_rp_button( pr_frame, pb_frame,  a_text, a_variable, a_function     ):
#        """
#        two frame one for radio buttons other for push
#        parent_frame   text   a_varible_for_what
#        make a combination check box and button
#        """
#        a_frame = Tk.Frame( p_frame, bd = 2, relief = Tk.SUNKEN, height=2 )
#
##        a_cb = Tk.Checkbutton( b_frame, text="",          variable = a_variable,    ) # value=0 )
##        a_cb.grid( row=0,  column=0 )
#
#        a_rb   =  Tk.Radiobutton( a_frame, text="off", variable = self.button_var, value = ix_col )
#        a_rb.grid( row=0,  column=0 )
#
#        a_button = Tk.Button( b_frame , width=10, height=1, text = a_text  )
#        a_button.config( command = a_function  )
#        a_button.grid( row=0, column= 1 )
#
#        return a_frame


# ===================== class
class GUI( object ):

    def __init__( self, controller  ):

        AppGlobal.gui       = self
        self.controller     = controller
        self.parameters     = controller.parameters
        self.logger         = logging.getLogger( AppGlobal.logger_id + ".gui")
        self.logger.info("in class GUI init for the clip_board_1") # logger not currently used by here

        # ----- start building gui
        self.root           = Tk.Tk()

        self.text_in        = None    # init later

        #self.dispatch_dict   = {  }    # !! this is a test, may not want or use

        # radio button values !! this stuff needs some clean up
        self.url_to_wiki    = 999    # used in controller  set below for radio button index
        self.comma_sep_rb   = 999
        self.undent_rb      = 999
        self.lower_rb       = 999
        self.no_ws_rb       = 999

        self.text_out       = None    # used in controller? set below

        #self.default_button = 0   # buttons not currently used at all

        self.button_var     = Tk.IntVar()
        self.button_var.set( self.controller.parameters.rb_num_on )

        # define here or in the panel with waring??

        self.cb_mulp_cmd_var   = Tk.IntVar()

        self.cb_star_cmd_var   = Tk.IntVar()
        self.cb_url_var        = Tk.IntVar()
        #self.cb_pb_cmd_var     = Tk.IntVar()
        self.cb_exe_file_var   = Tk.IntVar()

        self.cb_edit_txt_var   = Tk.IntVar()

        #self.root.title( self.controller.parameters.title )   f"Application: {self.app_name} {AppGlobal.parameters.mode}  {self.app_version}"
        self.root.title( f"{self.controller.app_name} mode: {AppGlobal.parameters.mode} " +
                         f" version: {self.controller.version}" )

        #        # ----- set up root for resizing
        #        self.root.grid_rowconfigure(    0, weight=0 )
        #        self.root.grid_columnconfigure( 0, weight=1 )
        #
        #        self.root.grid_rowconfigure(    1, weight=1 )
        #        self.root.grid_columnconfigure( 1, weight=1 )

        self.root.grid_rowconfigure(    0, weight=0 )
        self.root.grid_rowconfigure(    1, weight=0 )
        self.root.grid_rowconfigure(    2, weight=0 )
        # moving to frame placement
        # self.root.grid_rowconfigure(    3, weight=1 )
        # self.root.grid_rowconfigure(    4, weight=1 )

        self.root.grid_columnconfigure( 0, weight=1 )
        #self.root.grid_columnconfigure( 1, weight=1 )

        #placement = gui_helper.PlaceInGrid(  1, False )

        ix_row    = -1    # we are going to place frames from top to bottom

        # ----- top application buttons
        a_frame   = self.make_app_controls_frame( self.root,  )
        ix_row   += 1
        a_frame.grid( row=ix_row, column=0, columnspan = 2, sticky=Tk.N + Tk.S + Tk.E + Tk.W )

        a_frame   = Tk.Frame( self.root, width=300, height=20, bg = "red", relief = Tk.RAISED, ) # borderwidth=1 )
        ix_row   += 1
        a_frame.grid( row=ix_row, column=0, columnspan = 2, sticky=Tk.N + Tk.S + Tk.E + Tk.W )

        # ----- command buttons
        a_frame   = self._make_command_frame_( self.root,  )
        ix_row   += 1
        a_frame.grid( row=ix_row, column=0, columnspan = 2, sticky=Tk.N + Tk.S + Tk.E + Tk.W )

        a_frame   = Tk.Frame( self.root, width=300, height=20, bg = "green", relief = Tk.RAISED, ) # borderwidth=1 )
        ix_row   += 1
        a_frame.grid( row=ix_row, column=0, columnspan = 2, sticky=Tk.N + Tk.S + Tk.E + Tk.W )

        # ----- transformations buttons
        a_frame  = self._make_transform_frame_( self.root )
#        print( ix_row )
        ix_row   += 1
        a_frame.grid( row = ix_row, column=0, columnspan = 4, sticky=Tk.N + Tk.S + Tk.E + Tk.W )

        # frames on left and right
        ix_row   += 1
        # ----- frame0
        frame0 = self._make_clip_display_( self.root )
        frame0.grid( row=ix_row, column=0, sticky=Tk.N + Tk.S + Tk.E + Tk.W )
        self.root.grid_rowconfigure(    ix_row, weight=1 )

        # ----- frame_history
        frame_history = self._make_history_frame_( self.root )
        print( ix_row )
        ix_row += 1
        frame_history.grid( row=ix_row, column=0, columnspan=2, sticky=Tk.N + Tk.S + Tk.E + Tk.W)
        self.root.grid_rowconfigure(    ix_row, weight = 1 )

        # self.cb_cmd_var.set(      self.controller.parameters.cmd_on        )
        self.cb_url_var.set(      self.controller.parameters.auto_url_on   )
        self.cb_star_cmd_var.set( self.controller.parameters.star_cmd_on     )
        self.cb_exe_file_var.set( self.controller.parameters.exe_file_on   )

        self.root.geometry( self.controller.parameters.win_geometry )
#        print( "next icon..." )
        if self.parameters.os_win:
            # icon may cause problem in linux for now only use in win
#            Changing the application and taskbar icon - Python/Tkinter - Stack Overflow
#            https://stackoverflow.com/questions/14900510/changing-the-application-and-taskbar-icon-python-tkinter
            import ctypes
            myappid = self.parameters.icon # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
#            print( "in windows setting icon" )
            self.root.iconbitmap( self.parameters.icon )
        msg       = "... icon done...."
        print( msg )
    # ------------------------------------------
    def make_app_controls_frame( self, parent_frame,  ):
        """
        this contains a button area for app control stuff
        passed a parent
        returns this frame
        """
        placement = gui_helper.PlaceInGrid(  99, False )
        a_frame = Tk.Frame( parent_frame )

#        a_button = Tk.Button( a_frame , width=10, height=2, text = "Redo" )
#        a_button.config( command = self.controller.redo_transform  )
#        placement.place( a_button )

        a_button = Tk.Button( a_frame , width=10, height=2, text = "Ed Log" )
        a_button.config( command = self.controller.os_open_logfile  )
        placement.place( a_button )

        a_button = Tk.Button( a_frame , width=10, height=2, text = "Ed Parms" )
        a_button.config( command = self.controller.os_open_parmfile  )
        placement.place( a_button )

        a_button = Tk.Button( a_frame , width=10, height=2, text = "Ed Snippets" )
        a_button.config( command = self.controller.os_open_snippets  )
        placement.place( a_button )

        a_button = Tk.Button( a_frame , width=10, height=2, text = "Ed Snip Files" )
        a_button.config( command = self.controller.os_open_snip_file  )
        placement.place( a_button )

        a_button = Tk.Button( a_frame , width=10, height=2, text = "Help" )
        a_button.config( command = self.controller.os_open_help  )
        placement.place( a_button )

         # about
        a_button = Tk.Button( a_frame , width=10, height=2, text = "About" )
        a_button.config( command = self.controller.cb_about )
        placement.place( a_button )


#        a_button = Tk.Button( a_frame , width=10, height=2, text = "Remote CB" )
#        a_button.config( state = Tk.NORMAL )      # =Tk.DISABLED   = Tk.NORMAL ......
#        a_button.config( command = self.controller.remote_dialog_bcb  )
#        placement.place( a_button )

        a_button = Tk.Button( a_frame , width=10, height=2, text = "Restart" )
        a_button.config( command = self.controller.restart  )
        placement.place( a_button )

        return a_frame

    # ------------------------------------------
    def _make_command_frame_( self, parent_frame,  ):
        """
        make_check_box_frame
        returns this frame
        """
        main_frame          = Tk.Frame( parent_frame, bg = "yellow" ,  borderwidth = 2, relief = "solid" )
        #main_frame.grid_rowconfigure( 0, weight = 1 )
        main_frame.grid_columnconfigure( 0, weight = 1 )

        title_frame         = Tk.Frame( main_frame,  borderwidth = 1, relief = "solid" )
        a_label = Tk.Label( title_frame, text = "Commands",  ) #   relief = RAISED,  )
        #a_button.config( command = self.controller.redo_transform  )
        a_label.grid( row = 0, column = 0, ) # columnspan = 1, sticky = Tk.W + Tk.E )

        title_frame.grid( row = 0, column = 0, columnspan = 1, sticky = Tk.W + Tk.E )

        sub_frame_0         = Tk.Frame( main_frame,  borderwidth = 1, relief = "solid" )   # "solid"   Tk.RIDGE
        sub_frame_0.grid( row = 1, column = 0, columnspan = 1, sticky = Tk.W + Tk.E )

        a_frame   = sub_frame_0
        placement = gui_helper.PlaceInGrid(  99, False )

        # ------------------
        label_frame  = Tk.Frame( a_frame, bd = 2, relief = Tk.SUNKEN, height=2 )

        rb_title     = " Alway On:  "
        pb_title     = "    Press:  "

        b_label = Tk.Label( label_frame, text = pb_title,  ) #   relief = RAISED,  )
        b_label.grid( row = 0, column = 0 )

        a_label = Tk.Label( label_frame, text = "",  ) #   relief = RAISED,  )
        a_label.grid( row = 1, column = 0 )

        a_label = Tk.Label( label_frame, text = rb_title,  ) #   relief = RAISED,  )
        a_label.grid( row = 2, column = 0 )

        placement.place( label_frame )

        a_cb = make_check_button( a_frame, "*cmd", self.cb_star_cmd_var, self.controller.redo_if_star_cmd       )   # cmd_processor.do_if_cmd
        placement.place( a_cb )

        # may be only one that is correct or perhaps not even it
        a_cb = make_check_button( a_frame, "auto url", self.cb_url_var, self.controller.redo_if_url     )
        placement.place( a_cb )
#
#        a_cb = make_check_button( a_frame, "text file", self.cb_edit_txt_var, self.controller.redo_if_text     )
#        placement.place( a_cb )

        return main_frame


#======================
#
#
#        a_frame = Tk.Frame( p_frame, bd = 2, relief = Tk.SUNKEN, height=2 )
#
#        a_cb = Tk.Checkbutton( a_frame, text="",          variable = a_variable,    ) # value=0 )
#        a_cb.grid( row=1,  column=0 )
#
#        a_button = Tk.Button( a_frame , width=10, height=2, text = a_text )
#        a_button.config( command = a_function  )
#        a_button.grid( row = 0, column = 0 )
#
#
#
#
#
#
#  ===================

#        a_label = Tk.Label( a_frame, text = "Auto Commands: ",  ) #   relief = RAISED,  )
#        placement.place( a_label )

        # a_cb = Tk.Checkbutton( a_frame, text="mulp",          variable = self.cb_mulp_cmd_var,    ) # value=0 )
        # !! not sure what this was for, multiple commands vs single commands, want to make all mulp all the time ??
#        a_cb = make_check_button( a_frame, "mulp", self.cb_mulp_cmd_var, None     )
#        placement.place( a_cb )



    # ------------------------------------------
    def _make_transform_frame_( self, parent_frame,  ):
        """
        frame that contains radio buttons etc that control transformations
        may go to application.transform( self, in_text,  ):
        have added redo buttons
        """
#        print("make transform frame ")
        main_frame          = Tk.Frame( parent_frame, bg = "yellow" ,  borderwidth = 2, relief = "solid" )
        #main_frame.grid_rowconfigure( 0, weight = 1 )
        main_frame.grid_columnconfigure( 0, weight = 1 )

        title_frame         = Tk.Frame( main_frame,  borderwidth = .5, relief = "solid" )
        a_label = Tk.Label( title_frame, text = "Transformations",  ) #   relief = RAISED,  )
        #a_button.config( command = self.controller.redo_transform  )
        a_label.grid( row = 0, column = 0, ) # columnspan = 1, sticky = Tk.W + Tk.E )

        title_frame.grid( row = 0, column = 0, columnspan = 1, sticky = Tk.W + Tk.E )

        sub_frame_0         = Tk.Frame( main_frame,  borderwidth = .5, relief = "solid" )   # "solid"   Tk.RIDGE
        sub_frame_0.grid( row = 1, column = 0, columnspan = 1, sticky = Tk.W + Tk.E )

        sub_frame_1         = Tk.Frame( main_frame,  borderwidth = .5, relief = "solid" )   # "solid"   Tk.RIDGE
        sub_frame_1.grid( row = 2, column = 0, columnspan = 1, sticky = Tk.W + Tk.E )
        # !! clean up index and save as var
#        button_delta  = 1     # to place rb above or below the button will also ned to adjust ix_row

        rb_title     = " Alway On:  "
        pb_title     = "    Press:  "

        a_frame     = sub_frame_0

        ix_row        = 1
        ix_row        = 2

        ix_rb_index   = 0
        ix_col        = 0
      # or formula based on button delta ??
        a_label = Tk.Label( a_frame, text = rb_title,  ) #   relief = RAISED,  )
        a_label.grid( row = ix_row, column = ix_col )

        b_label = Tk.Label( a_frame, text = pb_title,  ) #   relief = RAISED,  )
        b_label.grid( row = ix_row -1, column= ix_col )

        # -----------------
        ix_rb_index         += 1
        ix_col              += 1
        self.trans_off_rb   = ix_col
        txt                 = "off"

        rb0 = make_and_place_transform_buttons ( a_frame,    text = "off",              ix_row = ix_row, ix_col = ix_col,
                                           button_var       = self.button_var,
                                           button_command   = self.controller.redo_off,
                                           rb_index         = ix_rb_index )

        rb0.select() # default this button

        # -----------------

        ix_rb_index        += 1
        ix_col             += 1
        self.uformat_rb    = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "unformmated",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_unformatted,
                                   rb_index         = ix_rb_index )

        # -----------------
        ix_rb_index  += 1
        ix_col       += 1
        self.cap_rb   = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "CAP",              ix_row = ix_row, ix_col = ix_col,
                                           button_var       = self.button_var,
                                           button_command   = self.controller.redo_cap,
                                           rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]          = self.controller.cmd_processor.transform_cap

        # -----------------
        ix_rb_index  += 1
        ix_col       += 1
        self.lower_rb   = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "lower",              ix_row = ix_row, ix_col = ix_col,
                                   button_var               = self.button_var,
                                   button_command           = self.controller.redo_lower,
                                   rb_index                 = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]          = self.controller.cmd_processor.transform_lower

        # -----------------
        ix_rb_index      += 1
        ix_col           += 1
        self.no_ws_rb    = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "No WS",              ix_row = ix_row, ix_col = ix_col,
                                   button_var               = self.button_var,
                                   button_command           = self.controller.redo_no_ws,
                                   rb_index                 = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]          = self.controller.cmd_processor.transform_no_ws

        # -----------------
        ix_rb_index  += 1
        ix_col       += 1
        self.less_ws_rb    = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "Less WS",              ix_row = ix_row, ix_col = ix_col,
                                   button_var               = self.button_var,
                                   button_command           = self.controller.redo_less_ws,
                                   rb_index                 = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]          = self.controller.cmd_processor.transform_less_ws

        # -----------------
        ix_rb_index  += 1
        ix_col       += 1
        self.indent_line_rb   = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "Indent",              ix_row = ix_row, ix_col = ix_col,
                                   button_var               = self.button_var,
                                   button_command           = self.controller.redo_insert_spaces,
                                   rb_index                 = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]          = self.controller.cmd_processor.transform_insert_spaces

        # -----------------
        ix_rb_index  += 1
        ix_col       += 1
        self.star_line_rb   = ix_col   # adjust for new button -- think this really should be radio button index or fails on second line

        make_and_place_transform_buttons ( a_frame,    text = "* Lines",              ix_row = ix_row, ix_col = ix_col,  # adjust for new button
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_star_line,   # adjust for new button
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_star_line

        # -----------------
        ix_rb_index  += 1
        ix_col       += 1
        self.url_to_wiki_rb   = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "URL to\n Wiki",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_url_to_wiki,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_url_wiki

         # -----------------
        ix_rb_index  += 1
        ix_col       += 1
        self.url_to_helpdb_rb   = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "Add\n *>url",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_url_to_helpdb,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_url_to_helpdb

        # -----------------
        ix_rb_index         += 1
        ix_col              += 1
        self.add_shell_rb    = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "Add\n *>shell",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_star_shell,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_star_line

        # -----------------
        ix_rb_index         += 1
        ix_col              += 1
        self.comma_sep_rb   = ix_col

        make_and_place_transform_buttons ( a_frame,    text = "comma,\n sep",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_comma_sep,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_comma_sep

        # -----------------
        ix_rb_index  += 1
        ix_col       += 1
        self.undent_rb      = ix_rb_index

        make_and_place_transform_buttons ( a_frame,    text = "undent",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_undent,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_un_dent

        # ---------   a new frame here -----------------------
        a_frame     = sub_frame_1

        ix_row        = 2
        ix_col        = 0

        a_label = Tk.Label( a_frame, text = rb_title,  ) #   relief = RAISED,  )
        a_label.grid( row = ix_row, column= ix_col )

        b_label = Tk.Label( a_frame, text = pb_title,  ) #   relief = RAISED,  )
        b_label.grid( row = ix_row - 1, column= ix_col )

        #--------
        ix_rb_index               += 1
        ix_col                    += 1
        self.alt_line_sort_rb      = ix_rb_index

        make_and_place_transform_buttons ( a_frame,    text = "Alt Line \nSort 0",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_alt_line_sort,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_alt_line_sort

        #--------
        ix_rb_index              += 1
        ix_col                   += 1
        self.sage_rb      = ix_rb_index

        make_and_place_transform_buttons ( a_frame,    text = "Sage",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_transform_sage,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_sage

       #--------
        ix_rb_index        += 1
        ix_col             += 1
        self.x_file_up_rb        = ix_rb_index
        # self.dispatch_dict[ self.rb_test ]   = self.controller.cmd_processor.transform_test  # controller not yet defined

        make_and_place_transform_buttons ( a_frame,    text = "wiki\nfile_upload",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_x_file_up,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_upload_log

        #--------
        ix_rb_index        += 1
        ix_col             += 1
        self.test_rb        = ix_rb_index
        # self.dispatch_dict[ self.rb_test ]   = self.controller.cmd_processor.transform_test  # controller not yet defined

        make_and_place_transform_buttons ( a_frame,    text = "test",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_test,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_test


        #--------
        ix_rb_index              += 1
        ix_col                   += 1
        self.sage_rb      = ix_rb_index

        make_and_place_transform_buttons ( a_frame,    text = "UserPage",              ix_row = ix_row, ix_col = ix_col,
                                   button_var       = self.button_var,
                                   button_command   = self.controller.redo_transform_user,
                                   rb_index         = ix_rb_index )
        self.controller.dispatch_dict[ix_rb_index]  = self.controller.cmd_processor.transform_user_pages

        #-------- chain --- this is different
        ix_col       += 1

        spacer       = Tk.Frame( a_frame, width = 50, )
        spacer.grid( row = ix_row -1, column = ix_col )

        ix_col       += 1

        txt   = "CHAIN\nLast Transform"
        a_button = Tk.Button( a_frame, width = 15, height = 3, text = txt )
        a_button.config( command = self.controller.chain_transform  )
        a_button.grid( row = ix_row -1, column = ix_col, rowspan = 2, columnspan = 2 )

#       # self.trans_off_rb.select()
#        #return ( a_frame, b_frame )
        return main_frame

    # ------------------------------------------
    def _make_clip_display_( self, parent_frame,  ):
        """
        make clipboard display area
        """
        frame0 = Tk.Frame( parent_frame )   # frame is not really needed laft over

        frame0.grid_rowconfigure(    0, weight=1 )
        frame0.grid_columnconfigure( 0, weight=1 )

        text0 = Tk.Text( frame0 , width=50, height=10 )
        #text0.takefocus = 0
        #text0.config(state=Tk.DISABLED)

        s_text0 = Tk.Scrollbar( frame0  )  # LEFT left
        s_text0.grid( row=0, column=1, sticky = Tk.N + Tk.S  )
        s_text0.config( command=text0.yview )

        text0.config( yscrollcommand=s_text0.set )
        text0.grid( row=0, column=0, sticky = Tk.N + Tk.S + Tk.E + Tk.W  )

        self.text_in  = text0   # not very ellegant

#        # spacer
#        s_frame = Tk.Frame( bframe, bg ="green", height=20 ) # width=30  )
#        s_frame.grid( row=0, column=0  )

        return frame0

    # ------------------------------------------
    def _make_history_frame_(self, parent_frame, ):
        """
        ?? and add make snipets
        returns this frame, parent should paste
        """
        a_frame    = Tk.Frame( parent_frame )
        ( a_tlistbox, a_listbox ) = self._make_titled_listbox_( a_frame, "Snippets" )
        #self.parameters.snippets
        for i_snip in self.parameters.snippets:
            i_id, i_text  = i_snip
            #rint i_snip
            self.controller.snippets.update( dict( [ i_snip ] ) )
            a_listbox.insert( 'end', i_id )

        #            for i in range(1, 101):
        #                l.insert('end', 'Line %d of 100' % i)

        #rint self.controller.snippets
        a_listbox.bind( "<<ListboxSelect>>", self.controller.snippet_select )
        a_tlistbox.grid( column=0, row=0, sticky=( Tk.N, Tk.S, Tk.E, Tk.W) )

        # -------------------------------
        ( a_tlistbox, a_listbox ) = self._make_titled_listbox_( a_frame, "SnipFiles" )
        a_tlistbox.grid( column=1, row=0, sticky=( Tk.N, Tk.S, Tk.E, Tk.W) )

        for i_snip in self.parameters.snip_files:
            i_id, i_text  = i_snip
            #rint i_snip
            self.controller.snip_files.update( dict( [ i_snip ] ) )
            a_listbox.insert( 'end', i_id )

        # still need to bind
        a_listbox.bind( "<<ListboxSelect>>", self.controller.snip_file_select )
        #a_tlistbox.grid( column=0, row=0, sticky=( Tk.N, Tk.S, Tk.E, Tk.W) )

        a_frame.grid_columnconfigure( 0, weight=1 )
        a_frame.grid_columnconfigure( 1, weight=1 )
        a_frame.grid_rowconfigure(    0, weight=1 )

        return a_frame

    # ==================== end construction ====================
    # construction helpers

    def _make_titled_listbox_( self, parent_frame, a_title ):
        """
        return ( famelike_thing, listbox_thing)  ?? make a class, better acces to components
        """
        a_frame      = Tk.Frame(parent_frame)
        a_listbox    = Tk.Listbox( a_frame, height=5 )
        a_listbox.grid( column=0, row=1, sticky=(Tk.N, Tk.W, Tk.E, Tk.S) )
        s = Tk.Scrollbar( a_frame, orient=Tk.VERTICAL, command=a_listbox.yview)
        s.grid(column=1, row=1, sticky=(Tk.N, Tk.S))
        a_listbox['yscrollcommand'] = s.set
        a_label = Tk.Label( a_frame, text= a_title )
        a_label.grid( column=0, row=0, sticky=( Tk.N, Tk.E, Tk.W) )
        #  ttk.Sizegrip().grid(column=1, row=1, sticky=(Tk.S, Tk.E)) size grip not appropriate here
        a_frame.grid_columnconfigure( 0, weight=1 )
        a_frame.grid_rowconfigure(    0, weight=0 )
        a_frame.grid_rowconfigure(    1, weight=1 )
        return ( a_frame, a_listbox )

    #----------------------------------------------------------------------
    def write_gui_wt(self, title, a_string ):
        """
        write to gui with a title.
        title     the title
        a_string  additional stuff to write
        make a better function with title = ""  ??
        title the string with some extra formatting
        clear and write string to input area
        """
        self.write_gui( " =============== " + title  + " ==> \n" +  a_string )   # better format or join ??

    #----------------------------------------------------------------------
    def write_gui(self, string ):
        """
        clear and write string to input area
        leave disabled
        """
        self.text_in['state'] = 'normal'      # normal  disabled
        self.text_in.delete( 1.0, Tk.END )
        self.text_in.insert( Tk.END, string )
        self.text_in['state'] = 'disabled'      # normal  disabled
        # self.text_in.see( Tk.END )  # add scrolling

        # self.text_in.delete( 1.0, str( cut ) + ".0" )

if __name__ == "__main__":

    # ------------------------------------------

    #----- run the full app
    import clip_board
    app  = clip_board.App( None, None )




