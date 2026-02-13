# Argumentor

Command and argument parsing and documentation for Python CLI.

> [!WARNING]  
> This project is not really meant for widespread application and was mostly made for fun. Use at your own risk.

<sub><sup>Feel free to contribute if you find any issues though.</sup></sub>

[![Publish to PyPI](https://github.com/gardehal/argumentor/actions/workflows/publish.yml/badge.svg)](https://github.com/gardehal/argumentor/actions/workflows/publish.yml)
[![GitHub Release](https://img.shields.io/github/release/gardehal/argumentor.svg)]()
[![MIT License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/gardehal/argumentor/blob/main/LICENSE)

## Install

[PyPi project](https://pypi.org/project/argumentor-gardehal/)

Install using pip
- $ `pip install argumentor-gardehal`
- In python files: `from Argumentor import *` 

Install from files locally
- $ `cd [path to this folder]`
- $ `pip cache purge` (may help if old packages are cached)
- $ `pip install .`

## Example

### Getting started

Creating a command to calculate volume for a given object we have stored somewhere with an ID.
- [ExampleBasic.py](https://github.com/gardehal/argumentor/blob/main/tests/ExampleBasic.py)
- $ `python .\tests\ExampleBasic.py -help`

### A step further

Creating a command that takes multiple inputs, validating dimensions, and a optional argument with custom casting and validation from string to an enum and lists.
- [ExampleAdvanced.py](https://github.com/gardehal/argumentor/blob/main/tests/ExampleAdvanced.py)
- $ `python .\tests\ExampleAdvanced.py -help`

##### Expected outcomes

The following list of examples explains some expected outcomes, or could be used to test Argumentor. 

>[!INFO] 
> These are based on [ExampleAdvanced.py](https://github.com/gardehal/argumentor/blob/main/tests/ExampleAdvanced.py).
> Depending on CLI, these results may vary compared to validateString version as below, or as input into CLI (using ' or " would be a main reason as CLI reads it differently).

    inputA = "-dim 1 2 3" # Valid
    inputB = "-d a b c" # Invalid, a b c cannot be cast to ints unless you create a custom cast function
    inputC = "-d width:4 d:5 h:6" # Valid
    inputD = "-d w:7 8 d:9" # Valid, note the order: width, then unnamed argument which will be resolved to height because width and depth are named with an alias, then depth
    inputE = "-d w:10 11 12" # Valid
    inputF = "-d w:13 d:'-14' h:-15" # Invalid, validateInt function does not allow negative values (-14), and arguments (h:-15) starting with the command prefix (default "-") must be a named alias with quotation marks
    inputG = "-d w:16 d:':17' h::18" # Invalid, the default int casting (':17') will fail, and arguments with colon ":" (h::18) must be a named alias or in quotation marks
    inputH = "-test 19 20 21" # Invalid, command "test" does not exist and nothing will be returned from validate
    inputI = "-d 22 24 25 --updateexternal" # Valid, flag --updateexternal will return a static value
    inputJ = "-d 26 27 28 --nosuchflag" # Valid, but flag does not exist and reports this through Result.messages
    inputK = "-d 29 30 31 ExternalVendorUpdateList:warehouse,default" # Valid, note that the string "warehouse,default" will be cast to a list of strings with these validated items
    inputL = "-d 31 32 33 evul:notvalid" # Valid, but "notvalid" is not part of pre-approved ExternalVendorUpdateList items, validated in validateFunc, and results in a message
    
    # Input as single string
    argResults = argumentor.validateString(inputA)

## Recommendations

1. Use another, more complete argument parser library
1. See [ExampleBasic.py](https://github.com/gardehal/argumentor/blob/main/tests/ExampleBasic.py) and [ExampleAdvanced.py](https://github.com/gardehal/argumentor/blob/main/tests/ExampleAdvanced.py) for examples of usage.
1. Argumentor().validate() returns a list of Result with detected commands. Parse the result with this in mind:
    1. If the list is empty, no command-like input was detected.
    1. When populated, each Result will specify what command was hit by name and have a hitValue that was specified on init.
    1. If a command is detected but has errors, isValid will be false, and messages will details.
    1. Valid commands will have a dict of cast arguments ready to use.
1. Document your Commands, Arguments, and Flags using descriptions, provide a command (HELP/MAN) for users to see this. Access a printable description of commands through Argumentor().getFormattedDescription().
1. Arguments may have fields for custom casting and validation functions (castFunc, validateFunc), the usage and limitations of these should be documented in descriptions.
1. Use arguments defaultValue and useDefaultValue to set a default or fallback in case casting or validating input from user fails. In some cases, a validation function is needed to apply default (e.g. default:0, validation: 0 >= value >= 100, input: -1, default of 0 is applied).
1. Static values can be set using a Flag, if the flag is present in input, the value set in Flag init will be in Result[x].arguments, otherwise the default value is added.

## TODO

- for description, some way to group commands or arguments to it can be printed with some sort of title? Makes it easier for walls of text, or maybe options to put something (newlines, "---") between all commands?
    - extra optional input for argumentor, dict[str, Command] where str is the "grouping"?
    - extra optional str to command, "grouping", with separate formatted print command that orders by grouping (sort groupings and commands how exactly?), with grouping header left/right args? e.g. "---- " + command.grouping + " ----"?
- guaranteed that multiple things can be improved in validate, both efficacy and readability
