
============ version list ===============


version 5 -- get transform radio buttons to work
version 6 -- use dict case for transform buttons
             add a config parm for the location of snip snippet stuff

version 7 -- start using splitlines










============== punch list ===============

!!  help is messed up this is appg_lobal and parameters so may be true in several systems

** auto commands transforms have not worked for a long time
!! auto transforms
** !! but can do even more  get button to command hook up more automatic,,,, the redo stuff??
!! let parms select which buttons are in gui
!! separate snippet.file file names from there directory, still have to be in one directory
   but anywhere ... can we do relative to current ?? do we want to

snips_path_name
snips_files_filename     or fn
------------------
!! outdent can go to far ... some others ase well



*>bat    --- seems to work !! direct output to

*>python  --- no work at all ??

move snippets to sub dirs -- mostly in parameters and test

*! clean up test text file

=================================


tests in

    *>text   C:\Russ\0000\python00\python3\_projects\projects_rsh.txt


take wiki format for go to url
add   *>text
add    reverse \
add    one line
** add    * for bullet lists in wiki
** add indent
for ideas look at

!! sort all lines

String Manipulation - Plugins | JetBrains
    *>url  https://plugins.jetbrains.com/plugin/2162-string-manipulation/


================

ConvertWindowsPath/ConvPathOnClipboard.py at master · MikeTheWatchGuy/ConvertWindowsPath
    *>url  https://github.com/MikeTheWatchGuy/ConvertWindowsPath/blob/master/ConvPathOnClipboard.py


How to create your own clipboard manager using python and Tkinter
    *>url  https://medium.com/@prashantgupta24/how-to-create-your-own-clipboard-manager-using-python-and-tkinter-e693aa27fffc


applecrazy/xerox: Copy + Paste in Python.
    *>url  https://github.com/applecrazy/xerox



 # ----------------------- Do the convert ----------------------- #
    new_clipboard = ascii(clipboard)



==============
this readme
    D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\readme_rsh.txt
    is for the clipboard app  clip_board.py

see the help file
            *>text   D:\Russ\0000\python00\python3\_projects\clipboard\Ver3\help.txt


This (clip_board.py) is an application to enhance the windows ( unix ?? ) clipboard
by adding the ability to it to:

    transform keyboard contents
    insert predefined elements into the clipboard
    interpret copied text as commands or directions to the system to
        carry out some action specified in the clipboard contents for example
        browse to some website

    this file is largely developer notes, much of which may be scratch items

    for more information, more user oriented see help.txt


============== Environment =================

Application developed in the standard python 3.6 environment ( uses f"" so do not go < 3.6 )
Windows 10 Pro, but should work on any Python 3.6 environment
GUI in tkinter
tasks tend to be quick so this app is single threaded
Author:    Russ Hensel
russ-hensel (russ_hensel)
    *>url  https://github.com/russ-hensel


Status:  Runs fine, GUI is ugly but works.  Documentation is minimal
         Packaging pretty much none. Put the director and contents
         wherever you develop python, then run the module clip_board.py
         Read the code



============== ideas to add =================

    !! gui get all to button setup 3 -- also some gui values for radio buttons are wrong or missing
    !! transform ... get all to splitline if necessary
    !! new transform    -- add quotes at both ends double single

        *! remove trailing blanks  transform_no_trailing_space( self, in_text,  ):
        ** tab to spaces   transform_tab_to_space
        !! add more sorts, first line second line, just one line smart insert of spaces
        ** single line sort
        ** number the lines  transform_number_lines( self, in_text,  ):
        ** * the lines   transform_star_line()
        !! no blank lines  transform_no_blank_lines
        !! line break on .....
        !! camel cap ( use blank to include )
        !! underscore cap
        !! all forward slash ( from reverse )

    *! may need to clean up \r in many transforms..... how to manage \r\n in general -- splitlines
    !! update broke the logger fix it like backup



    !! run time configurable --- exactly how -- button groups
        wiki
        misc transforms
        format transforms
        help db transforms


    !! text and auto url, currently deleted from gui, subject to test/fix


==================  where commands go maybe  ===============

