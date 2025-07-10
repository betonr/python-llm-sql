from sqlalchemy import create_engine

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding 
from llama_index.core import SQLDatabase
from llama_index.core.indices.struct_store import NLSQLTableQueryEngine

# ---------- build the NL → SQL engine ------------------------
def build_query_engine():
    table_desc = {
        "sales": (
            "Sales table. Each row represents a sale made by an attendant. "
            "Fields: id (int), attendant_id (int), amount (float), sale_date (date)."
        ),
        "attendants": (
            "Store attendants table. Each attendant has an id and a name. "
            "Fields: id (int), name (str)."
        )
    }
        
    engine = create_engine("postgresql://postgres:password@localhost:5432/sales_db")
    sql_db = SQLDatabase(
        engine, 
        include_tables=["attendants", "sales"], 
        custom_table_info=table_desc
    )

    llm = Ollama(
        model="sqlcoder:7b",  # or :15b, :q3_K_M etc.
        temperature=0,
        system_prompt=(
            "You are an SQL expert. Always respond using standard SQL compatible with SQLite. "
            "Use ORDER BY + LIMIT 1 for questions about most/least. "
            "Explain the answer based on the query results. "
            "Avoid irrelevant columns and simplify the language."
        ),
        request_timeout=180
    )

    embed_model = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url="http://localhost:11434",
        request_timeout=180
    )

    examples = [
        ("Who sold the most today?", 
        "SELECT a.name, SUM(s.amount) AS total "
        "FROM sales s JOIN attendants a ON s.attendant_id = a.id "
        "WHERE s.sale_date = CURRENT_DATE "
        "GROUP BY a.name ORDER BY total DESC LIMIT 1;"),
        ("Who sold the least today?",
        "SELECT a.name, SUM(s.amount) AS total "
        "FROM sales s JOIN attendants a ON s.attendant_id = a.id "
        "WHERE s.sale_date = CURRENT_DATE "
        "GROUP BY a.name ORDER BY total ASC LIMIT 1;")
    ]

    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_db,
        tables=["sales", "attendants"],
        llm=llm,
        embed_model=embed_model,
        verbose=True,
        examples=examples
    )

    return query_engine
