### Text Storage Interface
**Purpose:** Text storage for storing specific data or dynamic configs

#### Commands:
1. **Clear Storage**  
   `command.text_storage.clear`  
   - Resets storage to empty state
   - This command has no input parameters.

2. **Add Text**  
   `command.text_storage.add_text <TEXT_CONTENT>`  
   - Appends content with automatic newline
   - Supports multiline text

3. **Retrieve Text**  
   `command.text_storage.get_text`  
   - Returns full content
   - This command has no input parameters

#### Processing Rules:
- **Text Encoding:** UTF-8
- **Line Handling:**  
  - Automatic `\n` appended per `/add_text` call
  - Trailing newline preserved in storage


#### Storage Specifications:
- **Persistence:** Survives container restarts
