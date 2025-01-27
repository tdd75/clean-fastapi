from typing import Any, List


def mask_sensitive_values(data: Any, keywords: List[str], mask: str = '***') -> Any:
    def _mask(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: mask if any(kw.lower() in k.lower() for kw in keywords) else _mask(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [_mask(v) for v in value]
        return value

    return _mask(data)
