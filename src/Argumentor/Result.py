
class Result():
    isValid: bool
    commandName: str
    commandHitValue: object
    commandIndex: int
    arguments: dict[str, object]
    errorMessages: list[str]
    
    def __init__(self, isValid: bool, 
                 commandName: str, 
                 commandHitValue: object, 
                 commandIndex: int, 
                 arguments: dict[str, object], 
                 errorMessages: list[str]):
        """
        Result of validate, with info of what command was hit, what values was added, where it was in the input string, what to parse next for the caller
        
        Args:
            isValid (bool): Command and arguments are valid
            commandName (str): Name of command
            commandHitValue (object): Hit value supplied in Command init
            commandIndex (int): Index of command in input
            arguments (dict[str, object]): Dict of arguments, key being the name supplied to Argument init, the value being cast and validated to typeT
            errorMessages (list[str]): List of error messages, if any. Always populated when isValid = False, may contain messages when defaults are applied if casting and validating arguments failed
        """

        self.isValid = isValid
        self.commandName = commandName
        self.commandHitValue = commandHitValue
        self.commandIndex = commandIndex
        self.arguments = arguments
        self.errorMessages = errorMessages
        
    def toString(self) -> str:
        """
        Returns string with class properties.

        Returns: 
            str: String of class properties.
        """
        
        return f""" \
            isValid: {self.isValid},
            commandName: {self.commandName},
            commandHitValue: {self.commandHitValue},
            commandIndex: {self.commandIndex},
            arguments: {self.arguments},
            errorMessages: {self.errorMessages},
            """

    def getFormattedErrors(self) -> str:
        """
        Get errormessages formatted in a printable way.

        Returns: 
            str: String errors.
        """
        
        errorMessages = f"Input for {self.commandName} was not valid:"
        for error in self.errorMessages:
            errorMessages += f"\n* {error}"

        return errorMessages