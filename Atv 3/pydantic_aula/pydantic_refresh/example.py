from enum import auto, IntFlag
from typing import Any  
import hashlib
import re
import enum 


from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    ValidationError,
)


class Role(IntFlag):
    Author = auto()
    Editor = auto()
    Developer = auto()
    Admin = Author | Editor | Developer


""" 
    Classe importa 'BaseModel' de pydantic(que importas as definições básicas de validações)
    Como funciona: 
        nomeVariável: tipo = Field(examples= ["Líbna"])
"""

class User(BaseModel):
    name: str = Field(examples=["Arjan"])
    
    #  EmailStr é um tipo de variável importada do pydantic, que só recebe valores String que estejam no formato email
    email: EmailStr = Field(
        examples=["example@arjancodes.com"],
        description="The email address of the user",
        frozen=True,
    )
    
    # SecretStr é um tipo vindo de pydantic, que caso o valor esteja preenchido vai tapar com ***** não deixando a mostra o dado sensivel
    password: SecretStr = Field(
        examples=["Password123"], description="The password of the user"
    )
    
    role: Role = Field(default=Role.Author, description="The role of the user")


# função de validação
def validate(data: dict[str, Any]) -> None:
    try:
        # esse .model_validate vem do pydantic e essa classe criata o possui pois definimos ela assim User(BaseModel)
        user = User.model_validate(data)
        print(user)
    except ValidationError as e:
        print("User is invalid")
        for error in e.errors():
            print(error)



def main() -> None:
    good_data = {
        "name": "Arjan",
        "email": "example@arjancodes.com",
        "password": "Password123",
    }
    bad_data = {"email": "<bad data>", "password": "<bad data>"}

    validate(good_data)
    validate(bad_data)


if __name__ == "__main__":
    main()
