import unittest
from enum import IntEnum

from Argumentor import *

class ArgumentorTests(unittest.TestCase):
    
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        
    def test_Argumentor_WhenSpacesInNamesAndAlias_ShouldRemoveSpaces(self):
        argumentor = self.__basicArgumentor()
        argumentNames = [a.name for c in argumentor.commands for a in c.arguments]
        for name in argumentNames:
            print(name)
            self.assertFalse(name.__contains__(" "))
        
    def __basicArgumentor(self) -> Argumentor:
        widthArgument = Argument("Widt h", 1, ["w idt h", "w"], int, 
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
        arguments = [unitArgument, widthArgument, depthArgument, heightArgument]
        
        helpCommand = Command("Help", CommandHitValues.HELP, ["help", "h"], [], "Print this documentation")
        dimensionCommand = Command("Dimensions", CommandHitValues.DIMENSIONS, ["dimensions", "dimension", "dim", "d"], arguments, "Add the dimensions of object")
        return Argumentor([helpCommand, dimensionCommand])

    def __splitInput(self, input: str) -> list[str]:
        return input.split(" ")
    
if __name__ == '__main__':
    unittest.main()
    
class Measurement(IntEnum):
    CENTIMETERS = 1,
    INCHES = 2,
    
class CommandHitValues(IntEnum):
    HELP = 1,
    DIMENSIONS = 2,
    CALC_VOLUME = 3,
    
# Note: castFunc must be from string and return typeT
def castMeasurements(value: str) -> Measurement:
    match value.lower():
        case "1" | "cm":
            return Measurement.CENTIMETERS
        case "2" | "inch" | "inches":
            return Measurement.INCHES
        case _:
            return None
            
# Note: validateFunc must be from typeT and return bool
def validateMeasurements(value: Measurement) -> bool:
    return value in iter(Measurement)

# Note: validateFunc must be from typeT and return bool
def validateInt(value: int) -> bool:
    return value > -10 and value < 100