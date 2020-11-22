# How to debug in a Keyshot scripting environment

Nothing goes about a nice debugging experience during bug hunting. So this rather seems to be a standard problem. Even Keyshot uses an embedded Python this seems just a normal case for Reomte Debugging. But nope, it isn't. But this is still a standard problem, so there are many ways to find a working solution for this issue. The following table lists different ways I tried and the results:

|IDE            |Version    |Result|
|:--------------|:---------:|:-----|
|PyCharm        |2019.2.6   |Breaking in to the debugger will result in a file "\<currert_working_dir>/\<string> "not found" exception, so no Breakpoints will be hitted, but the script finishes without errors.|
|PyCharm        |2020.2.3   |Connecting to the debugger will block the main thread forever. So you have to kill Keyshot.|
|Visual Stuio   |2019       |Using mixed mode debugging, still results in not hitting any Breaktpoints (No Debugging Symbols found for script), but the script finishes without errors.|
|VS Code/pydebug|1.51       |During waiting for the debugger to Attach pydebug start a subprocess which results in starting a new Keyshot and Python instance, so a complete failure.|
|WingIDE        |7.2        |Even there is a [explicit guide for attaching the debugger to a embeded Python environment](https://wingware.com/doc/debug/debugging-embedded-code). Still no breakpoints will be hitted, but the script finishes without errors.|

There is at least a common pattern here, which hints at a problem with the path mappings, even there isn't a real remote. So taking a look into Pydevd which all (except Wing IDE?) rely on. Some fiddling around later the point where Pydevd transmits the filepath to the server of PyCharm was found. So applying a little patch into Pydevd made things work finally.

## How to get things working

This guide is based on Keyshot 9.3 and Windows (but this should work on other OSs too).

1. Make sure you have Python 3.8 installed or [which version your Keyshot requires](https://luxion.atlassian.net/wiki/spaces/K9M/pages/1062446718/Scripting).
2. Make sure this version is the version used by Keyshot adding this to your PATH environment variable/s and by checking:

```` cmd
python --version
````
There are multiple ways to setting up environemt variables in Windows. The following pictures show it through setting editing the system or user envrionment variables in the system control panel.

|Editing the System/User environment variables|Editing the Path environment variable|
|:-------------------------------------------:|:-----------------------------------:|
|![picture](doc/env_edit.png)                 |![picture](doc/env_path.png)         |

User variables append/overwrite system variables. Otherwise you can obsiously set the variable through your prefered command line interface. 

3. Then follow the [guide to setup PyCharm Remote debugging](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html#remote-interpreter). This repository already includes/is a PyCharm project with a "Remote Debugging" configuration.
4. After installing pydevd_pycharm replace pydevd.py with the [patched version](/.patches/site-packages/pydevd.py). See the site-packages directory of your python distribution.
5. Then just add the following to the top of your script additional to connect to the debugging server:

````python
import sys, os
import pydevd

root = os.path.dirname(__file__)
sys.path.append(root)
os.chdir(root)

pydevd.mapping_patches = {"<string>": os.path.basename(__file__)}

pydevd.settrace('localhost', port=15678, stdoutToServer=True, stderrToServer=True, suspend=True)
````

6. Start the remote debugging server in PyCharm and run the script to debug. Now the breakpoints should be hitted.

