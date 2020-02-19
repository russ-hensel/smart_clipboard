# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 21:06:50 2017

@author: Russ

 for clipboard
typical use
from app_global import AppGlobal

self.parameters          = AppGlobal.parameters
AppGlobal.parameters     = self

"""


import sys
import webbrowser
from   subprocess import Popen
from   pathlib import Path
import os
import psutil
from   tkinter import messagebox
import logging


# ----------------------------------------------

def addLoggingLevel( levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

     How to add a custom loglevel to Python's logging facility - Stack Overflow
     *>url  https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """

    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       #raise AttributeError('{} already defined in logging module'.format(levelName))
       return   # assum already set up ok -- could cause error in comtaminated environment

    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, *args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot )


# ===============================
class OSCall( object, ):
    """
    try to call os based on attempts with different utilities
    in different operating systems
    """
    #------------------------
    def __init__(self, command_list, ):
        """
        command list is the list of utilities to try, a list of strings
        command_aux: like command list but may be a list, a single string, or none, see code

        """
        self.command_list = []
        self.add_command( command_list )

    # ----------------------------------------------
    def add_command( self, more_command_list ):
        """
        add a command at the beginning and re init the list
        call internally at init or externally ( parameters ) to add to list
        """
        print( f"adding {more_command_list}")
        if more_command_list is None:
            self.command_list        = more_command_list     # [   r"D:\apps\Notepad++\notepad++.exe", r"gedit", r"xed", r"leafpad"   ]   # or init from parameters or put best guess first

        else:
            if type( more_command_list ) ==  str:
                more_command_list  = [ more_command_list ]
            # else we expect a list
            self.command_list = more_command_list + self.command_list

        self.ix_command          = -1
        self.working_command     = None
        print( f"command list now{self.command_list}")

    # ----------------------------------------------
    def get_next_command( self,  ):
        """
        what it says
        None if cannot find one ( at end of list )
        """
        self.ix_command += 1
        if         self.ix_command >= len( self.command_list ):
            ret =  None
        else:
            ret =         self.command_list[ self.ix_command ]
#        print( f"command = { self.ix_command} {ret} ", flush = True )
        return ret

    # ----------------------------------------------
    def os_call( self, cmd_arg,  ):
        """
        make an os call trying various utilities until one works

        """
#        proc = Popen( [ cls.parameters.ex_editor, txt_file ] )
        while True:   # will exit when it works or run out of editors
            a_command    = self.working_command
            if  a_command is None:
                a_command  = self.get_next_command( )

            if a_command is None:   # still
#                    msg = "Run out of editors to try"
#                    cls.logger.error( msg )
                    raise RuntimeError( msg )
                    break  # think we are aread done
            try:
                if cmd_arg is None:
                    proc = Popen( [ a_command,  ] )
                else:
                    proc = Popen( [ a_command, cmd_arg ] )
                self.working_command  = a_command
                break  # do not get here if exception
            except Exception as excpt:
                pass     # this should let us loop
#                 cls.logger.error( "os_open_logfile exception trying to use >" + str( cls.parameters.ex_editor ) + "< to open file >" + str( cls.parameters.pylogging_fn ) +
#                                  "< Exception " + str( excpt ) )


# ===============================
class AppGlobal( object ):
    """
    manages parameter values for all of Smart Terminal app and its various data logging
    and monitoring applications
    generally available to most of the application through the Controllers instance variable
    """
    controller              = None
    parameters              = None
    logger                  = None      # should be set when logger is configured
    logger_id               = None
    #scheduled_event_list    = "None"
    #helper                  = "None"

    force_log_level         = 99    # value to force logging, high but not for errors
    fll                     = force_log_level   # shorthand

    # gui                     = None      # populated by the gui

    #helper                  = None      # populated externally by...
    #helper_thread_id        = None      # set by run in helper thread
    main_thread_id          = None
    logger_id               = None      # populated by the controller
    scheduled_event_list    = None      # populated externally by... -- think dead


