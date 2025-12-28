# Argumentor

Command and argument parsing for Python CLI.

> [!WARNING]  
> This project is not really meant for widespread application and was mostly made for fun. Use at your own risk.

Feel free to contribute if you find any issues though.

## Install

TODO
$ `pip install xxx`

#### Local from folder

1. $ `cd [path to this folder]`
1. Check installed packages
    - $ `python pip list`
1. Purge (external) packages
    - $ `python -m pip cache purge`

## Example

#### Getting started

Creating a command to calculate volume for a given object we have stored somewhere with an ID.
[ExampleBeginner.py](./tests/examples/ExampleBeginner.py)
$ `cd test/examples ; python ExampleBeginner.py -help`

#### A step further

Creating a command that takes multiple inputs, validating dimensions, and a optional argument with custom casting and validation from string to an enum.
[ExampleAdvanced.py](./tests/examples/ExampleAdvanced.py)
$ `cd test/examples ; python ExampleAdvanced.py -help`

##### Expected outcomes

The following list of examples explains some expected outcomes, or could be used to test Argumentor. Note: These are based on [ExampleAdvanced.py](./tests/examples/ExampleAdvanced.py).

    # Note, depending on CLI, these results may vary compared to validateString version as below, or as input into CLI (using ' or " would be a main reason as CLI reads it differently)
    inputA = "-dim 1 2 3" # Valid
    inputB = "-d a b c" # Invalid, a b c cannot be cast to ints unless you create a custom cast function
    inputC = "-d width:4 d:5 h:6" # Valid
    inputD = "-d w:7 8 d:9" # Valid, note the order: width, then unnamed argument which will be resolved to height because width and depth are named with an alias, then depth
    inputE = "-d w:10 11 12" # Valid
    inputF = "-d w:13 d:'-14' h:-15" # Invalid, validateInt function does not allow negative values (-14), and arguments (h:-15) starting with the command prefix (default "-") must be a named alias with quotation marks
    inputG = "-d w:16 d:':17' h::18" # Invalid, the default int casting (':17') will fail, and arguments with colon ":" (h::18) must be a named alias or in quotation marks
    inputH = "-test 1 2 3" # Invalid, command "test" does not exist and nothing will be returned from validate
    
    # Input as string
    argResults = argumentor.validateString(inputA)

## TODO

- remove order from arguments, unnessecary since order is given by list to command anyway
- ArgumentValidation check on input empty and return empty/nonvalid result to prevent looping over all commands..
- if input is None and arg is nullable, apply defaults there, if no defaults and nullable, no keep it as None
- maybe some default print for printing errors like in advanced example
- add default value to help print if enabled
- clean up help print, looks weird, look at similar manual man etc., less indentation, no use of -, replace with * r something, remove command/argument before the names?
- publish pip
- add flags? 