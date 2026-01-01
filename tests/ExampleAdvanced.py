import sys
from Argumentor import *
from enums.Measurement import Measurement
from enums.CommandHitValues import CommandHitValues
    
class Main:
    def main():
        # Example input: python ExampleAdvanced.py -d 1 2 3 inches
        
        widthArgument = Argument("Width", ["width", "w"], int,
            validateFunc= validateInt, description= "Width of object, between 1 and 100")
        depthArgument = Argument("Depth", ["depth", "d"], int,
            validateFunc= validateInt, description= "Depth of object, between 1 and 100")
        heightArgument = Argument("Height", ["height", "h"], int,
            validateFunc= validateInt, description= "Height of object, between 1 and 100")
        unitArgument = Argument("Unit", ["unit", "u"], Measurement,
            optional= True,
            castFunc= castMeasurements, 
            validateFunc= validateMeasurements,
            useDefaultValue= True, defaultValue= Measurement.CENTIMETERS,
            description= "Unit of measurements, cm or inches, default cm")
        
        helpCommand = Command("Help", CommandHitValues.HELP, ["help", "h", "man"], 
            description= "Print this documentation")
        dimensionCommand = Command("Dimensions", CommandHitValues.DIMENSIONS, ["dimensions", "dimension", "dim", "d"], 
            [widthArgument, depthArgument, heightArgument, unitArgument],
            description= "Add the dimensions of object")
        argumentor = Argumentor([helpCommand, dimensionCommand])
        
        results = argumentor.validate(sys.argv)
        
        if(len(results) == 0):
            print("No valid command was found, please consult the manual for available commands.")
            return
        
        for result in results:
            # print(result.toString()) # For debugging
            if(not result.isValid):
                print(f"Input for {result.commandName} was not valid:")
                print(result.getFormattedErrors())
                continue
            
            if(result.errorMessages):
                print(f"Command {result.commandName} was accepted with modifications:")
                print(result.getFormattedErrors())
                        
            if(result.isValid and result.commandHitValue == CommandHitValues.HELP):
                print(argumentor.getFormattedDescription())
                
            if(result.isValid and result.commandHitValue == CommandHitValues.DIMENSIONS):
                print("Updating dimensions ...")
                # itemService.updateDimensions(result.arguments[widthArgument.name], 
                #   result.arguments[depthArgument.name], 
                #   result.arguments[heightArgument.name], 
                #   result.arguments[unitArgument.name])
        
# Note: castFunc must be from string and return typeT
def castMeasurements(value: str) -> Measurement:
    match value.lower():
        case "1" | "cm":
            return Measurement.CENTIMETERS
        case "2" | "inch" | "inches":
            return Measurement.INCHES
        case _:
            return Measurement.CENTIMETERS
            
# Note: validateFunc must be from typeT and return bool
def validateMeasurements(value: Measurement) -> bool:
    return value in iter(Measurement)

# Note: validateFunc must be from typeT and return bool
def validateInt(value: int) -> bool:
    return value > 0 and value < 100

if __name__ == "__main__":
    Main.main()
