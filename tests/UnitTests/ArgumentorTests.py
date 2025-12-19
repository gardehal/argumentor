import unittest
from enum import IntEnum

from Argumentor import *

class ArgumentorTests(unittest.TestCase):
        
    def test_Argumentor_ShouldRemoveSpaces_WhenSpacesInNamesAndAlias(self):
        argumentor = self.__basicArgumentor()
        namesAndAlias = []
        for command in argumentor.commands:
            namesAndAlias.append(command.name)
            namesAndAlias.extend(command.alias)
            for argument in command.arguments:
                namesAndAlias.append(argument.name)
                namesAndAlias.extend(argument.alias)
            
        for name in namesAndAlias:
            print(name)
            self.assertFalse(name.__contains__(" "))
            
    def test_Argumentor_ShouldSortArgumentsByOrder_WhenLastOrderArgAddedFirst(self):
        argumentor = self.__basicArgumentor()
        arguments = [a for c in argumentor.commands for a in c.arguments]
        
        self.assertEqual("Width", arguments[0].name)
        self.assertEqual("Depth", arguments[1].name)
        self.assertEqual("Height", arguments[2].name)
        self.assertEqual("Unit", arguments[3].name)
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateArgumentNameAlias(self):
        duplicateArgument = Argument("test", 1, ["test", "t"], int)
        try:
            Command("Duplicate", 1, [], [duplicateArgument])
            self.assertTrue(False) # Fail here
        except:
            self.assertTrue(True)
        
    def __basicArgumentor(self) -> Argumentor:
        # Note spaces in name and alias
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
        # Note order, unit (4) first
        arguments = [unitArgument, widthArgument, depthArgument, heightArgument]
        
        # Note spaces in name and alias
        helpCommand = Command("He lp", CommandHitValues.HELP, ["h e l p", "h"], [], "Print this documentation")
        dimensionCommand = Command("Dimensions", CommandHitValues.DIMENSIONS, ["dimensions", "dimension", "dim", "d"], arguments, "Add the dimensions of object")
        return Argumentor([helpCommand, dimensionCommand])
    
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