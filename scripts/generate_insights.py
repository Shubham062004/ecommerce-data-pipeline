import sqlite3
import pandas as pd
import os

def run_production_queries():
    db_path = 'data/ecommerce.db'
    sql_path = 'sql/queries.sql'
    
    if not os.path.exists(db_path):
        print("Error: Database not found. Please run the pipeline first.")
        return
    
    if not os.path.exists(sql_path):
        print("Error: SQL file not found.")
        return

    conn = sqlite3.connect(db_path)
    
    with open(sql_path, 'r') as f:
        sql_content = f.read()
    
    # Split queries by semicolon, filtering out empty strings and comments
    queries = [q.strip() for q in sql_content.split(';') if q.strip()]
    
    query_titles = [
        "1. Total Revenue Overview",
        "2. Revenue by City",
        "3. Top Customers (Lifetime Value)",
        "4. Customer Rank within City (Advanced)"
    ]

    print("# E-Commerce Business Insights Report")
    print(f"*Generated from updated production data (100 records)*\n")

    for i, query in enumerate(queries):
        if i < len(query_titles):
            print(f"### {query_titles[i]}")
        else:
            print(f"### Query {i+1}")
            
        try:
            df = pd.read_sql_query(query, conn)
            print(df.to_markdown(index=False))
        except Exception as e:
            print(f"Error running query: {e}")
        print("\n" + "-"*50 + "\n")
    
    conn.close()

if __name__ == "__main__":
    run_production_queries()
