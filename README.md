
This document tries to describe the complete structure and flow of the python application.
This repo does not contain the virtual environment used to develop it, so, when using for the first time
 it will require installation of all python modules used.( The application was developped in python 3.10).
The application is divided into sub programs for each sub systems and which are,
  1) **27Oct(Ganesh).ui**
  2) **Serial_file.py**
  3) **Z.py**
  4) **cli_file_handling.py**
  5) **cube_commands_boundary.py**27Oct(Ganesh).ui
  6) **cube_commands_hatch.py**
  7) **environment.py**
  8) **hopper.py**
  9) **main.py**
  10) **scancard.py**
  11) **timing.py**

*There are other files also present in the repo, but are not necessary to run the appplication*

# main.py
  This is the core of the application and the control system which sends and receives signals to all the other subsystems.
  In most cases, an instance of this class is sent to the other classes during initialisation.
  + All the gui Objects are initiased here and the signal and slot connections are also defined in this file.
  + It creates multiple threads to run concurrent functions, For example,
      + To read the inputs from tiva, this thread is in a while loop and is constantly reading the serial port.
      + If called a thread to run the automation process is created.
      + To read the temperature values from the octopus board.
  + All the changes to gui during operation needs to done on the main thread itself or else the program becomes unstable.
    So, For example, all the data received by the read thread is sent over to the main thread using signals and then it
    is printed in the console widget in the gui.

# Serial_file.py
  + This file holds the functions required to read, write and other methods related to the serial communication.
  + It automatically connects to the Tiva board regardless of the OS(Linux or Windows).

# Z.py
  + This file harbors the functions required to move the Z motors in the printer.
  + It provides functionality to move the "Z-axis" motor and the "Z-lifting" motor separately.

# cli_file_handling.py 
  + This file deals with reading and processing the .cli file and to generate a dat structure with data from the file.
  + There are functions to support the complete process of reading the file, get coordinates,
     making the commands( For repli-SLS) and has interall checks as well.
# cube_commands_boundary.py and cube_commands_hatch.py 
  + These files contain the commands(repli sls) to mark and hatch an arbitary cube.

# environment.py
  + This file hold the methods to get environment data like temperature values etc via ip address of the octopus board.
  + It also supports sending commands to set new temperatures.

# hopper.py
  + Here all the functions related to the movement of the hoppers( Right and Left) are defined.
  + It can be used in various combinations like with varying slot distance and time duration of the slot opening.

# scancard.py 
  + All the methods related to initialising, making the connection( to e1803) and even sending commands to boards are present here.
  + In this version, this file does not have an instance of main, so we can't write anything on the console widget (yet).

# timing.py
  + This file holds the functions used to measure the time elapsed during machine operation and also accounts for intermediated stops and restarts.

# 27Oct(Ganesh).ui
  + This is the ui file which holds the design of the gui and it is loaded at the start of the program in main.

# Code Flow 
 ## Recoater Code Flow
  ![Recoater_flow](./resource/recoater_example.png)
 ## Z/Hopper Code Flow
  ![Z/Hopper_flow](./resource/Z_hopper.png)

# IMPORTANT NOTES
 + Don't update the GUI contains from another thread or process.
 + Maintain proper communication between the sub-threads and the main thread using pipes, signals and slots.
 + Avoid using loops in the main thread, as PyQT in itself has an infinite loop which updates the GUI and if the user creates a loop without proper flow handling the GUI won't update until the flow is out of the user defined loop.
 + In case it is required to run an infinite loop, then it is best done in a sub thread.
 + To make a label invisible in designer set the background color attributes as rbg(x,y,), i.e. leave one of the parameters as blank.

