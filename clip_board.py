# -*- coding: utf-8 -*-
#! /usr/bin/python3
#!python3
# above for windows ??
#     /usr/bin/python



"""
this is the main module for the clipboard app

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
def print_uni( a_string_ish ):
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
        self.version           = "Ver 7: 2020 03 17.01"
        # clean out dead
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

        #if  self.parameters.set_default_path_here:    # Now change the directory to location of this file
#        if True:
#            py_path    = self.parameters.running_on.py_path
#
#            # retval = os.getcwd()
#            # print( f"Directory now            {retval}")
#
#            print( f"Directory now ( sw if not ''  {os.getcwd()} change to >>{py_path}<<")
#            if py_path != "":
#                os.chdir( py_path )

        self.config_logger()
        self.prog_info()
       # could combine with above ??

        self.snippets           = None       # define later automatically, leave alone
        self.snip_files         = None       # define later automatically, leave alone

        # this builds a list in parameters that is used by gui to build self.snippets and self.snip_files
        self._read_list_of_snippets_(   self.parameters.snippets_fn  )
        self._read_list_of_snip_files_( self.parameters.snip_file_fn )


        self.snippets_dict       = {}          # predefined stuff for clipboard -- do before gui
        self.snip_files_dict     = {}          # predefined stuff for clipboard -- do before gui

        self.button_dict    = {}          # for the button "case logic"

        # gets gui ref so make before gui
        self.cmd_processor  = cmd_processor.CmdProcessor(  )   # commands processed here

        self.dispatch_dict  =  {  }  # used somewhere for a case or switch like statement

        self.gui            = gui.GUI( self )  # gui references cmd processor and controller

        self.old_clip       = ""          # old value of info in clipboard -- may be transformed - checked to see if clipboad changed
        self.undo_clip      = ""          # old value never transformed for undo

        msg       = "Error messages may be in log file, check it if problems -- check parmeters.py for logging level "
        # print( msg )
        AppGlobal.print_debug( msg )
        self.logger.log( AppGlobal.fll, msg )
        self.polling_delta  = self.parameters.poll_delta_t

        self.starting_dir   = os.getcwd()    # or perhaps parse out of command line
        self.gui.root.after( self.polling_delta, self.polling )

#        self.history         = []      # begin to work on history, not be implemented

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
        AppGlobal.logger_id     = "App"
        logger                  = logging.getLogger( AppGlobal.logger_id )

        logger.handlers = []

        logger.setLevel( self.parameters.logging_level )

        # create the logging file handler
        fh = logging.FileHandler( self.parameters.pylogging_fn )

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # add handler to logger object -- want only one add may be a problem
        logger.addHandler(fh)
        msg  = f"pre logger debug -- did it work"
        AppGlobal.logger.debug( msg )

        logger.info( "Done config_logger .. next AppGlobal msg" )
        #print( "configed logger", flush = True )
        self.logger      = logger   # for access in rest of class?
        AppGlobal.set_logger( logger )

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
#                    msg    = f"polling clip change: \n>>{new_clip}<< {len(new_clip)}\n>>{self.old_clip}<< {len(self.old_clip)}\n"
#                    self.logger.debug( msg  )
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

    # -----------------------------------
    def print_list( self, a_list  ):
        for i_item in a_list:
            print( i_item )

    # some of these should probably not be in parameters
    # -----------------------------------
    def _read_list_of_snip_files_( self, file_name_list  ):
        """
        what it says
        file_name_list, a string or list of file names
        return mutate self.snip_files_dict
                # how about a delete dups ??
        """
        self.snip_files         = []
        if type( file_name_list ) == str:
            file_name_list = [ file_name_list ]

        for i_file in file_name_list:
            self._read_a_snip_file_( i_file )

        if self.parameters.snip_file_sort:
            a_list = sorted( self.snip_files, key=lambda data: data[0] )
            self.snip_files  = a_list
            b_list  = []
            last_snip_body = None
            for i_snip in a_list:
                i_snip_name, i_snip_body    = i_snip
                if not ( i_snip_body == last_snip_body ):
                    b_list.append( i_snip )
                    last_snip_body   = i_snip_body
                else:
                    msg = f"append {i_snip_body}"
                    print( msg )

            self.snip_files = b_list

    #--------------- old replace with above then delete this ??
    def _read_a_snip_file_( self, file_name ):
        """
        what it says
        populates self.snip_files which is a list of tuples ( name of snip, snip file name )
        """
        with open( file_name ) as f:
            lines = f.readlines()

        # filter of list comp ??
        lines_no_comments = list( filter( lambda i_line: not( i_line.startswith( "#" ) ), lines ) )
        lines = lines_no_comments

        #or with stripping the newline character:

        #lines = [line.strip() for line in open('filename')]
        #print lines
        # next now in caller
        #self.snip_files         = []
        snip_name  = ""
        marker     = ">>>>>"   # len of 5 scanning files
        ix_start_snip  = 0     # what
        ix_end_snip    = 0     # what
        for ix_line,i_line in enumerate( lines ):
            # look for name marker
            i_line   = i_line.rstrip()
            a_find   = i_line.find( marker, 0, )
            #rint "a_find ", a_find, i_line
            if a_find == 0:
                # save the old one if any
                if snip_name != "":
                    #snip_body     = "\n".join( lines[ ix_start_snip:ix_end_snip  ] )
                    #snip_body     = "".join( lines[ ix_start_snip:ix_end_snip  ] )
                    snip_body      = lines[ ix_start_snip ].strip()  # there is a crlf to be rid of
                    snip_body      = f"{self.parameters.snip_file_path}/{snip_body}"
                    # test for file exists
                    is_fn          =  os.path.isfile( snip_body )
                    if not is_fn:
                        msg  = f"cannot find snip file {snip_body} while reading {file_name}"
                        print( msg )
                        AppGlobal.logger.error( msg )
                    else:
                        msg  = f"add snip file {snip_body} while reading {file_name}"
                        print( msg )
                        AppGlobal.logger.debug( msg )
                        a_clip = ( snip_name, snip_body )
                        self.snip_files.append( a_clip )
                    # begin snip
                snip_name        = i_line[ 5: ]
                ix_start_snip    = ix_line + 1
                ix_end_snip      = ix_start_snip
            else:
                ix_end_snip    += 1
                # ---------------------

        self.print_list( self.snip_files )
        return
        # print( self.snip_files  )

    # -----------------------------------
    def _read_list_of_snippets_( self, list_of_file_names ):
        """
        read snippets from a list of files or a string with a file name
        consider a bit of cleanup of lines at end
        not very pythonic
        entry is a line with title, and one or more lines of content
        # how about a delete dups ??
        """
        if isinstance( list_of_file_names, str ):
              list_of_file_names  =  [ list_of_file_names ]

        lines  = []
        #read into a list for all files
        for i_file_name in list_of_file_names:
            with open( i_file_name ) as f:
                i_lines = f.readlines()
            lines  +=  i_lines           # seems to beat extend and append is wrong

        # --- process list, first get rid of comment lines
        lines_2    =   [ i_line for i_line in lines  if not( i_line[0] == "#" ) ]
        lines      = lines_2

        self.snippets           = []     # elements will be tuples (  string_name_of_snippet, snip_body_lines_sep_with_/n  )
        snip_name  = ""
        marker     = ">>>>>"   # len of 5
        ix_start_snip  = 0
        ix_end_snip    = 0
        for ix_line,i_line in enumerate( lines ):
            # look for name marker
            i_line   = i_line.rstrip()
            if len( i_line ) > 0:
                if i_line[0] == "#":
                    print( "read_snippets skip " + i_line )
                    continue
            a_find   = i_line.find( marker, 0, )
            #rint "a_find ", a_find, i_line
            if a_find == 0:
                # save the old one if any
                if snip_name != "":
                    #snip_body     = "\n".join( lines[ ix_start_snip:ix_end_snip  ] )
                    snip_body     = "".join( lines[ ix_start_snip:ix_end_snip  ] )    # \n is already in file?
                    a_clip = ( snip_name, snip_body )
                    self.snippets.append( a_clip )
                    # begin snip
                snip_name        = i_line[ 5: ]  # keyed to len of marker, prehaps should code this
                ix_start_snip    = ix_line + 1
                ix_end_snip      = ix_start_snip
            else:
                ix_end_snip    += 1
                # ---------------------
        # added a sort here -- may make optional
        # what about delete dupes ?
        if self.parameters.snippets_sort:
            a_list        = sorted( self.snippets, key=lambda data: data[0] )
            self.snippets = a_list


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
        can we essentially set up in gui.py so is not missed
        !! check to see if up to date
        """
        case = self.gui.button_var.get(  )   # value of the radio button, we will do only one transform ( at least for now later untill one succeeds )
        print("do_transform() for " + str( case ))

        # this first may be special need special management
        # may want to build from the gui or the command processor ( would tighten the coupling - bad )

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
        !! looks like this and above need to be combined
        input in_text return transformed -- checks gui to see if enabled
        return done flag and success message and transformed text all in tuple
        ex: ( False,"did_what" "new_text" )
        only one can be chosen at a time
        move to a dict or list implementation??
        can we essentially set up in gui.py so is not missed

        """
        case = self.gui.button_var.get(  )   # value of the radio button, we will do only one transform ( at least for now later untill one succeeds )
        print("do_transform() for " + str( case ))


        return self.do_transform_with_dict(  in_text,  )

    # ------------------------------------------
    def do_commands ( self, in_text,  ):
        """
        v3
        do checked commands if any
        input in_text
        return done flag and transformed text in tuple
        ex: ( False, "what_transform", "transformed text" )
        !! check up to date, may have dropped some commands

        seems still needed
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

    # -----------------
    def button_switcher( self, a_button ):
        """
        call function associated with the button
        pass the usual arguments

        similar to ... self.controller.redo_off,.....

        #self.button_dict[a_button]
        # is_done, did_what, new_clip  = self.cmd_processor.transform_url_wiki( self.undo_clip )
        # these will be cmd_processor like to old redo commands
        """
        is_done, did_what, new_clip  = self.button_dict[a_button]( self.undo_clip )
        if is_done :
              self.old_clip   = new_clip    # fake out sso do not trigger infinite polling changes
              pyperclip.copy( new_clip  )
              self.gui.write_gui_wt( did_what, new_clip  )
        else:
             self.gui.write_gui_wt( "button switcher did nothing", new_clip  )

    #  ------------------
    def redo_off( self, ):
        """
        v3 called from gui
        get back the old text
        but this may mean we always unformat .... look into this ??
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
        what to do depends on weather the parameter is a file name or list

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
        update for multiple files and use of AppGlobal
        """
        proc = Popen( [ self.parameters.ex_editor, self.parameters.snip_file_fn ] )

    # ----------------------------------------------
    def os_open_help( self,  ):
        """
        used as callback from gui button !! change to use appglobal
        """
        AppGlobal.os_open_help_file( AppGlobal.parameters.help_file )

    # ----------------------------------------------
    def os_open_parmfile( self,  ):
        """
        used as callback from gui button  !! change to use appglobal
        """
        # a_filename = self.starting_dir  + os.path.sep + "parameters.py"

        # from subprocess import Popen, PIPE  # since infrequently used ??
        # proc = Popen( [ self.parameters.ex_editor, a_filename ] )

        AppGlobal.os_open_txt_file( "parameters.py" )

    # ----------------------------------------------
    def snip_file_select( self, event ):
        """
        opens the seleted file from the snip file list in the configured editor or ide

        """
        # !! put filename in the clipboard
        #rint "list_box_select: ", event.x, event.y,  event.widget, event.widget.selection_get()
        akey  = event.widget.selection_get()
        print( akey )
        a_snip_file = self.snip_files_dict[ akey ]    # ?? error handling
        print( a_snip_file )
        #( is_done, did_what, ret_text )  = self.cmd_processor.do_if_edit_text_file( snippet )

        # ( is_done, did_what, ret_text )  = self.cmd_processor.do_if_ext_with( snippet, None, self.parameters.snip_file_command  )
        ( is_done, did_what, ret_text )  = self.cmd_processor.do_if_snip_file( a_snip_file, None, self.parameters.snip_file_command  )

        if is_done:
            self.old_clip  =  ret_text     # is this right ???yes  maybe in return
            pyperclip.copy(  ret_text  )
            #self.gui.write_out( ret_text )
            self.gui.write_gui_wt( "opening file (idle or text or... )  ", a_snip_file  )
            ## put filename in the clipboard
            return  # ( is_done, did_what, ret_text )
        else:
            self.gui.write_gui_wt( "snip file seems not to have opened ", a_snip_files  )
            return

    # ----------------------------------------------
    def snippet_select( self, event ):
        """
        switch or case like statement when snippet is clicked on in gui -- called from gui
        should pull snippet out of dict and place in clipboard
        event --

        """
        #rint "list_box_select: ", event.x, event.y,  event.widget, event.widget.selection_get()
        akey             = event.widget.selection_get()
        snippet          = self.snippets_dict[ akey ]    # ?? error handling

        self.old_clip    = snippet
        self.undo_clip   = self.old_clip
        pyperclip.copy(  self.old_clip  )
        #self.logger.info( "new_clip = " +  new_clip  )
        self.gui.write_gui_wt( "snippet", self.old_clip )

    # ----------------------------------
    def remote_dialog_bcb(self ):
        """
        button call back
        not clear what this does or if it works

        """
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






