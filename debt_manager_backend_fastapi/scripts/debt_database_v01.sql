
-- Habilitar a extensão para UUID no PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criar o banco de dados com codificação UTF-8
CREATE DATABASE debt_database
WITH 
    ENCODING 'UTF8'
    LC_COLLATE 'en_US.UTF-8'
    LC_CTYPE 'en_US.UTF-8'
    TEMPLATE template0;


CREATE OR REPLACE FUNCTION public.generate_sequential_uuid(seq_name text)
RETURNS uuid AS $$
DECLARE
    seq_value bigint;
BEGIN
    EXECUTE format('SELECT nextval(%L)', seq_name) INTO seq_value;
    RETURN md5(seq_value::text || clock_timestamp()::text)::uuid;
END;
$$ LANGUAGE plpgsql;



DO $$
BEGIN
    EXECUTE (
        SELECT string_agg(
            'GRANT EXECUTE ON FUNCTION ' || ns.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ') TO PUBLIC;',
            ' '
        )
        FROM pg_proc p
        JOIN pg_namespace ns ON ns.oid = p.pronamespace
        WHERE ns.nspname = 'public'
    );
END;
$$;


SELECT
    p.proname AS function_name,
    n.nspname AS schema_name,
    pg_catalog.pg_get_userbyid(p.proowner) AS owner,
    p.proacl
FROM
    pg_proc p
JOIN
    pg_namespace n ON p.pronamespace = n.oid
WHERE
    n.nspname = 'public'
    AND p.proname = 'generate_sequential_uuid';



-- Tabela de Usuários
CREATE SEQUENCE public.users_users_uuid_seq;
CREATE TABLE public.Users (
    id UUID UUID NOT NULL DEFAULT public.generate_sequential_uuid('public.users_users_uuid_seq') PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    hashed_password TEXT NOT NULL,
    creation_date DATE DEFAULT CURRENT_DATE,
    modification_date DATE NULL   
);

-- Tabela de Status
CREATE SEQUENCE public.status_status_uuid_seq;
CREATE TABLE public.Status (
    id UUID UUID NOT NULL DEFAULT public.generate_sequential_uuid('public.status_status_uuid_seq') PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Tabela de Dívidas
CREATE SEQUENCE public.debts_debts_uuid_seq;
CREATE TABLE public.Debts (
    id UUID NOT NULL DEFAULT public.generate_sequential_uuid('public.debts_debts_uuid_seq') PRIMARY KEY,
    user_id UUID NOT NULL,                           -- UUID como chave estrangeira
    title VARCHAR(255) NOT NULL,
    value DECIMAL(12, 2) NOT NULL,
    due_date DATE NOT NULL,
    status_id UUID NOT NULL,                         -- UUID como chave estrangeira
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES public.Users (id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES public.Status (id) ON DELETE CASCADE
);
