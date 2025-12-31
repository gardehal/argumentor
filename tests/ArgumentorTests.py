import unittest

from Argumentor import *
from enums.Measurement import Measurement
from enums.CommandHitValues import CommandHitValues

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
            self.assertFalse(name.__contains__(" "))
            
    def test_Argumentor_ShouldBeInAddedOrder_WhenAddedAsList(self):
        argumentor = self.__basicArgumentor()
        arguments = [a for c in argumentor.commands for a in c.arguments]
        
        self.assertEqual("Width", arguments[0].name)
        self.assertEqual("Depth", arguments[1].name)
        self.assertEqual("Height", arguments[2].name)
        self.assertEqual("Unit", arguments[3].name)
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateArgumentNameAlias(self):
        duplicateArgumentA = Argument("someargument", ["A"], int)
        duplicateArgumentB = Argument("B", ["someargument"], int)
        command = Command("Duplicate", "DUPLICATEHITVALUE", [], [duplicateArgumentA, duplicateArgumentB])

        try:
            Argumentor([command])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate arguments"))
            self.assertTrue(str(ex).__contains__("someargument"))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateArgumentNames(self):
        duplicateArgumentA = Argument("someargument", ["A"], int)
        duplicateArgumentB = Argument("someargument", ["B"], int)
        command = Command("Duplicate", "DUPLICATEHITVALUE", [], [duplicateArgumentA, duplicateArgumentB])

        try:
            Argumentor([command])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate arguments"))
            self.assertTrue(str(ex).__contains__("someargument"))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateArgumentAlias(self):
        duplicateArgumentA = Argument("A", ["someargument"], int)
        duplicateArgumentB = Argument("B", ["someargument"], int)
        command = Command("Duplicate", "DUPLICATEHITVALUE", [], [duplicateArgumentA, duplicateArgumentB])

        try:
            Argumentor([command])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate arguments"))
            self.assertTrue(str(ex).__contains__("someargument"))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateCommandNameAlias(self):
        duplicateCommandA = Command("somecommand", "DUPLICATEHITVALUE", ["A"])
        duplicateCommandB = Command("B", "DUPLICATEHITVALUE", ["somecommand"])

        try:
            Argumentor([duplicateCommandA, duplicateCommandB])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate commands"))
            self.assertTrue(str(ex).__contains__("somecommand"))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateCommandNames(self):
        duplicateCommandA = Command("somecommand", "DUPLICATEHITVALUE", ["A"])
        duplicateCommandB = Command("somecommand", "DUPLICATEHITVALUE", ["B"])

        try:
            Argumentor([duplicateCommandA, duplicateCommandB])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate commands"))
            self.assertTrue(str(ex).__contains__("somecommand"))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateCommandAlias(self):
        duplicateCommandA = Command("A", "DUPLICATEHITVALUE", ["somecommand"])
        duplicateCommandB = Command("B", "DUPLICATEHITVALUE", ["somecommand"])

        try:
            Argumentor([duplicateCommandA, duplicateCommandB])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate commands"))
            self.assertTrue(str(ex).__contains__("somecommand"))
            
    def test_Argumentor_ShouldDoNothing_WhenCommandAndArgumentHaveSameNames(self):
        name = "someargument"
        argument = Argument(name, ["A"], int)
        command = Command(name, "DUPLICATEHITVALUE", ["B"], [argument])

        argumentor = Argumentor([command])
        self.assertEqual(1, len(argumentor.commands))
        self.assertEqual(1, len(argumentor.commands[0].arguments))
        self.assertEqual(name, argumentor.commands[0].name)
        self.assertEqual(name, argumentor.commands[0].arguments[0].name)
            
    def test_Argumentor_ShouldReturnValid_WhenInputA(self):
        argumentor = self.__basicArgumentor()
        inputA = "-dim 1 2 3" # Valid
        result = argumentor.validate(inputA.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].errorMessages), 0)
        
    def test_Argumentor_ShouldReturnInvalid_WhenInputB(self):
        argumentor = self.__basicArgumentor()
        inputB = "-d a b c" # Invalid, a b c cannot be cast to ints unless you create a custom cast function
        result = argumentor.validate(inputB.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertFalse(result[0].isValid)
        self.assertEqual(len(result[0].errorMessages), 4)
        self.assertTrue(result[0].errorMessages[0].__contains__("a could not be cast"))
        self.assertTrue(result[0].errorMessages[1].__contains__("b could not be cast"))
        self.assertTrue(result[0].errorMessages[2].__contains__("c could not be cast"))
        self.assertTrue(result[0].errorMessages[3].__contains__("Critical error! Required arguments are missing (got 0/3)"))
        
    def test_Argumentor_ShouldReturnValid_WhenInputC(self):
        argumentor = self.__basicArgumentor()
        inputC = "-d width:4 d:5 h:6" # Valid
        result = argumentor.validate(inputC.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].errorMessages), 0)
        
    def test_Argumentor_ShouldReturnValid_WhenInputD(self):
        argumentor = self.__basicArgumentor()
        inputD = "-d w:7 8 d:9" # Valid, note the order: width, then unnamed argument which will be resolved to height because width and depth are named with an alias, then depth
        result = argumentor.validate(inputD.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].errorMessages), 0)
        
    def test_Argumentor_ShouldReturnValid_WhenInputE(self):
        argumentor = self.__basicArgumentor()
        inputE = "-d w:10 11 12" # Valid
        result = argumentor.validate(inputE.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].errorMessages), 0)
        
    def test_Argumentor_ShouldReturnInvalid_WhenInputF(self):
        argumentor = self.__basicArgumentor()
        # Note quatation markes ' removed as it's not CLI input
        inputF = "-d w:13 d:-14 h:-15" # Invalid, validateInt function does not allow negative values (-14), and arguments (h:-15) starting with the command prefix (default "-") must be a named alias with quotation marks
        result = argumentor.validate(inputF.split(" "))
    
        self.assertEqual(len(result), 1)
        self.assertFalse(result[0].isValid)
        self.assertEqual(len(result[0].errorMessages), 3)
        self.assertTrue(result[0].errorMessages[0].__contains__("-14 did not pass validation"))
        self.assertTrue(result[0].errorMessages[1].__contains__("-15 did not pass validation"))
        self.assertTrue(result[0].errorMessages[2].__contains__("Critical error! Required arguments are missing (got 1/3)"))
        
    def test_Argumentor_ShouldReturnInvalid_WhenInputG(self):
        argumentor = self.__basicArgumentor()
        # Note quatation markes ' removed as it's not CLI input
        inputG = "-d w:16 d::17 h::18" # Invalid, the default int casting (':17') will fail, and arguments with colon ":" (h::18) must be a named alias or in quotation marks
        result = argumentor.validate(inputG.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertFalse(result[0].isValid)
        self.assertEqual(len(result[0].errorMessages), 3)
        self.assertTrue(result[0].errorMessages[0].__contains__(":17 could not be cast to int"))
        self.assertTrue(result[0].errorMessages[1].__contains__(":18 could not be cast to int"))
        self.assertTrue(result[0].errorMessages[2].__contains__("Critical error! Required arguments are missing (got 1/3)"))
        
    def test_Argumentor_ShouldReturnEmptyResult_WhenInputH(self):
        argumentor = self.__basicArgumentor()
        inputH = "-test 1 2 3" # Invalid, command "test" does not exist and nothing will be returned from validate
        result = argumentor.validate(inputH.split(" "))
        
        self.assertEqual(len(result), 0)
        
    def __basicArgumentor(self) -> Argumentor:
        # Note spaces in name and alias
        widthArgument = Argument("Widt h", ["w idt h", "w"], int,
            validateFunc= self.validateInt, description= "Width of object, between 1 and 100")
        depthArgument = Argument("Depth", ["depth", "d"], int,
            validateFunc= self.validateInt, description= "Depth of object, between 1 and 100")
        heightArgument = Argument("Height", ["height", "h"], int,
            validateFunc= self.validateInt, description= "Height of object, between 1 and 100")
        unitArgument = Argument("Unit", ["unit", "u"], Measurement,
            castFunc= self.castMeasurements, nullable= True,
            validateFunc= self.validateMeasurements,
            useDefaultValue= True, defaultValue= Measurement.CENTIMETERS,
            description= "Unit of measurements, cm or inches, default cm")
        arguments = [widthArgument, depthArgument, heightArgument, unitArgument]
        
        # Note spaces in name and alias
        helpCommand = Command("He lp", CommandHitValues.HELP, ["h e l p", "h"], [], "Print this documentation")
        dimensionCommand = Command("Dimensions", CommandHitValues.DIMENSIONS, ["dimensions", "dimension", "dim", "d"], arguments, "Add the dimensions of object")
        return Argumentor([helpCommand, dimensionCommand])
    
    # Note: castFunc must be from string and return typeT
    def castMeasurements(self, value: str) -> Measurement:
        match value.lower():
            case "1" | "cm":
                return Measurement.CENTIMETERS
            case "2" | "inch" | "inches":
                return Measurement.INCHES
            case _:
                return None
                
    # Note: validateFunc must be from typeT and return bool
    def validateMeasurements(self, value: Measurement) -> bool:
        return value in iter(Measurement)

    # Note: validateFunc must be from typeT and return bool
    def validateInt(self, value: int) -> bool:
        return value > 0 and value < 100

if __name__ == '__main__':
    unittest.main()
    