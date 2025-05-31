### Terminal Gateway Interface
**Command Syntax:**  
`command.terminal.execute_command <YOUR_COMMAND>`

#### Processing Rules:
1. **Command Extraction**  
   - Example: `command.terminal.execute_command <ls -l>` → executes `ls -l`

2. **Security:**
   - Automatic blocking of:
     ```bash
     # Blacklisted patterns
     rm -rf /          # Recursive deletion
     chmod 777 /       # System permissions modification
     |dd|mkfs|fdisk    # Disk operations
     |sudo|su          # Privilege escalation
     /etc/passwd       # Access to system files
     >/dev/            # Device writing
     :(){:|:&};:       # Fork bombs
     ```