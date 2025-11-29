from .Argument import Argument
from .Command import Command

class ValidationDto():
    """
    DTO for working with arguments internally in Argumentor.
    """
    
    isValid: bool
    namedArguments: dict[str, str]
    validatedArguments: dict[str, str]
    castArguments: dict[str, object]
    errorMessages: list[str]
    
    def __init__(self):
        self.isValid = False
        self.namedArguments = {}
        self.castArguments = {}
        self.errorMessages = []
        
    def toString(self) -> str:
        return f"""
            isValid: {self.isValid},
            namedArguments: {self.namedArguments},
            validatedArguments: {self.validatedArguments},
            castArguments: {self.castArguments},
            errorMessages: {self.errorMessages},
            """

    def populateNamedArguments(self, inputList: list[str]) -> ResultDto:
        nameArgumentSplit = [e for e in inputList if(self.namedArgDelim in e)]
        namedArguments = {}
        for value in nameArgumentSplit:
            key, value = value.split(self.namedArgDelim)
            namedArguments[key] = value
            
        self.namedArguments = namedArguments
        return self
    
    # TODO combine with populate?
    def validateNamedArguments(self, arguments: list[Argument]) -> ResultDto:
        argumentAliasMap = {}
        for argument in arguments:
            argumentAliasMap[argument.name] = argument.name
            for alias in argument.alias:
                argumentAliasMap[alias] = argument.name
            
        for key in self.namedArguments.keys():
            if(key not in argumentAliasMap.keys()):
                self.errorMessages.append(self.__formatArgumentError(key, "Not a valid argument alias"))
                continue
            
            if(key in self.validatedArguments.keys()):
                self.errorMessages.append(self.__formatArgumentError(key, "Alias was already added"))
                continue
            
            self.validatedArguments[argumentAliasMap[key]] = self.namedArguments[key]
            
        return self
    
    def addPositionalArguments(self, inputList: list[str], namedArgDelim: str, command: Command) -> ResultDto:
        unnamedArgs = [e for e in inputList if(e.split(namedArgDelim)[0] not in list(self.validatedArguments.keys()))]
        
        for i in range(len(unnamedArgs)):
            if(i >= len(command.arguments)):
                self.errorMessages.append(f"Received more arguments ({len(unnamedArgs)}) than expected ({len(command.arguments)})")
                for extraArg in unnamedArgs[i:]:
                    self.errorMessages.append(self.__formatArgumentError(extraArg, f"Skipped, exceeds Arguments length"))
                    
                break
            
            unnamedArg = unnamedArgs[i]
            positionalArg = command.arguments[i]
            if(positionalArg.name in aliasArgs.keys()):
                self.errorMessages.append(self.__formatArgumentError(unnamedArg, f"Already added as named argument {positionalArg.name}"))
                continue
            
            self.validatedArguments[positionalArg.name] = unnamedArg
            
        return self
    
    def castAndValidateArguments(self, command: Command) -> ResultDto:
        failedValidation = False
        for key in self.validatedArguments.keys():
            argument = [e for e in command.arguments if e.name is key ][0]
            if(argument is None):
                self.errorMessages.append(self.__formatArgumentError(value, "No Argument found"))
                continue
            
            value = self.validatedArguments[key]
            if(value is None and not argument.nullable):
                if(argument.useDefaultValue):
                    self.errorMessages.append(self.__formatArgumentError(value, f"{key} was None and not nullable, default value {argument.defaultValue} was applied"))
                    castValue = argument.defaultValue
                    continue
                else:
                    self.errorMessages.append(self.__formatArgumentError(value, f"Critical error! {key} was None, and Argument is not nullable"))
                    failedValidation = True
            
            castValue = None
            try:
                if(argument.castFunc):
                    castValue = argument.castFunc(value)
                else:
                    castValue = (argument.typeT)(value)
            except:
                if(argument.useDefaultValue):
                    self.errorMessages.append(self.__formatArgumentError(value, f"{key} could not be cast, default value {argument.defaultValue} was applied"))
                    castValue = argument.defaultValue
                    continue
                else:
                    self.errorMessages.append(self.__formatArgumentError(value, f"Critical error! {key} could not be cast to {argument.typeT}")) 
                    failedValidation = True
        
            if(argument.validateFunc):
                resultValid = argument.validateFunc(castValue)
                if(not resultValid):
                    if(argument.useDefaultValue):
                        self.errorMessages.append(self.__formatArgumentError(value, f"{key} did not pass validation, default value {argument.defaultValue} was applied"))
                        castValue = argument.defaultValue
                        continue
                    else:
                        self.errorMessages.append(self.__formatArgumentError(value, f"Critical error! {key} did not pass validation"))
                        failedValidation = True
        
            self.castArguments[key] = castValue
        
        self.isValid = not failedValidation
        return self
    
    def __formatArgumentError(self, arg: str, error: str) -> str:
        return f"Argument \"{arg}\" error: {error}"
    