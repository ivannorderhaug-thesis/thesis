from abc import ABC, abstractmethod

class BasePromptTemplate(ABC):
    """
    Base class for prompt templates.
    """
    @abstractmethod
    def get_template(self) -> str:
        pass
