# -*- coding: utf-8 -*-

#  running_on.py master in smart plug for now  2019 12 17

"""

---- template header example -----
What:   introspection type stuff
Status: draft, ok draft but possibly useful
Refs:

Code introspection in Python - GeeksforGeeks
    *>url  https://www.geeksforgeeks.org/code-introspection-in-python/

home-assistant/home-assistant: Open source home automation that puts local control and privacy first
    *>url  https://github.com/home-assistant/home-assistant


view.View Python Example
    *>url  https://www.programcreek.com/python/example/15897/view.View

What are Python dictionary view objects?
    *>url  https://www.tutorialspoint.com/What-are-Python-dictionary-view-objects

python - What are dictionary view objects? - Stack Overflow
    *>url  https://stackoverflow.com/questions/8957750/what-are-dictionary-view-objects

Python reflection: how to list modules and inspect functions - Federico Tomassetti - Software Architect
    *>url  https://tomassetti.me/python-reflection-how-to-list-modules-and-inspect-functions/


Notes:



    ** memory
    ** disassemble
    types              ex_type.py
    is instance
    issubclass()	Checks if a specific class is a derived class of another class.
    isinstance()	Checks if an objects is an instance of a specific class.


    ** help()	It is used it to find what other functions do
    hasattr()	Checks if an object has an attribute
    getattr()	Returns the contents of an attribute if there are some.
    repr()	Return string representation of object
    callable()	Checks if an object is a callable object (a function)or not.

    sys()	Give access to system specific variables and functions
    __doc__	Return some documentation about an object
    __name__	Return the name of the object.
    ** which version of python
    ** which version of os

    inspect — Inspect live objects — Python 3.8.0 documentation
    *>url  https://docs.python.org/3/library/inspect.html

    platform — Access to underlying platform’s identifying data — Python 3.8.0 documentation
    https://docs.python.org/3.8/library/platform.html

"""



#import math
#import timeit
#import dis
#import sys

import sys
import os
import psutil
import platform
import socket;
from   platform import python_version
import pathlib


# --------------------------------------
class RunningOn( object ):
    """
    Provides information on the system..... we are running on
    now including some directory stuff
    i decided to make all available as class variables
    """
    def __init__(self,   ):
        """
        this is meant to be a singleton use class level only do not instantiated
        throw a exception if instantiated 1/0
        """
        y = 1/0

    # ----------------------------------------------
    @classmethod
    def gather_data( cls,  ):
        """
        what it says
        add flag for how much ??

        """
        our_os           = sys.platform       #testing if our_os == "linux" or our_os == "linux2"  "darwin"  "win32"
        cls.our_os       = our_os
        if our_os == "win32":
            os_win = True     # the OS is windows any version
        else:
            os_win = False    # the OS is not windows
        cls.os_win         = os_win

        cls.os_is_win      = os_win                # phase out but seems to be needed on linux
        if  os_win:
            cls.computername       = os.getenv( "COMPUTERNAME" ).lower() # at least in windows the lower case name of your computer.  what in linux?
        else:
            cls.computername       = ""

        process               = psutil.Process(os.getpid())
        cls.memory_mega       = process.memory_info().rss / 1e6   # mega bytes seem better

        cls.platform_system   = platform.system()
        cls.sys_version       = sys.version
        cls.sys_version_info  = sys.version_info
        cls.python_version    = python_version()

        # --- environment does not seem too useful but make sure defined
        cls.environments       = {"what": "not collected"}
