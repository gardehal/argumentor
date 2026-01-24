import sys
from Argumentor import *
from enums.Measurement import Measurement
from enums.CommandHitValues import CommandHitValues

class Main:
    def main():
        # Example input: python ExampleAdvanced.py -d 1 2 3 inches warehouse,default --uev

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
        externalVendorUpdateListArgument = Argument("ExternalVendorUpdateList", ["externalvendorsupdatelist", "evul"], list[str],
            optional= True,
            castFunc= castStringToList,
            validateFunc= validateExternalVendorsList,
            useDefaultValue= True, defaultValue= [],
            description= "List of external vendors to update")

        updateExternalFlag = Flag("UpdateExternalVendors", ["updateexternal", "uev", "ue"], 
            description= "Update all external vendors with new values.") 

        helpCommand = Command("Help", ["help", "h", "man"],
            CommandHitValues.HELP,
            description= "Print this documentation")
        dimensionCommand = Command("Dimensions", ["dimensions", "dimension", "dim", "d"],
            CommandHitValues.DIMENSIONS, 
            [widthArgument, depthArgument, heightArgument, unitArgument, externalVendorUpdateListArgument], [updateExternalFlag],
            description= "Add the dimensions of object")
        argumentor = Argumentor([helpCommand, dimensionCommand])

        results = argumentor.validate(sys.argv)

        if(len(results) == 0):
            print("No valid command was found, please consult the manual for available commands. See the syntax description below:")
            print(argumentor.getSyntaxDescription())
            return

        for result in results:
            print(result.toString()) # For debugging
            if(not result.isValid):
                print(f"Input for {result.commandName} was not valid:")
                print(result.getFormattedMessages())
                continue

            if(result.messages):
                print(f"Command {result.commandName} was accepted with modifications:")
                print(result.getFormattedMessages())

            if(result.isValid and result.commandHitValue == CommandHitValues.HELP):
                print(argumentor.getFormattedDescription())

            if(result.isValid and result.commandHitValue == CommandHitValues.DIMENSIONS):
                print("Updating dimensions ...")
                # itemService.updateDimensions(result.arguments[widthArgument.name],
                #   result.arguments[depthArgument.name],
                #   result.arguments[heightArgument.name],
                #   result.arguments[unitArgument.name],
                #   result.arguments[externalVendorUpdateListArgument.name])

                # if(result.arguments[updateExternalFlag.name]):
                #     externalService.update()

# Note: castFunc must be from string and return typeT
def castMeasurements(value: str) -> Measurement:
    match value.lower():
        case "1" | "cm":
            return Measurement.CENTIMETERS
        case "2" | "inch" | "inches":
            return Measurement.INCHES
        case _:
            # Note that a default value can be added here as well,
            # but doing so will override Arguments defaultValue 
            return None
        
# Note: castFunc must be from string and return typeT
def castStringToList(value: str, separator: str = ",") -> list[str]:
    return value.split(separator)

# Note: validateFunc must be from typeT and return bool
def validateMeasurements(value: Measurement) -> bool:
    return value in iter(Measurement)

# Note: validateFunc must be from typeT and return bool
def validateInt(value: int) -> bool:
    return value > 0 and value < 100

# Note: validateFunc must be from typeT and return bool
def validateExternalVendorsList(vendorsList: list[str]) -> bool:
    for vendor in vendorsList:
        if(vendor not in ["default", "warehouse", "webstore"]):
            return False
    
    return True 

if __name__ == "__main__":
    Main.main()
