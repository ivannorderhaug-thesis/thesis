from .builder import build_prompt_template

TEMPLATE_REGISTRY = {
    "regulative": build_prompt_template(),
    "regulative_with_examples": build_prompt_template(with_examples=True),
    "constitutive": build_prompt_template(),
    "constitutive_with_examples": build_prompt_template(with_examples=True),
}

def get_template(name: str):
    """
    Retrieve a prompt template by name from the registry.

    Args:
        name (str): The name of the template to retrieve.

    Returns:
        The corresponding prompt template.
    """
    if name not in TEMPLATE_REGISTRY:
        raise ValueError(f"Template '{name}' not found in registry.")
    
    return TEMPLATE_REGISTRY[name]