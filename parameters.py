# -*- coding: utf-8 -*-

"""
   parameters    for  clip_board.py
   some junk and unimplemented parms, !! clean up
   unfortunately this is a moving target, will try to keep documentation up to date

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
        # -------
    def choose_mode( self ):
        """
        typically choose one mode and if you wish add the plus_test_mode
        if you comment all out you get the default mode which should
        run, perhaps while limping
        """
        #self.new_user_mode()
#        self.millhouse_1_mode()

        self.russ_1_mode()

        # --- add on for testing, as desired
        self.plus_test_mode()

    # -------
    def plus_test_mode( self ):
        """
        scratch mode to add tests to other modes
        an add on mode
        """
        self.mode              = self.mode + " + test"  # change with care

        self.logging_level      = logging.DEBUG

        self.snippets_fn        = ["./snipsand/snippetts_test.txt", "./snipsand/snippetts_example.txt" ,"./snipsand/snippetts_1.txt"]
        #self.snippets_fn        = "./snipsand/snippetts_test.txt"

    # -------
    def new_user_mode( self ):
        """
        for a new user to customize, as shipped pretty much a copy of russ_1
        an example mode
        new users should start here for making a mode, you may want to make a copy for reference
        see .default_mode() for some documentation of the variables.
        """
        self.mode               = "New_user"

        self.logging_level      = logging.DEBUG

        # ----- snip or example files
#        self.snip_file_fn       = r"snips_file_test.txt"
#        self.snip_file_fn       = r"snip_files_nov_18.txt"
#        self._read_snip_files_( self.snip_file_fn )

        # ----- snippets
        self.snippets_fn        = "./snipsand/snippetts_example.txt"
        self.snippets_sort      = True


    # ------->> More methods:  one for each mode
    # -------
    def russ_1_mode( self ):
        """
        russ: first mode for smithers -- not documented
        """
        self.mode               = "Russ_1"

        self.logging_level      = logging.DEBUG

        # ----- snip or example files

#        self.snippets_fn        = [ "./snipsand/snippetts_1.txt", "./snipsand/snippetts_1.txt" ]   # multiple snippet files
        self.snippets_sort      = True
        # ================== snippets ============================
        self.snippets_sort      = True                # sort snippes on key, else in file order
        self.snippets_fn        = "./snipsand/snippetts_1.txt"

        # ================== snips ============================
        self.snip_file_sort     = True                # sort make them easier to find in the GUI

        # next:  this is prepended to a snip file prior to opening the file
        #        so you can easily keep the snip files in a place you find convient.
        self.snip_file_path     = r"C:\Russ\0000\python00\python3\_examples"
        #
          # path prepended to all snip files
        self.snip_file_fn       = "./snipsand/snip_files_russ.txt"

        self.snip_editor       = r"C:\apps\Anaconda3\Scripts\thonny.exe"  # editor used for opening snip files

        #self.snip_file_command  = r"c:\apps\Notepad++\notepad++.exe"    #russwin10  opens snip files, nice if can run it

    # -------
    def millhouse_1_mode( self ):
        """
        russ: first mode for millhouse -- not documented
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
#        self.snip_file_fn       = [ r"snip_files_nov_18.txt", r"snip_files_nov_18.txt" ]  #

        # ----- snippets
        self.snippets_fn        = "./snipsand/snippetts_1.txt"

        # self.snippets_fn        = [ "./snipsand/snippetts_1.txt", "./snipsand/snippetts_1.txt" ]
        self.snippets_sort      = True



    # -------
    def running_on_tweaks(self,  ):
        """
        not a mode, a tweak, see documentation
        use running on tweaks as a more sophisticated  version of os_tweaks and computer name tweaks which
        may replace them
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
            self.snip_file_path     = r"D:\Russ\0000\python00\python3\_examples"
            self.win_geometry       = '1450x700+20+20'      # width x height position

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
        this is an subroutine to tweak the default settings of "default_mode"
        for particular operating systems
        you may need to mess with this based on your os setup
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
        this is an subroutine to tweak the default settings of "default_mode"
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
            self.win_geometry       = '1300x700+50+5'          # width x height position
            self.pylogging_fn       = "millhouse_clipboard.py_log"   # file name for the python logging
            #self.snip_file_fn       = r"C:\Russ\0000\python00\python3\_projects\clipboard\Ver3\snips_file_auto.txt"
            # need to associate with extension -- say a dict
            self.snip_file_command  = r"C:\apps\Notepad++\notepad++.exe"  #russwin10   !! implement

        elif self.computername  == "theprof":
            self.ex_editor          =  r"c:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

    # -------
    def __init__( self, ):
        """
        Init for instance, usually not modified, except perhaps debug stuff ( if any )... but use plus_test_mode()
        may be down in listing because it should not be messed with.
        """
        AppGlobal.parameters       = self   # register as a global
        self.default_mode()
        self.running_on_tweaks()
        self.choose_mode()

        print( self )
        #print( self ) # for debugging

    # ------->> default mode, always call
    # -------
    def default_mode( self ):
        """
        sets up pretty much all settings
        documents the meaning of the modes
        call first, then override as necessary
        good chance these settings will at least let the app run
        """
        self.mode              = "default"  # name your config, so it will show in app tilte, may be changed later

        #--------------- automatic settings -----------------
        self.running_on   = running_on.RunningOn
        self.running_on.gather_data()

        # some of the next all?? should be moved over to RunningOn
        self.running_on.log_me( logger = None, logger_level = 10, print_flag = True )
        self.py_path                   = self.running_on.py_path   # this is the path to the main.py program

        self.set_default_path_here     = True  # to make app location the default path in the app, Think True may always be best.
        # above may be tricky to reset, but we may have the original dir in running on
        # no easy way to ovride this ??
        if  self.set_default_path_here:     # Now change the directory to location of this file

            py_path    = self.running_on.py_path

            print( f"Directory: (  >>{os.getcwd()}<< switch if not '' to >>{py_path}<<")
            if py_path != "":
                os.chdir( py_path )

        self.our_os             = self.running_on.our_os          # so we know our os  could be "linux" or our_os == "linux2"  "darwin"....
        self.os_win             = self.running_on.os_win          # boolean True if some version of windows
        self.computername       = self.running_on.computername    # a name of the computer if we can get it
        self.opening_dir        = self.running_on.opening_dir     # directory where app was opened, not where it resides

        self.platform           = self.our_os    # sometimes it matters which os but this value is redundant


        self.icon               = r"clipboard_c.ico"    # icon for running app -- not used in linux

        self.id_color           = "blue"                # to id the app - not implemented yet

        self.win_geometry       = '1500x800+20+20'     # size, position  of app on opening
        self.win_geometry       = '900x600+700+230'    # width x height position  x, y

        self.pylogging_fn       = "clipboard.py_log"   # file name for the python logging
        self.logging_level      = logging.DEBUG        # logging level DEBUG will log all captured text ! or logging.INFO
        #self.logging_level      = logging.INFO
        self.logger_id          = "clip_board"         # id of app in logging file

        # ------------- file names -------------------

        self.snip_editor       = r"C:\apps\Anaconda3\Scripts\thonny.exe"  # editor used for opening snip files

        # this is the name of a program: its executable with path info.
        # to be used in opening an external editor
        self.ex_editor         =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10

        # if we are writing scratch files to run in a shell or similar.
        self.scratch_bat       =  r"scratch.bat"   # rel filename
        self.scratch_py        =  r"scratch.py"    # rel filename

        self.run_py            =  r"c:\apps\Notepad++\notepad++.exe"    # program to run *>py commands  !! not yet implemented

        # extensions of files for text editing
        self.text_extends = [  ".txt",  ".rsh", ".ino", ".py", ".h" , ".cpp", ".py_log", ".log", ]  # include the dot!

        # ========================= buttons initial state  ======================

        #------------------------- default the named check box's see gui.py  ---------------
        # not really implemented now... in process
        self.cmd_on            = 1     # 1 is checked or on else 0
        self.auto_url_on       = 0
        self.star_cmd_on       = 0
        self.exe_file_on       = 0
        #... not all may be named see gui.py

        #------------------------- default the named radio buttons see gui.py  ---------------
        self.rb_num_on          = 0      # which radio button on, number is not nice, but easy !! is working ???
        #... not all may be named see gui.py

        self.include_wiki_buttons  = True    # experimental flag, leave True

        # may not be best for text help file
        # help file can be web ( open with browser ), or txt ( open with self.editor ) or anything else ( will try to shell out may or may not work )
        self.help_file       =  "help.txt"   #  >>. this is the path to our main .py file self.py_path + "/" +
        self.help_file       =  "http://www.opencircuits.com/Python_Smart_ClipBoard"   # can be url or a local file -- change for clipboard !!

        self.help_fn            = self.help_file    # old phase out

        # ================== snippets ============================
        self.snippets_sort      = True                # sort snippes on key, else in file order
        self.snippets_fn        = "./snipsand/snippetts_1.txt"  # file name with snippets, can also set as a list of strings

        # ================== snips ============================
        self.snip_file_sort     = True                # sort make them easier to find in the GUI

        # next:  this is prepended to a snip file prior to opening the file
        #        so you can easily keep the snip files in a place you find convient.
        self.snip_file_path     = r"./example_snips"
        #
          # path prepended to all snip files
        self.snip_file_fn       = "./snipsand/snip_files_example.txt"

        self.snip_file_command  = r"c:\apps\Notepad++\notepad++.exe"    #russwin10  opens snip files, nice if can run it

        self.max_history       = 9          # !! not implemented  -- maybe never
        #---------------------------------------------------

        #self.transform         = "off"       #["","",]  !! is what

        self.poll_delta_t      = 200            # how often we poll for clip changes, in ms, think my computer works well as low as 10ms

# -----------------------------------
    def __str__( self,   ):
        """
        sometimes it is hard to see where values have come out this may help if printed.
        not complete, add as needed -- compare across applications and code above
        """
        a_str = f">>>>>>>>>>* parameters (some) *<<<<<<<<<<<<"
        a_str = f"{a_str}\n   mode                {self.mode}"

        a_str = f"{a_str}\n   logger_id           {self.logger_id}"
        a_str = f"{a_str}\n   logging_level       {self.logging_level}"
        a_str = f"{a_str}\n   pylogging_fn        {self.pylogging_fn}"

        a_str = f"{a_str}\n   snippets_fn         {self.snippets_fn}"
        a_str = f"{a_str}\n   snippets_sort       {self.snippets_sort}"

        a_str = f"{a_str}\n   snip_file_fn        {self.snip_file_fn}"
        a_str = f"{a_str}\n   snip_file_sort      {self.snip_file_sort}"
        a_str = f"{a_str}\n   snip_file_command   {self.snip_file_command}"

        a_str = f"{a_str}\n   ex_editor           {self.ex_editor}"

        a_str = f"{a_str}\n   scratch_bat         {self.scratch_bat}"
        a_str = f"{a_str}\n   scratch_py          {self.scratch_py}"

        a_str = f"{a_str}\n   win_geometry        {self.win_geometry}"
        a_str = f"{a_str}\n   computername        {self.computername}"
        a_str = f"{a_str}\n   our_os              {self.our_os}"
        a_str = f"{a_str}\n   and so much more... \n\n"
        return a_str

# =================================================

if __name__ == "__main__":
    #----- run the full app
    import  clip_board
    app   = clip_board.App( None, None )

# =================== eof ==============================



