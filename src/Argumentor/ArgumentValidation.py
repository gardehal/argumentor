from .Argument import Argument
from .Command import Command

import re

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
        for input in namedInputs:
            namedSplit = input.split(namedArgDelim)
            key = namedSplit[0]
            value = namedArgDelim.join(namedSplit[1:])
            namedArguments[key] = value
            
        self.namedArguments = namedArguments
    
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
        namedInputRegex = fr"^\w+{namedArgDelim}\S*"
        unnamedInput = [e for e in inputList if(not re.search(namedInputRegex, e))]
        remainingArgument = [e for e in command.arguments if(e.name not in self.validatedArguments.keys())]

        for i in range(len(unnamedInput)):
            if(i >= len(remainingArgument)):
                self.errorMessages.append(f"Received more positional arguments ({len(unnamedInput)}) than expected ({len(remainingArgument)})")
                for extraArg in unnamedInput[i:]:
                    self.errorMessages.append(f"{extraArg} not added, exceeds expected Arguments length")
                    
                break # unnamedInput loop
            
            unnamedArg = unnamedInput[i]
            positionalArg = remainingArgument[i]
            if(positionalArg.name in self.validatedArguments.keys()):
                self.errorMessages.append(self.__formatArgumentError(positionalArg.name, f"Already added as named argument {unnamedArg}"))
                continue
            
            self.validatedArguments[positionalArg.name] = unnamedArg
            
    def __castAndValidateArguments(self, command: Command):
        inputIsValid = True
        for key in self.validatedArguments.keys():
            argument = [e for e in command.arguments if e.name is key][0]
            if(argument is None):
                self.errorMessages.append(self.__formatArgumentError(key, "No Argument object found"))
                inputIsValid = False
                continue
            
            value = self.validatedArguments[key]
            if(value is None and not argument.nullable):
                if(argument.useDefaultValue):
                    self.errorMessages.append(self.__formatArgumentError(key, f"Value was None and not nullable, default value {argument.defaultValue} was applied"))
                    castValue = argument.defaultValue
                    continue
                else:
                    self.errorMessages.append(self.__formatArgumentError(key, f"Critical error! Value was None, and Argument is not nullable"))
                    inputIsValid = False
                    continue
            
            castSuccess = False
            castValue = None
            try:
                if(argument.castFunc):
                    castValue = argument.castFunc(value)
                else:
                    castValue = (argument.typeT)(value)
                
                if(castValue is None and not argument.nullable):
                    if(argument.useDefaultValue):
                        self.errorMessages.append(self.__formatArgumentError(key, f"Value was None but argument was not nullable, default value {argument.defaultValue} was applied"))
                        castValue = argument.defaultValue
                        continue
                    else:
                        self.errorMessages.append(self.__formatArgumentError(key, f"Critical error! Value was None, not nullable, and no default was given")) # Remember useDefaultValue
                        inputIsValid = False
                        continue
                
                castSuccess = True
            except Exception as ex:
                if(argument.useDefaultValue):
                    self.errorMessages.append(self.__formatArgumentError(key, f"{value} could not be cast, default value {argument.defaultValue} was applied"))
                    castValue = argument.defaultValue
                    continue
                else:
                    self.errorMessages.append(self.__formatArgumentError(key, f"Critical error! {value} could not be cast to {argument.typeT.__name__}")) 
                    inputIsValid = False
                    continue
        
            if(castSuccess and argument.validateFunc):
                try: 
                    resultValid = argument.validateFunc(castValue)
                    if(not resultValid):
                        if(argument.useDefaultValue):
                            self.errorMessages.append(self.__formatArgumentError(key, f"{value} did not pass validation, default value {argument.defaultValue} was applied"))
                            castValue = argument.defaultValue
                            continue
                        else:
                            self.errorMessages.append(self.__formatArgumentError(key, f"Critical error! {value} did not pass validation"))
                            inputIsValid = False
                            continue
                except Exception as ex:
                    if(argument.useDefaultValue):
                        self.errorMessages.append(self.__formatArgumentError(key, f"{value} validation raised an exception, default value {argument.defaultValue} was applied"))
                        castValue = argument.defaultValue
                        continue
                    else:
                        self.errorMessages.append(self.__formatArgumentError(key, f"Critical error! {value} validation raised an exception and no defaults were given"))
                        inputIsValid = False
                        continue
        
            self.castArguments[key] = castValue
            
        requiredArgumentNames = [e.name for e in command.arguments if not e.nullable]
        if(len(self.castArguments.keys())) < len(requiredArgumentNames):
            self.errorMessages.append(f"Critical error! Required arguments are missing (got {len(self.castArguments.keys())}/{len(requiredArgumentNames)})")
            inputIsValid = False
        
        if(inputIsValid):
            for argument in command.arguments:
                if(argument.name not in self.castArguments.keys() and argument.useDefaultValue):
                    self.castArguments[argument.name] = argument.defaultValue
        
        self.isValid = inputIsValid
    
    def __formatArgumentError(self, arg: str, error: str) -> str:
        return f"{arg} error: {error}"
    