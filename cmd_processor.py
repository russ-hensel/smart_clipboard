# -*- coding: utf-8 -*-
#
#


"""
actually does the commands and transforms, try to be a little bit decoupled from rest of ap
CmdProcessor is main class
"""

# from subprocess import Popen, PIPE
import os
import os.path
import subprocess
import webbrowser
import logging

#local
from app_global import AppGlobal


# ----------------------------------------------
def   print_uni( a_string_ish ):
    """
    print even if Unicode char messes it conversion
    maybe doing as a call is over kill
    """

    print(  a_string_ish.encode('ascii', 'ignore') )

# ----------------------------------------------
class CmdProcessor( object ):
    """
    carry out both commands and transforms



    split into commands and transforms ??
    object executes commands for clip_board.ClipBoard
    ?? registered file names not same as os default
    ?? multiple items on multiple lines
    do_if .. passed something, usually a string and see if it is executable in some way,
             and if so do it.
             may have some additional data for what sort of executable it is
             all return a tuple for the controller
             the star commands all have an embedded * marker

    """
    # ----------------------------------------
    def __init__(self, ):
        #
        #self.controller     = controller
        #self.controller     = AppGlobal.controller
        self.parameters      = AppGlobal.parameters   # for local ref  parameters
        # self.gui            = self.controller.gui

        self.logger         = logging.getLogger( f"{AppGlobal.logger_id}.{ self.__class__.__name__ }" )

        self.logger.debug( "init app_state" )   #
        print( f"logger level in AppState = {self.logger.level}", flush = True )

        self.logger_id      = "xxx"    # !! fix this
        #self.parameters          = AppGlobal.parameters
        #AppGlobal.parameters     = self


#        self.star_commands  =  { "*>np":       self.do_if_star_bat_cmd,
#         list of *>cmds that we implement and in this order                        }
        self.star_commands  =  [ self.do_if_star_bat_cmd,
                                 self.do_if_edit_text_file,
                                 self.do_if_star_url_cmd,
                                 self.do_if_star_shell_cmd       ]

        self.url_valid_prefixs       = [ "www.", "http://", "https://" ]

#        # file commands do they use a list instead of a string ???
#        self.star_file_commands  =  { "*>bat":       self.do_if_star_bat_cmd,
#                                }
#
#        self.star_file_commands  =  { "*>bat":       self.do_if_star_bat_cmd,
#                                }


#                            "*>print":     self.print_cmd,
#        # these are for pb commands
#        self.pb_commands   = { "*>url":       self.do_url_cmd,
#                            "*>print":     self.print_cmd,
#                            "*>shell":     self.do_shell_cmd,
#                            "*>run":       self.do_run_cmd,
#                            "*>text":      self.do_text_cmd,
#                            }

        #self.text_extends = [  ".txt",  ".rsh", ".ino", ".py", ".h" , ".cpp"             ]    # could be set from parms

        self.text_extends =   self.parameters.text_extends

        self.return_texts = []
        self.begin( )

    # ----------------------------------------
    def begin( self,  ):
        """
        more or less a reset at beginning of processing some text, may not be a great idea
        """
        self.did_cmd        = False             # set to true if just onle line in command works
        self.return_texts   = []
        self.did_what       = set()             # may need to build in a more complicated way
        self.did_transform  = False

    # ----------------------------------------
    def do_cmds( self, cmd_text, cmds_checked ):
    #def do_cmds( self, cmd_text,  ):
        """
        v3 -- do_star_cmds  ??
        this is the process for all commands so cmds_checked is the list of the
        active ones, only the first one that works is run ( for now anyway )
        cmd_text for *> commands, must have *> on first line
        if   *>bat only one command ( multi line is run )
        else many lines might be run
        lines are generally cleaned up prior to being run like with strip
        return:
            ( <flag true if processed>, <what done text> <detail on processed lines> )
        """
        self.begin()
        cmd_lines        = cmd_text.split( "\n" )
        msg              = "do_cmds() we have n = lines =" + str( len( cmd_lines ))
        AppGlobal.print_debug( msg )

        msg              = f"do_cmds() checked = {cmds_checked} lines are = {cmd_lines}  )"
        AppGlobal.print_debug( msg )

        # *>bat is special so is it on first line
        cmd_lines        = [ i_line.strip()  for i_line in cmd_lines ]   # do we want to clean all lines?? or just the first
#        if not( cmd_lines[0].startswith(  "*>" ) ):
#            return( False, "do_cmds nothing done", "do_cmds nothing done text" )

        if "*>" in cmds_checked:
            """
            do all commands that start with *> .. only one *>bat first line must start with ( after clean up )
            *>
            can we mix commands ?? perhaps test
            """

            if ( cmd_lines[0].startswith(  "*>" ) ):

                # *>bat is one of these but if used is only one and must start on first line ( any text after -- ignore for now )
                if cmd_lines[0].startswith(  "*>bat" ):
                    ran_cmd, cmd_msg, cmd_text = self.do_bat_cmd( cmd_lines )
                    if ran_cmd:
                        self.did_cmd     = True
                    # process bat command ( then return  )
                    return ( ran_cmd, cmd_msg, cmd_text )  # true even if no success
                # now rest of *>
                for i_line in cmd_lines:
                    msg       = "line loop >>" + i_line
                    AppGlobal.print_debug( msg )

                    done, cmd_msg, cmd_text  = self.do_star_url_line(   i_line )
                    if done:
                        self.did_cmd     = True
                        self.return_texts.append( cmd_text )
                        self.did_what.add( cmd_msg )

                    done, cmd_msg, cmd_text  = self.do_star_shell_line(   i_line )
                    if done:
                        self.did_cmd     = True
                        self.return_texts.append( cmd_text )
                        self.did_what.add( cmd_msg )

                    done, cmd_msg, cmd_text  = self.do_star_text_line(   i_line )
                    if done:
                        self.did_cmd     = True
                        self.return_texts.append( cmd_text )
                        self.did_what.add( cmd_msg )

                    else:
                        pass
                        #self.do_star_url(   i_line )
    #                 self.do_star_text(  i_line )
    #                 self.do_star_shell( i_line )

                    pass

            if self.did_cmd:
                msg    = "True did_cmd"
                AppGlobal.print_debug( msg )

                return( True, str( self.did_what ), "\n".join( self.return_texts ) )
            else:
                # continue to try other commands
                pass

        if "url" in cmds_checked:
             # self.do_url(  cmd_lines )  !! this may be right where we give it line by line think this is old way patched in
             return self.do_if_url_cmd( cmd_text, "ignore" )


        if "txt" in cmds_checked:    # here we are doing the right line by line
            for ix, i_line in enumerate( cmd_lines ):
                print( "txt line loop >>" + i_line )
                done, cmd_msg, cmd_text  = self.do_text_line(   i_line )
                if done:
                    self.did_cmd     = True
                    self.return_texts.append( cmd_text )
                    self.did_what.add( cmd_msg )
                elif ix == 0:
                    break
            if self.did_cmd:
                print( " True did_cmd ")
                return( True, str( self.did_what ), "\n".join( self.return_texts ) )
            else:
                pass

#        if "exe" in cmds_checked:
#             do_exe(  cmd_lines )

