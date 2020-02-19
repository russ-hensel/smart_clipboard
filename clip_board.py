# -*- coding: utf-8 -*-
#! /usr/bin/python3
#!python3
# above for windows ??
#     /usr/bin/python

#print( "start imports" )  # debugging splash screen

"""
*>text

"""

import os
import logging
import sys
import traceback
import importlib
import pyperclip
from   subprocess import Popen   #, PIPE  #
import time
import datetime

#----- local imports
import parameters
import gui
import gui_snippets
import cmd_processor
#import splash
# print "done imports"
from   app_global import AppGlobal

# ------------------------------
def   print_uni( a_string_ish ):
    """
    print even if unicode char messes it con
    maybe doing as a call is over kill
    """
    print(  a_string_ish.encode( 'ascii', 'ignore') )

# ============================================
class App( object ):
    """
    this class is the "main" or controller for the whole app
    to run see end of this file
    it is the controller of an mvc app
     """
    def __init__( self,  q_to_splash, q_from_splash  ):
        """
        usual init for main app
        splash not working as desired, disabled
        splash screen which is of not help unless we sleep the init
        """
        self.app_name          = "ClipBoard"
        self.version           = "Ver 5: 2020 02 19"
        AppGlobal.controller   = self
        self.gui               = None

        self.q_to_splash       = q_to_splash

        self.restart( )

    # ----------------------------------
    def restart(self ):
        """
        use to restart the app without ending it
        this can be very quick
        it is also an extension of __init__
        """
        print( "========= restart =================" ) # not logged until logging is turned on
        if not( self.gui is None ):
            self.gui.root.destroy()
            importlib.reload( parameters )    # should work on python 3 but sometimes does not

        else:
            #self.q_to_splash
            pass

        self.parameters     = parameters.Parameters( ) # open early as may effect other parts of code
        self.config_logger()
        self.prog_info()
       # could combine with above ??

        self.snippets       = {}          # predefined stuff for clipboard -- do before gui
        self.snip_files     = {}          # predefined stuff for clipboard -- do before gui



        # gets gui ref so make after gui
        self.cmd_processor  = cmd_processor.CmdProcessor(  )   # commands processed here

        self.dispatch_dict   =  {  }
        """
        self.dispatch_dict   =  {   self.gui.cap_rb:            self.cmd_processor.transform_cap,
                                    self.gui.lower_rb:          self.cmd_processor.transform_lower,
                                    self.gui.no_ws_rb:          self.cmd_processor.transform_no_ws,
                                    self.gui.less_ws_rb:        self.cmd_processor.transform_less_ws,
                                    self.gui.url_to_wiki_rb:    self.cmd_processor.transform_url_wiki,
                                    self.gui.url_to_helpdb_rb:  self.cmd_processor.transform_url_to_helpdb,
                                    self.gui.add_shell_rb:      self.cmd_processor.transform_star_shell,
                                    self.gui.comma_sep_rb:      self.cmd_processor.transform_comma_sep,
                                    self.gui.undent_rb:         self.cmd_processor.transform_un_dent,
                                    self.gui.url_to_helpdb_rb:  self.cmd_processor.transform_url_to_helpdb,
                                    self.gui.alt_line_sort_rb:  self.cmd_processor.transform_alt_line_sort,
                                    self.gui.sage_rb:           self.cmd_processor.transform_sage,
                                    self.gui.test_rb:           self.cmd_processor.transform_test,
                                    self.gui.indent_line_rb:    self.cmd_processor.transform_insert_spaces,
                                    self.gui.star_line_rb:      self.cmd_processor.transform_star_line,

                                     }

        """




        self.gui            = gui.GUI( self )  # gui references cmd processor and controller

        # this take care of buttons, also command and redo commands
        # lets try to define this in the gui so it maintains itself.



        self.old_clip       = ""          # old value of info in clipboard -- may be transformed - checked to see if clipboad changed
        self.undo_clip      = ""          # old value never transformed for undo

        msg       = "Error messages may be in log file, check it if problems -- check parmeters.py for logging level "
        print( msg )
        AppGlobal.print_debug( msg )
        self.logger.log( AppGlobal.fll, msg )
        self.polling_delta  = self.parameters.poll_delta_t

        self.starting_dir   = os.getcwd()    # or perhaps parse out of command line
        self.gui.root.after( self.polling_delta, self.polling )

