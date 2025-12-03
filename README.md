# Argumentor

Command and argument parsing for Python CLI.

> [!WARNING]  
> This project is not really meant for widespread application and was mostly made for fun. Use at your own risk.

Feel free to contribute if you find any issues though.

## Install locally

1. $ `cd [path to this folder]`
1. Check installed packages
    - $ `python pip list`
1. Purge (external) packages
    - $ `python -m pip cache purge`

## Example

#### Getting started

Creating a command to read size of some objects with width, depth, height as arguments.

    # Set up Arguments
    widthArgument = Argument("Width", 1, ["width", "w"], int, description= "Width of object in CM")
    depthArgument = Argument("Depth", 2, ["depth", "d"], int, description= "Depth of object in CM")
    heightArgument = Argument("Height", 3, ["height", "h"], int, description= "Height of object in CM")
    dimensionArguments = [widthArgument, depthArgument, heightArgument]
    
    # Create command(s) and Argumentor 
    dimensionCommand = Command("Dimensions", 1, ["dimensions", "dimension", "dim", "d"], "DIM", dimensionArguments, "Add the dimensions of object in CM")
    argumentor = Argumentor([dimensionCommand])
    
    # The validation itself, input may be a string or a list of string like sys.argv
    argResults = argumentor.validate(sys.argv)
    
    # Print the description and alias available in Command and Arguments
    if(len(argResults) == 0): # Or input is None or empty...
        print(dimensionCommand.getFormattedDescription())
    
    # Looping over results. Note that only Command defined above will be output here 
    for result in argResults:
        # print(result.toString()) # Visualize content of result, i.e. debugging

        if(result.isValid and result.commandHitValue == "DIM"):
            print("Dimensions updated!")

The following list of examples explains some expected outcomes, or could be used to test Argumentor.

    # Example inputs
    inputA = "-dim 1 2 3" # Valid
    inputB = "-d a b c" # Invalid, a b c cannot be cast to ints unless you create a custom cast function
    inputC = "-d width:4 d:5 h:6" # Valid
    inputD = "-d w:7 8 d:9" # Valid, note the order: width, unnamed arg which will be resolved to height because width and depth are named with an alias, depth
    inputE = "-d w:10 11 12" # Valid
    # WIP(14') inputF = "-d w:13 d:'-14' h:-15" # Invalid, validateInt function does not allow negative values, note also arguments starting with the command prefix (default "-") must be put in quotation marks (anything CLI and Python accepts) or with a named alias e.g. h:-15
    # WIP(double ::) inputG = "-d w:16 d:':17' h::18" # Invalid, the defaault int casting will fail, note also arguments starting with the command prefix (default "-") must be put in quotation marks (anything CLI and Python accepts)
    inputH = "-test 1 2 3" # Invalid, and will not be returned from .validate()
    
    argResults = argumentor.validateString(inputA)

#### The opportunities

TODO

    # [...]

    # Note: castFunc must be from string and return typeT
    def castInt(value: str) -> int:
        return (int)(value.replace("-", ""))

    # Note: validateFunc must be from typeT and return bool
    def validateInt(value: int) -> bool:
        return value > 0 and value < 100

## TODO

- when giving named argument thats wrong, command should still hit and return valid + errors,
- example inputs F and G
- check duplicate command names/alias and argument/alias so it cant be -dimensions w:1 w:2 (width and weight)
  - throw error on init
- error messages should be improved, shorter, more concise
- make egg stuff
- publish pip       
- add unit as optional argument to example?
- make advanced example section with multiple commands, optional nullable arg unit default CM, casting and validator funcs
    - test and finish examples
