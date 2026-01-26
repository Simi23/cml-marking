import sys
from typing import Type, get_args, get_origin
from pydantic import BaseModel
from configuration import AppConfig


def generate_markdown(model: Type[BaseModel], level: int = 1):
    """
    Recursively generates a Markdown reference for a Pydantic model.
    """
    print(f"{'#' * level} {model.__name__}")
    if model.__doc__:
        print(f"{model.__doc__.strip()}\n")

    print("| Field | Type | Required | Default | Description |")
    print("| :--- | :--- | :---: | :--- | :--- |")

    sub_models = []

    for name, field in model.model_fields.items():
        # Get the type name
        type_display = str(field.annotation).replace("typing.", "")

        # Check for nested Pydantic models to recurse later
        origin = get_origin(field.annotation)
        args = get_args(field.annotation)

        # Identify if this field is a Pydantic model (or List[Model])
        target_model = None
        if isinstance(field.annotation, type) and issubclass(
            field.annotation, BaseModel
        ):
            target_model = field.annotation
        elif origin is list and args and issubclass(args[0], BaseModel):
            target_model = args[0]
            type_display = f"List[{target_model.__name__}]"

        if target_model:
            sub_models.append(target_model)
            type_display = f"[{type_display}](#{target_model.__name__.lower()})"
        else:
            # Clean up type display for markdown
            type_display = f"`{type_display}`"

        # Extract metadata
        required = "✅" if field.is_required() else "❌"
        default = (
            str(field.default)
            if field.default is not None and str(field.default) != "PydanticUndefined"
            else "-"
        )
        description = field.description if field.description else "-"

        print(
            f"| **{name}** | {type_display} | {required} | {default} | {description} |"
        )

    print("\n")

    # Recurse for nested models
    for sub in sub_models:
        generate_markdown(sub, level + 1)


if __name__ == "__main__":
    generate_markdown(AppConfig)
