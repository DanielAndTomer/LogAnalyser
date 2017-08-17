from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\user\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\user\AppData\Local\Programs\Python\Python36\tcl\tk8.6'

setup(name = "LogAnalyser",
    version = "0.1",
    description = "An example",
    executables = [Executable("LogAnalyser.py")]
    )
