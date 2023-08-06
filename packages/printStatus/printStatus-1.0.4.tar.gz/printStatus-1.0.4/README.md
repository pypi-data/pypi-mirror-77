printStatus
===========
A simple collection of functions to print a progress bar in the console. In addition, it facilitates to print the status
of a currently running job or the exit status of a finished job. 

The module is for instance used by the GIST pipeline (https://abittner.gitlab.io/thegistpipeline/) and the generated
messages look like this: 

.. image:: https://abittner.gitlab.io/thegistpipeline/V3.0.0-doc1/_images/runningPipeline.png
   :scale: 75%


Installation
-------------
You can install this package with pip::

   pip install printStatus


Usage
-------------
A simple example of the usage of this module is provided in ``demo.py``. The following functions are available:

``printStatus.module(message)``: Print the name of the currently active module. 

``printStatus.running(message)``:  Print a new message to stdout with the tag "Running".

``printStatus.done(message)``: Print a new message to stdout with the tag "Done". 

``printStatus.updateDone(message, progressbar=False)``: Overwrite the previous message in stdout with the tag "Done" and a new message. Set progressbar=True if the previous message was the progress bar. 

``printStatus.warning(message)``: Print a new message to stdout with the tag "Warning". 

``printStatus.updateWarning(message, progressbar=False)``: Overwrite the previous message in stdout with the tag "Warning" and a new message. Set progressbar=True if the previous message was the progress bar. 

``printStatus.failed(message)``: Print a new message to stdout with the tag "Failed". 

``printStatus.updateFailed(message)``: Overwrite the previous message in stdout with the tag "Failed" and a new message. Set progressbar=True if the previous message was the progress bar. 


Compatibility
-------------
Tested with Python3. Note that the appearance of the colours in the terminal depends on the specific setup of your terminal. 



