# fastscript
> A fast way to turn your python function into a script.


Part of [fast.ai](https://www.fast.ai)'s toolkit for delightful developer experiences. Written by Jeremy Howard.

## Install

`pip install fastscript`

## Overview

Sometimes, you want to create a quick script, either for yourself, or for others. But in Python, that involves a whole lot of boilerplate and ceremony, especially if you want to support command line arguments, provide help, and other niceties. You can use [argparse](https://docs.python.org/3/library/argparse.html) for this purpose, which comes with Python, but it's complex and verbose.

`fastscript` makes life easier. There are much fancier modules to help you write scripts (we recommend [Python Fire](https://github.com/google/python-fire), and [Click](https://click.palletsprojects.com/en/7.x/) is also popular), but fastscript is very fast and very simple. In fact, it's <50 lines of code! Basically, it's just a little wrapper around `argparse` that uses modern Python features and some thoughtful defaults to get rid of the boilerplate.

## Example

Here's a complete example - it's provided in the fastscript repo as `examples/test_fastscript.py`:

```python
from fastscript import *
@call_parse
def main(msg:Param("The message", str),
         upper:Param("Convert to uppercase?", bool_arg)=False):
    print(msg.upper() if upper else msg)
````

When you run this script, you'll see:

```
$ python examples/test_fastscript.py
usage: test_fastscript.py [-h] [--upper UPPER] msg
test_fastscript.py: error: the following arguments are required: msg
```

As you see, we didn't need any `if __name__ == "__main__"`, we didn't have to parse arguments, we just wrote a function, added a decorator to it, and added some annotations to our function's parameters. As a bonus, we can also use this function directly from a REPL such as Jupyter Notebook - it's not just for command line scripts!

## Param

Each parameter in your function should have an annotation `Param(...)` (as in the example above). You can pass the following when calling `Param`: `help`,`type`,`opt`,`action`,`nargs`,`const`,`choices`,`required` . Except for `opt`, all of these are just passed directly to `argparse`, so you have all the power of that module at your disposal. Generally you'll want to pass at least `help` (since this is provided as the help string for that parameter) and `type` (to ensure that you get the type of data you expect). `opt` is a bool that defines whether a param is optional or required (positional) - but you'll generally not need to set this manually, because fastscript will set it for you automatically based on *default* values.

You should provide a default (after the `=`) for any *optional* parameters. If you don't provide a default for a parameter, then it will be a *positional* parameter.

## setuptools scripts

There's a really nice feature of pip/setuptools that lets you create commandline scripts directly from functions, makes them available in the `PATH`, and even makes your scripts cross-platform (e.g. in Windows it creates an exe). fastscript supports this feature too. To use it, follow [this example](fastscript/test_cli.py) from `fastscript/test_cli.py` in the repo. As you see, it's basically identical to the script example above, except that we can treat it as a module. The trick to making this available as a script is to add a `console_scripts` section to your setup file, of the form: `script_name=module:function_name`. E.g. in this case we use: `test_fastscript=fastscript.test_cli:main`. With this, you can then just type `test_fastscript` at any time, from any directory, and your script will be called (once it's installed using one of the methods below).

You don't actually have to write a `setup.py` yourself. Instead, just copy the setup.py we have in the fastscript repo, and copy `settings.ini` as well. Then modify `settings.ini` as appropriate for your module/script. Then, to install your script directly, you can type `pip install -e .`. Your script, when installed this way (it's called an [editable install](http://codumentary.blogspot.com/2014/11/python-tip-of-year-pip-install-editable.html), will automatically be up to date even if you edit it - there's no need to reinstall it after editing.

You can even make your module and script available for installation directly from pip by running `make`. There shouldn't be anything else to edit - you just need to make sure you have an account on [pypi](https://pypi.org/) and have set up a [.pypirc file](https://docs.python.org/3.3/distutils/packageindex.html#the-pypirc-file).

## Importing Command Line Functions
Sometimes it might be useful to also be able to import command-line functions and use them as regular functions.

```
from fastscript.test_cli import main
main("This can also be used as a regular imported function.", upper=True)
```




    'THIS CAN ALSO BE USED AS A REGULAR IMPORTED FUNCTION.'


