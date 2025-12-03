from .Argument import Argument

class Command():
    """
    Designates commands
    eg. dimensions in 
    $ -dimensions value:100
    """
    
    name: str
    order: int
    alias: list[str]
    hitValue: object
    arguments: list[Argument]
    description: str
    
    def __init__(self, name: str, 
                 order: int, 
                 alias: list[str], 
                 hitValue: object, 
                 arguments: list[Argument], 
                 description: str = None):
        self.name = name
        self.order = order
        self.alias = alias
        self.hitValue = hitValue
        self.arguments = arguments 
        self.description = description
        
        self.arguments.sort(key=lambda x: x.order)
        
    def getFormattedDescription(self) -> str:
        """
        Get the description of command and arguments combined with formatting.

        Returns:
            str: String description.
        """
        
        argumentDescriptions = ""
        for argument in self.arguments:
            argumentDescriptions = f"{argumentDescriptions}\n{argument.getFormattedDescription()}"
        
        return f"Command: {self.name} - {self.description}\n- Alias: {self.alias}{argumentDescriptions}"