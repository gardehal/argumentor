import unittest

from Argumentor import *
from enums.Measurement import Measurement
from enums.CommandHitValues import CommandHitValues

class ArgumentorTests(unittest.TestCase):
    # Run from base directory
    # py .\tests\ArgumentorTests.py
    
    def test_Argumentor_ShouldRaiseException_WhenSpaceInArgumentName(self):
        invalidName = "invalid name"
        try:
            Argument(invalidName, [], int)
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__(f"Argument \"{invalidName}\" name or alias (['{invalidName}']) contain invalid characters"))
            
    def test_Argumentor_ShouldRaiseException_WhenSpaceInArgumentAlias(self):
        name = "A"
        invalidName = "invalid name"
        try:
            Argument(name, [invalidName], int)
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__(f"Argument \"{name}\" name or alias (['{invalidName}']) contain invalid characters"))
            
    def test_Argumentor_ShouldRaiseException_WhenSpaceInFlagName(self):
        invalidName = "invalid name"
        try:
            Flag(invalidName, [], 1)
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__(f"Flag \"{invalidName}\" name or alias (['{invalidName}']) contain invalid characters"))
            
    def test_Argumentor_ShouldRaiseException_WhenSpaceInFlagAlias(self):
        name = "A"
        invalidName = "invalid name"
        try:
            Flag(name, [invalidName], 1)
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__(f"Flag \"{name}\" name or alias (['{invalidName}']) contain invalid characters"))
            
    def test_Argumentor_ShouldRaiseException_WhenSpaceInCommandName(self):
        invalidName = "invalid name"
        try:
            Command(invalidName, [], "HITVALUE")
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__(f"Command \"{invalidName}\" name or alias (['{invalidName}']) contain invalid characters"))
            
    def test_Argumentor_ShouldRaiseException_WhenSpaceInCommandAlias(self):
        name = "A"
        invalidName = "invalid name"
        try:
            Command(name, [invalidName], "HITVALUE")
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__(f"Command \"{name}\" name or alias (['{invalidName}']) contain invalid characters"))
            
    def test_Argumentor_ShouldBeInAddedOrder_WhenAddedAsList(self):
        argumentor = self.__basicArgumentor()
        arguments = [a for c in argumentor.commands for a in c.arguments]
        
        self.assertEqual("Width", arguments[0].name)
        self.assertEqual("Depth", arguments[1].name)
        self.assertEqual("Height", arguments[2].name)
        self.assertEqual("Unit", arguments[3].name)
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateArgumentorPrefix(self):
        prefix = "someprefix"
        try:
            Argumentor([], commandPrefix= prefix, flagPrefix= prefix)
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate prefixes or delims"))
            self.assertTrue(str(ex).__contains__(prefix))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateArgumentNameAlias(self):
        argumentName = "someargument"
        argumentA = Argument(argumentName, ["A"], int)
        argumentB = Argument("B", [argumentName], int)
        command = Command("Duplicate", [], "HITVALUE", [argumentA, argumentB])

        try:
            Argumentor([command])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate arguments"))
            self.assertTrue(str(ex).__contains__(argumentName))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateArgumentNames(self):
        argumentName = "someargument"
        argumentA = Argument(argumentName, ["A"], int)
        argumentB = Argument(argumentName, ["B"], int)
        command = Command("Duplicate", [], "HITVALUE", [argumentA, argumentB])

        try:
            Argumentor([command])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate arguments"))
            self.assertTrue(str(ex).__contains__(argumentName))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateArgumentAlias(self):
        argumentName = "someargument"
        argumentA = Argument("A", [argumentName], int)
        argumentB = Argument("B", [argumentName], int)
        command = Command("Duplicate", [], "HITVALUE", [argumentA, argumentB])

        try:
            Argumentor([command])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate arguments"))
            self.assertTrue(str(ex).__contains__(argumentName))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateFlagNameAlias(self):
        flagName = "someflag"
        flagA = Argument(flagName, ["A"], int)
        flagB = Argument("B", [flagName], int)
        command = Command("Duplicate", [], "HITVALUE", flags= [flagA, flagB])

        try:
            Argumentor([command])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate flag"))
            self.assertTrue(str(ex).__contains__(flagName))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateFlagNames(self):
        flagName = "someflag"
        flagA = Flag(flagName, ["A"], int)
        flagB = Flag(flagName, ["B"], int)
        command = Command("Duplicate", [], "HITVALUE", flags= [flagA, flagB])

        try:
            Argumentor([command])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate flags"))
            self.assertTrue(str(ex).__contains__(flagName))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateFlagAlias(self):
        flagName = "someflag"
        flagA = Flag("A", [flagName], int)
        flagB = Argument("B", [flagName], int)
        command = Command("Duplicate", [], "HITVALUE", flags= [flagA, flagB])

        try:
            Argumentor([command])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate flags"))
            self.assertTrue(str(ex).__contains__(flagName))

    def test_Argumentor_ShouldRaiseException_WhenDuplicateCommandNameAlias(self):
        commandName = "somecommand"
        commandA = Command(commandName, ["A"], "HITVALUE")
        commandB = Command("B", [commandName], "HITVALUE")

        try:
            Argumentor([commandA, commandB])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate commands"))
            self.assertTrue(str(ex).__contains__(commandName))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateCommandNames(self):
        commandName = "somecommand"
        commandA = Command(commandName, ["A"], "HITVALUE")
        commandB = Command(commandName, ["B"], "HITVALUE")

        try:
            Argumentor([commandA, commandB])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate commands"))
            self.assertTrue(str(ex).__contains__(commandName))
        
    def test_Argumentor_ShouldRaiseException_WhenDuplicateCommandAlias(self):
        commandName = "somecommand"
        commandA = Command("A", [commandName], "HITVALUE")
        commandB = Command("B", [commandName], "HITVALUE")

        try:
            Argumentor([commandA, commandB])
            self.assertTrue(False) # Fail here
        except AttributeError as ex:
            self.assertTrue(str(ex).__contains__("Duplicate commands"))
            self.assertTrue(str(ex).__contains__(commandName))
            
    def test_Argumentor_ShouldDoNothing_WhenCommandAndArgumentHaveSameNames(self):
        name = "someargument"
        argument = Argument(name, ["A"], int)
        command = Command(name, ["B"], "HITVALUE", [argument])

        argumentor = Argumentor([command])
        self.assertEqual(1, len(argumentor.commands))
        self.assertEqual(1, len(argumentor.commands[0].arguments))
        self.assertEqual(name, argumentor.commands[0].name)
        self.assertEqual(name, argumentor.commands[0].arguments[0].name)
            
    def test_Argumentor_ShouldReturnValid_CommandCalledByName(self):
        commandName = "testCommand"
        commandHitValue = "HITVALUE"
        command = Command(commandName, [], commandHitValue)
        
        argumentor = Argumentor([command])
        
        result = argumentor.validate([f"-{commandName}"])

        self.assertEqual(1, len(result))
        self.assertTrue(result[0].isValid)
        self.assertEqual(commandName, result[0].commandName)
        self.assertEqual(commandHitValue, result[0].commandHitValue)
            
    def test_Argumentor_ShouldReturnValid_CommandCalledByAlias(self):
        commandName = "testCommand"
        commandAlias = "testAlias"
        commandHitValue = "HITVALUE"
        command = Command(commandName, [commandAlias], commandHitValue)
        
        argumentor = Argumentor([command])
        
        result = argumentor.validate([f"-{commandAlias}"])

        self.assertEqual(1, len(result))
        self.assertTrue(result[0].isValid)
        self.assertEqual(commandName, result[0].commandName)
        self.assertEqual(commandHitValue, result[0].commandHitValue)
            
    def test_Argumentor_ShouldReturnValid_WhenInputA(self):
        argumentor = self.__basicArgumentor()
        inputA = "-dim 1 2 3" # Valid
        result = argumentor.validate(inputA.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].arguments), 6)
        self.assertEqual(len(result[0].messages), 0)
        
    def test_Argumentor_ShouldReturnInvalid_WhenInputB(self):
        argumentor = self.__basicArgumentor()
        inputB = "-d a b c" # Invalid, a b c cannot be cast to ints unless you create a custom cast function
        result = argumentor.validate(inputB.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertFalse(result[0].isValid)
        self.assertEqual(len(result[0].messages), 4)
        self.assertTrue(result[0].messages[0].__contains__("a could not be cast"))
        self.assertTrue(result[0].messages[1].__contains__("b could not be cast"))
        self.assertTrue(result[0].messages[2].__contains__("c could not be cast"))
        self.assertTrue(result[0].messages[3].__contains__("Critical error! Required arguments are missing (got 0/3)"))
        
    def test_Argumentor_ShouldReturnValid_WhenInputC(self):
        argumentor = self.__basicArgumentor()
        inputC = "-d width:4 d:5 h:6" # Valid
        result = argumentor.validate(inputC.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].messages), 0)
        
    def test_Argumentor_ShouldReturnValid_WhenInputD(self):
        argumentor = self.__basicArgumentor()
        inputD = "-d w:7 8 d:9" # Valid, note the order: width, then unnamed argument which will be resolved to height because width and depth are named with an alias, then depth
        result = argumentor.validate(inputD.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].messages), 0)
        
    def test_Argumentor_ShouldReturnValid_WhenInputE(self):
        argumentor = self.__basicArgumentor()
        inputE = "-d w:10 11 12" # Valid
        result = argumentor.validate(inputE.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].messages), 0)
        
    def test_Argumentor_ShouldReturnInvalid_WhenInputF(self):
        argumentor = self.__basicArgumentor()
        # Note quotation marks ' removed as it's not CLI input
        inputF = "-d w:13 d:-14 h:-15" # Invalid, validateInt function does not allow negative values (-14), and arguments (h:-15) starting with the command prefix (default "-") must be a named alias with quotation marks
        result = argumentor.validate(inputF.split(" "))
    
        self.assertEqual(len(result), 1)
        self.assertFalse(result[0].isValid)
        self.assertEqual(len(result[0].messages), 3)
        self.assertTrue(result[0].messages[0].__contains__("-14 did not pass validation"))
        self.assertTrue(result[0].messages[1].__contains__("-15 did not pass validation"))
        self.assertTrue(result[0].messages[2].__contains__("Critical error! Required arguments are missing (got 1/3)"))
        
    def test_Argumentor_ShouldReturnInvalid_WhenInputG(self):
        argumentor = self.__basicArgumentor()
        # Note quotation marks ' removed as it's not CLI input
        inputG = "-d w:16 d::17 h::18" # Invalid, the default int casting (':17') will fail, and arguments with colon ":" (h::18) must be a named alias or in quotation marks
        result = argumentor.validate(inputG.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertFalse(result[0].isValid)
        self.assertEqual(len(result[0].messages), 3)
        self.assertTrue(result[0].messages[0].__contains__(":17 could not be cast to int"))
        self.assertTrue(result[0].messages[1].__contains__(":18 could not be cast to int"))
        self.assertTrue(result[0].messages[2].__contains__("Critical error! Required arguments are missing (got 1/3)"))
        
    def test_Argumentor_ShouldReturnEmptyResult_WhenInputH(self):
        argumentor = self.__basicArgumentor()
        inputH = "-test 19 20 21" # Invalid, command "test" does not exist and nothing will be returned from validate
        result = argumentor.validate(inputH.split(" "))
        
        self.assertEqual(len(result), 0)

    def test_Argumentor_ShouldReturnValidResultWithFlagValue_WhenInputI(self):
        argumentor = self.__basicArgumentor()
        inputI = "-d 22 24 25 --updateexternal" # Valid, flag --updateexternal will return a static value
        result = argumentor.validate(inputI.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].arguments), 6)
        self.assertEqual(len(result[0].messages), 0)

    def test_Argumentor_ShouldReturnValidWithoutFlags_WhenInputJ(self):
        argumentor = self.__basicArgumentor()
        inputJ = "-d 26 27 28 --nosuchflag" # Valid, but flag does not exist and reports this through Result.messages
        result = argumentor.validate(inputJ.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].arguments), 6)
        self.assertEqual(len(result[0].messages), 1)
        self.assertTrue(result[0].messages[0].__contains__("nosuchflag"))
        self.assertTrue(result[0].messages[0].__contains__("No such flag(s)"))

    def test_Argumentor_ShouldReturnValidWithExternalVendorUpdateList_WhenInputK(self):
        argumentor = self.__basicArgumentor()
        inputK = "-d 29 30 31 ExternalVendorUpdateList:warehouse,default" # Valid, note that the string "warehouse,default" will be cast to a list of strings with these validated items
        result = argumentor.validate(inputK.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].arguments), 6)
        self.assertListEqual(result[0].arguments["ExternalVendorUpdateList"], ["warehouse", "default"])
        self.assertEqual(len(result[0].messages), 0)

    def test_Argumentor_ShouldReturnValidWithInvalidExternalVendorUpdateListItem_WhenInputL(self):
        argumentor = self.__basicArgumentor()
        inputL = "-d 31 32 33 evul:notvalid" # Valid, but "notvalid" is not part of pre-approved ExternalVendorUpdateList items, validated in validateFunc, and results in a message
        result = argumentor.validate(inputL.split(" "))
        
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].isValid)
        self.assertEqual(len(result[0].arguments), 6)
        self.assertListEqual(result[0].arguments["ExternalVendorUpdateList"], [])
        self.assertEqual(len(result[0].messages), 1)
        self.assertTrue(result[0].messages[0].__contains__("did not pass validation"))
        self.assertTrue(result[0].messages[0].__contains__("default value [] was applied"))
        
    def __basicArgumentor(self) -> Argumentor:
        widthArgument = Argument("Width", ["width", "w"], int,
            validateFunc= self.validateInt, description= "Width of object, between 1 and 100")
        depthArgument = Argument("Depth", ["depth", "d"], int,
            validateFunc= self.validateInt, description= "Depth of object, between 1 and 100")
        heightArgument = Argument("Height", ["height", "h"], int,
            validateFunc= self.validateInt, description= "Height of object, between 1 and 100")
        unitArgument = Argument("Unit", ["unit", "u"], Measurement,
            optional= True,
            castFunc= self.castMeasurements,
            validateFunc= self.validateMeasurements,
            useDefaultValue= True, defaultValue= Measurement.CENTIMETERS,
            description= "Unit of measurements, cm or inches, default cm")
        externalVendorUpdateListArgument = Argument("ExternalVendorUpdateList", ["externalvendorsupdatelist", "evul"], list[str],
            optional= True,
            castFunc= self.castStringToList,
            validateFunc= self.validateExternalVendorsList,
            useDefaultValue= True, defaultValue= [],
            description= "List of external vendors to update")
        
        updateExternalFlag = BoolFlag("UpdateExternalVendors", ["updateexternal", "uev", "eu"], 
            description= "Update all external vendors with new values.") 
        
        helpCommand = Command("Help", ["help", "h"],
            CommandHitValues.HELP, 
            description= "Print this documentation")
        dimensionCommand = Command("Dimensions", ["dimensions", "dimension", "dim", "d"],
            CommandHitValues.DIMENSIONS,
            [widthArgument, depthArgument, heightArgument, unitArgument, externalVendorUpdateListArgument], [updateExternalFlag],
            description= "Add the dimensions of object")
        return Argumentor([helpCommand, dimensionCommand])
    
    # Note: castFunc must be from string and return typeT
    def castMeasurements(self, value: str) -> Measurement:
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
    def castStringToList(self, value: str, separator: str = ",") -> list[str]:
        return value.split(separator)
                
    # Note: validateFunc must be from typeT and return bool
    def validateMeasurements(self, value: Measurement) -> bool:
        return value in iter(Measurement)

    # Note: validateFunc must be from typeT and return bool
    def validateInt(self, value: int) -> bool:
        return value > 0 and value < 100

    # Note: validateFunc must be from typeT and return bool
    def validateExternalVendorsList(self, vendorsList: list[str]) -> bool:
        for vendor in vendorsList:
            if(vendor not in ["default", "warehouse", "webstore"]):
                return False
        
        return True 

if __name__ == '__main__':
    unittest.main()
    