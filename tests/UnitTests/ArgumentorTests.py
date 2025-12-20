import unittest
from enum import IntEnum

from Argumentor import *

class ArgumentorTests(unittest.TestCase):
        
    inputA = "-dim 1 2 3" # Valid
    inputB = "-d a b c" # Invalid, a b c cannot be cast to ints unless you create a custom cast function
    inputC = "-d width:4 d:5 h:6" # Valid
    inputD = "-d w:7 8 d:9" # Valid, note the order: width, then unnamed argument which will be resolved to height because width and depth are named with an alias, then depth
    inputE = "-d w:10 11 12" # Valid
    inputF = "-d w:13 d:'-14' h:-15" # Invalid, validateInt function does not allow negative values (-14), and arguments (h:-15) starting with the command prefix (default "-") must be a named alias with quotation marks
    inputG = "-d w:16 d:':17' h::18" # Invalid, the default int casting (':17') will fail, and arguments with colon ":" (h::18) must be a named alias or in quotation marks
    inputH = "-test 1 2 3" # Invalid, command "test" does not exist and nothing will be returned from validate
    
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
            
    def test_Argumentor_ShouldReturnValid_WhenInputA(self):
        argumentor = self.__basicArgumentor()
        result = argumentor.validate(self.inputA.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0].errorMessages), 0)
        self.assertTrue(result[0].isValid)
        
    def test_Argumentor_ShouldReturnInvalid_WhenInputB(self):
        argumentor = self.__basicArgumentor()
        result = argumentor.validate(self.inputB.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0].errorMessages), 3)
        self.assertFalse(result[0].isValid)
        
    def test_Argumentor_ShouldReturnValid_WhenInputC(self):
        argumentor = self.__basicArgumentor()
        result = argumentor.validate(self.inputC.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0].errorMessages), 0)
        self.assertTrue(result[0].isValid)
        
    def test_Argumentor_ShouldReturnValid_WhenInputD(self):
        argumentor = self.__basicArgumentor()
        result = argumentor.validate(self.inputD.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0].errorMessages), 0)
        self.assertTrue(result[0].isValid)
        
    def test_Argumentor_ShouldReturnValid_WhenInputE(self):
        argumentor = self.__basicArgumentor()
        result = argumentor.validate(self.inputE.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0].errorMessages), 0)
        self.assertTrue(result[0].isValid)
        
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