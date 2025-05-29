**Task:** Convert raw documentation into:
1. OpenAPI 3.0 YAML 
2. Database models in tables
3. Request/response examples in Markdown

**Hint**
1. Before using the final `/response <>` command to end the dialog, you may use interface commands

**Steps:**
1. List all endpoints 
2. Design request/response models and entities
3. Write OpenAPI documentation
4. Add endpoint logic descriptions in Markdown docs
5. Always use special commands to save documentation:
   - `/openapi <OpenAPI 3.0 YAML>`
   - `/docs <Markdown>`

**Rules:**
- All names → snake_case
- If information is missing → create a minimal example

**Final Message Output Format:**
```
--- EXECUTE ---
/openapi <openapi: 3.0.3
info:
  title: Example
  version: 1.0.0
paths:
  /hello:
    get:
      summary: Greeting
      responses:
        '200':
          description: Successful response
          content:
            text/plain:
              example: "Hello world!">
/docs <# Basic Hello World Service>
--- END EXECUTE ---
```

**Process this documentation:**
===
%|user_docs|%
===
