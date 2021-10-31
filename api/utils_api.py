from typing import Any


def dictionary_compress(
    dictionary_to_compress: dict[str, Any],
    keys_to_keep: set,
) -> dict[str, Any]:
    """Compress dictionary by passed keys."""
    return {dict_key: dictionary_to_compress[dict_key] for dict_key in keys_to_keep}
