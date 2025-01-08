import jwt
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave secreta do .env
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não foi definido no .env")

def generate_jwt(password: str) -> str:
    """
    Gera um token JWT baseado na senha.
    
    Args:
        password (str): Senha do usuário.

    Returns:
        str: Token JWT gerado.
    """
    payload = {"password": password}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token: str) -> dict:
    """
    Decodifica um token JWT assinado usando HS256.
    
    Args:
        token (str): Token JWT a ser decodificado.

    Returns:
        dict: Dados contidos no token JWT.
    """
    try:
        # Decodificar o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise RuntimeError("O token expirou.")
    except jwt.InvalidTokenError:
        raise RuntimeError("Token inválido.")

# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo (payload)
    payload = {
        "username": "johndoe",
        "email": "john@example.com"
    }

    # Gerar o token JWT
    token = generate_jwt(payload)
    print(f"Token JWT gerado: {token}")

    # Decodificar o token JWT
    decoded_payload = decode_jwt(token)
    print(f"Dados decodificados do token: {decoded_payload}")
