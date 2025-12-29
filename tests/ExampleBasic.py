import sys
from Argumentor import *
from enums.CommandHitValues import CommandHitValues
    
class Main:
    def main():
        # Example input: python ExampleBasic.py -cv 1

        # Set up Arguments
        idArgument = Argument("ObjectID", ["id"], int, description= "Int ID of object to get volume for")
        arguments = [idArgument]
        
        # Create command(s) and Argumentor 
        volumeCommand = Command("Calculate Volume", CommandHitValues.CALC_VOLUME, ["calculatevolume", "calcvolume", "cv"], arguments, "Calculate volume of object by ID")
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
                print(result.getFormattedErrors())
                continue
                    
            if(result.isValid and result.commandHitValue == CommandHitValues.CALC_VOLUME):
                itemDetails = f"{idArgument.name}: {result.arguments[idArgument.name]}"
                print(f"Calculating volume for {itemDetails} ...")
                # itemService.calculateVolumeById(id= result.arguments[idArgument.name])
        
if __name__ == "__main__":
    Main.main()
