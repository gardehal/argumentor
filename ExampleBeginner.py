import sys
from Argumentor.Argument import *
from Argumentor.Command import *
from Argumentor.Argumentor import *

from enum import IntEnum
class CommandHitValues(IntEnum):
    HELP = 1,
    DIMENSIONS = 2,
    GET_VOLUME = 3,
    
class Main:
    def main():
        # Set up Arguments
        idArgument = Argument("Object ID", 1, ["id"], int, description= "Width of object")
        arguments = [idArgument]
        
        # Create command(s) and Argumentor 
        volumeCommand = Command("Calculate Volume", CommandHitValues.GET_VOLUME, ["calculatevolume", "calcvolume", "cv"], arguments, "Calculate volume of object by ID")
        argumentor = Argumentor([volumeCommand])

        # The validation itself, input may be a string or a list of string like sys.argv
        results = argumentor.validate(sys.argv)
        
        # Print the description and aliases available for the Command and Arguments when arguments are missing
        if(len(sys.argv) < 2 or len(results) == 0): # Or input is None or empty...
            print(argumentor.getFormattedDescription())
        
        # Looping over results. Note that only Command defined above will be output here 
        for result in results:
            if(not result.isValid):
                print(f"Input for {result.commandName} was not valid:")
                for error in result.errorMessages:
                    print(f"\t{error}")
                    
            if(result.isValid and result.commandHitValue == CommandHitValues.GET_VOLUME):
                itemDetails = f"{idArgument.name}: {result.arguments[idArgument.name]}"
                print(f"Calculating volume for {itemDetails} ...")
                # itemService.calculateVolumeById(id= result.arguments[idArgument.name])
        
if __name__ == "__main__":
    Main.main()
