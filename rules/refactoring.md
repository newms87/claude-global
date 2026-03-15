# Refactoring Rules

## CRITICAL: Use Language-Specific Refactoring Tools

**Never manually rename/move classes, methods, or symbols across a codebase.** Use the appropriate refactoring tool for the language. These tools update all references automatically — manual find-and-replace is error-prone and wastes time.

### PHP: phpactor

**Binary:** `~/.config/composer/vendor/bin/phpactor`

**Class move/rename (updates namespace, class declaration, and all references):**
```bash
phpactor class:move app/Old/Path/MyClass.php app/New/Path/MyClass.php
```

**Move entire directory (bulk namespace move):**
```bash
phpactor class:move app/Old/Directory/ app/New/Directory/
```

**Known quirk:** When moving a class back to its original namespace, phpactor may add a redundant same-namespace `use` statement. The Pint hook cleans this up automatically.

### Other Languages

Use equivalent tools when available:
- **TypeScript/JavaScript:** IDE refactoring or `ts-morph` for programmatic renames
- **Go:** `gorename`, `gopls rename`
- **Rust:** `rust-analyzer` rename
- **Python:** `rope`, `jedi`

### When to Use Refactoring Tools

- Renaming a class, method, function, or variable used across multiple files
- Moving a class to a different namespace/directory
- Renaming a directory that represents a namespace
- Any operation where references in other files must be updated to match

### When NOT to Use Refactoring Tools

- Renaming a local variable within a single function (just use Edit)
- Simple string replacements that aren't code symbols (use batch-editor)
- Renaming files that have no cross-file references