#        cls.environments        = os.environ     # not sure of type, dict like

        host_name              = socket.gethostname()
        cls.host_name          = host_name

        # next has failed on raspberry pi us try until better understood
        try:
             cls.host_tcpip         = socket.gethostbyname( host_name )
        except Exception as a_execpt:
            # no logger at this point
            print( f"RunningOn.gatherdata() failed to get hostname {a_execpt}" )
            cls.host_tcpip         = None

        # try to make computer id, and host_tcpid the best indicators of our box
        if cls.computername == "":
            cls.computer_id    = cls.host_name.lower()
        else:
            cls.computer_id    = cls.computername

        cls.platform_machine   = platform.machine()

        # !! decide which and eliminate other
        cls.org_path           = os.getcwd()
        cls.opening_dir        = os.getcwd()    # name of the directory that the application is started in. Probably "....../smart_plug

        cls.program_py_fn      = sys.argv[ 0 ]

        # under linux it looks like this may return a blank if already in current dir
        # in that case should we populate with the current dir !! probably yes
        cls.py_path            = os.path.dirname(  cls.program_py_fn  )

        print( f"running on for {cls.program_py_fn}  path is  {cls.py_path}" )


        # cls.program_py_fn
        sys_argv0               = sys.argv[ 0 ]

        a_path    = pathlib.Path( sys_argv0 )
        print( f"a_path {a_path}" )

        a_cwd     = a_path.cwd()
        print( f"a_cwd {type(a_cwd)}  {a_cwd}" )

        cls.cwd    = str( a_cwd )

        a_resolve   = a_path.resolve( strict=False )
        print( f"a_resolve {type(a_resolve)} {a_resolve}" )
        cls.program_py_fn           = str( a_resolve )

        # under linux it looks like this may return a blank if already in current dir
        # in that case should we populate with the current dir !! probably yes
        cls.py_path            = os.path.dirname(  cls.program_py_fn  )

        print( f"running on for {cls.program_py_fn}  path is  {cls.py_path}" )

        # os.chdir( desired_path )
        # logger.log( fll,  "current directory now " +  os.getcwd() )

#       ...... as needed

        # os.chdir( desired_path )
        # logger.log( fll,  "current directory now " +  os.getcwd() )

#       ...... as needed

    # ----------------------------------------------
    @classmethod
    def linux_distribution( cls ):
        """
        may use later
        """
        try:
            return platform.linux_distribution()
        except:
            return "N/A"

    # ----------------------------------------------
    @classmethod
    def log_msg(cls, msg, logger, logger_level = 10, print_flag = False  ):
        """
        for debugging
        !! consider some sort of print if no logger
        """
        if logger is None:
            pass
        else:
            logger.log( logger_level, msg )
        if print_flag:
            print( msg )

    # ----------------------------------------------
    @classmethod
    def log_me(cls, logger, logger_level, print_flag  ):
        """
        for debugging
        log and/or print info
        add log level, and defalut
        """
        cls.log_msg( f">>>>>>>>>>> running_on() log_me() <<<<<<<<<<<<<",     logger, logger_level, print_flag )
        cls.log_msg( f"platform_system    >{cls.platform_system}<",     logger, logger_level, print_flag )
        cls.log_msg( f"sys_version        >{cls.sys_version}<",         logger, logger_level, print_flag )
        cls.log_msg( f"sys_version_info   >{cls.sys_version_info}<",    logger, logger_level, print_flag )
        cls.log_msg( f"memory_mega        >{cls.memory_mega}<",         logger, logger_level, print_flag )
        cls.log_msg( f"python_version     >{cls.python_version}<",      logger, logger_level, print_flag )

        cls.log_msg( f"environments       >{cls.environments}<",        logger, logger_level, print_flag )

        cls.log_msg( f"host_name          >{cls.host_name}<",           logger, logger_level, print_flag )
        cls.log_msg( f"host_tcpip         >{cls.host_tcpip}<",          logger, logger_level, print_flag )
        cls.log_msg( f"computername       >{cls.computername}<",        logger, logger_level, print_flag )
        cls.log_msg( f"computer_id        >{cls.computer_id}<",         logger, logger_level, print_flag )
        cls.log_msg( f"platform_machine   >{cls.platform_machine}<",    logger, logger_level, print_flag )

        cls.log_msg( f"os_is_win          >{cls.os_is_win}<",           logger, logger_level, print_flag )
        cls.log_msg( f"program_py_fn      >{cls.program_py_fn}<",       logger, logger_level, print_flag )

        cls.log_msg( f"py_path            >{cls.py_path }<",            logger, logger_level, print_flag )
        cls.log_msg( f"org_path           >{cls.org_path}<",            logger, logger_level, print_flag )

        cls.log_msg( f"cls.cwd            >{cls.cwd }<",                 logger, logger_level, print_flag )

        cls.log_msg( f"---------------- end running on --------------",  logger, logger_level, print_flag )


