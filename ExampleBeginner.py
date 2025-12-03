import sys
from Argumentor.Argument import *
from Argumentor.Command import *
from Argumentor.Argumentor import *

from enum import IntEnum
class CommandHitValues(IntEnum):
    DIMENSIONS = 1,
    CALC_VOLUME = 2,
    
class Main:
    def main():
        # Set up Arguments
        idArgument = Argument("Object ID", 1, ["id"], int, description= "Width of object")
        arguments = [idArgument]
        
        # Create command(s) and Argumentor 
        volumeCommand = Command("Calculate Volume", 1, ["calculatevolume", "calcvolume", "cv"], CommandHitValues.CALC_VOLUME, arguments, "Calculate volume of object by ID")
        argumentor = Argumentor([volumeCommand])

        # The validation itself, input may be a string or a list of string like sys.argv
        results = argumentor.validate(sys.argv)
        
        # Print the description and aliases available for the Command and Arguments
        if(len(results) == 0): # Or input is None or empty...
            print(volumeCommand.getFormattedDescription())
        
        # Looping over results. Note that only Command defined above will be output here 
        for result in results:
            if(result.isValid and result.commandHitValue == CommandHitValues.CALC_VOLUME):
                print("Calculating volume!")
                # volumeService.calculateById(id= result.arguments[idArgument.name])
        
if __name__ == "__main__":
    Main.main()
