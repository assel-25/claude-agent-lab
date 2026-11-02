---
context: fork
allowed-tools: ["Read", "Grep", "Glob"]
argument-hint: "Enter the directory name to audit (e.g. domain)"
---
# Audit Directory Skill

Perform a structured code-quality and architectural audit of the directory provided in the user's argument.

## Instructions
1. Use `Glob` or `Grep` to find all Python files inside the directory specified by the user in the argument.
2. Read their contents.
3. Check the code for the following architectural violations:
   - Are there any hardcoded values that should be in models/config?
   - Are error responses properly formatted according to the Domain Services Error Handling Standard (returning success, errorCategory, isRetryable)?
   - Are database state modifications safe?
4. Present your findings as a clean Markdown report with sections: "Issues Found", "Design Violations", and "Recommended Fixes". Do not modify any files.