#        else:
        return ( False, "do_cmds False msg", "do_cmds False txt" )

    # ----------------------------------------
    def do_bat_cmd( self, cmd_lines ):
        """
        v3
        call with lines ( cleaned for now )
        already validated that *>bat is on line 0 but have not found the end yet
        """
        found_end     = False
        bat_lines     = []


        for i_line in cmd_lines[1:]:

            if i_line == "*>end":
                found_end     = True
                break
            else:
                bat_lines.append( i_line )

        if not( found_end ):
            return ( False, "no *>end", "xxx" )

        bat_string  =  "\n".join( bat_lines )

        #print( "bat string,=  " + str ( bat_string ) )
        # stdout_stuff           = "stdout_stuff disabled "

        #This seems ok but blocks until app closed
        # timeout=1 lets us go on
        po     = subprocess.Popen(  [  'cmd.exe', ], shell=True,    stdout=subprocess.PIPE,    stdin=subprocess.PIPE, )    #  captures output
        msg    = str( po )
        AppGlobal.print_debug( msg )

        stdout_stuff, stderr_stuff    = po.communicate( input = bat_string.encode('utf-8'), timeout=2 ) # python 3 timeout=None )  # try to fix bat error issue
        stdout_stuff                  = stdout_stuff.decode("utf-8")

        #print( "stdout_stuff" , "   ", stdout_stuff )
        self.return_texts   = stdout_stuff # may not be list ??
        return ( True, "ran bat, returned = ", stdout_stuff )


    # ----------------------------------------
    def do_star_url_line(  self,  a_line ):
        """
        v3
        do this one line at a time return
        (flag action, ret text )
        """
        done       = False
        action     = "no do_star_url"   # normally ignored, but may be usefull for debugging
        ret_text   = "no do_star_url return text "

        print( "url line =" + a_line )
        if a_line.startswith(  "*>url" ):

        # cmd> url  https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python
        # cmd> url  http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/
        # a_url  = r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"

            a_url     = a_line[5:]   # .strip()    # should strip "*>url"  5 = len( "*>url" )

            print( " *>url>> " + a_url )

            a_url           = a_url.strip( )
            url_flag, a_url = self.is_url( a_url )
            if url_flag:

                self.controller.logger.info( "webbrowser.open( " + a_url )

                webbrowser.open( a_url, new=0, autoraise=True )
                done       = True
                action     = "*>url_found"   # normally ignored, but may be useful for debugging
                ret_text   = "*>url     " + a_url        # what is standard for returned text

        return (done, action, ret_text )

    # ----------------------------------------
    def do_star_shell_line(  self,  a_line ):

        """
        v3
        do this one line at a time return
        ?? no caputre of returned data
        (flag action, ret text )
        """
        done       = False
        action     = "False do_star_shell_line"   # normally ignored, but may be useful for debugging
        ret_text   = "False do_star_shell_line return text "

        print( "url line =" + a_line )
        if a_line.startswith(  "*>shell" ):

        # cmd> url  https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python
        # cmd> url  http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/
        # a_url  = r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"

            a_shell     = a_line[7:]   # .strip()    # should strip "*>url"  5 = len( "*>url" )

            print( "*>shell " + a_shell )

            a_shell           = a_shell.strip( )
            # check if file ???
            if True:

                self.controller.logger.info( "*>shell: " + a_shell )
                os.popen( a_shell )

                done       = True
                action     = "*>shell_found"
                ret_text   = "*>shell     " + a_shell       # what is standard for retured text

        return ( done, action, ret_text )

    # ----------------------------------------
    def do_star_text_line(  self,  a_line ):

        """
        v3
        do this one line at a time return

        (flag action, ret text )
        """
        done       = False
        action     = "False do_star_text_line"   # normally ignored, but may be useful for debugging
        ret_text   = "False do_star_text_line return text "

        print( "text line =" + a_line )
        if a_line.startswith(  "*>text" ):

        # cmd> url  https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python
        # cmd> url  http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/
        # a_url  = r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"

            a_text     = a_line[6:]   # .strip()    # should strip "*>url"  5 = len( "*>url" )

            print( "*>text " + a_text )

            a_text           = a_text.strip( )
            # check if file ???
            if True:

                AppGlobal.controller.logger.info( "*>text: " + a_text )
                proc    = subprocess.Popen( [ self.parameters.ex_editor, a_text  ] )  # a_cmds[1:999]  ]  ) # self.parameters.pylogging_fn ] )

                done       = True
                action     = "*>text_found"
                ret_text   = "*>text     " + a_text       # what is standard for returned text

        return ( done, action, ret_text )

    # ----------------------------------------
    def do_text_line(  self, a_line ):
        """
        v3
        """
        # default for fail
        done       = False
        action     = "False do_text_line"   # normally ignored, but may be useful for debugging
        ret_text   = "False do_text_line return text "

        fn         = a_line.strip()   # may want to clean up more to allow text after file name ?? make sure a file name....

        #flag, fn, a_ext =  self.is_filename_with_ext(  fn, self.text_extends  )  # type and existence, both in one line or separate ??

        fn_1, fn_ext    = os.path.splitext( fn )   # fn_1 is <full path up to dot>   fn_ext like ".txt"

        if  not( fn_ext in self.text_extends ):
            return ( done, action, ret_text )

        if  not( os.path.isfile( fn ) ):
            return ( done, action, ret_text )

        # print( fn + " is a text file " )
        #print_uni( "do_edit_text_file>>>>" + str( a_cmds )  +  "<<<<<" )  #str may fail, may need encoding fix

        proc       = subprocess.Popen( [ self.parameters.ex_editor, fn  ] )  # a_cmds[1:999]  ]  ) # self.parameters.pylogging_fn ] )

        done       = True
        action     = "text_file_found"
        ret_text   = a_line      # what is standard for retured text

        return ( done, action, ret_text )

    # ------------------------------------------
    def is_url( self, a_string,  ):
        """
        v2->v3
        clean up the string and see if it starts with a url, return cleaned url

        is the ( cleaned up ) string a url? !!  url must be on the first line if multiple and at first non white space
        consider typing the string get_string_type
        return ( boolean, cleaned up url ( truncate at space or cr or lf ... ) )
        """
        is_url                 = False

        parts       = a_string.split()
        test_url    = parts[0]
        #test_url   = (a_string.split() ).[0])  #.strip()     # parse off using whitespace  and strip

        for i_prefix in self.url_valid_prefixs:
            if test_url.find( i_prefix ) == 0:    # find str2 in str1
                is_url = True

        return ( is_url, test_url )

    # ------------------------------------------
    def is_url_old_delete_perhaps( self, a_string,  ):
        """
        clean up the string and see if it starts with a url,

        is the ( cleaned up ) string a url? !!  url must be on the first line if multiple and at first non white space
        consider typing the string get_string_type
        return ( boolean, cleaned up url ( truncate at space or cr or lf ... ) )
        if false then cleaned up url does not matter
        """
        is_url                 = False
        if a_string == "":
            return( False, "" )
        parts       = a_string.split()
        test_url    = parts[0]
        #test_url   = (a_string.split() ).[0])  #.strip()     # parse off using whitespace  and strip

        for i_prefix in self.url_valid_prefixs:
            if test_url.find( i_prefix ) == 0:    # find str2 in str1
                is_url = True

        return ( is_url, test_url )



