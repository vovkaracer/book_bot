import logging
from math import ceil
import os

logger = logging.getLogger(__name__)

def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    symbols = ',.!:;?'
    for index in range(start + size - 1, start, -1):
        if index == len(text):
            if text[index - 1] in symbols and text[index - 2] not in symbols:
                page_text = text[start:]
                break
        elif index < len(text):
            if (
                    text[index] in symbols and
                    text[index - 1] not in symbols and
                    text[index + 1] not in symbols
            ):
                page_text = text[start:index + 1]
                break
    page_size = len(page_text)
    return page_text, page_size

def prepare_book(path: str, page_size: int = 1050) -> dict[int, str]:
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
        book: dict[int, str] = {}
        cursor: int = 0
        for page in range(1, ceil(len(text) / page_size) + 1):
            page_text = _get_part_text(text, cursor, page_size)
            book[page] = page_text[0].lstrip()
            cursor += page_text[1]
    return book
