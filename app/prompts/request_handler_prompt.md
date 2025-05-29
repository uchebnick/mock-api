```markdown
**Task:** Process the HTTP request and return a response according to:
1. *OpenAPI 3.0 YAML docs* - ```%|openapi|%```
2. *Markdown docs* - ```%|docs|%```

**Hint**
1. Before using the final `/response <>` command to end the dialog, you may use interface commands

**Steps:**
1. Find the corresponding endpoint in *OpenAPI 3.0 YAML docs*
2. Check the request format; if it doesn't match, return a 400 error
3. If it matches, review the endpoint logic in *Markdown docs*
4. Use the obtained data to process the request
5. Form a response according to *OpenAPI 3.0 YAML docs*
6. Always return the response using the `/response <JSON_RESPONSE>` command

**Final Message Output Format:**
```
--- EXECUTE ---
/response <{"ok": true, "msg": "hello world"}>
--- END EXECUTE ---
```

**Process this request:**
===
%|request|%
===
```