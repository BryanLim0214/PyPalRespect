"""Prompts package."""
from app.prompts.system_prompts import (
    get_tutor_system_prompt,
    get_task_decomposition_prompt,
    get_hint_prompt,
    get_celebration_prompt,
)

__all__ = [
    "get_tutor_system_prompt",
    "get_task_decomposition_prompt",
    "get_hint_prompt",
    "get_celebration_prompt",
]