#==================== v2 may be updated ===============

    # ----------------------------------------
    def do_text(  self, cmd_lines ):
        """
        this is for a * command, old version 2?
        cmd_lines     is a list of strings, the lines -- cleaned at all ??
        """
        for i_line in cmd_lines:
            print("")
            print( i_line )
            if i_line.startswith(  "*>text" ):  # for now *>textxxxx will trigger it
                fn = i_line[ len( "*>text" ) :]    # fn now rest of line
                fn = fn.strip()     # may want to clean up more to allow text after file name ??
                #flag, fn, a_ext =  self.is_filename_with_ext(  fn, self.text_extends  )  # type and existence, both in one line or separate ??

                fn_1, fn_ext    = os.path.splitext( fn )   # fn_1 is <full path up to dot>   fn_ext like ".txt"

                if  not( fn_ext in self.text_extends ):
                    #print( " does not have correct ext " )
                    continue   # on to next line

                if  not( os.path.isfile( fn ) ):
                    # file does not exist
                    #print( ">>>" + fn + "<<<  does not exist " )

                    continue

                print( " is a text file " )
                #print_uni( "do_edit_text_file>>>>" + str( a_cmds )  +  "<<<<<" )  #str may fail, may need encoding fix

                proc     = subprocess.Popen( [ self.parameters.ex_editor, fn  ] )  # a_cmds[1:999]  ]  ) # self.parameters.pylogging_fn ] )
                # if ext_list is None:
#                    return ( True, file_name, extension )
#                elif  ( extension in  ext_list ):
#                    return ( True, file_name, extension )
#                else:
#                    return ( False, "", "" )

            else:
                pass
                #print( "does not start with *>text" )

        #print( "end of for loop " )

      #start here

# ===================== old delete?? +++++++++++++++++++++++++++

    # ----------------------------------------
    def do_if_cmds( self, mulp_flag, a_cmds, in_text ):
        """
        think does not do file like commands, that is those that span multiple lines
        is still in use, name easy to mix up with do_if_cmd .....
        look at text and see if can do any of the commands in a_cmds which should be do_if... cmds
        text is split into lines so command may not span line
        status:
        mulp_flag    = more than one line, else first to clean up
        a_cmds       = command functions to call all take text and ret ( )
                       if one command works do not call the rest
        in_text      = text with commands
        retrun       = ( True, "went to url", ret_text )
                        ret_text  = ???
                       ( False ???, ??? )

        """
        ret_is_ok       = False
        ret_mulp_text   = ""
        ret_action      = "ret_action_default"

        is_ok           = False
        ret_mulp_text   = ""
        no_done         = 0

        #print a_cmds
        in_texts        = in_text.split()

        # old mulp imp
        # text needs to be in a list
#        if mulp_flag:
#            in_texts    = in_text.split()
#        else:
#            in_texts    = [ in_text ]
        # !! PRETTY MUCH A MESS
        for i_cmd in a_cmds:
            for i_text in in_texts:
                # print_uni( "cmd on i_text " + i_text )
                is_ok, act_text, ret_text     = i_cmd( i_text )
                # result like  ( True, "went to url", ret_text )
                if is_ok:
                    ret_is_ok      = True
                    ret_action     = act_text
                    no_done = no_done + 1
                    if no_done > 1:
                        ret_mulp_text   += "\r\n"
                    ret_mulp_text   += ret_text    # may be short enought to have many
                    if not( mulp_flag ):
                        break
                        # consider not mulp break here, go to first line that can be processed

            # if one type works we do not try the others -- but we could
            if is_ok:
                break

#        if no_done > 1:
#               mulp_text  = mulp_text + "multiple line"

        return ( ret_is_ok, ret_action, ret_mulp_text )

    # ----------------------------------------
    def do_if_url_cmd(self, a_string, ignore ):
        """
        go to a url only if a url or multiples are found in string
        to start with lets have one url per line no junk at beginning of line, later clean up one url per line ??
        return ( done, what, text )
        may want to quit if not found on first line

        Return:  usual tuple
        """
        went_to      = []   # record where we went
        lines        = a_string.split()
        for ix_line, i_line in enumerate( lines ):

            i_line = i_line.strip()
            ok, b_url  = self.is_url( i_line )
            if  ok :
                self.process_url( i_line )
                went_to.append( i_line )
            else:
                if ix_line == 0:
                    msg = "no url on line ix = 0 probably should return "
                    AppGlobal.print_debug( msg )

        if ( len( went_to )  > 0 ):
            a_text   = "\n".join( went_to )
            return  ( True, "found url's", a_text )
        else:
            return  ( False, "did not find url's", "" )

   # ----------------------------------------
    def is_line_cmd( self, a_cmd, a_string ):
        """
        used by come of other methods in this class, not externally
        checks only the *> part and strips off stuff beyond
        think now this looks at multiple lines and returns all
        lines that start with the command, the content of the lines is returned
        in the second argument
        true if just one of the lines is a command
        return ( True/False list_of_lines_from_a_string )


        ----- may all be wrong
        can there be multiple lines, i thik so
        a_cmd   something like *>bat ends with *>end junk before and after dropped
        a_string   a string which for success needs to be multi lined
        return ( True/False list_of_lines_from_a_string )
        see samples in test below

        *>batshit should not pass as bat command should be *>bat<space>
        "  *>shell " should not pass because of blank at begin of line,  no should be ok we strip the line
        """
        print( "-------------is_line_cmd --------------" )

        lines         = a_string.split( "\n" )   # \r does not find stuff
        a_cmd         = a_cmd + " "
        cmd_len       = len( a_cmd )
        flg_found     = False
        cmd_lines     = []
        found_start   = False
        found_end     = False
        #run_me        = False

        for i_line in lines:
             s_line   =  i_line.strip()      # .strip( )    # what about cr lf and both, strip and split in both cases
            # print( "s_line = " + s_line )
             start    = s_line.find( a_cmd, 0,  )
             if not( start == -1 ):
                flg_found   = True
                t_line      = ( s_line[ start + cmd_len : ] ).strip()
                u_line      = t_line.split()[0]
                #u_line      =

#                print( "-> ", u_line )
                cmd_lines.append( u_line )

        return ( flg_found,  cmd_lines )

    # ----------------------------------------
    def is_file_cmd( self, a_cmd, a_string ):
        """
        uncertain what this is looking for may be old version of shell
        or work like shell without the *>shell being required.
        a_cmd   something like *>bat ends with *>end junk before and after dropped
        a_string   a string which for success needs to be multi lined
        return ( True/False, list_of_lines_from_a_string )
        see samples in tests in readme.txt
        """
        print( "------ is_file_cmd ----------")
        lines         = a_string.split( "\n" )   # \r does not find stuff

        file_lines    = []           # the lines we have found in this pseudo file
        found_start   = False
        found_end     = False
        #run_me        = False

        for i_line in lines:
             s_line  =  i_line.strip()      # .strip( )    # what about cr lf and both, strip and split in both cases
             #print j_line
             if found_start:   # look for end
                 #if j_line.startswith( "*>end" ):
                 if s_line == "*>end":
                     #print j_line.strip()
                     found_end = True
                     break
                 else:
                     #print j_line
                     file_lines.append( i_line )
                 pass
             else:        # look for start
                 if s_line   == a_cmd:
                     #print( "found_start" )
                     found_start = True