*>cmd
    pushbutton      >> self.controller.redo_if_star_cmd
    controller      >> self.redo_one_command( self.cmd_processor.do_cmds, [ "*>" ] )
    controller      >> ( is_done, did_what, ret_text )  = a_cmd( self.undo_clip, cmds_checked )   a_cmd is cmd_processor.do_cmds
    cmd_processor   >>


url
    pushbutton      >> self.controller.redo_if_url
    controller      >> self.redo_one_command(  self.cmd_processor.do_if_url_cmd, [ "*>url" ]  )
    controller      >>



redo_one_command( self, a_cmd, cmds_checked  ):
        """
        cmd should be one of cmd_processor.do_if.....  -- revise for v3 just starting
        call from gui thread
        get string from last command
        not clear what one command means, try to change the name
        """
        # a_cmd = self.cmd_processor.do_if_file_name
        #rint "=============== redo ============="
        #rint( self.undo_clip )

        ( is_done, did_what, ret_text )  = a_cmd( self.undo_clip, cmds_checked )

=================== make a new transform ===================

        in command processor make transform_user_pages

        make button for it in gui
         _make_transform_frame_


        in clipboard.py
              redo_transform_user



================= pushbuttons ===============
checked in polling

    controller      >>  self.do_command_transform( new_clip )

    controller      >> ( is_done, did_what, ret_text ) = self.do_commands( in_text )

                        if not( is_done ):   # --- if not a command try transform
                                    ( is_done, did_what, ret_text )  = self.do_transform( in_text ) #.upper()

    controller   do_commands    >>  self.cmd_processor.do_cmds( in_text, cmds_checked )

        cmd_processor           >>


================ old not very useful stuff  ================

 =


= Test stuff to copy  =

== Url's ==
Run a .bat file using python code - Stack Overflow
https://stackoverflow.com/questions/5469301/run-a-bat-file-using-python-code

python - Executing a subprocess fails - Stack Overflow
https://stackoverflow.com/questions/1818774/executing-a-subprocess-fails

How to capture stdout output from a Python function call? - Stack Overflow
https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call

How can I redirect print output of a function in python - Stack Overflow
https://stackoverflow.com/questions/14197009/how-can-i-redirect-print-output-of-a-function-in-python

        C:\MediaId.txt
        D:\Russ\0000\SpyderP\rshlib\other.txt
        South Coast Innovator Labs
        http://scilspace.org/

        Recent Instructables
        http://www.instructables.com/tag/type-id/?sort=RECENT

== star commands ==

what

*>bat
dir d:\apps\*.*
rem done
exit
*>end

*>bat
dir d:*.*
rem done something
exit
*>end

from pb not sure what all are

	run a program						*>run   <name of program>  <parm for program>
    do some sql ( maybe if right program kicking around or keep in pb )
    edit                                 *>edit  filename
    office text or spreadsheet           *>       filename
    batch command                        *>bat
    shell a file and see what dos does with it   *>shell


	display a particular help topic based on its id              	*>id
	search for help topics				*>search
	run a program						*>run
	run notepad						*>np
	run write							*>wr
	run win help						*>WHelp
	bridge command line				*>br
	bridge commands, one line use or multiple		*>pb.br
	psr
			*>search 	psr		hyper command test
	sql
			*>search 	sql		hyper command test
	bat dos commands, via batch file		*>bat
			*>search 	bat 	hyper command test
	go to a url -- open new window or not
			*>search 	url 		hyper command test
	datawindow
			*>search   dw 		hyper command test
	pbl
			*>search   pbl		hyper command test
	app
			*>search   app		hyper command test
	shell
			*>search   shell	hyper command test
	datawindow
			*>search   dw hyper command test
	datawindow
			*>search   dw hyper command test
	datawindow
			*>search   dw hyper command test


            How about the logic

            Only one thing happens:  the first command or transform that "works" ends the processing.  When using the
            individual command buttons you can execute an unchecked/or checked command on the last copied text.

            Transforms
                   Transforms may be conditional.  For example the transformation of url's to wiki format will not
                   occur if the text does not look like it meets the criteria for a list of url's.
                   Shifting case on the other hand is unconditional ( always works ).

            Commands
                Implied
                   Single commands .. scan the text for special stuff ( perhaps after text clean up )
                   and execute a command base on the special stuff.  The special stuff might be a url
                   or a file name.

                   Multiple commands are same a single but do not stop after the first occurance of the magic text
                   so several actions may take place.

               Star Commands

                    Begin with *>  may be multi-lined or single lined.

                    Single Line


                    Multiline



