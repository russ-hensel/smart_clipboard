# -*- coding: utf-8 -*-

"""
#   parameters    for  clip_board.py
#   some junk and unimplemented parms, !! clean up
#    for clipboard
"""

import logging
import sys
from   app_global import AppGlobal
import os

import running_on

# ========================================
class Parameters( object ):
    """
    manages parameter values use like ini file
    a struct but with a few smarts
    """
    def __init__( self, ):

        self.controller        = AppGlobal.controller    # save a link to the controller not actually used now
        #self.parameters    = AppGlobal.parameters
        AppGlobal.parameters   = self
        # ---------  os platform... ----------------
        self.default_config()
        self.os_tweaks( )
        self.computer_name_tweaks()


        # same mode does not work on both so a final tweak
        if self.computername == "smithers":
             self.russ_1_mode()

        elif self.computername == "millhouse":
             self.millhouse_1_mode()

        else:
             self.russ_1_mode()

    # -------
    def russ_1_mode( self ):
        """
        first mode for smithers
        """
        self.mode               = "Russ_1"

        self.logging_level      = logging.DEBUG

        # ----- snip or example files
        self.snip_file_fn       = "snip_files_1.txt"
        self.snip_file_fn       = r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\snips_file_test.txt"
        self.snip_file_fn       = r"snips_file_test.txt"
        #D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\snip_files_nov_18.txt
        self.snip_file_fn       =   r"snip_files_nov_18.txt"
#        self.snip_file_fn       = [ r"snip_files_nov_18.txt", r"snip_files_nov_18.txt" ]
        self._read_snip_files_( self.snip_file_fn )

        # ----- snippets
        self.snippets_fn        = "snippetts_1.txt"

#        self.snippets_fn        = [ "snippetts_1.txt", "snippetts_1.txt" ]   # multiple snippet files
        self.snippets_sort      = True
        # how about a delete dups ??

#        self._read_snippets_(   self.snippets_fn  )
        self._read_list_of_snippets_( self.snippets_fn  )

        # read the snippets
#        self._read_list_of_snip_files_( self.snippets_fn )  # read the snippets


    # -------
    def millhouse_1_mode( self ):
        """
        """
        self.mode               = "millhouse_1"

        self.logging_level      = logging.DEBUG
        self.logging_level      = logging.INFO
        # ----- snip or example files

        self.snip_file_fn       = "snip_files_1.txt"
        self.snip_file_fn       = r"c:\Russ\0000\python00\python3\_projects\clipboard\Ver3\snips_file_test.txt"
        self.snip_file_fn       = r"snips_file_test.txt"
        #D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\snip_files_nov_18.txt
        self.snip_file_fn       =   r"snip_files_nov_18.txt"
#        self.snip_file_fn       = [ r"snip_files_nov_18.txt", r"snip_files_nov_18.txt" ]
        self._read_snip_files_( self.snip_file_fn )

        # ----- snippets
        self.snippets_fn        = "snippetts_1.txt"

        # self.snippets_fn        = [ "snippetts_1.txt", "snippetts_1.txt" ]
        self.snippets_sort      = True
        # how about a delete dups ??

#        self._read_snippets_(   self.snippets_fn  )
        self._read_list_of_snippets_( self.snippets_fn  )

        # read the snippets
