from pydantic import BaseModel, Field, EmailStr
from typing import Literal, List, Optional, Annotated
from uuid import UUID, uuid4


class User(BaseModel):
    model_config = {"extra": "forbid"}  # proibe atributos extras que não tem no schema

    model_config = {  # maneira mais facil de colocar exemplo
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Joao Bresser",
                    "email": "joao.bresserpereira@gmail.com",
                    "senha": "1234d",
                }
            ]
        },
        "from_attributes": True,  # Permite a conversão de modelos ORM
    }
    id: UUID = Field(
        ...,
        default_factory=uuid4,  # ja gera automaticamento o uuid
        unique=True,
        description="ID único referente ao usuario",
    )
    nome: str = Field(
        ...,
        description="Nome do usuário",
    )
    email: EmailStr = Field(  # faz a validação com email
        ...,
        # pattern=r"[A-Za-z0-9._%+-]+[@][A-Za-z0-9_%-]+[.]?[A-Za-z0-9_%-]+?[.]com", # isso é se eu quiser verificar o email com uma string ai teria que retirar o Emailstr e colocar str
        description="email do usuario",
    )
    senha: str = Field(..., description="Coloque a sua senha")


class UserValidate(BaseModel):
    model_config = {"extra": "forbid"}  # proibe atributos extras que não tem no schema

    model_config = {  # maneira mais facil de colocar exemplo
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Joao Bresser",
                    "email": "joao.bresserpereira@gmail.com",
                    "senha": "1234d",
                }
            ]
        },
        "from_attributes": True,  # Permite a conversão de modelos ORM
    }
    email: EmailStr = Field(  # faz a validação com email
        ...,
        # pattern=r"[A-Za-z0-9._%+-]+[@][A-Za-z0-9_%-]+[.]?[A-Za-z0-9_%-]+?[.]com", # isso é se eu quiser verificar o email com uma string ai teria que retirar o Emailstr e colocar str
        description="email do usuario",
    )
    senha: str = Field(..., description="Coloque a sua senha")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    exp: str


class Validate(BaseModel):
    model_config = {  # maneira mais facil de colocar exemplo
        "json_schema_extra": {
            "examples": [
                {
                    "questao": "Compare as teorias de evolução propostas por Darwin e Lamarck, destacando os pontos principais de cada uma.",
                    "texto": "Lamarck  acreditava que os organismos mudam ao longo da vida para se adaptar às necessidades do ambiente. Ele dizia que, se um animal usasse muito uma parte do corpo, ela ficaria maior ou mais forte, e essas mudanças seriam passadas para os filhos.  Já Charles Darwing propôs que a seleção natural é a principal forma de evolução. Ele acreditava que, dentro de uma população, existem diferenças entre os indivíduos, e alguns têm características que ajudam na sobrevivência, como ser mais rápido ou mais forte. Esses indivíduos têm mais chances de viver e se reproduzir, passando suas características para os filhos. Com o tempo, essas características vão se tornando mais comuns na população, porque as pessoas ou animais com essas vantagens sobrevivem mais.",
                    "gabarito": "Charles Darwin propôs a teoria da seleção natural como o principal mecanismo de evolução. Segundo essa teoria, os indivíduos de uma população apresentam variações herdáveis, e aqueles com características que lhes conferem maior vantagem em seu ambiente têm maior probabilidade de sobreviver e se reproduzir. Com o tempo, essas características vantajosas tornam-se mais comuns na população. Para Darwin, a evolução ocorre por meio de um processo gradual e cumulativo, impulsionado pela sobrevivência diferencial dos mais aptos. Jean-Baptiste Lamarck, por outro lado, acreditava que a evolução se dava pelo uso e desuso de estruturas e pela transmissão de características adquiridas. Em sua teoria, os organismos se adaptavam ao longo de suas vidas em resposta às necessidades impostas pelo ambiente, e essas adaptações eram passadas para seus descendentes. Um exemplo clássico de sua teoria é o pescoço das girafas, que, segundo Lamarck, teria se alongado porque os ancestrais das girafas esticavam o pescoço para alcançar folhas mais altas.",
                }
            ]
        },
        "from_attributes": True,  # Permite a conversão de modelos ORM
    }
    questao: str = Field(
        ...,
        description="Questão a ser validada",
    )
    texto: str = Field(
        ...,
        description="Texto a ser avaliado",
    )
    gabarito: str = Field(
        ...,
        description="Texto de gabarito",
    )
