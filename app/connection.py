import psycopg2

class Connection:
    
    # ==== DATABASE CONNECTION ====
    # Conexão ao banco de dados PostgreSQL
    def init_connection():
        try:
            print("Connection established")
            return psycopg2.connect(
                database="recipes_collection",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432",
                client_encoding="UTF8"
            )
        except Exception as e:
            print(f"Connection cannot be established: {e}")
            exit(1)  # Encerra o programa se a conexão falhar