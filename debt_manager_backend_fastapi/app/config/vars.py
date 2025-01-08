# vars/__init__.py
import os
from dotenv import load_dotenv

def read_env_file(file_path):
    config = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace and ignore comments or blank lines
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Split into key and value
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"Error reading the file {file_path}: {e}")
    
    return config



# Caminho absoluto para o arquivo .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = BASE_DIR + '\.env'

# Carregar as variáveis do .env
load_dotenv(dotenv_path=ENV_PATH)


# Example: Populate DATABASE_CONFIG from the parsed os
DATABASE_CONFIG = {
    "name": os.getenv("DATABASE_NAME", "default_db_name"),  # Default if not set
    "schema": os.getenv("DATABASE_SCHEMA", "public"),  # Default if not set
    "user": os.getenv("DATABASE_USER", "default_user"),
    "password": os.getenv("DATABASE_PASSWORD", "default_password"),
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": os.getenv("DATABASE_PORT", "5432"),
    "encoding": os.getenv("DATABASE_ENCODING", "UTF8"),  # Default if not set
    "ll_collate": os.getenv("DATABASE_LC_COLLATE", "en_US.UTF-8"),  # Default if not set
    "ll_type": os.getenv("DATABASE_LC_CTYPE", "en_US.UTF-8"),  # Default if not set
    "template": os.getenv("DATABASE_TEMPLATE", "template0"),  # Default if not set
}

DATABASE_URL = (
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['name']}"
)

print("DATABASE_CONFIG:", DATABASE_CONFIG)
print("DATABASE_URL:", DATABASE_URL)



# Populate MongoDB configuration from the parsed os
MONGODB_CONFIG = {
    "username": os.getenv("MONGO_INITDB_ROOT_USERNAME", "default_user"),
    "password": os.getenv("MONGO_INITDB_ROOT_PASSWORD", "default_password"),
    "host": os.getenv("MONGO_HOST", "localhost"),
    "port": os.getenv("MONGO_PORT", "27017"),
    "database": os.getenv("MONGO_DB_NAME", "default_db_name"),
}

MONGO_URI = (
    f"mongodb://{MONGODB_CONFIG['username']}:{MONGODB_CONFIG['password']}@"
    f"{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}"
)

print("MONGODB_CONFIG:", MONGODB_CONFIG)
print("MONGO_URI:", MONGO_URI)


# Extract JWT settings
JWT_SETTINGS = {
    "SECRET_KEY": os.getenv("SECRET_KEY", "default_secret_key"),
    "ALGORITHM": os.getenv("ALGORITHM", "HS256"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)),
}

print("JWT_SETTINGS:", JWT_SETTINGS)