#                 else:
#                     print( "not found_start" )

        if found_end:
            return ( True,  file_lines )
        else:
            return ( False, [] )

    # ----------------------------------------
    def do_if_star_shell_cmd( self, a_string ):
        """
        think should be *>shell  <blanks> filename <optionally blanks plus crap
        seems to work at first level
        *>shell    D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt
        next not valid
        *>shell   file_name   ... ok if on many lines
        *>shell    D:\Russ\2017\shitstorm.odt


        return ( done, what, new_text )
        """
        print ( "do_if_star_shell_cmd" )
        ( flag, lines )   = self.is_line_cmd( "*>shell", a_string )

        if not( flag ):
            return ( False, "", "" )
        # else:
        print( "*>shell" )
        print( str( lines ) )

        for i_line in lines:
            #pass
            os.popen( i_line )

        #print ( lines )
        # next will run and return stuff to us
        # for bat put exit on the end?? yes if no command window else not ??
#        bat_string  =  "\n".join( lines )
#        po     = subprocess.Popen(  [  'cmd.exe', ], shell=True,    stdout=subprocess.PIPE,    stdin=subprocess.PIPE )   #  captures output
#
#
#        stdout_stuff, stderr_stuff    = po.communicate( input = bat_string, ) # python 3 timeout=None )  # try to fix bat error issue
        #print "stdout_stuff"
        #print stdout_stuff
        new_text  = "\n".join( lines )
        return ( True, "shells_found..popopen  ",  new_text )

    # ----------------------------------------
    def do_if_star_url_cmd( self, a_string ):
        """

        return ( done, what, text )
        """
        print ( "do_if_star_url_cmd" )
        ( flag, lines )   = self.is_line_cmd( "*>url", a_string )

        if not( flag ):
            return ( False, "", "" )
        # else:
        print( "*>url" )
        print( str( lines ) )

        for i_line in lines:
            #pass
            print( i_line )
            self.process_url( i_line )
        print( "do_if_star_url_cmd return True")
        return  ( True, "url visited", str( lines ) )

        # =============== old ================
        print ( "do_if_star_url_cmd" )
        ( flag, lines )   = self.is_line_cmd( "*>url", a_string )

        if not( flag ):
            return ( False, "", "" )
        # else:
        print ( "bat_lines" )
        #print ( lines )
        # next will run and return stuff to us
        # for bat put exit on the end?? yes if no command window else not ??
#        bat_string  =  "\n".join( lines )
#        po     = subprocess.Popen(  [  'cmd.exe', ], shell=True,    stdout=subprocess.PIPE,    stdin=subprocess.PIPE )   #  captures output
#
#
#        stdout_stuff, stderr_stuff    = po.communicate( input = bat_string, ) # python 3 timeout=None )  # try to fix bat error issue
        #print "stdout_stuff"
        #print stdout_stuff


        print( "return true" )
        return ( True, "urls visited", "not done " )

    # ----------------------------------------
    def do_if_star_bat_cmd( self, a_string ):
        """
        construct the bat file ( perhaps virtually )  from text and then do it

        return text is the text from the bat file ... if *>bat found  for now must be lower case *>end must be found
        *>bat must be on first line
        *>end

        return ( done, what, text )
        """
        found_end     = False
        bat_lines     = []

        lines         = a_string.split( "\n" )   # \r does not find stuff
        if not( lines[0].strip()  == "*>bat" ):
            return ( False, "no *>bat", "xxx" ) # 1,2 part of tuple should not matter

        for i_line in lines[1:]:
            i_line       = i_line.strip()
            if i_line == "*>end":
                found_end     = True
                break
            else:
                bat_lines.append( i_line )

        if not( found_end ):
            return ( False, "no *>end", "xxx" )

        bat_string  =  "\n".join( bat_lines )

        #print( "bat string,=  " + str ( bat_string ) )
        # stdout_stuff           = "stdout_stuff disabled "

        #This seems ok but blocks untill app closed
        # timeout=1 lets us go on
        po     = subprocess.Popen(  [  'cmd.exe', ], shell=True,    stdout=subprocess.PIPE,    stdin=subprocess.PIPE, )    #  captures output
        print( po )
        stdout_stuff, stderr_stuff    = po.communicate( input = bat_string.encode('utf-8'), timeout=2 ) # python 3 timeout=None )  # try to fix bat error issue
        stdout_stuff                  = stdout_stuff.decode("utf-8")

        #print( "stdout_stuff" , "   ", stdout_stuff )

        return ( True, "ran bat ran, returned = ", stdout_stuff )


    # ----------------------------------------
    def do_if_star_cmd( self, a_string ):
        """
        master of all star commands, essentially just loops through the list of
        them all
        there may be a command hidden in the string we have to look through
        all our star commands
        look for first marker then switch to correct do_if...
        maybe star should be put in all their names

        # ==================== probable junk move or delete

        may go elsewhere
        a_cmd    a string, then parsed into parts
        *>cmd with different commands
        use a dict, this is cool!

        *>bat

        return ( done, did_what, ret_text )
        "*>url":       self.do_url_cmd,
                            "*>print":     self.print_cmd,
                            "*>shell":     self.do_shell_cmd,
                            "*>run":       self.do_run_cmd,
                            "*>text":
        test copy
        *>shell notepad++.exe      fail not full path to file
        *>shell D:/apps/Notepad++/notepad++.exe      ok
        look in readme.txt   for test cases


        """
        print( "------- do_if_star_cmd ------------" )
        print( self.star_commands )
        for i_cmd in self.star_commands:
            print( str(i_cmd ) )
            ok, what, details = i_cmd( a_string )
            if ok:
                return( ok, what, details )
        return ( False, "do_star_cmd did zip", "" )
