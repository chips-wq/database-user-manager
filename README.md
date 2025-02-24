# Summary
This utility can be expressed as a mathematical function:

$$f: (D, A, U, P) \rightarrow S$$

Where:
- $D \in \{\text{mongo}, \text{mysql}, \text{postgresql}\}$ (database type)
- $A$ is the admin connection string
- $U$ is the username to create
- $P$ is the password for the user
- $S$ is the resulting connection string for your `.env`

# Database Manager

A command-line utility for idempotent database user and access management.

## Key Features

- ✨ **Idempotent Operations**: Safely ensure users and permissions exist
- 🔐 **Secure Credentials**: Hidden password prompts with confirmation
- 🔄 **Multiple Database Support**: Strategy pattern for database implementations
- 🤖 **Automated Setup**: One command to create users, databases, and permissions

## Supported Databases

- ✅ MongoDB
- 🔄 MySQL (coming soon)
- 🔄 PostgreSQL (coming soon)

## Usage

```bash
uv run main.py --db-type mongo --connection-string "mongodb://root:root@localhost/" --username test123 --password test123
```

Or use the interactive mode:

```bash
uv run main.py
```