#        self.history         = []      # begin to work on history, may not be implementd or incompletely

        # if not(self.q_to_splash == None ):
        #     self.q_to_splash.put( "stop" )
        msg       = "mainloop..."
        print( msg )
        self.gui.root.mainloop()

        msg       = ".... mainloop done"
        print( msg )

    # ------------------------------------------
    def config_logger( self, ):
        """
        configure the python logger
        """
        AppGlobal.logger_id     = "App"        # or prerhaps self.__class__.__name__
        logger                  = logging.getLogger( AppGlobal.logger_id )

        logger.handlers = []

        logger.setLevel( self.parameters.logging_level )

        # create the logging file handler
        fh = logging.FileHandler( self.parameters.pylogging_fn )

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # add handler to logger object -- want only one add may be a problem
        logger.addHandler(fh)

        logger.info( "Done config_logger .. next AppGlobal msg" )
        #print( "configed logger", flush = True )
        self.logger      = logger   # for access in rest of class?
        AppGlobal.logger = logger

        msg  = f"Message from AppGlobal.print_debug >> logger level in App = {self.logger.level} will show at level 10"
        AppGlobal.print_debug( msg )


    # --------------------------------------------
    def prog_info( self,  ):

        #logger_level( "util_foo.prog_info"  )
        fll         = AppGlobal.force_log_level
        logger      = self.logger
        logger.log( fll, "" )
        logger.log( fll, "============================" )
        logger.log( fll, "" )
        title       =   f"Application: {self.app_name} in mode {AppGlobal.parameters.mode} and version  {self.version}"
        logger.log( fll, title )
        logger.log( fll, "" )

        if len( sys.argv ) == 0:
            logger.info( "no command line arg " )
        else:

            for ix_arg, i_arg in enumerate( sys.argv ):
                msg = f"command line arg + {str( ix_arg ) }  =  { i_arg })"
                logger.log( AppGlobal.force_log_level, msg )

        logger.log( fll, f"current directory {os.getcwd()}"  )

        start_ts     = time.time()
        dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
        string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        logger.log( fll, "Time now: " + string_rep )
        # logger_level( "Parameters say log to: " + self.parameters.pylogging_fn ) parameters and controller not available can ge fro logger_level

        return

    # ----------------------------------
    def polling( self,  ):
        """
        poll for clipboard change and process themn
        protect with a try so polling is not crashed -- "no matter what"
        """
        # msg       = "polling ...."
        # print( msg )

        try:
#            !! need a skip in here if doing a redo -- do this next
            new_clip  = pyperclip.paste()

            if ( new_clip != "" ) and ( new_clip is not None ):
                if new_clip != self.old_clip:
                    print( "\n\n new clip ------" )
                    self.logger.debug( "polling clip change >>" + new_clip + "<<\n>>>" + self.old_clip +"<<<\n"  )
                    #self.history.append( new_clip )
                    # !! need to truncate
                    self.undo_clip   = new_clip
