"""Typed, side-effect-free prompt template rendering."""

from __future__ import annotations

import re
from dataclasses import dataclass
from string import Template
from typing import Any


class TemplateValidationError(ValueError):
    """Raised before a prompt can be rendered with invalid values."""


@dataclass(frozen=True)
class TemplateField:
    name: str
    value_type: type
    required: bool = True
    default: Any = None


@dataclass(frozen=True)
class RenderedPrompt:
    text: str
    template_id: str
    values: dict[str, Any]


@dataclass(frozen=True)
class PromptTemplate:
    template_id: str
    source: str
    fields: tuple[TemplateField, ...]

    def render(self, values: dict[str, Any]) -> RenderedPrompt:
        definitions = {field.name: field for field in self.fields}
        unknown = sorted(set(values) - set(definitions))
        if unknown:
            raise TemplateValidationError(f"unknown template fields: {unknown}")
        resolved: dict[str, Any] = {}
        for name, field in definitions.items():
            if name in values:
                value = values[name]
            elif field.required and field.default is None:
                raise TemplateValidationError(f"missing template field: {name}")
            else:
                value = field.default
            if not isinstance(value, field.value_type):
                raise TemplateValidationError(
                    f"field {name} requires {field.value_type.__name__}"
                )
            resolved[name] = value
        try:
            rendered = Template(self.source).substitute(resolved)
        except (KeyError, ValueError) as error:
            raise TemplateValidationError(
                f"invalid template source: {error}"
            ) from error
        if re.search(r"\$\{?[A-Za-z_][A-Za-z0-9_]*\}?", rendered):
            raise TemplateValidationError("rendered prompt contains unresolved fields")
        return RenderedPrompt(
            text=rendered,
            template_id=self.template_id,
            values=resolved,
        )
