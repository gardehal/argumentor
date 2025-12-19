import re

from .Argument import Argument

class Command():
    name: str
    hitValue: object
    alias: list[str]
    arguments: list[Argument]
    description: str
    
    def __init__(self, name: str, 
                 hitValue: object, 
                 alias: list[str] = [], 
                 arguments: list[Argument] = [], 
                 description: str = None):
        """
        Designates commands
        eg. dimensions in 
        $ -dimensions value:100

        Args:
            name (str): Name of command
            hitValue (object): Value to return in Result when this command is found in input
            alias (list[str]): Alias of command. Defaults to [].
            arguments (list[Argument]): Arguments to be cast and validated, then returned in Result. Defaults to [].
            description (str, optional): Explaining what the command does. Defaults to None.
        """
        
        self.name = re.sub(r"\s", "", name)
        self.hitValue = hitValue
        self.alias = [re.sub(r"\s", "", e) for e in alias]
        self.arguments = arguments 
        self.description = description
        
        argumentNamesAndAlias = [e.name for e in self.arguments]
        argumentNamesAndAlias.extend([e.alias for e in self.arguments])
        aliasDuplicates = [e for e in argumentNamesAndAlias if argumentNamesAndAlias.count(e) > 1]
        if(aliasDuplicates):
            message = f"Duplicates found in arguments (name or alias): {aliasDuplicates}"
            raise Exception(message)
        
        self.arguments.sort(key=lambda e: e.order)
        
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