#                    new_clip_b       = str( new_clip.encode( 'ascii', 'ignore') )  # some uni just does not seem to work
#                    self.logger.info( "new_clip = " +  new_clip_b  )
                    self.old_clip    = new_clip

                    ( is_done, did_what, ret_text )  = self.do_command_transform( new_clip )
                    # if true will have done something ( did_what, and new text if false, the other two args are basically ignored )
                    if is_done:
                        self.old_clip   = ret_text
                        pyperclip.copy( ret_text  )
                        self.gui.write_gui_wt( did_what, ret_text  )
                    else:
                    #rnot a fileis_done false"
                        self.gui.write_gui_wt( "polling did nothing", new_clip  )

        except Exception as ex_arg:
            self.logger.error( "polling Exception: " + str( ex_arg ) )
            # ?? need to look at which we catch maybe just rsh
            (atype, avalue, atraceback)   = sys.exc_info()
            a_join  = "".join( traceback.format_list ( traceback.extract_tb( atraceback ) ) )
            self.logger.error( a_join )

        finally:
            self.gui.root.after( self.polling_delta, self.polling )  # reschedule event

    # ---------------- functions -------------------    # ------------------------------------------
    def do_command_transform( self, in_text,  ):
        """
        do both commands and transforms each with its own method -- only if the always on button is called
        extension and called from polling
        basically splits into a command part and a transform part
        input in_text return transformed -- checked gui to see if enabled
        return done flag and transformed text in tuple
        ex: ( False, "what_transform", "transformed text" )
        """
        # try commands first
        ( is_done, did_what, ret_text ) = self.do_commands( in_text )

        if not( is_done ):   # --- if not a command try transform
            print( f"not is done for command try transform" )
            ( is_done, did_what, ret_text )  = self.do_transform( in_text )      #.upper()

        if is_done:
            self.old_clip  = ret_text     # is this right ???yes  maybe in return
            pyperclip.copy(  ret_text  )
            #self.gui.write_out( ret_text )
            return ( is_done, did_what, ret_text )

        else:
            pass
        return ( False, "", "" )

    # ------------------------------------------
    def do_transform_with_dict( self, in_text,  ):
        """
        input in_text return transformed -- checked gui to see if enabled
        return done flag and transformed text in tuple
        ex: ( False,"did_what" "new_text" )
        need to maintain in right order no only one can be chosen at a time
        move to a dict or list implementation??
        can we essencially set up in gui.py so is not missed
        !! check to see if up to date
        """
        case = self.gui.button_var.get(  )   # value of the radio button, we will do only one transform ( at least for now later untill one succeeds )
        print("do_transform() for " + str( case ))

        # this first may be special need special management
        # may want to build from the gui or the comd processor ( would tighten the coupling bad)

        # !! make functions for these first 2 then get rid of this
        if   case == self.gui.trans_off_rb:
            return ( False, "", "transform off"  )

        elif case == self.gui.uformat_rb:
            return ( True, "unformat", in_text )

        if  case in self.dispatch_dict:
            function      = self.dispatch_dict[ case ]
            return function( in_text )
        else:
            print( f"case >>{case}<< not in dispatch_dict" )

        return ( False, "", "" )

    # ------------------------------------------
    def do_transform( self, in_text,  ):
        """
        input in_text return transformed -- checks gui to see if enabled
        return done flag and success message and transformed text all in tuple
        ex: ( False,"did_what" "new_text" )
        only one can be chosen at a time
        move to a dict or list implementation??
        can we essencially set up in gui.py so is not missed
        !! check to see if up to date
        works for
            cap
            lower failed
            no whitespace ok

        """
        case = self.gui.button_var.get(  )   # value of the radio button, we will do only one transform ( at least for now later untill one succeeds )
        print("do_transform() for " + str( case ))


        return self.do_transform_with_dict(  in_text,  )


    # ------------------------------------------
    def do_transform_old( self, in_text,  ):
        """
        input in_text return transformed -- checks gui to see if enabled
        return done flag and success message and transformed text all in tuple
        ex: ( False,"did_what" "new_text" )
        only one can be chosen at a time
        move to a dict or list implementation??
        can we essencially set up in gui.py so is not missed
        !! check to see if up to date
        works for
            cap
            lower failed
            no whitespace ok

        """
        case = self.gui.button_var.get(  )   # value of the radio button, we will do only one transform ( at least for now later untill one succeeds )
        print("do_transform() for " + str( case ))
        #print("self.gui.no_ws_rb " + str( self.gui.no_ws_rb ))
