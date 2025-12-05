import sys
from Argumentor.Argument import *
from Argumentor.Command import *
from Argumentor.Argumentor import *

from enum import IntEnum
class Measurement(IntEnum):
    CENTIMETERS = 1,
    INCEHES = 2,
    
class CommandHitValues(IntEnum):
    DIMENSIONS = 1,
    GET_VOLUME = 2,
    
class Main:
    def main():
        if(len(sys.argv) == 0):
            print(dimensionCommand.getFormattedDescription())
            
        widthArgument = Argument("Width", 1, ["width", "w"], int, 
                                 validateFunc= validateInt, description= "Width of object, between 1 and 100")
        depthArgument = Argument("Depth", 2, ["depth", "d"], int, 
                                 validateFunc= validateInt, description= "Depth of object, between 1 and 100")
        heightArgument = Argument("Height", 3, ["height", "h"], int, 
                                  validateFunc= validateInt, description= "Height of object, between 1 and 100")
        unitArgument = Argument("Unit", 4, ["unit", "u"], Measurement, 
                                castFunc= castMeasurements, nullable= True, 
                                validateFunc= validateMeasurements, 
                                useDefaultValue= True, defaultValue= Measurement.CENTIMETERS, 
                                description= "Unit of measurements, cm or inches, default cm")
        arguments = [widthArgument, depthArgument, heightArgument, unitArgument]
        
        dimensionCommand = Command("Dimensions", ["dimensions", "dimension", "dim", "d"], CommandHitValues.DIMENSIONS, arguments, "Add the dimensions of object")
        argumentor = Argumentor([dimensionCommand])
        results = argumentor.validate(sys.argv)
        
        if(len(results) == 0):
            print(dimensionCommand.getFormattedDescription())
        
        for result in results:
            # For debugging
            # print(result.toString())
            
            if(not result.isValid):
                print(f"Input for {result.commandName} was not valid:")
                for error in result.errorMessages:
                    print(f"\t{error}")
                    
            if(result.isValid and result.commandHitValue == CommandHitValues.DIMENSIONS):
                print("Updating dimensions ...")
                # itemService.updateDimensions(result.arguments[widthArgument.name], 
                #   result.arguments[depthArgument.name], 
                #   result.arguments[heightArgument.name], 
                #   result.arguments[unitArgument.name])
        
# Note: castFunc must be from string and return typeT
def castMeasurements(value: str) -> Measurement:
    match value.lower():
        case "1", "cm":
            return Measurement.CENTIMETERS
        case "2", "inch", "inches":
            return Measurement.INCEHES
        case _:
            return None
            
# Note: validateFunc must be from typeT and return bool
def validateMeasurements(value: Measurement) -> bool:
    return value in Measurement

# Note: validateFunc must be from typeT and return bool
def validateInt(value: int) -> bool:
    return value > 0 and value < 100

if __name__ == "__main__":
    Main.main()
