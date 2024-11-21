from fastapi import FastAPI, Query, APIRouter, HTTPException, status, Depends, Request
from sqlalchemy import select  # para conseguir manipular a base de dados
from models import User as UserModel
from models import UserIn as UserModelIn
from schema import User as UserSchema
from schema import UserValidate as UserSchemaValidate
from schema import Validate
from database import SessionDB, create_db_and_tables
from typing import List, Annotated
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from pydantic import BaseModel, ValidationError


# usado para authenticacao
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext  # usado para hash
from typing import Union, Any

from schema import Token, TokenData
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


SALT = os.getenv("SALT")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# modulo usado para verificar, fazer hash  etc..
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# funcao para verificar se esta certo o hash
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password + str(SALT), hashed_password)


# retorna o password como hash
def get_password_hash(password):
    return pwd_context.hash(password + str(SALT))


# Utility function to generate a new access token.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


router_user = APIRouter()


@router_user.get(
    "/usuarios/",
    response_model=List[UserSchema],  # Usa o schema para a resposta
    tags=["Usuarios"],
    summary="Obter todos os usuarios",
    description="Retorna a lista de todos os usuarios disponíveis (cadastrados).",
)
def read_usuarios(
    session: SessionDB,
    offset: int = 0,  # coloca quanto de offset ent se for 10 nao retorna os 10 primeiros
    limit: Annotated[
        int, Query(le=100)
    ] = 100,  # limite de quantidade para ser retornado
):
    stmt = select(UserModel).offset(offset).limit(limit)
    usuarios = session.execute(stmt)
    # Converte os objetos ORM para Pydantic (UserSchema) usando model_validate
    locais_resposta = [UserSchema.model_validate(user) for user, in usuarios]
    return locais_resposta


@router_user.post(
    "/registrar/",
    response_model=Token,  # Usa o schema para a resposta
    tags=["Usuarios"],
    summary="Criar novo usuario",
    description="Adiciona um novo usuario com as informações fornecidas.",
)
def create_usuario(usuario: UserSchema, session: SessionDB):
    email_existe = session.query(UserModelIn).filter_by(email=usuario.email).first()
    if email_existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado.",
        )
    # Cria o hash da senha antes de salvar no banco
    hashed_password = get_password_hash(usuario.senha)
    novo_usuario = UserModelIn(
        **usuario.model_dump(exclude_unset=True)
    )  # coloca todas as infirmacoes de usuario na configuração de UserModel
    novo_usuario.senha = hashed_password
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)
    # Gera o token JWT com o ID ou email do usuário
    access_token = create_access_token(data={"email": novo_usuario.email})
    return Token(access_token=access_token, token_type="bearer")


@router_user.post(
    "/login",
    response_model=Token,
    tags=["Usuarios"],
    summary="Login de usuario",
    description="Autentica um usuario e retorna o token JWT se as credenciais estiverem corretas.",
)
def login(session: SessionDB, usuario: UserSchemaValidate):
    usuario_banco = session.query(UserModel).filter_by(email=usuario.email).first()
    if not usuario_banco:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email Não foi encontrado cadastrado.",
        )
    if not verify_password(usuario.senha, usuario_banco.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="senha incorreta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"email": usuario_banco.email})
    return Token(access_token=access_token, token_type="bearer")


# como essa classe é uma dependencia de uma função o fast-api compreende que é uma dependencia e que precisa adicionar um token de validação
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        # Obtém as credenciais (token) da requisição
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            # Retorna o token para ser validado em `get_current_user`
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


async def get_current_user(
    session: SessionDB, token: str = Depends(JWTBearer())
) -> UserSchema:
    try:
        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Verifica se o token está expirado
    except jwt.ExpiredSignatureError:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}
        )
        exp_timestamp = payload.get("exp")
        # Calcula quanto tempo desde a expiração
        if exp_timestamp:
            expired_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            time_since_expiration = datetime.now(timezone.utc) - expired_at
            expired_message = f"Token expired {time_since_expiration} ago"
        else:
            expired_message = "Token expired, but expiration time is unavailable."
        # Aqui da erro de token invalidado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=expired_message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    # aqui da erro de token não foi credenciado
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Obtém o usuário pelo email do payload
    user = session.query(UserModelIn).filter_by(email=payload["email"]).first()
    # se usuario sumiu vem para ca
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserSchema.model_validate(user)


# validando
@router_user.post(
    "/validar",
    tags=["Usuarios"],
    summary="Essa api tem como objetivo caso você se o usuário estiver validado ele vai mandar um texto a ser corrigido e um texto gabarito e o modelo de llm retornará se as informações correspondem.",
)
async def get_validar(
    informacoes: Validate, user: UserSchema = Depends(get_current_user)
):

    def validate():

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Voce é um corretor de textos."},
                {
                    "role": "user",
                    "content": f"""Voce receberá uma questão, um texto e um gabarito e retornará escrevendo apenas 'Certo','Errado' ou 'incompleto' Após isso de um \n e caso estiver errado ou incompleto falar que tópicos o texto precisa abordar para ser considerado certo.\n
                    Questao: {informacoes.questao}
                    Texto: {informacoes.texto} \n
                    Gabarito: {informacoes.gabarito}""",
                },
            ],
        )

        print(completion.choices[0].message.content)

        print(informacoes.gabarito)
        print(informacoes.texto)
        return completion.choices[0].message.content

    if user:

        return validate()
