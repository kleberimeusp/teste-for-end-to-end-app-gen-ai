from typing import Dict, Generic, List, Type, TypeVar, Union
from sqlalchemy.sql import text
from math import ceil

T = TypeVar("T")  # Tipo genérico

from sqlalchemy.exc import SQLAlchemyError

class GenericRepository(Generic[T]):
    def __init__(self, session_factory, model: Type[T]):
        """
        Repositório genérico para buscar registros de qualquer modelo.

        Args:
            session_factory: Função para criar sessões do banco de dados.
            model: Classe do modelo SQLAlchemy.
        """
        self.session_factory = session_factory
        self.model = model
        self.entities = []  # Lista simulada para armazenar as entidades (pode ser substituído por um banco de dados)

        
 
    def find_all(self, page: int = 1, per_page: int = 10) -> dict:
        """
        Recupera registros do modelo genérico com paginação.

        Args:
            page (int): Página atual (1-indexed).
            per_page (int): Número de registros por página.

        Returns:
            Dict: Dados paginados com registros e informações de paginação.
        """
        try:
            if page < 1:
                page = 1  # Garante que a página seja, no mínimo, 1

            with self.session_factory() as session:
                # Garantir que o nome da tabela tenha a primeira letra maiúscula
                table_name = self.model.__tablename__.capitalize()

                # Query para contar o total de registros
                total_query = f'SELECT COUNT(*) FROM "{table_name}"'
                total_records = session.execute(text(total_query)).scalar()

                # Query para buscar registros com paginação
                query = f"""
                    SELECT * FROM "{table_name}"
                    ORDER BY id LIMIT :limit OFFSET :offset
                """
                offset = (page - 1) * per_page
                result = session.execute(
                    text(query),
                    {"limit": per_page, "offset": offset}
                ).fetchall()

                # Assuming each row has a `_fields` attribute containing the column names
                # and `result` is your list of rows
                field_names = []

                # Extracting `_fields` from the first row (assuming all rows have the same fields)
                if result and hasattr(result[0], '_fields'):
                    field_names = list(result[0]._fields)

                # Printing the extracted field names
                print("Field Names:", field_names)

                # Example: converting the rows to dictionaries using field_names
                records = [
                    {field: value for field, value in zip(field_names, row)}
                    for row in result
]
                # Total de registros
                total_records = len(result)

                # Construir a resposta
                total_pages = ceil(total_records / per_page)
                
                # Resposta final com status_code

                value = {
                    "status_code": 200,
                    "data": {
                        "records": records,
                        "pagination": {
                            "page": page,
                            "per_page": per_page,
                            "total_pages": total_pages,
                            "total_records": total_records,
                        },
                    },
                }

                dictValue = dict(value)

                return dictValue
            
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar registros com paginação: {e}")
        
    def get_by_id(self, id: str) -> Dict[str, Union[dict, int]]:
        """
        Recupera um registro específico pelo ID.

        Args:
            id (str): O ID do registro a ser buscado.

        Returns:
            Dict[str, Union[dict, int]]: Um dicionário contendo o status_code e o registro encontrado.
        """
        try:
            with self.session_factory() as session:
                # Garantir que o nome da tabela tenha a primeira letra maiúscula
                table_name = self.model.__tablename__.capitalize()

                # Query para buscar o registro pelo ID
                query = f'SELECT * FROM "{table_name}" WHERE id = :id'
                result = session.execute(text(query), {"id": id}).fetchone()

                # Verifica se o registro foi encontrado
                if result is None:
                    return {
                        "status_code": 404,
                        "message": f"Registro com ID '{id}' não encontrado."
                    }

                # Extrai os nomes dos campos (field_names)
                field_names = list(result._fields) if hasattr(result, '_fields') else []

                # Converte o registro encontrado em um dicionário
                record = {field: value for field, value in zip(field_names, result)}

                # Retorna o registro com um status_code de sucesso
                return {
                    "status_code": 200,
                    "data": record
                }

        except Exception as e:
            raise RuntimeError(f"Erro ao buscar registro por ID: {str(e)}")

            
    

    def save(self, data, sequence_name: str, entity_class=None):
        """
        Salva um registro genérico no banco de dados usando SQL ANSI e gera o ID automaticamente.

        Args:
            data: Dados a serem inseridos como um objeto com atributos ou dicionário.
            sequence_name (str): Nome da sequência para gerar o ID.
            entity_class: A classe associada à tabela para acessar os atributos e o nome da tabela.

        Returns:
            str: ID gerado para o registro.
        """
        try:
            if not entity_class:
                raise ValueError("A `entity_class` deve ser fornecida para determinar o nome da tabela.")

            # Obter o nome da tabela da classe
            if not hasattr(entity_class, "__tablename__"):
                raise AttributeError(f"A classe `{entity_class.__name__}` não define o atributo `__tablename__` para o nome da tabela.")
            
            table_name = entity_class.__tablename__.capitalize()

            # Extrair atributos da entidade
            entity_attributes = {key for key in dir(entity_class) if not key.startswith("_") and not callable(getattr(entity_class, key))}

            # Converter o objeto em um dicionário se necessário
            if not isinstance(data, dict):
                data = {key: getattr(data, key) for key in dir(data) if not key.startswith("_") and not callable(getattr(data, key))}

            # Atributos a serem excluídos
            excluded_attributes = {"metadata", "registry", "id"}

            # Filtrar apenas atributos válidos, que não sejam coleções, e não estejam na lista de exclusão
            filtered_data = {
                key: value
                for key, value in data.items()
                if key in entity_attributes
                and not isinstance(value, (list, dict, set, tuple))
                and key not in excluded_attributes
            }

            # Montar os campos e os placeholders dinamicamente
            columns = ', '.join(filtered_data.keys())
            placeholders = ', '.join([f":{key}" for key in filtered_data.keys()])

            # Query genérica para inserção
            query = text(f"""
                INSERT INTO "{table_name}" (id, {columns})
                VALUES (generate_sequential_uuid('{sequence_name}'), {placeholders})
                RETURNING id
            """)

            with self.session_factory() as session:
                # Executar a query de inserção
                result = session.execute(query, filtered_data)

                # Obter o ID gerado
                generated_id = result.scalar()
                session.commit()
                return generated_id

        except SQLAlchemyError as e:
            session.rollback()  # Reverte as alterações no banco em caso de erro
            raise RuntimeError(f"Erro ao salvar no banco: {e}") from e

    def update(self, record_id: str, data, entity_class=None):
        """
        Atualiza um registro genérico no banco de dados usando SQL ANSI.

        Args:
            record_id (str): O ID do registro a ser atualizado.
            data: Dados a serem atualizados como um objeto com atributos ou dicionário.
            entity_class: A classe associada à tabela para acessar os atributos e o nome da tabela.

        Returns:
            bool: True se a atualização for bem-sucedida, False caso contrário.
        """
        try:
            if not entity_class:
                raise ValueError("A `entity_class` deve ser fornecida para determinar o nome da tabela.")

            # Obter o nome da tabela da classe
            if not hasattr(entity_class, "__tablename__"):
                raise AttributeError(f"A classe `{entity_class.__name__}` não define o atributo `__tablename__` para o nome da tabela.")
            
            table_name = entity_class.__tablename__.capitalize()

            # Extrair atributos da entidade
            entity_attributes = {key for key in dir(entity_class) if not key.startswith("_") and not callable(getattr(entity_class, key))}

            # Converter o objeto em um dicionário se necessário
            if not isinstance(data, dict):
                data = {key: getattr(data, key) for key in dir(data) if not key.startswith("_") and not callable(getattr(data, key))}

            # Atributos a serem excluídos
            excluded_attributes = {"metadata", "registry", "id"}

            # Filtrar apenas atributos válidos, que não sejam coleções, e não estejam na lista de exclusão
            filtered_data = {
                key: value
                for key, value in data.items()
                if key in entity_attributes
                and not isinstance(value, (list, dict, set, tuple))
                and key not in excluded_attributes
            }

            if not filtered_data:
                raise ValueError("Nenhum dado válido para atualização.")

            # Montar os campos para o SET dinamicamente
            set_clause = ', '.join([f"{key} = :{key}" for key in filtered_data.keys()])

            # Query genérica para atualização
            query = text(f"""
                UPDATE "{table_name}"
                SET {set_clause}
                WHERE id = :record_id
            """)

            with self.session_factory() as session:
                # Adicionar o ID do registro ao conjunto de dados
                filtered_data["record_id"] = record_id

                # Executar a query de atualização
                result = session.execute(query, filtered_data)

                # Confirmar se a atualização afetou alguma linha
                updated = result.rowcount > 0
                session.commit()
                return updated

        except SQLAlchemyError as e:
            session.rollback()  # Reverte as alterações no banco em caso de erro
            raise RuntimeError(f"Erro ao atualizar no banco: {e}") from e
