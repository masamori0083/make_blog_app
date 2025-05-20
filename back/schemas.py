from pydantic import BaseModel


class CodeInput(BaseModel):
    code: str


class TextInput(BaseModel):
    text: str
