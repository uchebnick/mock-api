### Text Storage Interface
**Purpose:** Persistent text storage for complex API workflows  

#### Commands:
1. **Clear Storage**  
   `/text_storage.clear`  
   - Resets storage to empty state

2. **Add Text**  
   `/text_storage.add_text TEXT_CONTENT`  
   - Appends content with automatic newline
   - Supports multiline text

3. **Retrieve Text**  
   `/text_storage.get_text`  
   - Returns full content

#### Processing Rules:
- **Text Encoding:** UTF-8
- **Line Handling:**  
  - Automatic `\n` appended per `/add_text` call
  - Trailing newline preserved in storage


#### Storage Specifications:
- **Persistence:** Survives container restarts
