import re

from typing import Any

class Flag():
    name: str
    alias: list[str]
    value: Any
    description: str

    # TODO add to init
    # TODO add prefix to argumentor, duplicate checks, and desc strings
    # TODO add flag to commands
    # TODO add flags to example advanced
    # TODO add to example advanced 
    # updateExternalFlag = Flag[bool]("UpdateExternalVendors", ["updateexternal", "uev", "eu"],
        # description= "Update all external vendors with new values.") 
    
    def __init__(self, name: str, 
                 alias: list[str] = [], 
                 value: Any = None, 
                 description: str = None):
        """
        Designates values input as a flag after commands 
        eg. update_external in 
        $ -dimensions height:100 --update_external

        Args:
            name (str): Name of argument, key for dictionary in Return
            alias (list[str], optional): Alias of argument. Defaults to [].
            value (Any, optional): The value to use if flag is present in input. Defaults to None.
            description (str, optional): Explaining what the argument is for. Defaults to None.
        """
        
        self.name = re.sub(r"\s", "", name)
        self.alias = [re.sub(r"\s", "", e) for e in alias]
        self.value = value
        self.description = description
                
    def getFormattedDescription(self) -> str:
        """
        Get the description of flags with formatting.

        Returns:
            str: String description.
        """
        
        aliasDisplayString = f"alias: {", ".join(self.alias)}" if self.alias else ""
        return f"* Flag {self.name} ({aliasDisplayString}): \
            \n\t{self.description}"