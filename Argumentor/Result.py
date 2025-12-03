
class Result():
    """
    Returns of validate, with info of what command was hit, what values was added, where it was in the input string, what to parse next for the caller
    """
    
    isValid: bool
    commandName: str
    commandHitValue: object
    commandIndex: int
    arguments: dict[str, object]
    errorMessages: list[str]
    
    def __init__(self, isValid: bool, commandName: str, commandHitValue: object, commandIndex: int, arguments: dict[str, object], errorMessages: list[str]):
        self.isValid = isValid
        self.commandName = commandName
        self.commandHitValue = commandHitValue
        self.commandIndex = commandIndex
        self.arguments = arguments
        self.errorMessages = errorMessages
        
    def toString(self) -> str:
        return f"""
            isValid: {self.isValid},
            commandName: {self.commandName},
            commandHitValue: {self.commandHitValue},
            commandIndex: {self.commandIndex},
            arguments: {self.arguments},
            errorMessages: {self.errorMessages},
            """
