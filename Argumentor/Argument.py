from typing import TypeVar, Type, Callable

T = TypeVar("T")

class Argument():
    name: str
    order: int
    alias: list[str]
    typeT: Type[T]
    castFunc: Callable[[str], T]
    nullable: bool
    validateFunc: Callable[[T], bool]
    useDefaultValue: bool
    defaultValue: T
    description: str
    
    def __init__(self, name: str, 
                 order: int, 
                 alias: list[str], 
                 type: Type[T], 
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
            order (int): Order in which arguments are expected to appear in input
            alias (list[str]): Alias of argument
            type (Type[T]): Type of argument, str, int, bool, enum, etc.
            castFunc (Callable[[str], T], optional): Optional function for custom casting of input to type. Must take in 1 argument: str and return type. Defaults to None.
            nullable (bool, optional): Argument is nullable (from input). Defaults to False.
            validateFunc (Callable[[T], bool], optional): Optional function for custom validation. Must take in 1 argument: type and return bool. Defaults to None.
            useDefaultValue (bool, optional): Use a default value if casting and validation fails. Defaults to False.
            defaultValue (T, optional): The default value to use if casting and validation fails, and useDefaultValue is True. Must be type. Defaults to None.
            description (str, optional): Explaining what the argument is for. Defaults to None.
        """
        
        self.name = name
        self.order = order
        self.alias = alias
        self.typeT = type
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
        
        return f"\tArgument: {self.name} - {self.description}\n\t- Alias: {self.alias}"