**Task:** Convert raw documentation into:
1. OpenAPI 3.0 YAML 
2. Database models in tables
3. Request/response examples in Markdown


**Steps:**
1. List all endpoints 
2. Design request/response models and entities
3. Write OpenAPI documentation
4. Add endpoint logic descriptions in Markdown docs
5. Always use special commands to save documentation:
   - `command.openapi <OpenAPI 3.0 YAML>`
   - `command.markdown <Markdown>`


**Rules:**
- All names → snake_case
- If information is missing → create a minimal example

**Final Message Output Format:**
```
command.openapi <openapi: 3.0.3
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
command.markdown <# Basic Hello World Service>
```

**Process this documentation:**
===
%|user_docs|%
===