#
    # ----------------------------------------
    def do_if_ext_with( self, a_file_name, a_ext, a_exe ):
        """
        execute if a file name ending with e_a_ext, launch with a_exe
        a_file_name, string with the file name, we do no clean up maybe we should
        return usual tuple
        a_ext   a list or None for no checking of extension    --
        """
        # print "-------------------"
        # print( "test text " + a_file_name )
        if ( a_ext is None ):
            flag, fn        = self.is_filename( a_file_name  )
            if not( flag ):
                return ( False, "not file_name", a_file_name  )
        else:
            flag, fn, ext   =  self.is_filename_ext( a_file_name, [ a_exe ]   )
            if not( flag ):
                return ( False, "not ext file_name", a_file_name  )

        print_uni( "do_if_ext_with>>>>" + fn  +  "<<<<<" )  #str may fail, may need encoding fix
        proc = subprocess.Popen( [ a_exe, fn  ] )  # a_cmds[1:999]  ]  ) # self.parameters.pylogging_fn ] )

        return ( True, "exe file", fn  )

    # ----------------------------------------
    def do_if_edit_text_file( self, a_file_cmd ):
        """
        Think files must start from a drive letter -- windows not url's
        test copy
        should we do any clean up, perhaps at least whitespace ....  trailing blanks kill it now !!
        *>shell notepad++.exe
        *>shell D:/apps/Notepad++/notepad++.exe
        D:/Russ/2015/instruct_view.txt
        D:/Russ/2015/ladyadair.txt
        D:/PhotosRaw/2016/BoxInstructable\DSCN        D:/Russ/2015/instruct_view.txtG
        return   tuple ( worked, what, file_name ) .....
        """
        # print "-------------------"
        # print( "test text " + a_file_name )

        # ----------------   look at:    def do_if_star_url_cmd( self, a_string ):
        """

        return ( done, what, text )
        """
        print ( "do_if_edit_text_file" )
        ( flag, lines )   = self.is_line_cmd( "*>text", a_file_cmd )

        if not( flag ):
            return ( False, "", "" )
        # else:
        print( "*>text" )
        print( str( lines ) )

        for  fn in lines:
                self.do_edit_text_file( fn )
        return ( True, "edit text", lines  )

    # ----------------------------------------
    def do_if_file_name( self, a_string ):
        """
        Think files must start from a drive letter -- windows not url's
        test copy
        *>shell notepad++.exe
        *>shell D:/apps/Notepad++/notepad++.exe
        D:/Russ/2015/instruct_view.txt
        D:/Russ/2015/ladyadair.txt
        D:/PhotosRaw/2016/BoxInstructable/DSCN        D:/Russ/2015/instruct_view.txtG
        return   tuple ( worked, what, file_name ) .....
        """
        # print "-------------------"

        parts          = a_string.split()     # no spaces allowed
        #print( "do_if_file_name parts", parts )   # ?? print_uni may nott work for this
        a_file_name    = parts[0]

        if not( self.is_filename(  a_file_name ) ):
            # print_uni( "not a filename "  +  a_file_name )  # printing the file name caused a problem this may crop up other places
            return ( False, "not a file_name", a_file_name )

        try:
            #proc = Popen( [ " ", a_file_name ]   ) # self.parameters.pylogging_fn ] )  why 1:999 0 is the command **>
            #os.system( a_file_name )
            os.startfile( a_file_name )
        except Exception as exception:
            # exception
            print( "do_if_file_name exception: ",  exception )
            return ( False, "got exception", a_file_name )

        return ( True, "exe the file", a_file_name )

    # ----------------------------------------
    def do_edit_text_file( self, a_cmds ):
        #
        """
        move this to appGlobal implementation
        edit a file in text editor, name is not great
        may want to break file name on space to elim junk
        ??? return ( done_flag, string_what_i_did )
        """
        print_uni( "do_edit_text_file>>>>" + str( a_cmds )  +  "<<<<<" )  #str may fail, may need encoding fix

        proc = subprocess.Popen( [ self.parameters.ex_editor, a_cmds  ] )  # a_cmds[1:999]  ]  ) # self.parameters.pylogging_fn ] )

    # ----------------------------------------
    def do_run_cmd( self, a_cmds ):
        #
        """
        think ?? runs a command in a shell

        """
        print_uni( "do_run_cmd>>>" + str(a_cmds) +"<<<" )
        proc = subprocess.Popen( a_cmds[0:999] ) # self.parameters.pylogging_fn ] )

    # ----------------------------------------
    def process_url(self, a_url ):
        """
        go to url, clean up head and tail with strip
        return string saying what we did
        """
        import webbrowser
        # cmd> url  https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python
        # cmd> url  http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/
        # a_url  = r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"

        print( " url>> " + a_url )

        a_url  = a_url.strip( )

        self.controller.logger.info( "webbrowser.open( " + a_url )

        webbrowser.open( a_url, new=0, autoraise=True )
        return "opening " + a_url

    # ------------------------------------------
    def transform_alt_line_sort(self, in_text, ):
        """
        split up alternate lines and sort by the first line, then reassemble
        drop blank lines, which come from copy url and possibly other places
        ?? should we drop comment lines #
        """
        return  self.transform_line_sort( in_text, which_line = 0 )
#        lines_0 = in_text.split("\n")
#        if ( len( lines_0 )  < 2 ):
#            return (False, "not", "2 short to sort")
#
#        # clean up white space often every third line
#        lines_1   = []
#        for i_line in lines_0:
#            line = i_line.strip()
#            if line != "":  # not sure why this is good idea
#                lines_1.append(line)
#
#        odd         = True  # we are going to split into odd and even lines
#        lines_a     = []
#        lines_b     = []
#
#        for i_line in ( lines_1 ):
#            # alternate odd even
#            if odd:
#                lines_a.append( i_line )
#                odd    = False
#            else:
#                lines_b.append( i_line )
#                odd    = True
#
#        if not( odd ):       # even up the lists
#               lines_b.append( "i_line" )
#
#        zipped         = zip( lines_a, lines_b) # Output: Zip Object. <zip at 0x4c10a30>
#
#        sorted_zip     = sorted( zipped,  key=lambda i_list: i_list[0] )
#        # rebuild the list
#        out_list      = []
#        for a_sorted in sorted_zip:
#            a, b = a_sorted
#            #a_line = a_line + "\n"     # could make big list and join, may be better
#            out_list.append( a )
#            out_list.append( b )
#            out_list.append( "" )       # put in a blank line for readabality
#        out_lines    = "\r\n".join( out_list )
#
#        print( out_lines )
#        return ( True, "sorted", out_lines )


    # ------------------------------------------
    def transform_line_sort(self, in_text, which_line = 0 ):
        """
        utility for alternate line sorts, start setting up with options
        use old functions for setting options and calling
        Args:   which_line  line to sort must be 0 or 1
        Return: tuple usual conventions look around
        """
        lines_0 = in_text.split("\n")
        if ( len( lines_0 )  < 2 ):
            return (False, "not", "2 short to sort")

        # clean up white space often every third line but can be more or never
        # non blank lines need to appear in pairs, can have odd at end but
        # probably will be sorted oddly
        lines_1   = []
        for i_line in lines_0:
            line = i_line.strip()
            if line != "":  # not sure why this is good idea
                lines_1.append(line)

        odd         = True  # we are going to split into odd and even lines
        lines_a     = []
        lines_b     = []

        for i_line in ( lines_1 ):
            # alternate odd even
            if odd:
                lines_a.append( i_line )
                odd    = False
            else:
                lines_b.append( i_line )
                odd    = True

        if not( odd ):       # even up the lists
               lines_b.append( "i_line" )

        zipped         = zip( lines_a, lines_b) # Output: Zip Object. <zip at 0x4c10a30>
        sorted_zip     = sorted( zipped,  key=lambda i_list: i_list[ which_line ] )
        # rebuild the list
        out_list      = []
        for a_sorted in sorted_zip:
            a, b = a_sorted
            out_list.append( a )
            out_list.append( b )
            out_list.append( "" )       # put in a blank line for readabality
        out_lines    = "\r\n".join( out_list )   # crlf to make windows happy guy

        #print( out_lines )
        return ( True, f"sorted on line {which_line}", out_lines )

    # ------------------------------------------
    def transform_star_shell(self, in_text, ):
        """
        for now do to all lines   may want to validated file names, url...... think on it
             *>shell   https://www.aliexpress.com/item/S
        """
        return self._transform_prefix_line( in_text, "*>shell  ")



    # ------------------------------------------
    def transform_insert_spaces(self, in_text, ):
        """
        also know as indent
        for now do to all lines   put in 4 spaces, later
        may take from parms and or strip spaces on left first
        do a strip on right -- should this be another function ??
        """

        return self._transform_prefix_line( in_text, 4*" " )

    # ------------------------------------------
    def transform_star_line(self, in_text, ):
        """
        put * at front of each line for wiki bullet points
        """
        return self._transform_prefix_line( in_text, "* " )

    # ------------------------------------------
    def _transform_prefix_line(self, in_text, a_prefix, new_nl = "\r\n"  ):
        """
        this works for all the prefix operations
        for now do to all lines   put in a_pfefix, later
        may take from parms and or strip spaces on left first
        do a strip on right -- should this be another function ??
        do we have to worry about lines seperated with \r\n and what should we add back in
        strings have a replace method can replace \r\n with \n as a first step
        """

        lines0 = in_text.split("\n")

        lines1 = []

#       this may have stripped \r at end of strings if any
#        for i_line in lines0:
#            line = i_line.strip()
#            if line != "":  # not sure why this is good idea
#                lines1.append( line )

