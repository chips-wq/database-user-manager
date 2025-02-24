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

### Step 1: Install `uv` Python Package Manager

First, install `uv` python package manager and then add it to PATH by following instructions.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Sample Output
```bash
downloading uv 0.6.2 x86_64-unknown-linux-gnu
no checksums to verify
installing to /root/.local/bin
  uv
  uvx
everything's installed!

To add $HOME/.local/bin to your PATH, either restart your shell or run:

    source $HOME/.local/bin/env (sh, bash, zsh)
    source $HOME/.local/bin/env.fish (fish)
WARNING: The following commands are shadowed by other commands in your PATH: uv uvx
```

### Step 2: Create a Database User

Run the following command to create a database user:

```bash
uv run manager.py create --db-type mongo --connection-string "mongodb://root:root@localhost/" --username test123 --password test123
```

#### Output
```bash
Connection string: mongodb://test123:test123@localhost:27017
```

### Step 3: Verify the Database User

Run the following command to verify the database user:

```bash
uv run manager.py verify --db-type mongo --connection-string mongodb://test123:test123@localhost:27017
```