import sqlite3
import pandas as pd
import os

def run_analytics():
    db_path = 'data/ecommerce.db'
    if not os.path.exists(db_path):
        print("Database not found.")
        return

    conn = sqlite3.connect(db_path)
    
    queries = {
        "Revenue Overview": "SELECT COUNT(*) as transactions, SUM(total_amount) as revenue FROM transactions WHERE status = 'completed';",
        "Top 5 Cities": "SELECT city, SUM(total_amount) as revenue FROM transactions WHERE status = 'completed' GROUP BY city ORDER BY revenue DESC LIMIT 5;",
        "Top 5 Categories": "SELECT category, SUM(total_amount) as revenue FROM transactions WHERE status = 'completed' GROUP BY category ORDER BY revenue DESC LIMIT 5;"
    }
    
    print("# Analytics Report (Updated Data)\n")
    for name, query in queries.items():
        print(f"### {name}")
        df = pd.read_sql_query(query, conn)
        print(df.to_markdown(index=False))
        print("\n")
    
    conn.close()

if __name__ == "__main__":
    run_analytics()