# ==============================================
if __name__ == '__main__':
    """
    do not run the app here for convenience of launching
    """

#    print("")
#    print("================= do not run me ( app_global.py ) please, I have nothing to say  ===================")


    the_class   =  RunningOn
    the_class.gather_data()
    the_class.log_me( logger = None, logger_level = 20, print_flag = True )

"""
=============================== notes ====================
======== output ( perhaps out of date ) from various computers
------------------------ buzsaw --------------------

platform_system    >Linux<
sys_version        >3.6.1 | packaged by rpi | (default, Apr 20 2017, 19:35:19)
[GCC 4.9.2]<
sys_version_info   >sys.version_info(major=3, minor=6, micro=1, releaselevel='final', serial=0)<
memory_mega        >38.281216<
python_version     >3.6.1<
environments       >{'what': 'not collected'}<
host_name          >raspberrypi_ddclock<
host_tcpip         >127.0.1.1<
computername       ><
computer_id        >raspberrypi_ddclock<
platform_machine   >armv7l<
os_is_win          >False<
---------------- end running on --------------
In parameters: no special settings for computer_id raspberrypi_ddclock
process memory =      43.02 mega bytes

----------------------- the_prof ---------------------------
2019-11-24 12:31:21,399 - splug - Notice - command line arg 0 = D:/Russ/0000/python00/python3/_projects/smart_plug/Ver8/smart_plug.py
2019-11-24 12:31:21,399 - splug - Notice - current directory D:\Russ\0000\python00\python3\_projects\smart_plug\Ver8
2019-11-24 12:31:21,399 - splug - Notice - COMPUTERNAME theprof
2019-11-24 12:31:21,399 - splug - Notice - platform win32
2019-11-24 12:31:21,399 - splug - Notice - our os win32
2019-11-24 12:31:21,399 - splug - Notice - Time now: 2019-11-24 17:31:21
2019-11-24 12:31:21,399 - splug - Notice - platform_system    >Windows<
2019-11-24 12:31:21,399 - splug - Notice - sys_version        >3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]<
2019-11-24 12:31:21,399 - splug - Notice - sys_version_info   >sys.version_info(major=3, minor=7, micro=4, releaselevel='final', serial=0)<
2019-11-24 12:31:21,399 - splug - Notice - memory_mega        >137.25696<
2019-11-24 12:31:21,399 - splug - Notice - python_version     >3.7.4<
2019-11-24 12:31:21,399 - splug - Notice - environments       >{'what': 'not collected'}<
2019-11-24 12:31:21,400 - splug - Notice - host_name          >theprof<
2019-11-24 12:31:21,400 - splug - Notice - host_tcpip         >192.168.56.1<
2019-11-24 12:31:21,400 - splug - Notice - computername       >theprof<
2019-11-24 12:31:21,400 - splug - Notice - computer_id        >theprof<
2019-11-24 12:31:21,400 - splug - Notice - platform_machine   >AMD64<
2019-11-24 12:31:21,400 - splug - Notice - os_is_win          >True<
2019-11-24 12:31:21,401 - splug - DEBUG - helper run
2019-11-24 12:31:21,464 - splug - Notice - process memory =     138.83 mega bytes

------------------------ running on bulldog -------------------------

2019-11-24 15:26:51,130 - splug - INFO - Done config_logger
2019-11-24 15:26:51,131 - splug - Notice -
2019-11-24 15:26:51,131 - splug - Notice -
2019-11-24 15:26:51,131 - splug - Notice - ============================
2019-11-24 15:26:51,131 - splug - Notice -
2019-11-24 15:26:51,131 - splug - Notice - Running SmartPlug version = Ver7 2019 11 24.5
2019-11-24 15:26:51,131 - splug - Notice -
2019-11-24 15:26:51,132 - splug - Notice - command line arg 0 = /home/russ/python3/_projects/smart_plug/Ver8/smart_plug.py
2019-11-24 15:26:51,132 - splug - Notice - current directory /home/russ/python3/_projects/smart_plug/Ver8
2019-11-24 15:26:51,132 - splug - Notice - COMPUTERNAME linux_box
2019-11-24 15:26:51,132 - splug - Notice - platform linux
2019-11-24 15:26:51,132 - splug - Notice - our os linux
2019-11-24 15:26:51,132 - splug - Notice - Time now: 2019-11-24 20:26:51
2019-11-24 15:26:51,133 - splug - Notice - platform_system    >Linux<
2019-11-24 15:26:51,133 - splug - Notice - sys_version        >3.6.8 (default, Oct  7 2019, 12:59:55)
[GCC 8.3.0]<
2019-11-24 15:26:51,133 - splug - Notice - sys_version_info   >sys.version_info(major=3, minor=6, micro=8, releaselevel='final', serial=0)<
2019-11-24 15:26:51,133 - splug - Notice - memory_mega        >74.93632<
2019-11-24 15:26:51,133 - splug - Notice - python_version     >3.6.8<
2019-11-24 15:26:51,134 - splug - Notice - environments       >{'what': 'not collected'}<
2019-11-24 15:26:51,134 - splug - Notice - host_name          >bulldog<
2019-11-24 15:26:51,134 - splug - Notice - host_tcpip         >127.0.1.1<
2019-11-24 15:26:51,134 - splug - Notice - computername       ><
2019-11-24 15:26:51,134 - splug - Notice - computer_id        >bulldog<
2019-11-24 15:26:51,135 - splug - Notice - platform_machine   >x86_64<
2019-11-24 15:26:51,135 - splug - Notice - os_is_win          >False<
2019-11-24 15:26:51,136 - splug - DEBUG - helper run
2019-11-24 15:26:51,867 - splug - Notice - process memory =      82.42 mega bytes
2019-11-24 15:27:23,500 - splug - ERROR - smart_plug_helper.HelperThread threw exception: no such table: plug_measurements


--------------------- buldog mint -----------


platform_system    >Linux<
sys_version        >3.6.9 (default, Nov  7 2019, 10:44:02)
[GCC 8.3.0]<
sys_version_info   >sys.version_info(major=3, minor=6, micro=9, releaselevel='final', serial=0)<
memory_mega        >74.989568<
python_version     >3.6.9<
environments       >{'what': 'not collected'}<
host_name          >bulldod-mint-russ<
host_tcpip         >127.0.1.1<
computername       ><
computer_id        >bulldod-mint-russ<
platform_machine   >x86_64<
os_is_win          >False<
In parameters: no special settings for computer_id bulldod-mint-russ
platform_system    >Linux<
sys_version        >3.6.9 (default, Nov  7 2019, 10:44:02)
[GCC 8.3.0]<
sys_version_info   >sys.version_info(major=3, minor=6, micro=9, releaselevel='final', serial=0)<
memory_mega        >74.989568<
python_version     >3.6.9<
environments       >{'what': 'not collected'}<
host_name          >bulldod-mint-russ<
host_tcpip         >127.0.1.1<
computername       ><
computer_id        >bulldod-mint-russ<
platform_machine   >x86_64<
os_is_win          >False<
process memory =      87.97 mega bytes
1574658000.0 1574744400.0



"""


#
#        bs   = "\n"
#        print( sys.hexversion )
#
#        print( f"platform.platform(){platform.platform()}" )
#
#        print( f"platform.release(){platform.release()}" )
#        print( f"platform.version(){platform.version()}" )
#        print( f"platform.processor(){platform.processor()}" )
#        print( f"""Python version: {sys.version.split( bs )}
#        dist: {str(platform.dist())}
#        linux_distribution: linux_distribution(),
#

#        platform: platform.platform(),
#        uname: platform.uname(),
#        version:  platform.version(),
#        mac_ver:  platform.mac_ver(),
#        """ )


