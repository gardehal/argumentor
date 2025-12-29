import re

from typing import TypeVar, Type, Callable

T = TypeVar("T")

class Argument():
    name: str
    alias: list[str]
    typeT: Type[T]
    castFunc: Callable[[str], T]
    nullable: bool
    validateFunc: Callable[[T], bool]
    useDefaultValue: bool
    defaultValue: T
    description: str
    
    def __init__(self, name: str, 
                 alias: list[str] = [], 
                 typeT: Type[T] = str, 
                 castFunc: Callable[[str], T] = None, 
                 nullable: bool = False, 
                 validateFunc: Callable[[T], bool] = None, 
                 useDefaultValue: bool = False, 
                 defaultValue: T = None, 
                 description: str = None):
        """
        Designates values input as arguments after commands 
        eg. height in 
        $ -dimensions height:100

        Args:
            name (str): Name of argument, key for dictionary in Return
            alias (list[str]): Alias of argument. Defaults to [].
            typeT (Type[T]): Type of argument, str, int, bool, enum, etc. Defaults to str.
            castFunc (Callable[[str], T], optional): Optional function for custom casting of input to typeT. Must take in 1 argument: str and return typeT. Defaults to None.
            nullable (bool, optional): Argument is nullable (from input). Defaults to False. Note that this implies the argument can be None in result, unless useDefaultValue and defaultValue are both set.
            validateFunc (Callable[[T], bool], optional): Optional function for custom validation. Must take in 1 argument: typeT and return bool. Defaults to None.
            useDefaultValue (bool, optional): Use a default value if casting and validation fails. Defaults to False.
            defaultValue (T, optional): The default value to use if casting and validation fails, and useDefaultValue is True. Must be typeT. Defaults to None.
            description (str, optional): Explaining what the argument is for. Defaults to None.
        """
        
        self.name = re.sub(r"\s", "", name)
        self.alias = [re.sub(r"\s", "", e) for e in alias]
        self.typeT = typeT
        self.castFunc = castFunc
        self.nullable = nullable
        self.validateFunc = validateFunc
        self.useDefaultValue = useDefaultValue
        self.defaultValue = defaultValue
        self.description = description
                
    def getFormattedDescription(self) -> str:
        """
        Get the description of arguments with formatting.

        Returns:
            str: String description.
        """
        
        nullableDisplayString = "optional" if self.nullable else "required"
        typeDisplayString = f", type: {self.typeT.__name__}"
        aliasDisplayString = f", alias: {", ".join(self.alias)}" if self.alias else ""
        defaultDisplayString = f", default: {str(self.defaultValue)}" if self.useDefaultValue else ""
        return f"* Argument {self.name} ({nullableDisplayString}{typeDisplayString}{defaultDisplayString}{aliasDisplayString}): \
            \n\t{self.description}"