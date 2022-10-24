from abc import ABC, abstractmethod


class SynonymsFinder(ABC):
    @abstractmethod
    def __call__(self, word: str) -> str:
        ...


class EmptySynonymsFinder(ABC):
    def __call__(self, word: str) -> str:
        return ''