#    live_graph_opt          = 1         # 1 = all in helper                this is just an experiment

    text_editors            = [   r"D:\apps\Notepad++\notepad++.exe", r"C:\apps\Notepad++\notepad++.exe",
                                  r"gedit", r"xed", r"leafpad"   ]   # or init from parameters or put best guess first

    text_editors            = [   r"gedit", r"xed", r"D:\apps\Notepad++\notepad++.exe", r"C:\apps\Notepad++\notepad++.exe",
                                  r"gedit", r"xed", r"leafpad", r"mousepad"  ]

    file_explorer           = OSCall( [ r"explorer",    ] )
    file_text_editor        = OSCall( text_editors,  )

    # for the hours in the gui and their conversion to time
    dd_hours                = [ "0 Begin Day","01 - 1am","02 2am","03 3am","04 4am","05 5am","06 6am","07 7am","08 8am","09 9am","10 10am","11 11am","12 12am Noon",
                             "13 - 1pm","14 2pm","15 3pm","16 4pm","17 5pm","18 6pm","19 7pm","20 8pm","21 9pm","22 10pm","23 11pm",  ]

    # cls not yet defined
    # this gives the name notice to force_log_level... perhaps a better name might be used
    addLoggingLevel( "Notice", force_log_level, methodName=None)




    # -----------------------
    def __init__(self,  controller  ):
        """
        use as singleton as a class never instance
        """
        y=1/0





    # ----------------------
    def state_info():
        """
        return some info as a list that might be diagonistic, print or log
        perhaps at end of app

        """
        info_list   = []
        #info_list   += AppGlobal.__dir__()
        info_list   += dir( AppGlobal )

        return info_list
        #AppGlobal.state_info( )


    #--------------------------------
    @classmethod
    def print_debug( cls, msg  ):  #
        """
        very temp   AppGlobal.print_debug( msg )
        all shoudl be removed ??
        !! add a level or can the print output be added as a handler
        """
        if cls.logger.getEffectiveLevel() <=  logging.DEBUG :
            print( msg, flush = True )
        cls.logger.debug( msg )


    # ----------------------------------------------
    @classmethod
    def os_open_help_file( cls, help_file ):
        """
		what it says
        see parameters for different types of files and naming that will work with this
        """
        #help_file            = self.parameters.help_file
        if help_file.startswith( "http:" ) or help_file.startswith( "https:" ):
           ret  = webbrowser.open( help_file, new=0, autoraise=True )    # popopen might also work with a url
#           print( f"help http: {help_file} returned {ret}")
           return

        a_join        = Path(Path( help_file ).parent.absolute() ).joinpath( Path( help_file ).name )
#        print( f"a_join {type( a_join )} >>{a_join}<<" )

        #if a_join.endswith( ".txt" ):
        if a_join.suffix.endswith( ".txt" ):
            cls.os_open_txt_file( str(a_join) )
            return

        file_exists   = os.path.exists( a_join )
        print( f"file {a_join} exists >>{file_exists}<<" )
        #full_path     = Path( help_file ).parent.absolute()
#        print( f"a_join {a_join}" )
        help_file     = str( a_join )

        ret = os.popen( help_file )
#        print( f"help popopen  {help_file} returned {ret}")

    # ----------------------------------------------
    @classmethod
    def about( cls,   ):
        """
		show about box -- might be nice to make simple to go to url ( help button )
        """
        url   =  r"http://www.opencircuits.com/SmartPlug_Help_File"
        __, mem_msg   = cls.show_process_memory( )
        msg  = f"{cls.controller.app_name}  version:{cls.controller.version} \n  by Russ Hensel\n  Memory in use {mem_msg} \n  Check <Help> or \n     {url} \n     for more info."
        messagebox.showinfo( "About", msg,  )   #   tried ng: width=20  icon = "spark_plug_white.ico"


    # ----------------------------------------------
    @classmethod
    def show_process_memory( cls, call_msg = "", log_level = None, print_it = False ):
        """
        log and/or print memory usage
        """
        process      = psutil.Process(os.getpid())    #  import psutil
        mem          = process.memory_info().rss
        # convert to mega and format
        mem_mega     = mem/( 1e6 )
        msg          = f"{call_msg}process memory = {mem_mega:10,.2f} mega bytes "
        if print_it:
            print( msg )
        if not ( log_level is None ):
            cls.logger.log( log_level,  msg )
        msg           =  f"{mem_mega:10,.2f} mega bytes "
        return ( mem, msg )

    # ----------------------------------------------
    @classmethod
    def log_if_wrong_thread( cls, id, msg = "forgot to include msg", main = True ):
        """
        debugging aid
        check if called by intended thread
        main thread must be set first
        ex:   AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )
        """
        on_main = ( id == cls.main_thread_id )

        if main:
            ok  = on_main
        else:
            ok = not( on_main )

        if not ok:
            msg    = f"In wrong thread = {cls.name_thread( id )}: + {msg}"
            cls.logger.log( cls.force_log_level,  msg )

    # ----------------------------------------------
    @classmethod
    def name_thread( cls, id, ):
        """
        return thread name Main/Helper
        ex call:  AppGlobal.name_thread( threading.get_ident(),  )
        """
        if  cls.main_thread_id is None:
            y= 1/0   # cheap exception when main_thread not set up

        if id == cls.main_thread_id:
            ret = f"Main"
        else:
            ret = f"Helper"

        return ret

    # ----------------------------------------------
    @classmethod
    def thread_logger( cls, id, call_msg = "", log_level = None ):
        """
        debugging aid
        log a message, identifying which thread it came from
        ex call: AppGlobal.thread_logger( threading.get_ident(), "here we are", 50  )
        """
        thread_name   = cls.name_thread( id )
        msg  = f"in {thread_name} thread>> {call_msg}"

        if not ( log_level is None ):
            cls.logger.log( log_level,  msg )

   # ----------------------------------------------
    @classmethod
    def os_open_help_file( cls, help_file ):
        """
		what it says
        see parameters for different types of files and naming that will work with this
        """
        #help_file            = self.parameters.help_file
        if help_file.startswith( "http:" ) or help_file.startswith( "https:" ):
           ret  = webbrowser.open( help_file, new=0, autoraise=True )    # popopen might also work with a url
