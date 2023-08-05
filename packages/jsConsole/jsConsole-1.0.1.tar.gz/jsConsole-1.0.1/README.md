# jsConsole
 A JavaScript Console written for and in python

### What is jsConsole?
jsConsole is a python module that lets you use JavaScript classes and control a browser as you would do in JavaScript in Python!

### Usage
Just import everything from the module and you are ready to go!

```python
>>> from jsConsole import *
#### And now you can use classes like document, window, Math or console from Python!

>>> console.log('jsConsole is ready!')
'jsConsole is ready!'

>>> window.open('https://google.com', '_self')
# Opens google.com on the browser #

>>> def hello():
...     print('Hello')
...

>>> document.getElementsByClassName('RNNXgb')[0].addEventListener('click', hello) ### Adding an event listener to the search bar from google.com which executes hello() when clicked.

>>> window.kill() # Needed to kill the browser (for it not to stay in the background even with Python quited)
``` 

### Installation
Install it with PyPI (`pip`) the Python Dependency/Module Manager.

```bash
pip install jsConsole
```

### Browser Configuration
By default, jsConsole uses Pyppeteer which runs on Chromium to execute JavaScript.

You can configure the browser you want to use with `jsConsole.internal.config`
```python
>>> import jsConsole.internal.config as jsConsoleConfig

>>> jsConsoleConfig.layer # defines the layer (Selenium of Pyppeteer) you want to use --> String

>>> jsConsoleConfig.executable_path # Sets the executable path of the browser you want to use. --> String

>>> jsConsoleConfig.no_sandbox # Sets wether you want to use the --no-sandbox argument whie opening the browser or not (useful for Linux) --> bool

>>> jsConsoleConfig.args # Sets this to pass arguments while opening the browser. --> Needs to be a list

>>> jsConsoleConfig.headless # Sets wether you want the browser to be headless or not with Selenium --> bool

>>> jsConsoleConfig.browsername # Sets the browser you want to use with Selenium ('Chrome', 'Firefox' and 'PhantomJS' are currently supported) --> String

"""
Default Configuration is:

layer = 'Selenium'

executable_path = ''
no_sandbox = False
args = []

headless = True
browsername = 'Chrome'
"""

## Experiment and try different browsers and layers to find the one that fits the best for you. I've personnaly tried my module with the default configurations.

###### If you don't want to worry about drivers and browsers you can use Pyppeteer which will download, install and set up a browser for you.


>>> from jsConsole import *
...
```

### jsConsole specific functions/method and classes.
- browser.kill() or window.kill()

Used to kill the browser instance opened when launched in order to prevent it from staying open in the background even after stopping your script/python execution.

> Check your activity monitor (top, htop, activity monitor, etc.) if there isn't any non-used browsers opened as it may happen when using Selenium and other browser control softwares.


- browser (Browser Object)

Contains multiple informations about the current browser instance opened:

    - browser: The browser instance, a new page object if using Pyppeteer or a driver instance if using Selenium
    - layer: The name of the layer used (Selenium or Pyppeteer)
    - executable_path: The executable path (if specified one) of the browser in use
    - browsername: The name of the browser in use (i.e Chrome, Firefox)
    - no_sandbox: Wether or not you activated the option no-sandbox (useful for Linux users)
    - headless: If you opened the browser instance headlessly (works for Selenium)
    - args: The arguments passed (if configured) while opening the browser
    - drivername: The name of the driver in use
    - connected: Wether or not you are connected to the browser
    - areClassesInitialized: Internal variable to indicate if the JavaScript are correctly initialized
    - list_of_variables: Internal variable which tells the variables ID created by jsConsole (i.e when using addEventListener or setTimeout)
    - dict_of_ids = Internal variable which tells the different setTimeout/setInterval IDs that had been created and if each of them should be enabled or not.
    - ids_to_thread = Internal variable which tells the different setTimeout/setInterval IDs that had been created and their corresponding thread.

- fresh()

Returns a tuple with a brand new document and window class (after a new page is loaded)

Use it like so:
```python
>>> document, window, history = fresh()

Which returns a new document (_Document) object in the document variable, a new window (_Window) object in the window variable and a new history (_History) object in the history variable.

## I can't provide a new document and window in real-time, seamlessly (even though I tried) because of the way they work.
```

- newDocument():

Returns a new document (_Document) object

- newWindow():

Returns a new window (_Window) object

- newHistory():

Returns a new history (_History) object

- evaluate():

Evaluates a snippet of JavaScript code if needed (i.e not avaiable yet)

> return_value=True adds "`return `" in front of the snippet of code if you want the value to be returned while using Selenium

- document.window and window.window will return an error message because I didn't find a way of linking them without creating a recursion error.

#### You can use python functions in setTimeout(), clearInterval() and addEventListener.

### You should be able to write code as if you were writing in JavaScript.


> © Anime no Sekai - 2020