def get_inner_type(
    type_hint: Union[Type[BaseModel], Optional[BaseModel]]
) -> Union[Type[BaseModel], Type[int], Type[str], Type[float]]:
    """Get the inner type of a type hint, i.e., List[Something] -> Something"""
    if hasattr(type_hint, "__origin__"):
        type_origin = type_hint.__origin__
        type_args = type_hint.__args__

        if type_origin == list:
            return get_inner_type(type_args[0])

        if type_origin == Union:  # Optional is a subclass of Union
            # Remove 'None' from Union args to get the base type
            non_none_args = [arg for arg in type_args if arg is not type(None)]
            # Assuming only one non-None type argument for Optional
            if len(non_none_args) == 1:
                return get_inner_type(non_none_args[0])
            else:  # For Union with multiple non-None types
                return get_inner_type(type_hint)
    else:
        # If the type hint has no origin, it is a base type
        return type_hint
