"""Utility helpers for formatting numeric input/output in the Torn BS helper UI."""

from __future__ import annotations

import tkinter as tk
from typing import Optional, Union

NumberLike = Union[int, float, str]


def format_number(value: Optional[NumberLike]) -> str:
    """Return the value with thousands separators; defaults to 0 when empty."""
    if value in (None, ""):
        return "0"
    try:
        number = int(float(value))
    except (TypeError, ValueError):
        return "0"
    return f"{number:,}"


def validate_digit_input(new_value: str, inserted_text: str, action_type: str) -> bool:
    """Allow only digit characters for user edits while letting deletions pass."""
    if action_type == "0":  # deletion
        return True
    return inserted_text.isdigit()


class NumericEntryFormatter:
    """Bind an Entry to an IntVar while showing formatted text."""

    def __init__(self, entry: tk.Entry, variable: tk.IntVar):
        self.entry = entry
        self.variable = variable
        self.formatter = format_number
        self._cursor_digit_index: Optional[int] = None
        self._var_trace_id = self.variable.trace_add("write", self._handle_var_update)
        self.entry.bind("<KeyRelease>", self._handle_user_change, add="+")
        self.entry.bind("<FocusOut>", self._handle_user_change, add="+")
        self._handle_var_update()

    def _handle_user_change(self, _event=None) -> None:
        raw_text = self.entry.get()
        digits_only = _strip_non_digits(raw_text)
        numeric_value = int(digits_only) if digits_only else 0
        cursor_index = self.entry.index(tk.INSERT)
        self._cursor_digit_index = _count_digits(raw_text[:cursor_index])
        if self.variable.get() != numeric_value:
            self.variable.set(numeric_value)
        else:
            self._handle_var_update()

    def _handle_var_update(self, *_args) -> None:
        formatted_value = self.formatter(self.variable.get())
        current_text = self.entry.get()
        digits_left = self._cursor_digit_index
        if digits_left is None:
            digits_left = _count_digits(formatted_value)
        if current_text != formatted_value:
            self._set_entry_text(formatted_value)
        self._cursor_digit_index = digits_left
        self._restore_cursor()

    def _set_entry_text(self, text: str) -> None:
        original_validate = self.entry.cget("validate")
        if original_validate:
            self.entry.configure(validate="none")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        if original_validate:
            self.entry.configure(validate=original_validate)

    def _restore_cursor(self) -> None:
        digits_needed = self._cursor_digit_index or 0
        formatted_text = self.entry.get()
        if digits_needed <= 0:
            self.entry.icursor(0)
            return
        digit_counter = 0
        for idx, char in enumerate(formatted_text):
            if char.isdigit():
                digit_counter += 1
            if digit_counter >= digits_needed:
                self.entry.icursor(idx + 1)
                return
        self.entry.icursor(len(formatted_text))


def _strip_non_digits(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())


def _count_digits(text: str) -> int:
    return sum(1 for ch in text if ch.isdigit())
