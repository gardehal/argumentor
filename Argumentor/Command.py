from .Argument import Argument

class Command():
    name: str
    order: int
    alias: list[str]
    hitValue: object
    arguments: list[Argument]
    description: str
    
    def __init__(self, name: str, 
                 alias: list[str], 
                 hitValue: object, 
                 arguments: list[Argument], 
                 description: str = None):
        """
        Designates commands
        eg. dimensions in 
        $ -dimensions value:100

        Args:
            name (str): Name of command
            alias (list[str]): _description_
            hitValue (object): _description_
            arguments (list[Argument]): _description_
            description (str, optional): _description_. Defaults to None.
        """
        self.name = name
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