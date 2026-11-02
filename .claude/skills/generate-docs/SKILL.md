---
context: fork
allowed-tools: ["Read", "Write", "Glob"]
argument-hint: "Enter the main title of the project (e.g., E-Commerce Core Agent)"
---
# Documentation Generator Skill

Automatically generate or update a comprehensive, high-quality `README.md` file in the root of the project.

## Instructions
1. Use `Glob` to scan the project files (exclude `.venv` or temporary folders).
2. Use `Read` to analyze the core code:
   - `domain/models.py` (to understand catalog items and database structure).
   - `domain/services.py` (to understand business logic, refund limits, and payment rules).
   - `CLAUDE.md` (to understand project rules and commands).
3. Draft a professional `README.md` in the root of the project containing:
   - **Title:** Use the title provided in the user's argument.
   - **Overview:** A brief description of this e-commerce backend with AI capabilities.
   - **Project Structure:** A clean tree map of the files in the project.
   - **Business Domain Logic:** Clear explanation of models (catalog, orders) and core services (ordering, payment, and the $500 security refund limit).
   - **How to Run:** Quick guide on how to run commands using `uv`.
4. Save the generated documentation to `README.md` using `Write`.
5. Output a success message in the chat.