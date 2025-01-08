from sqlalchemy import Float, Text, create_engine, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func, UUID
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
import psycopg2
from app.config.vars import DATABASE_URL, DATABASE_CONFIG

# Base for SQLAlchemy models
Base = declarative_base()

# Example Models for Tables
class User(Base):
    __tablename__ = "Users"
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, server_default=func.public.generate_sequential_uuid('public.users_users_uuid_seq'))
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

class Debt(Base):
    __tablename__ = "Debts"
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, server_default=func.public.generate_sequential_uuid('public.debts_debts_uuid_seq'))
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("Users.id"), nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    debtor_name = Column(String(100), nullable=False)
    creditor_name = Column(String(100), nullable=False)
    due_date = Column(DateTime, nullable=True)
    debt_closing_date = Column(DateTime, nullable=True)
    status_id = Column(UUID(as_uuid=True), ForeignKey('Status.id'), nullable=False)
    notes = Column(Text, nullable=True)

class Status(Base):
    __tablename__ = "Status"
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, server_default=func.public.generate_sequential_uuid('public.status_status_uuid_seq'))
    name = Column(String, nullable=False, unique=True)

class Logs(Base):
    __tablename__ = "Logs"
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, server_default=func.public.generate_sequential_uuid('public.logs_debts_uuid_seq'))
    action = Column(String, nullable=False)
    details = Column(String, nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("Users.id"), nullable=True)

# Database Connection Handler
class DatabaseConnection:
    """Responsible for creating PostgreSQL connections."""

    @staticmethod
    def create_connection(dbname: str):
        try:
            return psycopg2.connect(
                dbname=dbname,
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                host=DATABASE_CONFIG['host'],
                port=DATABASE_CONFIG['port']
            )
        except psycopg2.Error as e:
            raise RuntimeError(f"Error connecting to the database {dbname}: {e}")

# Database Creator
class DatabaseCreator:
    """Handles database creation and extension setup."""

    @staticmethod
    def create_database():
        try:
            conn = DatabaseConnection.create_connection('postgres')
            conn.autocommit = True
            cursor = conn.cursor()

            # Create the database if it doesn't exist
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DATABASE_CONFIG['name']}'")
            if not cursor.fetchone():
                cursor.execute(f"""
                    CREATE DATABASE {DATABASE_CONFIG['name']}
                    WITH 
                        ENCODING '{DATABASE_CONFIG['encoding']}'
                        LC_COLLATE '{DATABASE_CONFIG['ll_collate']}'
                        LC_CTYPE '{DATABASE_CONFIG['ll_type']}'
                        TEMPLATE {DATABASE_CONFIG['template']};
                """)
                print(f"Database '{DATABASE_CONFIG['name']}' created successfully.")

            cursor.close()
            conn.close()

            # Enable UUID extension and create UUID function
            conn = DatabaseConnection.create_connection(DATABASE_CONFIG['name'])
            conn.autocommit = True
            cursor = conn.cursor()

            cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            print("UUID extension enabled.")

            # Create the sequential UUID generation function
            cursor.execute("""
                CREATE OR REPLACE FUNCTION generate_sequential_uuid(seq_name TEXT)
                RETURNS UUID AS $$
                DECLARE
                    seq_val BIGINT;
                BEGIN
                    SELECT nextval(seq_name) INTO seq_val;
                    RETURN uuid_generate_v1mc() || lpad(seq_val::text, 12, '0');
                END;
                $$ LANGUAGE plpgsql;
            """)
            print("Function generate_sequential_uuid created successfully.")

            # Generate Sequences
            sequences = [
                "CREATE SEQUENCE IF NOT EXISTS public.users_users_uuid_seq START 1;",
                "CREATE SEQUENCE IF NOT EXISTS public.debts_debts_uuid_seq START 1;",
                "CREATE SEQUENCE IF NOT EXISTS public.status_status_uuid_seq START 1;",
                "CREATE SEQUENCE IF NOT EXISTS public.logs_debts_uuid_seq START 1;",
            ]
            for sequence in sequences:
                cursor.execute(sequence)
                print(f"Sequence created or already exists: {sequence.split(' ')[3]}")

            cursor.close()
            conn.close()
        except Exception as e:
            raise RuntimeError(f"Error creating the database: {e}")

# Schema Initializer
class DatabaseInitializer:
    """Responsible for initializing the database schema."""

    def __init__(self, engine):
        self.engine = engine

    def initialize_schema(self):
        try:
            Base.metadata.create_all(bind=self.engine)
            print("All tables created successfully.")
        except Exception as e:
            raise RuntimeError(f"Error initializing the database schema: {e}")

# Database Engine and Session Configuration
class DatabaseConfig:
    """SQLAlchemy database configuration."""

    @staticmethod
    def get_engine():
        return create_engine(DATABASE_URL)

    @staticmethod
    def get_session(engine):
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Main Function
def main():
    try:
        DatabaseCreator.create_database()
        engine = DatabaseConfig.get_engine()
        initializer = DatabaseInitializer(engine)
        initializer.initialize_schema()
    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    main()
