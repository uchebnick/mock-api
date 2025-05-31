# DB Interface
**Command Syntax:**  
`command.db.execute_query <SQLITE_QUERY>`

#### Processing Rules:
1. **Query Extraction**  
   - Example: `command.db.execute_query <SELECT * FROM users;>` → executes `SELECT * FROM users`

2. **Database Context:**
   - Automatic connection handling
   - Supports all SQLite3 features:
     - Transactions (`BEGIN`, `COMMIT`)
     - Schema modifications (`CREATE TABLE`, `ALTER TABLE`)
     - Complex queries (`JOIN`, `WITH RECURSIVE`)
     - JSON1 extension