================= tests =====================

        cmd
             self.cmd_processor.do_if_cmd( in_text )
                             *>url":       self.do_if_url_cmd,
                            "*>print":     self.print_cmd,
                            "*>shell":     self.do_shell_cmd,
                            "*>run":       self.do_run_cmd,
                            "*>text





--------  user pages



 15:35 	The Final Phrase With Food Journalist Mark Bittman‎ (diff | hist) . . (+6,226)‎ . . CaryGoodisson (Talk | contribs | block) (Created page with "Pre-order cakes are a hundred and fifteen EUR for example don't eat breakfast twice a week. Lovers to wear a tie though there are vacationers in Italy heading for. Not everybo...")
 m ! 15:35 	User:CaryGoodisson‎ (diff | hist) . . (+130)‎ . . CaryGoodisson (Talk | contribs | block) [rollback]
	     15:33 	(User creation log)‎ . . [JamisonLain0‎; JurgenNye626‎; KBBVeda5763755‎; Hung77237633‎; Heidi59X8103‎; Arianne58W‎; BlytheFulcher6‎; ErnestoSprouse5‎; KaleyHansen‎; Larhonda50U‎; TrinidadHaugen8‎; TristaGoudie6‎; VeolaNorthey‎; QuincyMaki105‎; OliviaSpangler‎; LoriGreco9549‎; MapleTen5438388‎; NaomiOman77‎; WilsonIfy4013993‎]
N  ! 15:32 	Vegas TV Series RK 0 RS eZ3Zef4fV4YPCly6tCjMwMWTpX0‎ (diff | hist) . . (+6,158)‎ . . IngeAshburn8 (Talk | contribs | block) (Created page with "It's exhausting relearning how eating meat 2 they perception in the well being and health. Why is not it was a marbled cheddar cheese and a hearty meat sauce. Thought due to t...")
	N  ! 15:32 	User:IngeAshburn8‎‎ (3 changes | hist) . . (+510)‎ . . [IngeAshburn8‎ (3×)]
N  ! 15:21 	How To Sketch Clothed Figures ★‎ (diff | hist) . . (+5,823)‎ . . AdelaidaBeadle (Talk | contribs | block) (Created page with "Buddhism in the Dundee space then think about doing so would solely make. Hugo Boss a couple of regimental clothing objects that you're going to take pleasure in doing so whet...")
 m ! 15:21 	User:AdelaidaBeadle‎ (diff | hist) . . (+44)‎ . . AdelaidaBeadle (Talk | contribs | block) [rollback]
N  ! 15:09 	What Occurred After I Went Vegan Gluten-Free‎ (diff | hist) . . (+5,275)‎ . . NoelGrills38487 (Talk | contribs | block) (Created page with "Canasta also buy park passes and save even more money to spend the day. The placement to be able to test it out as a lot money on a meal. Franchises have chosen a location it ...")
N  ! 14:39 	Scrumptious Tea Sandwich Ideas For Valentine s Day‎ (diff | hist) . . (+5,567)‎ . . IngeAshburn8 (Talk | contribs | block) (Created page with "Butterfly knives have two words raw vegan meals exclude meat poultry seafood dairy. As a result of it could sound tough however emotionally Talking I find that as a vegan. Pru...")
N  ! 14:18 	What Do I Imply By That‎ (diff | hist) . . (+6,210)‎ . . IngeAshburn8 (Talk | contribs | block) (Created page with "A really busy schedule and protein bars and powders akin to pasta with tomato roasted vegetables. Pack stable shampoo bars and protein contain nutrients that plant-based prote...")
	     13:30 	(Block log)‎ . . [Russ hensel‎ (6×)]
	     08:35 	(Deletion log)‎ . . [Russ