#        odd      = True  # we are going to split into odd and even lines
        lines2   = []
        ## change me to list comp
        for ix, i_line in enumerate( lines0 ):  # !! unless gets more complicated change to list comp
            lines2.append( a_prefix  + i_line   )

        new = new_nl.join( lines2 )
        return ( True, f"prefixed with >>{a_prefix}<<", new )

    # ------------------------------------------
    def transform_url_to_helpdb(self, in_text, ):
        """
        now links to add *>url
        make output something like:
        Hot bed Module High Power MOS Tube Module with Cable Tube Add on Heated Bed Power Expansion Module-in Integrated Circuits from Electronic Components & Supplies on Aliexpress.com | Alibaba Group
             *>url   https://www.aliexpress.com/item/S
        """
        lines0 = in_text.split("\n")
        if len(lines0) < 2:
            return (False, "not", "2 short")
        # rint lines0
        lines1 = []

        # clean up white space often every third line
        for i_line in lines0:
            line = i_line.strip()
            if line != "":  # not sure why this is good idea
                lines1.append(line)

        odd      = True  # we are going to split into odd and even lines
        lines2   = []

        for ix, i_line in enumerate(lines1):

            # alternate odd even
            if odd:
                part_b = i_line
                odd    = False
            else:
                # if first line does not start with http or https
                # we will return False
                if ix == 1:  # 2 in a way fix this?
                    #  add www,  use in to find a beinning  !! may need a bit mopre work
                    #  https://snippets.readthedocs.org/en/latest/
                    #  012345
                    #  !! need to check for both http and htts
                    # !! find and use is_url function
                    prefix = i_line[0:4]
                    if prefix != "http":
                        prefix = i_line[0:5]
                        if prefix != "https":
                            self.logger.info( "prefix " + prefix )
                            return ( False, "not http or https", "" )

                lines2.append(  part_b + '\r\n    *>url  ' + i_line   )

                lines2.append( "" )  # for a blank line, or could be put in above
                odd = True

        new = '\r\n'.join( lines2 )
        return ( True, "urls to helpdb", new )

    # ------------------------------------------
    def transform_url_to_helpdbxx(self, in_text, ):
        """
        !!!!!!take url list and change to wiki format
        return success flag and transformed text in tuple
        ** modify so makes bold ?? consider underlined
        !! current code ugly does not do www.

        ( is_done, did_what, ret_text )
        """
        lines0 = in_text.split("\n")
        if len(lines0) < 2:
            return (False, "not", "2 short")
        # rint lines0
        lines1 = []

        # clean up white space
        for i_line in lines0:
            line = i_line.strip()
            if line != "":  # not sure why this is good idea
                lines1.append( line )

        odd = True  # we are going to split into odd and even lines
        lines2 = []

        for ix, i_line in enumerate( lines1 ):

            # alternate odd even
            if odd:
                part_b = i_line
                odd    = False
            else:
                # if first line does not start with http or https
                # we will return False
                if ix == 1:  # 2 in a way fix this?
                    #  add www,  use in to find a beginning
                    #  https://snippets.readthedocs.org/en/latest/
                    #  012345
                    #  !! need to check for both http and htts
                    # !! find and use is_url function
                    prefix = i_line[0:4]
                    if prefix != "http":
                        prefix = i_line[0:5]
                        if prefix != "https":
                            self.logger.info("prefix " + prefix)
                            return (False, "not http or https", "")

                lines2.append( i_line + " " + part_b  )
                odd = True

        new = '\r\n'.join( lines2 )
        return (True, "transform_url_to_helpdb", new)


    # ------------------------------------------
    def transform_upload_log(self, in_text, ):
        """
        17:12 	(Upload log)‎[Smithers‎ (8×)]
         		17:12  Smithers talk contribs block uploaded File:Bolt hole sketch.png ‎
         		17:11  Smithers talk contribs block uploaded File:Key hole sketch detailed.png ‎
         		17:11  Smithers talk contribs block uploaded File:Key hole pad.png ‎
         		17:10  Smithers talk contribs block uploaded File:Body with kh sketch closeup.png ‎
         		16:45  Smithers talk contribs block uploaded File:Body 2a.png ‎
         		16:45  Smithers talk contribs block uploaded File:Body 2.png ‎
         		16:44  Smithers talk contribs block uploaded File:Body.png ‎
         		14:02  Smithers talk contribs block uploaded File:Assembly.png ‎
    N   17:03 	FreeCAD - Editing step and stl Files‎‎ 5 changes history+3,417‎ [Smithers‎ (5×)]
        13:56 	MediaWiki on Mint‎‎ 5 changes history+902‎ [Smithers‎ (5×)]

        ---------------
        take url list and change to wiki format
        return success flag and transformed text in tuple
        ** modify so makes bold ?? consider underlined
        !! current code ugly does not do www.

        ( is_done, did_what, ret_text )
        make something like:
        *'''[https://www.ebay.com/sch/i.html?_odkw=arduino+nano+usb+with+cable
         arduino nano usb with cable ftdi | eBay ]'''

        """

        # print( f" transform upload log called " )
        lines0 = in_text.split("\n")
        if len(lines0) < 2:
            return (False, "not", "2 short")
        # rint lines0

        # print( f" transform upload log called  passed 2 line test " )
        lines1 = []
        # clean up white space -- list comp ??
        lines1 = []
        for i_line in lines0:
            line = i_line.strip()
            if line != "":  # not sure why this is good idea
                lines1.append(line)

        # find " File:"    len( " File:" )  6
        lines2     = []
        for i_line in lines1:

            ix_find    =  i_line.find( " File:",)
            if ix_find >=0:
                lines2.append( i_line[ ix_find + 6 : ])
            # else:
            #     print( f" File: not found in {i_line}" )


        ret_str   = self.file_list_to_gallery_str( lines2 )

        ret_str   = f"{ret_str}\n{self.file_list_to_image_str( lines2 )}"

        return (True, "upload_log", ret_str)



        # odd = True  # we are going to split into odd and even lines
        # lines2 = []

        # for ix, i_line in enumerate(lines1):

        #     # alternate odd even
        #     if odd:
        #         part_b = i_line
        #         odd    = False
        #     else:
        #         # if first line does not start with http or https
        #         # we will return False
        #         if ix == 1:  # 2 in a way fix this?
        #             #  add www,  use in to find a beinning
        #             #  https://snippets.readthedocs.org/en/latest/
        #             #  012345
        #             #  !! need to check for both http and htts
        #             # !! find and use is_url function
        #             prefix = i_line[0:4]
        #             if prefix != "http":
        #                 prefix = i_line[0:5]
        #                 if prefix != "https":
        #                     self.logger.info("prefix " + prefix)
        #                     return (False, "not http or https", "")

        #         lines2.append("*'''[" + i_line + " " + part_b + " ]'''")
        #         odd = True

        # new = '\r\n'.join( lines2 )
        # return (True, "upload_log", new)

    # ------------------------------------------
    def file_list_to_gallery_str( self, file_list ) :
        """
        <gallery>
          Image: Key hole sketch detailed.png |‎ Key hole sketch detailed.png ‎    *image1
          Image: Key hole pad.png ‎ | Key hole pad.png
          Image: Body with kh sketch closeup.png ‎| Body with kh sketch closeup.png ‎
          Image: Body 2a.png |‎ Body 2a.png ‎
          Image: Body 2.png |‎ Body 2.png
          Image: Body.png |‎ Body.png
          Image: Assembly.png ‎| Assembly.png
        </gallery>


        """
        if len( file_list ) == 0:
            return ""

        ret_str   = "<gallery>\n"
        for ix, i_file in enumerate( file_list ):
            ret_str   = f"{ret_str}   Image: {i_file} | {i_file} #{ix}\n"

        ret_str       = f"{ret_str}</gallery>"

        return ret_str

   # ------------------------------------------
    def file_list_to_image_str( self, file_list ) :
        """
        <!-------------- image 1 ------------->
        [[Image: Body with kh sketch closeup.png |500px|left|The Body]]
        Sketch place just where the plug is to go.
        <br style="clear:both" />

        """
        if len( file_list ) == 0:
            return ""

        ret_str   = "\n"
        for ix, i_file in enumerate( file_list ):
            ret_str   = f"{ret_str}<!-------------- image {ix} ------------->\n"
            ret_str   = f"{ret_str}[[Image: {i_file} |500px|left| image {ix} image {i_file}]]\n"
            ret_str   = f"{ret_str}text for file  {i_file} image {ix}\n"
            ret_str   = f"{ret_str}<br style=\"clear:both\" />\n\n"
        #ret_str    = f"{ret_str}</gallery>"

        return ret_str


    # ------------------------------------------
    def transform_url_wiki(self, in_text, ):
        """
        take url list and change to wiki format
        return success flag and transformed text in tuple
        ** modify so makes bold ?? consider underlined
        !! current code ugly does not do www.

        ( is_done, did_what, ret_text )
        make something like:
        *'''[https://www.ebay.com/sch/i.html?_odkw=arduino+nano+usb+with+cable
         arduino nano usb with cable ftdi | eBay ]'''

        """
        lines0 = in_text.split("\n")
        if len(lines0) < 2:
            return (False, "not", "2 short")
        # rint lines0
        lines1 = []

        # clean up white space
        for i_line in lines0:
            line = i_line.strip()
            if line != "":  # not sure why this is good idea
                lines1.append(line)

        odd = True  # we are going to split into odd and even lines
        lines2 = []

        for ix, i_line in enumerate(lines1):

            # alternate odd even
            if odd:
                part_b = i_line
                odd    = False
            else:
                # if first line does not start with http or https
                # we will return False
                if ix == 1:  # 2 in a way fix this?
                    #  add www,  use in to find a beinning
                    #  https://snippets.readthedocs.org/en/latest/
                    #  012345
                    #  !! need to check for both http and htts
                    # !! find and use is_url function
                    prefix = i_line[0:4]
                    if prefix != "http":
                        prefix = i_line[0:5]
                        if prefix != "https":
                            self.logger.info("prefix " + prefix)
                            return (False, "not http or https", "")

                lines2.append("*'''[" + i_line + " " + part_b + " ]'''")
                odd = True

        new = '\r\n'.join(lines2)
        return (True, "urls to wiki", new)

    # ------------------------------------------
    def transform_no_ws( self, in_text,  ):
        """
        no white space
        """
        ret_text   ="".join( in_text.split() )
        #ret_text = "no ws not implemented"
        return ( True, "no white space", ret_text )

    # ------------------------------------------
    def transform_less_ws( self, in_text,  ):
        """
        less white space -- multiple spaces reduced to one
        """
        ret_text   =" ".join( in_text.split() )
        #ret_text = "no ws not implemented"
        return ( True, "less white space", ret_text )

    # ------------------------------------------
    def transform_cap( self, in_text,  ):
        """
        capitalize  -- always works
        """
        ret_text   = in_text.upper()
        #ret_text = "no ws not implemented"
        return ( True, "cap", ret_text )


    # ------------------------------------------
    def transform_test( self, in_text,  ):
        """
        test -- look at supporting stuff
        """
        ret_text    = in_text
        #ret_text   = in_text.upper()
        #ret_text = "no ws not implemented"
        return (False, "test not implemented", ret_text )

    # ------------------------------------------
    def transform_lower( self, in_text,  ):
        """
        lower -- always works
        """
        ret_text   = in_text.lower()
        #ret_text = "no ws not implemented"
        return ( True, "lower", ret_text )

    # ------------------------------------------
    def transform_user_pages(self, in_text, ):
        """
        for mass delete of user pages
        """
        lines = in_text.split("\n")
        # non_blank_lines = [a_line.strip() for a_line in lines if len(a_line.strip()) > 0]  # drop empty line

        trans_lines    = []
        for i_line in lines:
            #m ! 15:35 	User:

            ix_find    = i_line.find( "User:", 0, ) # end=len(string) )
            if ix_find > 0:
#                i_line    = i_line[ ix_find + 5 : ]
                i_line    = i_line[ ix_find : ]
                splits    = i_line.split( " " )
                i_line    = splits[0]

                trans_lines.append( i_line )
            else:
                pass

        ret_text = "\n".join( trans_lines )

        return (True, "user page transform", ret_text)

    # ------------------------------------------
    def transform_comma_sep(self, in_text, ):
        """
        for email concat, extract each line, put in a comma to replace \n
        ?? enhance other seps, quote elements..... look a csv stuff that might already exist
        """
        lines = in_text.split("\n")
        non_blank_lines = [a_line.strip() for a_line in lines if len(a_line.strip()) > 0]  # drop empty line

        # rint non_blank_lines

        if len(non_blank_lines) == 0:
            return (False, "commas in", "")

        ret_text = ",".join(non_blank_lines)

        return (True, "commas in", ret_text)

    # ------------------------------------------
    def transform_sage(self, in_text, ):
        """
        for sage to sage math notebook
        """
        lines = in_text.split( "\r" )

        new_lines = []

        for a_line in lines:
            b_line     = a_line.replace("\n", "")
            new_lines.append( b_line )

        lines = new_lines
        #non_blank_lines = [a_line.strip() for a_line in lines if len(a_line.strip()) > 0]  # drop empty line

        #print( lines )

        # lines to drop  --
        # lines to blank
        # lines to comment

        # replace an entire of line
        for ix_line, a_line in enumerate( lines ):
            #print( a_line )
            a_line     = a_line + " "
            print( a_line )
            print("")
            if a_line.startswith( "SageMath " ):
                print("fix SageMath")
                a_line = " "
                lines[ix_line]  = a_line

        # -- words to blank
        # replace at beginning of line
        # replace sage with blank
        for ix_line, i_line in enumerate( lines ):
            #a_line = a_line.replace( )
            if i_line.startswith( "sage: " ):
                i_line = i_line[6:]
                lines[ix_line]  = i_line