#        self._read_list_of_snip_files_( self.snippets_fn )  # read the snippets

    # -------
    def test_mode( self ):
        self.mode              = "Test"
        pass

    # -------
    def running_on_tweaks(self,  ):
        """
        use running on tweaks as a more sophisticated  version of os_tweaks and computer name tweaks,
        """
        computer_id    =   self.running_on.computer_id

        if computer_id == "smithers":
            self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"
            self.db_file_name       =  "smithers_db.db"

        elif computer_id == "millhouse":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.win_geometry   = '1300x600+20+20'
            self.db_file_name       =  "millhouse_db.db"

        elif computer_id == "theprof":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            self.db_file_name       =  "the_prof_db.db"

        elif computer_id == "bulldog":
            self.ex_editor          =  r"gedit"
            self.db_file_name       =  "bulldog_db.db"

        elif computer_id == "bulldog-mint-russ":
            self.ex_editor          =  r"xed"
            self.db_file_name       =  "bulldog_db.db"

        else:
            print( f"In parameters: no special settings for computer_id {computer_id}" )
            if self.running_on.os_is_win:
                self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            else:
                self.ex_editor          =  r"leafpad"    # linux raspberry pi maybe

    # -------
    def os_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_ _mode"
        for particular operating systems
        you may need to mess with this based on your os setup


        D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\clipboard_b.ico   seems much to dark
        D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\clipboard_c.ico


        """
        if  self.os_win:
            pass
            self.icon               = r"./clipboard_b.ico"    #  very dark greenhouse this has issues on rasPi
            self.icon               = r"./clipboard_b_red_GGV_icon.ico"     #  looks same as clipboard_b_red_gimp.ico
#            self.icon               = r"./clipboard_b_red2.gif"  #  looks same as clipboard_b_red_gimp.ico
            self.icon               = r"./clipboard_b_red_gimp.ico"    # pretty visible

            #self.icon              = None                    #  default gui icon

        else:
            pass

    # -------
    def computer_name_tweaks( self ):
        """
        this is an sufroutine to tweak the default settings of "default_mode"
        for particular computers.  Put in settings for you computer if you wish
        these are for my computers, add what you want ( or nothing ) for your computes
        !! use computer name or id ??
        """
        print(self.computername, flush=True)

        if self.computername == "smithers":
            self.win_geometry       = '1250x700+20+20'      # width x height position
            self.ex_editor          =  r"c:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

        elif self.computername == "millhouse":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"    # russ win 10 millhouse
            self.win_geometry       = '1000x700+250+5'          # width x height position
            self.pylogging_fn       = "millhouse_clipboard.py_log"   # file name for the python logging
            self.snip_file_fn       = r"C:\Russ\0000\python00\python3\_projects\clipboard\Ver3\snips_file_auto.txt"
            # need to associate with extension -- say a dict
            self.snip_file_command  = r"C:\apps\Notepad++\notepad++.exe"  #russwin10   !! implement

        elif self.computername  == "theprof":
            self.ex_editor          =  r"c:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

    # ------->> Subroutines:  one for each mode alpha order - except tutorial
    # -------
    def default_config( self ):

        self.mode              = "default_config"

        #--------------- automatic settings -----------------

        self.running_on   = running_on.RunningOn
        self.running_on.gather_data()

        # some of the next all?? should be moved over to RunningOn
        self.running_on.log_me( logger = None, logger_level = 10, print_flag = True )
        self.py_path       = self.running_on.py_path

        self.set_default_path_here  = True  # may be tricky to reset, but we may have the original dir in running on

        if  self.set_default_path_here:    # Now change the directory to location of this file

            py_path    = self.running_on.py_path

            # retval = os.getcwd()
            # print( f"Directory now            {retval}")

            print( f"Directory now ( sw if not ''  {os.getcwd()} change to >>{py_path}<<")
            if py_path != "":
                os.chdir( py_path )

        self.our_os             =   self.running_on.our_os
        self.os_win             =   self.running_on.os_win

        self.computername       = self.running_on.computername

        self.opening_dir        = self.running_on.opening_dir


#        print( "our_os is ", our_os )

        #if our_os == "linux" or our_os == "linux2"  "darwin":

        if self.our_os == "win32":
            self.os_win = True     # right now windows and everything else
        else:
            self.os_win = False

        self.platform           = self.our_os    # sometimes it matters which os



        self.snippets           = None       # define later
        self.snip_files         = None       # define later

        self.title              = "ClipBoard Utility"   # window title  !! drop for name version
        self.icon               = r"D:\Temp\ico_from_windows\terminal_blue.ico"    #"icon.ico"  ?? not implementd
        self.icon               = "clipboard.png"       #"icon.ico"  ?? throws  not implementd error
        self.icon               = r"D:\Russ\0000\SpyderP\SmartTerminal\smaller.ico"    #  greenhouse will rename
        self.icon               = r"D:\Russ\0000\SpyderP\ClipBoardStuff\clipboard_c.ico"
        self.icon               = r"clipboard_c.ico"

        self.id_color           = "red"                # ?? not implementd

        self.win_geometry       = '1500x800+20+20'     # width x height position
        self.win_geometry       = '900x600+700+230'     # width x height position  x, y

        self.pylogging_fn       = "clipboard.py_log"   # file name for the python logging
        self.logging_level      = logging.DEBUG        # logging level DEBUG will log all catured text !
        #self.logging_level      = logging.INFO
        self.logger_id          = "clip_board"         # id in logging file

        # ------------- file names -------------------

        # this is the name of a program: its excutable with path inof.
        # to be used in opening an exteranl editor
        self.ex_editor         =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10

        # if we are writing scratch files to run in a shell or similar.
        self.scratch_bat       =  r"scratch.bat"   # rel or absolute?
        self.scratch_py        =  r"scratch.py"    # rel or absolute?

        self.run_py            =  r"c:\apps\Notepad++\notepad++.exe"    # program to run *>py commands  !! not implemented

        # files for text editing
        self.text_extends = [  ".txt",  ".rsh", ".ino", ".py", ".h" , ".cpp", ".py_log", ".log", ]  # include the dot! add?? log py_log

        # ----------------- junk ---------------

        self.startup_sec       = 10   # expected startup time 10 for smithers

        #  example use as if self.controller.parameters.os_win:

        # ========================= buttons ======================
        #------------------------- check box ---------------

        self.cmd_on            = 1     # 1 is checked or on else 0
        self.auto_url_on       = 0
        self.star_cmd_on       = 0
        self.exe_file_on       = 0

        #------------------------- radio buttons ---------------

        self.rb_num_on          = 0      # which radio button on, number is not nice, but easy !! is working ???

        self.help_fn            = "help.txt"  # old phase out

        # help file can be web ( open with browser ), or txt ( open with self.editor ) or anything else ( will try to shell out may or may not work )
        self.help_file       =  self.py_path + "/" + "help.txt"   #  >>. this is the path to our main .py file self.py_path + "/" +
        self.help_file       =  "http://www.opencircuits.com/SmartPlug_Help_File"   # can be url or a local file -- change for clipboard !!

        self.help_fn            = self.help_file    # old phase out

        # ================== snippest ============================

        self.snippets_sort      = True                # sort snippes on key, else in file order
        self.snippets_fn        = "snippetts_1.txt"

        self.snip_file_sort     = True
        self.snip_file_fn       = "snip_files_1.txt"
        self.snip_file_fn       = "snip_files_2.txt"
        self.snip_file_fn       = r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\snips_file_auto.txt"
        # need to associate with extension -- say a dict
        self.snip_file_command  = r"c:\apps\Notepad++\notepad++.exe"  #russwin10   !! implement
        #self.snip_file_command  = r"D:\apps\Anaconda\Lib\idlelib\idle.bat"
        # self.ex_editor=r"D:\apps\Notepad++\notepad++.exe"#russwin10

#        self._read_snippets_(   self.snippets_fn  )       # read the snippets
#        self._read_snip_files_( self.snip_file_fn )

        self.max_history       = 9          # !! not implemented  -- maybe never
        #---------------------------------------------------

        self.transform         = "off"   #["","",]  !! is what
        self.max_lines         = 10         # max number of lines logging  !! remove see history
        # befor older lines are truncated
        # limits memory used  0 for unlimited
        self.default_scroll    = 1          # 1 auto scroll the recieve area, else 0  not implemnted drop ??

        self.poll_delta_t      = 200        # how often wee poll for clip changes, in ms

# ------------  Internal Subs Generally should not be modified  -----------------------
    # -----------------------------------
    def _read_list_of_snip_files_( self, file_name ):

        pass
    #--------------- old replace with above then delete this
    def _read_snip_files_( self, file_name ):
        with open( file_name ) as f:
            lines = f.readlines()

        lines_no_comments = list( filter( lambda i_line: not( i_line.startswith( "#" ) ), lines ) )
        lines = lines_no_comments

        #or with stripping the newline character:

        #lines = [line.strip() for line in open('filename')]
        #print lines
        self.snip_files         = []
        snip_name  = ""
        marker     = ">>>>>"   # len of 5 scanning files
        ix_start_snip  = 0
        ix_end_snip    = 0
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
                    a_clip = ( snip_name, snip_body )
                    self.snip_files.append( a_clip )
                    # begin snip
                snip_name        = i_line[ 5: ]
                ix_start_snip    = ix_line + 1
                ix_end_snip      = ix_start_snip
            else:
                ix_end_snip    += 1
                # ---------------------

        if self.snip_file_sort:
                a_list = sorted( self.snip_files, key=lambda data: data[0] )
                self.snip_files  = a_list

        return
        # print( self.snip_files  )

    # -----------------------------------
    #--------------- old replace with above then delete this
    def _read_list_of_snippets_( self, list_of_file_names ):
        """
        read snippets from a list of files or a string with a file name
        consider a bit of cleanup of lines at end
        not very pythonic
        entry is a line with title, and one or my lines of content


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
                    snip_body     = "".join( lines[ ix_start_snip:ix_end_snip  ] )    # /n is already in file?
                    a_clip = ( snip_name, snip_body )
                    self.snippets.append( a_clip )
                    # begin snip
                snip_name        = i_line[ 5: ]
                ix_start_snip    = ix_line + 1
                ix_end_snip      = ix_start_snip
            else:
                ix_end_snip    += 1
                # ---------------------
        # lets add a sort here -- may make optional or its own function ?
        if self.snippets_sort:
            a_list        = sorted( self.snippets, key=lambda data: data[0] )
            self.snippets = a_list

    # -----------------------------------
    def _sort_snippets_( self, ):
        """
        see above
        """
        pass

    # -----------------------------------
    def _read_snippets_( self, file_name ):
        """
        read snippets from a file
        consider a bit of cleanup of lines at end
        not very pythonic
        """
        with open( file_name ) as f:
            lines = f.readlines()
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
                    snip_body     = "".join( lines[ ix_start_snip:ix_end_snip  ] )    # /n is already in file?
                    a_clip = ( snip_name, snip_body )
                    self.snippets.append( a_clip )
                    # begin snip
                snip_name        = i_line[ 5: ]
                ix_start_snip    = ix_line + 1
                ix_end_snip      = ix_start_snip
            else:
                ix_end_snip    += 1
                # ---------------------

        if self.snippets_sort:
                a_list = sorted( self.snippets, key=lambda data: data[0] )
                self.snippets   = a_list

# =================================================

if __name__ == "__main__":
    #----- run the full app
    import  clip_board
    app   = clip_board.App( None, None )

# =================== eof ==============================



