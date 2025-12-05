from .Argument import Argument
from .Command import Command

class ArgumentValidation():
    """
    Internal validation in Argumentor.
    """
    
    isValid: bool
    namedArguments: dict[str, str]
    validatedArguments: dict[str, str]
    castArguments: dict[str, object]
    errorMessages: list[str]
    
    def __init__(self, inputList: list[str], command: Command, namedArgDelim: str):
        self.isValid = False
        self.namedArguments = {}
        self.validatedArguments = {}
        self.castArguments = {}
        self.errorMessages = []
        
        self.__populateNamedArguments(inputList, namedArgDelim)
        self.__validateNamedArguments(command.arguments)
        self.__addPositionalArguments(inputList, namedArgDelim, command)
        self.__castAndValidateArguments(command)
        
    def toString(self) -> str:
        return f"""
            isValid: {self.isValid},
            namedArguments: {self.namedArguments},
            validatedArguments: {self.validatedArguments},
            castArguments: {self.castArguments},
            errorMessages: {self.errorMessages},
            """
            
    def __populateNamedArguments(self, inputList: list[str], namedArgDelim: str):
        namedInputs = [e for e in inputList if(namedArgDelim in e)]
        namedArguments = {}
        for value in namedInputs:
            key, value = value.split(namedArgDelim)
            namedArguments[key] = value
            
        self.namedArguments = namedArguments
    
    # TODO combine with populate?
    def __validateNamedArguments(self, arguments: list[Argument]):
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
    
    def __addPositionalArguments(self, inputList: list[str], namedArgDelim: str, command: Command):
        unnamedArgs = [e for e in inputList if(e.split(namedArgDelim)[0] not in list(self.validatedArguments.keys()))]
        
        for i in range(len(unnamedArgs)):
            if(i >= len(command.arguments)):
                self.errorMessages.append(f"Received more arguments ({len(unnamedArgs)}) than expected ({len(command.arguments)})")
                for extraArg in unnamedArgs[i:]:
                    self.errorMessages.append(self.__formatArgumentError(extraArg, f"Skipped, exceeds Arguments length"))
                    
                break # unnamedArgs loop
            
            unnamedArg = unnamedArgs[i]
            positionalArg = command.arguments[i]
            if(positionalArg.name in self.validatedArguments.keys()):
                self.errorMessages.append(self.__formatArgumentError(unnamedArg, f"Already added as named argument {positionalArg.name}"))
                continue
            
            self.validatedArguments[positionalArg.name] = unnamedArg
            
    def __castAndValidateArguments(self, command: Command):
        isValid = True
        for key in self.validatedArguments.keys():
            argument = [e for e in command.arguments if e.name is key][0]
            if(argument is None):
                self.errorMessages.append(self.__formatArgumentError(value, "No Argument object found"))
                continue
            
            value = self.validatedArguments[key]
            if(value is None and not argument.nullable):
                if(argument.useDefaultValue):
                    self.errorMessages.append(self.__formatArgumentError(value, f"{key} was None and not nullable, default value {argument.defaultValue} was applied"))
                    castValue = argument.defaultValue
                    continue
                else:
                    self.errorMessages.append(self.__formatArgumentError(value, f"Critical error! {key} was None, and Argument is not nullable"))
                    isValid = False
            
            castSuccess = False
            castValue = None
            try:
                if(argument.castFunc):
                    castValue = argument.castFunc(value)
                else:
                    castValue = (argument.typeT)(value)
                
                if(castValue is None and not argument.nullable):
                    if(argument.useDefaultValue):
                        self.errorMessages.append(self.__formatArgumentError(value, f"{key} was None but argument was not nullable, default value {argument.defaultValue} was applied"))
                        castValue = argument.defaultValue
                    else:
                        self.errorMessages.append(self.__formatArgumentError(value, f"Critical error! {key} was None, not nullable, and no default was given")) # Remember useDefaultValue
                        isValid = False
                        continue
                
                castSuccess = True
            except Exception as ex:
                if(argument.useDefaultValue):
                    self.errorMessages.append(self.__formatArgumentError(value, f"{key} could not be cast, default value {argument.defaultValue} was applied"))
                    castValue = argument.defaultValue
                    continue
                else:
                    self.errorMessages.append(self.__formatArgumentError(value, f"Critical error! {key} could not be cast to {argument.typeT}")) 
                    isValid = False
        
            if(castSuccess and argument.validateFunc and isValid):
                try: 
                    resultValid = argument.validateFunc(castValue)
                    if(not resultValid):
                        if(argument.useDefaultValue):
                            self.errorMessages.append(self.__formatArgumentError(value, f"{key} did not pass validation, default value {argument.defaultValue} was applied"))
                            castValue = argument.defaultValue
                        else:
                            self.errorMessages.append(self.__formatArgumentError(value, f"Critical error! {key} did not pass validation"))
                            isValid = False
                            continue
                except Exception as ex:
                    if(argument.useDefaultValue):
                        self.errorMessages.append(self.__formatArgumentError(value, f"{key} validation raised an exception, default value {argument.defaultValue} was applied"))
                        castValue = argument.defaultValue
                    else:
                        self.errorMessages.append(self.__formatArgumentError(value, f"Critical error! {key} validation raised an exception and no defaults were given"))
                        isValid = False
                        continue
        
            self.castArguments[key] = castValue
            
        # check for missing arguments, add defaults for nullable arguments?
        
        self.isValid = isValid
    
    def __formatArgumentError(self, arg: str, error: str) -> str:
        return f"Argument \"{arg}\" error: {error}"
    