#        lines_2 =
#        # rint non_blank_lines
#
#        if len(non_blank_lines) == 0:
#            return (False, "commas in", "")

        ret_text = "\r\n".join( lines )

        return (True, "notebook edits", ret_text)

    # ------------------------------------------
    def transform_un_dent( self, in_text,  ):
        """
        find no of spaces on first line and remove from rest of lines
        return tuple
        """
        lines             = in_text.split( "\n" )

        if len( lines ) < 1:
            return ( False, "un_dent", "" )

        no_blank = 0
        for  i_char in lines[0]:
            if i_char != " ":
                break
            no_blank += 1
        if no_blank == 0:
            return ( False, "un_dent", "" )

        delete_me         = " " * no_blank
        new_lines         = []
        # now work through lines
        for i_line  in lines:
            ix_del   = i_line.find( delete_me, 0, )
            if ix_del == 0:
                new_lines.append( i_line[ no_blank: ] )
            else:
                new_lines.append( i_line )
                # should not happen, but could ( bad copy )

        #rint new_lines

        ret_text     = "\n".join( new_lines )

        return ( True, "un_dentn", ret_text )

    # ------------------------------------------
    def is_filename( self, a_string,  ):
    #def is_filename( self, a_string,  ):   is_file    file_exists  ?? not sure
        """
        looks to see if file exists
        clean up a_string and see if it starts with a file name
        return flag, cleaned_up_filename
        is the  string a file name -- full path
        might at least strip the name??
        unlike is url no clean up, perhaps a different name
        consider typing the string get_string_type
        return ( < boolean >, <cleaner filename perhaps > )

        """
        #print( "a_string = " + str( a_string ) )
        parts       = a_string.split()
        test_fn     = parts[0]
        #print( "parts = " + str( parts ) )
        #print( "----------------------------")
        #print( "a_string = " + str( a_string ) )

        is_fn        =  os.path.isfile( test_fn )   # accepts spaces on end under windows
        #print( a_string )
        #print( " in is_filename  " + str( is_fn ) )

        return is_fn, test_fn

    # ------------------------------------------
    def is_filename_with_ext( self, a_string, ext_list  ):
        """
        is a_string a file name with an extension in the list a_list, and does file exist  -- not clear why we return the file name

        returns the tuple ( <flag true false>, <filename with extension, may clean up in future or not >, <extension found > )
        extensions include the . as in .txt not txt

        should this test for existence I think so else it is looks like file name not is
        a_string  is the  string a file name -- full path with an extension in the list of strings
                  no cleanup
        strip the filename before calling for \r\n....  ??
        look at extensions and see if match list
        extension includes the dot .txt

        """
        # print("is_filename_text:")
        #print( a_string )
        flag, file_name  = self.is_filename( a_string )
        if not( flag ):
            #print( "--not a filename" )
            return ( False, "", "" )

        file_name_1, extension = os.path.splitext( a_string )
        if ext_list is None:
            return ( True, file_name, extension )
        elif  ( extension in  ext_list ):
            return ( True, file_name, extension )
        else:
            return ( False, "", "" )
        # or return ( extension in  a_list )
        #  never get here

    # ------------------------------------------
#    def is_filename_ext( self, a_string, a_list  ):
#        """
#        drop this guy
#        a_string  is the  string a file name -- full path with an extension in the list of strings
#                  no cleanup
#        strip the filename before calling for \r\n....
#        look at extensions and see if match list
#        return boolean
#        """
#        print("drop this guy")
#        #print( a_string )
#        ( flag, file_name, ext )  = self.is_filename_with_ext( a_string, a_list  )
#        return flag

    # ------------------------------------------
    def is_filename_text( self, a_string,  ):
        """
        how different from above, this is a mess !!
        not really right doc, may need refactoring

        is the  string a file name for a text file -- full path
        consider typing the string get_string_type
        look at extensions and see if match list
        return boolean
        """

        flag, a_fn, a_ext =  self.is_filename_with_ext(  a_string, self.text_extends  )
        return flag

    # ----------------------------------------
    def clean_string(self, a_string):
        #def clean_string( a_string ):
        """
        clean up string into non empty parts, eliminate excess white space

        is this worth a function ?? this is a one liner
        :param self:
        :param a_string:
        :return: list of clean parts or clean string

        """
        # cmd> url  https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python
        # cmd> url  http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/
        # a_url  = r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"

        #print "clean up whitespace "
        # sentence = ' hello \r\n   apple'
        # print sentence.split()
        b_string = " ".join(a_string.split())
        #  print b_string

        return ( b_string )

# ------------------- unit tests -------------------
# not really maintained, to use may need to fix
# comment out to delete or revise and use

#def old_test():
#
#    a_string = "this is it \t and what             \n and more    . "
#    print( "------------------" )
#    print( a_string )
#    #print clean_s
#
## -------------------
#def test_clean():
#
#    test_object       = CmdProcessor(  "controller" )
#
#    a_string = "this is it \t and what             \n and more    . "
#    print( "------------------" )
#    print( a_string )
#    print( test_object.clean_string( a_string ) )
#
## -------------------
#def test_process_url():
#    """
#    unit test type function
#    """
#    test_object       = CmdProcessor(  "controller" )
#
#    # test urls
#
#    a_string = r"structables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"     # not a url  invoks a search stop this
#    a_string = r"www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"
#    a_string = r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"
#    #a_string = r"       http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"
#    #a_string = r"       http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/  junk at end, does what"  # junk seems to be ignored
#    # a_string = r"       http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"
#    print( "------------------" )
#    print( a_string )
#
#    # choose a function
#    #print test_object.process_url( a_string )
#    #print test_object.process_if_url( a_string )
#
#
## -------------------
#def test_do_if_cmd():
#    """
#    unit test type function
#    check against pb style commands and if it is one execute
#    for now back in the contoller
#    why do this way ??
#    """
#
#    test_object       = CmdProcessor(  "controller" )
#
#    cmds  = [ "*>print hello world",
#              "*>url http://www.instructables.com/tag/type-id/?sort=RECENT",
#              "*>shell shell command",
#              "*>shellfish shell command",
#              r"*>text  D:\router.txt",
#              "*>shellfish shell command",
#              "*>shell shell command",
#              "*>shellfish shell command",
#              ]
#
#
#def cmd_strings_1( ):
#        strings         = [    "junk",
#                                "other cruft",
#                               "*>bat",   # mess with this for different tests
#                               "c:",
#                               "dir",
#                               r"rem high there",
#                               r"rem",
#                               r"dir       d:\*.txt" ,
#                               r"rem exit next ",
#                               r"exit",
#                               r"rem after exit end next",
#                               r"*>end",
#                               r"exit"
#                           ]
#
#        return strings
#
## ----------
#
#def test_do_if_star_bat_cmd():
#    """
#    unit test type function
#    check against pb style commands and if it is one execute
#    for now back in the controller
#    why do this way ??
#    """
#    #do_if_star_bat_cmd(self, a_string ):
#    # output is coming back here
#    import test_controller
#    a_controller    = test_controller.TestController( )
#    a_tester        = CmdProcessor( a_controller )
#
#    strings = cmd_strings_1()
#
#    a_string  =  "\n".join( strings )
#    #print( a_string )
#
#    a, b, c  = a_tester.do_if_star_bat_cmd( a_string )
#
#    print( c )
#
## -------------------
#def test_is_file_cmd():
#    """
#    unit test type function
#    check against pb style commands and if it is one execute
#    for now back in the controller
#    why do this way ??
#    """
#    #do_if_star_bat_cmd(self, a_string ):
#    # output is coming back here
#    import test_controller
#    a_controller = test_controller.TestController( )
#    a_tester        = CmdProcessor( a_controller )
#
#    strings = cmd_strings_1()
#
#    a_string  =  "\n".join( strings )
#    #print( a_string )
#    ( flag, list )   = a_tester.is_file_cmd( "*>bat", a_string )
#
#    print( flag, list )


if __name__ == "__main__":
    """
    bunch of tests or run app
    """

    # this are likely out of date and will not work
    # need fake controller to run these now
    #test_clean()
    #test_process_url()
    #test_is_url()
    # test_do_if_cmd()

#    test_do_if_star_bat_cmd()
    #test_is_file_cmd()

    # no test just run it
    import clip_board
    app = clip_board.App( None, None  )


