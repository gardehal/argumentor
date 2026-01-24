from .Flag import Flag

class BoolFlag(Flag):
    def __init__(self, name: str, 
        alias: list[str],
        description: str = None):
        """
        Designates values input as a flag after commands. These are always optional and only return a static value.
        eg. update_external in 
        $ -dimensions height:100 --update_external
        
        Inherit from Flag, where value = True and defaultValue = False.
        
        Args:
            name (str): Name of flag, key for dictionary in Return.
            alias (list[str]): Alias of flag.
            description (str, optional): Explaining what the flag is for. Defaults to None.
        """
        
        super().__init__(name, alias, True, False, description)
                
    def getFormattedDescription(self) -> str:
        """
        Get the description of flags with formatting.

        Returns:
            str: String description.
        """
            
        return super().getFormattedDescription()