import psycopg2
from pgvector.psycopg2 import register_vector

def connect_to_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="3fz3f0h4",
        host="178.164.28.100", 
        # host="localhost",
        port="5432"
    )

def query_chunks(conn, limit=10):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM chunks_2024only LIMIT %s", (limit,))
        return cur.fetchall()

def query_embeddings(conn, limit=5):
    with conn.cursor() as cur:
        cur.execute("SELECT id, chunk_id, embedding[:5] FROM embeddings_2024only LIMIT %s", (limit,))
        return cur.fetchall()

def main():
    try:
        conn = connect_to_db()
        register_vector(conn)

        print("Querying chunks:")
        chunks = query_chunks(conn)
        for chunk in chunks:
            print(f"ID: {chunk[0]}, Content: {chunk[1][:100]}...")  # Print first 100 characters of content

        print("\nQuerying embeddings:")
        embeddings = query_embeddings(conn)
        for embedding in embeddings:
            print(f"ID: {embedding[0]}, Chunk ID: {embedding[1]}, Embedding (first 5 values): {embedding[2]}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# if name == "main":
#     main()

main()