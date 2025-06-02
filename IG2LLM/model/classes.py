from typing import List
from pydantic import BaseModel, Field

class Regulative(BaseModel):
    """
    Represents a regulative component with various attributes.
    """
    I: List[str] = Field(default_factory=list)
    A: List[str] = Field(default_factory=list)
    Ap: List[str] = Field(default_factory=list, alias="A,p")
    Bdir: List[str] = Field(default_factory=list)
    Bdirp: List[str] = Field(default_factory=list, alias="Bdir,p")
    Bind: List[str] = Field(default_factory=list)
    Bindp: List[str] = Field(default_factory=list, alias="Bind,p")
    D: List[str] = Field(default_factory=list)
    Cac: List[str] = Field(default_factory=list)
    Cex: List[str] = Field(default_factory=list)
    O: List[str] = Field(default_factory=list)

    class Config:
        populate_by_name = True

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        return {k: v for k, v in data.items() if v != []}


class Constitutive(BaseModel):
    """
    Represents a constitutive component with various attributes.
    """
    E: List[str] = Field(default_factory=list)
    Ep: List[str] = Field(default_factory=list, alias="E,p")
    F: List[str] = Field(default_factory=list)
    P: List[str] = Field(default_factory=list)
    Pp: List[str] = Field(default_factory=list, alias="P,p")
    M: List[str] = Field(default_factory=list)
    Cac: List[str] = Field(default_factory=list)
    Cex: List[str] = Field(default_factory=list)
    O: List[str] = Field(default_factory=list)

    class Config:
        populate_by_name = True

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        return {k: v for k, v in data.items() if v != []}

class Classification(BaseModel):
    """
    Represents a classification of a component with its type.
    """
    type: str

    def to_dict(self):
        return self.model_dump()
