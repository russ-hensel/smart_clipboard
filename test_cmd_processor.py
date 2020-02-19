# -*- coding: utf-8 -*-


"""
tests for cmd_processor.CmdProcessor
"""


import sys
sys.path.append( "../" )
import test_controller
#import smart_terminal_helper
import cmd_processor
import unittest

class TestStuff( unittest.TestCase ):
    """
    magically run all methods that start with test, turn off with x
    """

#    def __init__(self, name, chases_cats):
#        unittest.TestCase.__init__(self, )
#    @classmethod
#    def setUpClass( cls ):
#        print "what is cls "
#        # self.tc   = test_controller.TestController()

    # seem to run for each test function below
    def setUp(self):
        # can put condeitionals in here to do different setup... for differen tests
        print('In setUp()')

        a_controller           = test_controller.TestController( )
        self.cmd_processor     = cmd_processor.CmdProcessor(   )
        # self.fixture = range(1, 10)

    def tearDown(self):
        print( 'In tearDown()' )
        del self.cmd_processor

#    def test_upper(self):
#        """test_upper"""   # have this for testing messages
#        self.assertEqual('foo'.upper(), 'FOOd')
#========================== v3 =============================


    # -------------------
    def xtest_do_cmds( self ):
        print( """
        v3
        test_do_cmds()

        """)
        test_list         = []     # commands can be multi or single line

#        --------------------- bat command --------------
#        a_string          = r"*>bat      " + "\nrem test1  \ndir D:\\*.* \ndir e:\\*.* \ndir f:\\*.* " + "\n*>end"
#        test_list.append( ( a_string ,       True, [""]  ) )

        #-----------------------------  single line url
        a_string          = r"*>url          http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"
        test_list.append( ( a_string ,       True, [""]  ) )

#       ----------------- single line bad url
        a_string          = r"*>url          tp://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"
        test_list.append( ( a_string ,       False, [""]  ) )

#       ----------------- a long line of stuff ---------------------
        a_string          = r"How to use Split in Python"

        a_string          = a_string + "\n" +  r"http://www.pythonforbeginners.com/dictionary/python-split"

        a_string          = a_string + "\n" + r"Python String split() Method"

        a_string          = a_string + "\n" + r"httttttps://www.tutorialspoint.com/python/string_split.htm"

#        a_string          = r"welcome russ_hensel
#
#        a_string          = r"https://www.instructables.com/you?show=PUBLISHED&limit=70&sort=VIEWS
#
#
#        a_string          = r"Polishing Badly Tarnished Brass: 7 Steps"
#        test_list.append( ( a_string ,       False, [""]  ) )
#
#        a_string          = r"https://www.instructables.com/id/Polishing-Badly-Tarnished-Brass/"
#        test_list.append( ( a_string ,       False, [""]  ) )
#
#        a_string          = r"Battery Holder for Double A, Triple A, C and D Cells-batteries. Cheap, Good, Easy: 6 Steps"
#        test_list.append( ( a_string ,       False, [""]  ) )
#
#        a_string          = r"https://www.instructables.com/id/Battery-Holder-for-Double-A-Triple-A-C-and-D-cel/"
#        test_list.append( ( a_string ,       False, [""]  ) )
#
#        a_string          = r"Almost a Power Supply: 5 Steps"
#        test_list.append( ( a_string ,       False, [""]  ) )
#
#        a_string          = r"https://www.instructables.com/id/Almost-a-Power-Supply/"
        test_list.append( ( a_string ,       False, [""]  ) )
#       -------------------- multi line *> command no bat   ---------------------

        a_string          =                    r"*>text    D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\test_controller.py"

        a_string          = a_string + "\n" + r"*>shell   %windir%\system32\notepad.exe"

        a_string          = a_string + "\n" +r"*>text   D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\help.txt"

        a_string          = a_string + "\n" +  r"http://www.pythonforbeginners.com/dictionary/python-split"

        test_list.append( ( a_string ,       True, [""]  ) )
