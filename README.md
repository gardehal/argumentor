# Argumentor

Command and argument parsing for Python CLI.

## Install locally

1. $ `cd [path to this folder]`
1. Check installed packages
    - $ `python pip list`
1. Purge (external) packages
    - $ `python -m pip cache purge`

## Example
TODO

## TODO

- fix __argsAreValid
- use description and name/alias to make a help string that can be printed to show users what commands and args do
- check duplicate command names/alias and argument/alias so it cant be -dimensions w:1 w:2 (width and weight)
- Let user find out themselves? 
- reverse? as in get inputs with prefix, remove it, and match on alias, then find index again?
- Main loop and handleing should be reworked, spinning up 15 vars and reassigning seems unnessecary
- rename things, argument is a really bad name, command and argumentor is good, argresult is passable
- error messages should be improved, shorter, more concise

- make egg stuff
- publish pip       

old:
- input validation and read improvement
  - define a flag with aliases
  - set up some positional argument matrix including positional arg name, index, type and nullability, max value min value, max len, min len
  - when a flag is hit, return some key value, enum?, and dict? with positional arguments
  - if a enum or something is required type, universal way of casting? non primitives casting???
  - input null as None, if "None" is wanted as a string, double quote it?
  - validate missing order numbers, starting at 0
  - init should happen, then add lines of args
  - Args(flag = "-", namedArgumentDelim = ":")
  - valueSubArgs = SubArg(name = "value", order = 0, aliases = ["value", "v"], type = int, nullable = False, max = 1000, min = 0)
  - unitsSubArgs = SubArg(name = "unit", order = 1, aliases = ["unit", "u", "measurement", "m"], type = str, nullable = True, maxLen = 6, minLen = 0)
  - Args.addArg(name = "Height", hitValue = DimensionEnum.HEIGHT, aliases = ["h", "height", "up"], subArgs = [valueSubArgs, unitsSubArgs], printErrors = True)
  - results = Args.validate(inputString)
  - argResults(flagName, flagHitValue, flagIndex/order from input, subargsdict? obj?, )
    - The following syntax expected as input
      - Main.py -h 100 
      - Main.py -height 100 
      - Main.py -height 100 cm 
      - Main.py -height value:100 unit:cm 
      - Main.py -height value : 100 unit : cm 
      - Main.py -height value:100
      - Main.py -height 100 99 ...........  (99 is a str technically.., if unit was an enum or something, this would fail.. custom value mapping as input per subarg?)
    - incorrect input, should return errors from validation since its True
      - Main.py height .. (missing flag indicator) 
      - Main.py -height .. (missing required positional arg 0, "value") 
      - Main.py -height -width value:100 .. (missing required positional arg 0, "value" on first flag) 
      - Main.py -height asd .. (expected required positional arg 0, "value" to be int) 
      - Main.py -height 999999 .. (expected required positional arg 0, "value" to be less than 1000)
      - Main.py -height -1 .. (expected required positional arg 0, "value" to be more than -1)
      - Main.py -height 100 aaaaaaaaaaaa .. (expected positional arg 1, "unit" to be shorter than 6 chars)
    - unsure
      - Main.py -height unit:cm value:100 .... (if they're named, order shouldnt matter as long as the required are there and they're all named?)
      - Main.py -height 1 2 3 4 unit:cm value:100 .... (positional and named mixed, but all required are ok, prefer named)