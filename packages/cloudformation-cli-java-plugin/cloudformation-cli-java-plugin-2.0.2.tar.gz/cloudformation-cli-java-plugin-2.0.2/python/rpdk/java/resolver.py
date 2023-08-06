from rpdk.core.jsonutils.resolver import UNDEFINED, ContainerType

PRIMITIVE_TYPES = {
    "string": "String",
    "integer": "Integer",
    "boolean": "Boolean",
    "number": "Double",
    UNDEFINED: "Object",
}


def translate_type(resolved_type):
    if resolved_type.container == ContainerType.MODEL:
        return resolved_type.type
    if resolved_type.container == ContainerType.PRIMITIVE:
        return PRIMITIVE_TYPES[resolved_type.type]

    if resolved_type.container == ContainerType.MULTIPLE:
        return "Object"

    item_type = translate_type(resolved_type.type)

    if resolved_type.container == ContainerType.DICT:
        key_type = PRIMITIVE_TYPES["string"]
        return f"Map<{key_type}, {item_type}>"
    if resolved_type.container == ContainerType.LIST:
        return f"List<{item_type}>"
    if resolved_type.container == ContainerType.SET:
        return f"Set<{item_type}>"

    raise ValueError(f"Unknown container type {resolved_type.container}")