#           print( f"help http: {help_file} returned {ret}")
           return

        a_join        = Path(Path( help_file ).parent.absolute() ).joinpath( Path( help_file ).name )
#        print( f"a_join {type( a_join )} >>{a_join}<<" )

        #if a_join.endswith( ".txt" ):
        if a_join.suffix.endswith( ".txt" ):
            cls.os_open_txt_file( str(a_join) )
            return

        file_exists   = os.path.exists( a_join )
        print( f"file {a_join} exists >>{file_exists}<<" )
        #full_path     = Path( help_file ).parent.absolute()
#        print( f"a_join {a_join}" )
        help_file     = str( a_join )

        ret = os.popen( help_file )
#        print( f"help popopen  {help_file} returned {ret}")

    # ----------------------------------------------
    @classmethod
    def os_open_help_file( cls, help_file ):
        """
		what it says
        see parameters for different types of files and naming that will work with this
        """
        #help_file            = self.parameters.help_file
        if help_file.startswith( "http:" ) or help_file.startswith( "https:" ):
           ret  = webbrowser.open( help_file, new=0, autoraise=True )    # popopen might also work with a url
#           print( f"help http: {help_file} returned {ret}")
           return

        a_join        = Path(Path( help_file ).parent.absolute() ).joinpath( Path( help_file ).name )
#        print( f"a_join {type( a_join )} >>{a_join}<<" )

        #if a_join.endswith( ".txt" ):
        if a_join.suffix.endswith( ".txt" ):
            cls.os_open_txt_file( str(a_join) )
            return

        file_exists   = os.path.exists( a_join )
        print( f"file {a_join} exists >>{file_exists}<<" )
        #full_path     = Path( help_file ).parent.absolute()
#        print( f"a_join {a_join}" )
        help_file     = str( a_join )

        ret = os.popen( help_file )
#        print( f"help popopen  {help_file} returned {ret}")

    # ----------------------------------------------
    @classmethod
    def os_open_txt_file( cls, txt_file ):
        """
        open a text file with system configured editor
		?? could check for validity of the editor or use try except
        """
        cls.file_text_editor.os_call( txt_file )


     # ----------------- debuging ----------------
    def to_str():
        """
        debug aid, but dead
        convert some of AppGlobals contents to a string for debugging - left over from some other app
        might revive or delete
        """
        a_string   = (   "AppGlobal" +
                                  str (AppGlobal.parameter_dicts ) +
                           "\n    ---------- greenhouse ----------\n" + str( AppGlobal.parameter_dicts["greenhouse"]) )
        return a_string

    def print_me():
         sys.stdout.flush()
         print("========== AppGlobal =================")
         print( AppGlobal.to_str( ) )
         sys.stdout.flush()




# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    print( "" )
    print( " ========== starting ScheduleMe from sch_me.py ==============" )
#    import sch_me
#    a_app = sch_me.ScheduleMe(  )

    print( AppGlobal.state_info( ) )

# ======================== eof ======================