#        print("self.gui.url_to_helpdb " + str( self.gui.url_to_helpdb ))
        #        print "transform() button_var case " + str( case )
        #        sys.stdout.flush()
        #        self.logger.info( "transform() button_var case " + str( case ) )

        # could we loop thru a dict  with key of rb_index, then command to be called
        #this would look

        """
        { 1: self.controller.cmd_processor.transform_cap }
        how do we get the index -- use a ix_rb
        """

        # this first may be special need special management
        if   case == self.gui.trans_off_rb:
            return ( False, "", "transform off"  )

        elif case == self.gui.uformat_rb:
            return ( True, "unformat", in_text )

        elif    case == self.gui.cap_rb:
            return self.cmd_processor.transform_cap( in_text )

        elif case == self.gui.no_ws_rb:
            #print( "self.gui.no_ws_rb" )
            return self.cmd_processor.transform_no_ws( in_text )

        elif case == self.gui.less_ws_rb:
            #print( "less_ws_rb" )
            return self.cmd_processor.transform_less_ws( in_text )

        elif case == self.gui.url_to_wiki:
            return self.cmd_processor.transform_url_wiki( in_text )

        elif case == self.gui.comma_sep_rb:
            return self.cmd_processor.transform_comma_sep( in_text )

        elif case == self.gui.undent_rb:
            return self.cmd_processor.transform_un_dent( in_text )

        elif case == self.gui.url_to_helpdb:
            return self.cmd_processor.transform_url_to_helpdb( in_text )

        elif case == self.gui.lower_rb:
            print( "try lower_rb " )    # looks like we may not get here
            ret =  self.cmd_processor.transform_lower( in_text )
            print( ret )
            return ret

        else:
            print( "no transform worked" )
            return ( False, "", "" )

    # ------------------------------------------
    def do_commands ( self, in_text,  ):
        """
        v3
        do checked commands if any
        input in_text
        return done flag and transformed text in tuple
        ex: ( False, "what_transform", "transformed text" )
        !! check up to date, may have dropped some commands

        seems still need
        """

        # !! change this by index into list which is what bove does
        cmds_checked     = []
        if self.gui.cb_url_var.get():
            cmds_checked.append( "url" )

        msg    = f"self.gui.cb_star_cmd_var.get(): {self.gui.cb_star_cmd_var.get()}"
        print( msg )
        if self.gui.cb_star_cmd_var.get():
            cmds_checked.append( "*>" )

        if self.gui.cb_edit_txt_var.get():
            cmds_checked.append( "txt" )

        msg    = f"self.gui.cb_exe_file_var.get(): {self.gui.cb_exe_file_var.get()}"
        print( msg )
        if self.gui.cb_exe_file_var.get():
            print( "gui.cb_exe_file_var.get" )
            cmds_checked.append( "exe" )

        self.cmd_processor.begin()   # reset response and processed
        cmd_result   = self.cmd_processor.do_cmds( in_text, cmds_checked )   # process them return a tuple, name it

        return cmd_result

    # ------------------------------------------
    def redo_transform( self,   ):

        #rint "=============== redo ============="
        #rint self.undo_clip
        self.old_clip   = self.undo_clip

        ( is_done, did_what, ret_text )  = self.do_command_transform( self.undo_clip  )

        if is_done:
            self.old_clip  =  ret_text
            pyperclip.copy( ret_text  )
            self.gui.write_gui( " =============== " +  did_what + " \n " +  ret_text  )
        else:
            pass

    # ----------------- button call backs from gui
    def cb_about( self, ):
        """
        what it says
        """
        AppGlobal.about()

    #  ------------------
    def redo_url_to_wiki( self, ):
        #rint("redo_url_to_wiki "  + self.undo_clip )
        is_done, did_what, new_clip  = self.cmd_processor.transform_url_wiki( self.undo_clip )
        if is_done :
              pyperclip.copy( new_clip  )
              self.gui.write_gui_wt( did_what, new_clip  )
        else:
             self.gui.write_gui_wt( "did nothing", new_clip  )

    #  ------------------
    def redo_star_shell( self, ):
        """
        v3 called from gui
        """
        print("redo_star_shell "  + self.undo_clip )
        is_done, did_what, new_clip  = self.cmd_processor.transform_star_shell( self.undo_clip )
        if is_done :
              pyperclip.copy( new_clip  )
              self.old_clip    = new_clip
              self.gui.write_gui_wt( did_what, new_clip  )
        else:
             #rnot a fileis_done false"
             self.gui.write_gui_wt( "did nothing redo_star_shell", new_clip  )

    #  ------------------
    def redo_insert_spaces( self, ):
        """
        v3 called from gui
        !! make more general purpose and call with transform function
        """
        print("redo_insert_spaces "  + self.undo_clip )
        is_done, did_what, new_clip  = self.cmd_processor.transform_insert_spaces( self.undo_clip )
        if is_done :
              pyperclip.copy( new_clip  )
              self.old_clip    = new_clip
              self.gui.write_gui_wt( did_what, new_clip  )
        else:
             #rnot a fileis_done false"
             self.gui.write_gui_wt( "did nothing redo_insert_spaces", new_clip  )

    #  ------------------
    def redo_off( self, ):
        """
        v3 called from gui
        get back the old text
        """
        #print( "redo_off "  + self.undo_clip )
        new_clip         = self.undo_clip
        self.old_clip    = new_clip
        pyperclip.copy( new_clip )
        self.gui.write_gui_wt( "redo_off get back clipped", new_clip  )

    # ----------------------------------
    def redo_unformatted( self, ):
        self.redo_off()    # same as

    # ----------------------------------
    def redo_star_line( self, ):
        self.redo_function( self.cmd_processor.transform_star_line  )
    # ----------------------------------
    def redo_cap( self, ):
        self.redo_function( self.cmd_processor.transform_cap  )
    # ----------------------------------
    def redo_lower( self, ):
        self.redo_function( self.cmd_processor.transform_lower  )
    # ----------------------------------
    def redo_comma_sep( self, ):
        self.redo_function( self.cmd_processor.transform_comma_sep  )
    # ----------------------------------
    def redo_undent( self, ):
        self.redo_function( self.cmd_processor.transform_un_dent  )
    # ----------------------------------
    def redo_no_ws( self, ):
        self.redo_function( self.cmd_processor.transform_no_ws  )
    # ----------------------------------
    def redo_less_ws( self, ):
        self.redo_function( self.cmd_processor.transform_less_ws  )
    # ----------------------------------
    def redo_transform_sage( self, ):
        self.redo_function( self.cmd_processor.transform_sage  )
    # ----------------------------------
    def redo_test( self, ):
        self.redo_function( self.cmd_processor.transform_alt_line_sort  )

    # ----------------------------------
    def redo_x_file_up( self, ):
        self.redo_function( self.cmd_processor.transform_upload_log  )



     # ----------------------------------
    def redo_transform_user( self, ):
        self.redo_function( self.cmd_processor.transform_user_pages  )

    # ----------------------------------
    def redo_alt_line_sort( self, ):
        self.redo_function( self.cmd_processor.transform_alt_line_sort  )
    # ---------------------------------
    def redo_url_to_helpdb( self, ):
        self.redo_function( self.cmd_processor.transform_url_to_helpdb  )

    # ----------------------------------
    def chain_transform( self, ):
        #rint("chain transform")
        self.undo_clip      = self.old_clip

    # ----------------------------------
    def redo_function( self, foo ):
        """
        # foo is the function for the transformation
        #rint( "redo_function foo "  + self.undo_clip )
        """
        is_done, did_what, new_clip  = foo( self.undo_clip )
        if is_done :
              pyperclip.copy( new_clip  )
              self.old_clip   = new_clip
              self.gui.write_gui_wt( did_what, new_clip  )

        else:
             #rnot a fileis_done false"
             self.gui.write_gui_wt( "redo did nothing", self.old_clip  )


    # ==================== commands cmd ===================
    # ------------------------------------------
    def redo_if_star_cmd( self,   ):  #
          # v3 in test now will take out the if at some point
          #self.redo_one_command_transform( self.cmd_processor.do_if_url_cmd( a_string ) )
          #self.redo_one_command( self.cmd_processor.do_if_star_cmd  )

