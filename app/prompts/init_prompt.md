# Task: API Initialization
Initialize core API components including storage, database, and documentation of [user_docs].

## Critical Execution Order
1. **ALL interface commands** (storage setup, DB configuration, etc.)  
   MUST be executed BEFORE documentation commands
   
2. **Final documentation commands** (termination triggers):  
   ```
   command.openapi <YAML_OPENAPI_DOCS>
   command.markdown <MARKDOWN_DOCS>
   ```
   - Must be executed LAST
   - Dialog terminates automatically upon success

## Mandatory Documentation Commands
- `command.openapi`: Submit complete OpenAPI spec in YAML format
- `command.markdown`: Submit full system documentation in Markdown

## Workflow Requirements
1. Execute ALL preparation commands first:
   - Storage initialization
   - Database configuration
   - System bootstrapping
   - Any other setup operations
   
2. ONLY AFTER successful preparation:
   Submit both documentation commands:
   ```
   command.openapi <your_yaml_here>
   command.markdown <your_markdown_here>
   ```

## Termination Rules
- Dialog ends IMMEDIATELY after successful execution of BOTH documentation commands
- Documentation becomes available for all subsequent dialogs

## Constraints
- Standard command format: single parameter per command
- Parallel execution allowed EXCEPT for documentation commands (must be final step)

### Key Features:
1. **Explicit Order Enforcement**  
   - Clear "BEFORE/AFTER" terminology for command sequencing
   - Documentation commands explicitly marked as FINAL step

2. **Workflow Safeguards**  
   - Prevents mixed-phase command execution
   - Ensures system is fully configured before documentation submission

## **IMPORTANT**
   - Make sure to follow the [format]
   - Parameter of command must be between <>
   - Openapi and markdown documentation should describe the api by [user_docs]
   - You must respond only with a functional text

# **Api should perform the functionality according to this raw [user_docs]:**
===
%|user_docs|%
===