#        a_string          = a_string + "\n" + r"Python String split() Method"
#       -----------------
#        a_string          = a_string + "\n" + r"httttttps://www.tutorialspoint.com/python/string_split.htm"
#
#        test_list.append( ( a_string ,       True, [""]  ) )
#       -------------------- ---------------------

#        a_string          = r"*>text    D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\test_controller.py"
#        test_list.append( ( a_string ,       True, [""]  ) )
#       -------------------- ---------------------
#        a_string          = r"*>shell   %windir%\system32\notepad.exe"
#        test_list.append( ( a_string ,       True, [""]  ) )
#       -------------------- ---------------------
#        a_string          = r"*>text   D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\help.txt"
#        test_list.append( ( a_string ,       True, [""]  ) )


        # -----------------

        all_passed = True
        for i_test in test_list:
                print( " " )
                print( " -------------------------------------------------- " )
                test_lines, right_fl, right_list  = i_test

                msg    = "Testing test lines =>> "
                print( msg )
                print( test_lines )
                print( "<<=Testing test lines \n"   )

                flag, what_done, new_text    = self.cmd_processor.do_cmds( test_lines, ["*>"] )

                print( "returned = " + str( flag ) + " " + str( what_done ),  end="" )
                #print( new_text )

#                an_assert    = flag is right_fl
                if not( flag is right_fl ):
                    all_passed =  False
                    print( ":  line failed" )
                else:
                    print( ":  line passed \n\n" )

        self.assertTrue( all_passed is True )
        if all_passed:
            print("all test in test_do_if_star_shell_cmd  passed")
        else:
            print("NOT all test in test_do_if_star_shell_cmd  passed")

    # -------------------
    def xtest_do_cmds_bat( self ):
        print( """
        v3
        test_do_cmds_bat     for do_bat_cmd

        """)
        test_list         = []

        a_string          = r"*>bat      " + "\nrem test1  \ndir D:\\*.* \ndir e:\\*.* \ndir f:\\*.* " + "\n*>end"
        test_list.append( ( a_string ,       True, [""]  ) )

        a_string          = r"*>bat       " +  "\nrem test2 \ndir D:\\*.* \ndir e:\\*.* \ndir f:\\*.* " + "\n*>endx"
        test_list.append( ( a_string ,       False, [""]  ) )

        a_string          = r"*>bat  JACK    " + "\nrem test3 \ndir D:\\*.* \ndir e:\\*.* \ndir f:\\*.* " + "\n*>end"
        test_list.append( ( a_string ,       False, [""]  ) )

        a_string          = "\nrem test4  \n*>bat  JACK    " + "\nrem test4 \ndir D:\\*.* \ndir e:\\*.* \ndir f:\\*.* " + "\n*>end"
        test_list.append( ( a_string ,       False, [""]  ) )

        all_passed = True
        for i_test in test_list:
                print( " " )
                print( " -------------------------------------------------- " )
                test_lines, right_fl, right_list  = i_test

                msg    = "Testing test lines =>> "
                print( msg )
                print( test_lines )
                print( "<<=Testing test lines "   )

                flag, what_done, new_text    = self.cmd_processor.do_cmds( test_lines, ["*>"] )

                print( "returned = " + str( flag ) + " " + str( what_done ),  end="" )
                #print( new_text )

                #an_assert    = flag is right_fl
                if not( flag is right_fl ):
                    all_passed =  False
                    print( ":  line failed" )
                else:
                    print( ":  line passed" )

        self.assertTrue( all_passed is True )
        if all_passed:
            print("all test in test_do_if_star_shell_cmd  passed")
        else:
            print("NOT all test in test_do_if_star_shell_cmd  passed")

    # -------------------
    def xtest_is_url( self ):
        """
        v2 -> v3
        unit test type function here testing is_url( test_url )
        only gets counted as one test, quits on first fail else ok
        all are ok if no errors found
        """
        print( """---------------------------

        test_is_url()

        """)

        test_list   = [ (   r"structables.com/id/Bandsaw-Stand-From-Scrap-Lumber/" ,  False, "" ),

                        (   r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/" , True,
                            r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"               ),

                        (   r"       http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/" , True,
                                   r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"       ),

                        (   r"       http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/ and then a bunch of junk" , True,
                                   r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"       ),

                        (   r"       https://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/ and then a bunch of junk" , True,
                                   r"https://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"       ),

                        (   r"www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/ and then a bunch of junk" , True,
                                   r"www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"       ),

                       ]

        for i_test in test_list:

                test_url, right_ans, clean  = i_test
                print( "Testing =>>" + test_url )
                msg = test_url + " should be  " + str( right_ans )
                flag, ret_url    = self.cmd_processor.is_url( test_url )
                self.assertTrue( flag is right_ans ,  msg )

                if (flag is right_ans) and flag:
                    msg = test_url + " did not clean up "
                    self.assertTrue( ret_url == clean, msg )


    # -------------------
    def xtest_do_star_url_line( self ):
        """
        ver 3
        """
        print( """---------------------------

        test_do_star_url()

        """)

        test_list         = []

        a_string          = r"*>url   https://forum.allaboutcircuits.com"
        test_list.append( ( a_string ,       True, [""]  ) )

        a_string          = r"*>xurl   https://forum.allaboutcircuits.com"
        test_list.append( ( a_string ,       False, [""]  ) )

        a_string          = r"*>url   gttps://forum.allaboutcircuits.com"
        test_list.append( ( a_string ,       False, [""]  ) )

#        a_string          = r"*>url   https://forum.allaboutcircuits.com"
#        test_list.append( ( a_string ,       True, [""]  ) )

#
#
#        # get two
#        a_string          = r"""*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt
#        \n    *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt
#        \n    and junk here *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt """


        all_passed = True
        for i_test in test_list:
                print( " " )
                #err_list     = []

                test_line, right_fl, right_list  = i_test

                msg    = "Testing is_line =>> "   + test_line
                #err_list.append( msg )
                print( msg )

                #msg = cmd  + " should be  " + str( right_list )

                flag, what_done, new_text    = self.cmd_processor.do_star_url_line( test_line )

                print( "return = " + str( flag ) + " " + str( what_done ) )

                #an_assert    = flag is right_fl
                if not( flag is right_fl ):
                    all_passed =  False
                    print( "line failed" )
                else:
                    print( "line passed" )
                    # msg = test_url + " did not clean up "
                    #self.assertTrue( ret_url == clean, msg )

                #self.assertTrue( flag is right_ans ,  msg )
                self.assertTrue( flag is right_fl )
        if all_passed:
            print("all test in test_do_star_url  passed")

    # -------------------
    def xtest_do_star_shell_line( self ):
        """
        ver 3
        """
        print( """---------------------------

        test_do_star_shell_line()

        """)

        test_list         = []

        a_string          = r"*>shell   https://forum.allaboutcircuits.com"
        test_list.append( ( a_string ,       True, [""]  ) )

        a_string          = r"*>shell   %windir%\system32\notepad.exe"
        test_list.append( ( a_string ,       True, [""]  ) )

        a_string          = r"*>shell   D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\help.txt"
        test_list.append( ( a_string ,       True, [""]  ) )

#        a_string          = r"*>url   https://forum.allaboutcircuits.com"
#        test_list.append( ( a_string ,       True, [""]  ) )

#        # get two
#        a_string          = r"""*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt
#        \n    *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt
#        \n    and junk here *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt """

        all_passed = True
        for i_test in test_list:
                print( " " )
                #err_list     = []

                test_line, right_fl, right_list  = i_test

                msg    = "Testing is_line =>> "   + test_line
                #err_list.append( msg )
                print( msg )

                #msg = cmd  + " should be  " + str( right_list )

                flag, what_done, new_text    = self.cmd_processor.do_star_shell_line( test_line )

                print( "return = " + str( flag ) + " " + str( what_done ) )

                #an_assert    = flag is right_fl
                if not( flag is right_fl ):
                    all_passed =  False
                    print( "line failed" )
                else:
                    print( "line passed" )
                    # msg = test_url + " did not clean up "
                    #self.assertTrue( ret_url == clean, msg )

                #self.assertTrue( flag is right_ans ,  msg )
                self.assertTrue( flag is right_fl )
        if all_passed:
            print("all test in test_do_star_url  passed")

    # -------------------
    def xtest_do_star_text_line( self ):
        """
        ver 3
        """
        print( """---------------------------

        test_do_star_text_line()

        """)

        test_list         = []

        a_string          = r"*>text    D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\test_controller.py"
        test_list.append( ( a_string ,       True, [""]  ) )

        a_string          = r"*>shell   %windir%\system32\notepad.exe"
        test_list.append( ( a_string ,       False, [""]  ) )

        a_string          = r"*>text   D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\help.txt"
        test_list.append( ( a_string ,       True, [""]  ) )

#        a_string          = r"*>url   https://forum.allaboutcircuits.com"
#        test_list.append( ( a_string ,       True, [""]  ) )

#        # get two
#        a_string          = r"""*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt
#        \n    *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt
#        \n    and junk here *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt """


        all_passed = True
        for i_test in test_list:
                print( " " )
                #err_list     = []

                test_line, right_fl, right_list  = i_test

                msg    = "Testing *>text =>> "   + test_line
                #err_list.append( msg )
                print( msg )

                #msg = cmd  + " should be  " + str( right_list )

                flag, what_done, new_text    = self.cmd_processor.do_star_text_line( test_line )

                print( "return = " + str( flag ) + " " + str( what_done )   + " >>  " + str( new_text ))

                #an_assert    = flag is right_fl
                if not( flag is right_fl ):
                    all_passed =  False
                    print( "line failed" )
                else:
                    print( "line passed" )
                    # msg = test_url + " did not clean up "
                    #self.assertTrue( ret_url == clean, msg )

                #self.assertTrue( flag is right_ans ,  msg )
                self.assertTrue( flag is right_fl )
        if all_passed:
            print("all test in test_do_star_url  passed")



# =============================== v2 not yet updated =====================
    # -------------------
    def xtest_do_text( self ):
        print( """

        testing do_text()

        """)

        file_list   = [
        r"*>text D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\clipboard.py_log",
        r"*>xtext D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\cmd_processor_utest.py",
        r"*>text D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\cmd_processor.py    ",
        r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\help.txt",
        r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\readme_rsh.txt   ",
        r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\parameters.py",
        r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\clip_board.p",
        r"*>xtextxxx D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\test_controller.py",
        r"*>xtext D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\readme.txt",
        r"*>xtext D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\gui.py",
        r"*>xtext D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\app_global.py joe",
        r"*>text D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\ver2.zip",
        ]
        #print( file_list )
        #file_list_str  = "\n".join( file_list )
        #print( file_list_str )
        ret   = self.cmd_processor.do_text( file_list )
        #print( ret )

    # -------------------
    def xtest_is_filename_with_ext( self,  ):
        """
        """
        print( """

        test_is_filename_with_ext()   is name of existing file with an extension ( is file existance tested ?? )

        """)
        test_list         = [  ]

        a_string          =  r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\readme_rsh.txt"
        test_list.append( (  a_string ,  [".txt"],     True, [""]  ) )

        a_string          =  r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\readme_rshxxx.txt"
        test_list.append( (  a_string ,  [".txt"],     False, [""]  ) )

        a_string          =  r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\readme_rsh.txt"
        test_list.append( (  a_string ,  [".txt", ".exe"],     True, [""]  ) )

        a_string          =  r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\readme_rsh.txt"
        test_list.append( (  a_string ,  [ ".exe", ".txt",],    True, [""]  ) )

        a_string          =  r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\readme_rsh.txt"
                          #     D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\readme_rsh.txt
        test_list.append( (  a_string ,  self.cmd_processor.text_extends,    True, [""]  ) )

        a_string          =  r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\readme_rsh.txt"
        test_list.append( (  a_string ,  [ ".exe"],     False, [""]  ) )

        #test_list.append( (  a_string ,  [".txt"],    True, [""]  ) )
        all_pass   = True
        for i_test in test_list:

                test_fn, test_ext_list, right_flag, text_ret  = i_test
                print( "Testing file =>>" + test_fn )
                msg = ">>" + test_fn + "<< should be  " + str( right_flag )

                a_tuple            = self.cmd_processor.is_filename_with_ext( test_fn, test_ext_list )
                flag, fn, a_ext    = a_tuple
                print( "returned a_tuple = " + str( a_tuple ))
                if not( flag is right_flag ):
                    all_pass   = False
                    print( "test fail" )
                else:
                    print( "pass")
        msg = "at least one fail in tests "
        #self.assertTrue( flag is right_flag ,  msg )
        self.assertTrue( all_pass ,  msg )
#                if (flag is right_ans) and flag:
#                    msg = test_url + " did not clean up "
#                    self.assertTrue( ret_url == clean, msg )
        if all_pass:
            print("all test in ... passed")

    # -------------------
    def xtest_is_filename( self ):
        """
        check to make sure "answers" are right
        consider allow blank lines befor file name
        """
        # these files are out of date, wrong directory
        print( """

        test_is_filename()   is name of existing file == True

        """)

        test_list   =  [ ( r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\help.txt",    True  ),
                         ( r"D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\readme_rsh.txt",   True  ),
                         ( r"D:\Russ\0000\python00\python3\_projects\readme_rsh.txt",  True ),
                         ( r"D:\Russ\0000\python00\python3\_projects\readme_rsh.text",  False ),
                       ]
        all_pass   = True

        for i_test in test_list:

                test_fn, right_flag,   = i_test
                print( "Testing file =>>" + test_fn )
                msg = ">>" + test_fn + "<< should be  " + str( right_flag )
                flag, fn    = self.cmd_processor.is_filename( test_fn )
                if not( flag is right_flag ):
                    all_pass   = False
                    print( "test fail" )
                else:
                    print( "pass")
                msg = "at least one fail in tests "
                #self.assertTrue( flag is right_flag ,  msg )
                self.assertTrue( all_pass ,  msg )
#                if (flag is right_ans) and flag:
#                    msg = test_url + " did not clean up "
#                    self.assertTrue( ret_url == clean, msg )
                if all_pass:
                    print("all test in ... passed")




    # -------------------
    def test_transform_add_url( self ):
        """
        transform_url_to_helpdb may be  add *>url in gui

        """
        test_list    = []    # build tuples for test

        in_text      = ( "Subscriptions - YouTube\n"   +
                        "https://www.youtube.com/feed/subscriptions" )



        right_text   = "not_testing"
        right_flag   = True

        test_list.append( (in_text, right_flag, right_text )  )


        for i_test in test_list:
            in_text, right_flag, right_text  = i_test

            ( flag, action, ret_text )  =  self.cmd_processor.transform_url_to_helpdb( in_text, )
            print( f"test_transform_add_url flag = {flag} action = {action} ret_text = {ret_text}" )
            msg = "test_transform_add_url"
            self.assertTrue( flag == right_flag,  msg )

 #  add test for





    # -------------------
    def xtest_transform_comma_sep( self ):
        """
        consider allow blank lines
        """
        print( """\n
        test_transform_comma_sep()

        """)

        test_list    = []

        in_texts     = [ "joe", "sue" ]
        in_text      = "\n".join( in_texts )
        right_text   = "joe,sue"
        test_list.append( (in_text, right_text )  )

        in_texts     = [ " joe", "sue " ]
        in_text      = "\n".join( in_texts )
        right_text   = "joe,sue"
        test_list.append( (in_text, right_text )  )

        for i_test in test_list:
            in_text, right_text  = i_test

            ( flag, action, ret_text )  =  self.cmd_processor.transform_comma_sep( in_text, )
            print( "ret_text = " + ret_text )
            msg = "comma_sep"
            self.assertTrue( right_text == ret_text,  msg )

     #  add test for

    # -------------------
    def xtestt_is_file_cmd( self ):
        #self.cmd_processor.is_file_cmd( self, a_cmd, a_string ):
        pass

    # -------------------
    def xxtest_is_line_cmd( self ):
        """
        unit test type function here testing is_line_cmd( "*>url" "*>url  here is a url " )
        only gets counted as one test, quits on first fail else ok
        all are ok if no errors found
        note that is_line_cmd is a subroutine in the object, not called externally
        """

        print( """

        test_is_line_cmd()  -- tests are incomplete as is code   -- put false at the end

        """)
        test_list   = [ (  r"*>url",    r"*>url    structables.com/id/Bandsaw-Stand-From-Scrap-Lumber/" ,       True, [""] ),  # really false if url is checked

                        (  r"*>url",    r"       *>url    http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/" ,   True, [""] ),

                        (  r"*>url",    r" noise      *>url    http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/" ,   True, [""] ),



                        (  r"*>shell",  r"*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt "  ,   True, [""] ),

                        (  r"*>shell",  r"*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt "  ,   True, [""] ),

                        (  r"*>url",    r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/" ,   False, [""] ),

#                        (   r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/" , True,
#                            r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"               ),

#                        (   r"       http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/" , True,
#                                   r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"       ),
#
#                        (   r"       http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/ and then a bunch of junk" , True,
#                                   r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"       ),
#
#                        (   r"       https://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/ and then a bunch of junk" , True,
#                                   r"https://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"       ),
#
#                        (   r"       www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/ and then a bunch of junk" , True,
#                                   r"www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"       ),

                       ]

        a_string          = r"*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt "
        test_list.append( ( r"*>url",    a_string ,       False, [""]  ) )
        test_list.append( ( r"*>shell",  a_string ,       True, [""]  ) )

        a_string          = r"""*>shellwww   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt """
        test_list.append( ( r"*>shell",  a_string ,       False, [""]  ) )

        # get two
        a_string          = r"""*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt
        \n    *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt
        \n    and junk here *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt """

        test_list.append( ( r"*>shell",  a_string ,       True, [""]  ) )

        # -------------------------------------
        a_string          = " some stuff  \n more stuff *>url https://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/ and then a bunch of junk"
        test_list.append( ( r"*>url",    a_string ,       True, [""]  ) )
        test_list.append( ( r"*>shell",  a_string ,       False, [""]  ) )

        all_passed = True
        for i_test in test_list:
                print( " " )
                err_list     = []

                cmd, test_line, right_fl, right_list  = i_test

                msg    = "Testing is_line_cmd =>>   " + cmd + " in " + test_line
                err_list.append( msg )
                print( msg )

                msg = cmd  + " should be  " + str( right_list )

                flag, ret_list    = self.cmd_processor.is_line_cmd( cmd, test_line, )

                print( str( flag ) + " " + str( ret_list ) )

                an_assert    = flag is right_fl
                if not( an_assert ):
                    all_passed =  False
                    print( "failed" )
                else:
                    print( "passed" )
                    # msg = test_url + " did not clean up "
                    #self.assertTrue( ret_url == clean, msg )

                #self.assertTrue( flag is right_ans ,  msg )
                self.assertTrue( flag is right_fl )
        if all_passed:
            print("all test in ... passed")

#    def test_upper(self):
#        """test_upper"""   # have this for testing messages
#        self.assertEqual('foo'.upper(), 'FOO')
#
#    def test_isupper(self):
#        self.assertTrue(  'FOO'.isupper(), "so good" )   # we can have a message
#        self.assertFalse( 'Foo'.isupper(), "is good" )
#
#    def test_split(self):
#        s = 'hello world'
#        self.assertEqual(s.split(), ['hello', 'world'])
#        # check that s.split fails when the separator is not a string
#        with self.assertRaises(TypeError):
#            s.split(2)


    # -------------------
    def xtest_do_if_star_shell_cmd( self ):
        """
        unit test type function here testing is_line_cmd( "*>url" "*>url  here is a url " )
        only gets counted as one test, quits on first fail else ok
        all are ok if no errors found
        note that is_line_cmd is a subroutine in the object, not called externally
        should it check if shell is in fact a file name, not now I guess ???
        """

        print( """

        test_do_if_star_shell_cm  -- t

        """)

        test_list         = []
        a_string          = r"*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_fileff.txt "
        test_list.append( ( a_string ,       True, [""]  ) )
        #test_list.append( ( a_string ,       True, [""]  ) )

        a_string          = r"""*>shellT   D:\Russ\0000\SpyderP\clipboard\fortosting\a_filfffe.txt """
        test_list.append( ( a_string ,       False, [""]  ) )

#        a_string          = r"*>shell   D:\Russ\0000\python00\python3\_projects\readme_rsh.txt "
#        test_list.append( ( a_string ,       True, [""]  ) )

        # not sure if popopen cmd should do anything or not
        a_string          = r"*>shell   cmd "
        test_list.append( ( a_string ,       True, [""]  ) )


        # get two
        a_string          = r"""*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt
        \n    *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt
        \n    and junk here *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt """


        all_passed = True
        for i_test in test_list:
                print( " " )
                #err_list     = []

                test_line, right_fl, right_list  = i_test

                msg    = "Testing is_line =>> "   + test_line
                #err_list.append( msg )
                print( msg )

                #msg = cmd  + " should be  " + str( right_list )

                flag, what_done, new_text    = self.cmd_processor.do_if_star_shell_cmd( test_line )

                print( "return = " + str( flag ) + " " + str( what_done ) )

                #an_assert    = flag is right_fl
                if not( flag is right_fl ):
                    all_passed =  False
                    print( "line failed" )
                else:
                    print( "line passed" )
                    # msg = test_url + " did not clean up "
                    #self.assertTrue( ret_url == clean, msg )

                #self.assertTrue( flag is right_ans ,  msg )
                self.assertTrue( flag is right_fl )
        if all_passed:
            print("all test in test_do_if_star_shell_cmd  passed")

    # -------------------
    def xtest_do_if_star_url_cmd( self ):
        """
        unit test type function here testing is_line_cmd( "*>url" "*>url  here is a url " )
        only gets counted as one test, quits on first fail else ok
        all are ok if no errors found
        note that is_line_cmd is a subroutine in the object, not called externally
        should it check if shell is in fact a file name, not now I guess ???
        """
        print( """\n
         test_do_if_star_url_cmd

        """)

        test_list         = []

        a_string          = r"*>url   https://forum.allaboutcircuits.com"

        #                   what to test     works????
        test_list.append( ( a_string ,       True, [""]  ) )

#        a_string          = r"*>url   https://forum.allaboutcircuits.com"
#        test_list.append( ( a_string ,       True, [""]  ) )



#
#
#        # get two
#        a_string          = r"""*>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt
#        \n    *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt
#        \n    and junk here *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt """


        all_passed = True
        for i_test in test_list:
                print( " " )
                #err_list     = []

                test_line, right_fl, right_list  = i_test

                msg    = "Testing is_line =>> "   + test_line
                #err_list.append( msg )
                print( msg )

                #msg = cmd  + " should be  " + str( right_list )

                flag, what_done, new_text    = self.cmd_processor.do_if_star_url_cmd( test_line )

                print( f"return = {flag} ,  {what_done} , { new_text }" )

                #an_assert    = flag is right_fl
                if not( flag is right_fl ):
                    all_passed =  False
                    print( "line failed" )
                else:
                    print( "line passed" )
                    # msg = test_url + " did not clean up "
                    #self.assertTrue( ret_url == clean, msg )

                #self.assertTrue( flag is right_ans ,  msg )
                self.assertTrue( flag is right_fl )
        if all_passed:
            print("all test in test_do_if_star_shell_cmd  passed")

    # -------------------
    def xtest_do_if_edit_text_file( self ):
        print( """

        test_do_if_edit_text_file

        """)

        test_list         = []

        a_string          = r"*>text   D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\readme_rsh.txt"
        test_list.append( ( a_string ,       True, [""]  ) )

        a_string          = r"*>text   D:\Russ\0000\python00\python3\_projects\clipboard\Ver2\gui.py"
        test_list.append( ( a_string ,       True, [""]  ) )


#        # get two
#        a_string          = r"""*>text   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file.txt
#        \n    *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt
#        \n    and junk here *>shell   D:\Russ\0000\SpyderP\clipboard\fortosting\a_file_2.txt """


        all_passed = True
        for i_test in test_list:
                print( " " )
                #err_list     = []

                test_lines, right_fl, right_list  = i_test

                msg    = "Testing is_lines =>> "   + test_lines
                print( msg )

                #msg = cmd  + " should be  " + str( right_list )

                flag, what_done, new_text    = self.cmd_processor.do_if_edit_text_file( test_lines )

                print( "return = " + str( flag ) + " " + str( what_done ) )

                #an_assert    = flag is right_fl
                if not( flag is right_fl ):
                    all_passed =  False
                    print( "line failed" )
                else:
                    print( "line passed" )
                    # msg = test_url + " did not clean up "
                    #self.assertTrue( ret_url == clean, msg )

                #self.assertTrue( flag is right_ans ,  msg )
        self.assertTrue( flag is right_fl )
        if all_passed:
            print("all test in test_do_if_star_shell_cmd  passed")


    # -------------------
    def xtest_do_if_star_bat_cmd( self ):
        print( """

        test_do_if_star_bat_cmd()

        """)
        test_list         = []

        a_string          = r"*>bat      " + "\nrem test1  \ndir D:\\*.* \ndir e:\\*.* \ndir f:\\*.* " + "\n*>end"
        test_list.append( ( a_string ,       True, [""]  ) )

        a_string          = r"*>bat       " +  "\nrem test2 \ndir D:\\*.* \ndir e:\\*.* \ndir f:\\*.* " + "\n*>endx"
        test_list.append( ( a_string ,       False, [""]  ) )

        a_string          = r"*>bat  JACK    " + "\nrem test3 \ndir D:\\*.* \ndir e:\\*.* \ndir f:\\*.* " + "\n*>end"
        test_list.append( ( a_string ,       False, [""]  ) )

        a_string          = "\nrem test4  \n*>bat  JACK    " + "\nrem test4 \ndir D:\\*.* \ndir e:\\*.* \ndir f:\\*.* " + "\n*>end"
        test_list.append( ( a_string ,       False, [""]  ) )

        all_passed = True
        for i_test in test_list:
                print( " " )
                print( " -------------------------------------------------- " )
                test_lines, right_fl, right_list  = i_test

                msg    = "Testing test lines =>> "
                print( msg )
                print( test_lines )
                print( "<<=Testing test lines "   )

                flag, what_done, new_text    = self.cmd_processor.do_if_star_bat_cmd( test_lines )

                print( "returned = " + str( flag ) + " " + str( what_done ) )
                print( new_text )

                #an_assert    = flag is right_fl
                if not( flag is right_fl ):
                    all_passed =  False
                    print( "line failed" )
                else:
                    print( "line passed" )

        self.assertTrue( flag is right_fl )
        if all_passed:
            print("all test in test_do_if_star_shell_cmd  passed")
        else:
            print("NOT all test in test_do_if_star_shell_cmd  passed")


if __name__ == '__main__':

    """
    magically run all methods that start with test, turn off with x

    comment out test with x   xtest
    tested  -- not all that well
    *>shell
    *>bat
    *>url


    """

    print("")
    print("")
    print("")
    print("==================== begin tests ===================")
    print("")
    unittest.main( exit = False )




    # ================== eof ================