#          cmds_checked     = [ "*>" ]
          self.redo_one_command( self.cmd_processor.do_cmds, [ "*>" ]  )

    # ------------------------------------------
    def redo_if_pb( self,   ):  # !! not done  what is it

          self.redo_one_command( self.cmd_processor.do_if_url_cmd, [ "*>" ]  )

    # ------------------------------------------
    def redo_if_url( self,   ):

          # old nov 2018
          self.redo_one_command(  self.cmd_processor.do_if_url_cmd, [ "*>url" ]  )
          self.redo_one_command(  self.cmd_processor.do_if_url_cmd, [ "*>url" ]  )

    # ------------------------------------------
    def redo_if_text( self,  ):
          self.redo_one_command( self.cmd_processor.do_cmds, [ "txt" ] )
          """
          do_if_file_name
          """
    # ------------------------------------------
    def redo_one_ct_difn( self, a_string   ):
          self.redo_one_command_transform( self.cmd_processor.do_if_file_name( a_string ) )

    # ------------------------------------------
    def redo_one_command( self, a_cmd, cmds_checked  ):
        """
        cmd should be one of cmd_processor.do_if.....  -- revise for v3 just starting
        call from gui thread
        get string from last command
        not clear what one command means, try to change the name
        """
        # a_cmd = self.cmd_processor.do_if_file_name
        #rint "=============== redo ============="
        #rint( self.undo_clip )
        ( is_done, did_what, ret_text )  = a_cmd( self.undo_clip, cmds_checked )     # self.command_transform( self.undo_clip  )

        if is_done:
            # self.old_clip   = self.undo_clip
            self.old_clip  =  ret_text
            pyperclip.copy( ret_text  )
            self.gui.write_gui( " ============= " +  did_what  + " =============== \n" +  ret_text  )
        else:
            pass
            # add something here
            #pyperclip.copy( "self.undo_clip" )
            #something like
            #self.gui.write_gui( " =============== undo \n " +  a_string  )

        return

    # ------------------------------------------
    def redo_one_command_transform( self, a_string, a_cmd ):
        """
        """
        ( is_done, did_what, ret_text )  = a_cmd( self.undo_clip )     # self.command_transform( self.undo_clip  )

        if is_done:
            # self.old_clip   = self.undo_clip
            self.old_clip  =  ret_text
            pyperclip.copy( ret_text  )
            self.gui.write_gui( " =============== " +  did_what + " \n " +  ret_text  )
        else:
            pass
            # add something here

            #pyperclip.copy( "" )
            #something like
            #self.gui.write_gui( " =============== undo \n " +  a_string  )

    # ------------------------------------------
    def undo_transform( self,   ):
        """
        used, maybe done right ??
        """
        self.old_clip   = self.undo_clip
        pyperclip.copy( self.undo_clip )
        self.gui.write_gui_wt( "undo", self.undo_clip )

    # ----------------------------------------------
    def os_open_logfile( self,  ):
        """
        used as callback from gui button
        """
        proc = Popen( [ self.parameters.ex_editor, self.parameters.pylogging_fn ] )

    # ----------------------------------------------
    def os_open_snippets( self,  ):
        """
        used as callback from gui button
        what to do depends on wheather the parameter is a file name or list

        """
        snippet_list  = self.parameters.snippets_fn

        if not isinstance( snippet_list, str ):
            mutuable_dict    = { "snippet_list": snippet_list }
            gui_snippets.SnippetFilesDialog( mutuable_dict )

        else:
             proc = Popen( [ self.parameters.ex_editor, snippet_list ] )

    # ----------------------------------------------
    def os_open_snip_file( self,  ):
        """
        used as callback from gui button
        """
        proc = Popen( [ self.parameters.ex_editor, self.parameters.snip_file_fn ] )
    # ----------------------------------------------
    def os_open_help( self,  ):
        """
        used as callback from gui button
        """
        proc = Popen( [ self.parameters.ex_editor, self.parameters.help_fn ] )

    # ----------------------------------------------
    def os_open_parmfile( self,  ):
        """
        used as callback from gui button
        """
        a_filename = self.starting_dir  + os.path.sep + "parameters.py"

        from subprocess import Popen, PIPE  # since infrequently used ??
        proc = Popen( [ self.parameters.ex_editor, a_filename ] )

    # ----------------------------------------------
    def snip_file_select( self, event ):
        """
        """
        # !! put filename in the clipboard
        #rint "list_box_select: ", event.x, event.y,  event.widget, event.widget.selection_get()
        akey  = event.widget.selection_get()
        print( akey )
        snippet = self.snip_files[ akey ]    # ?? error handeling
        print( snippet )
        #( is_done, did_what, ret_text )  = self.cmd_processor.do_if_edit_text_file( snippet )

        ( is_done, did_what, ret_text )  = self.cmd_processor.do_if_ext_with( snippet, None, self.parameters.snip_file_command  )
        if is_done:
            self.old_clip  =  ret_text     # is this right ???yes  maybe in return
            pyperclip.copy(  ret_text  )
            #self.gui.write_out( ret_text )
            self.gui.write_gui_wt( "oppening file (idle or text or... )  ", snippet  )
            ## put filename in the clipboard
            return  # ( is_done, did_what, ret_text )
        else:
            self.gui.write_gui_wt( "did nothing", snippet  )
            return

    # ----------------------------------------------
    def snippet_select( self, event ):
        #rint "list_box_select: ", event.x, event.y,  event.widget, event.widget.selection_get()
        akey      = event.widget.selection_get()
        snippet   = self.snippets[ akey ]    # ?? error handeling

        self.old_clip    = snippet
        self.undo_clip   = self.old_clip
        pyperclip.copy(  self.old_clip  )
        #self.logger.info( "new_clip = " +  new_clip  )
        self.gui.write_gui_wt( "snippet", self.old_clip )

    # ----------------------------------
    def remote_dialog_bcb(self ):
        self.gui_remote.show_it()
        print( "back from gui_remote" )

# ------------------------------------------
if __name__ == "__main__":

    #try:
        a_app = App( None, None )
    #except Exception as exception:
#        msg   = "exception in __main__ run the app -- it will end"
#        a_app.logger.critical( msg )
#        a_app.logger.critical( exception,  stack_info=True )   # just where I am full trace back most info
#        raise
#
#    #finally:
#        print( "here we are done with clipboard" )
#        sys.stdout.flush()
#



# ======================= eof =======================






