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
- ✅ MySQL
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
$ uv run manager.py create --db-type mongo --connection-string "mongodb://root:root@localhost/" --username test123 --password test123

```
### Step 2: Create a Database User

Run the following command to create a database user:

```bash
$ uv run manager.py create --db-type mongo --connection-string "mongodb://root:root@localhost/" --username test123 --password test123
```

#### Output
```bash
Connection string: mongodb://test123:test123@localhost:27017
```

This creates both the `test123` user and the `db_test123` database, giving the user full access to this database. 

**For a certain `username` we always create `db_username`.**

### Step 3: Verify the Database User

Run the following command to verify the database user:

```bash
uv run manager.py verify --db-type mongo --connection-string mongodb://test123:test123@localhost:27017
```

# Using in a Docker Swarm environment

### Step 1: Verify Database Network
First, ensure there exists an attachable overlay network for databases:

```bash
$ docker network ls | grep db_network
fvlfdi58ebdbi   db_network        overlay   swarm
```

The network should be created as an attachable overlay network if it doesn't exist:

```bash
docker network create --driver overlay --attachable db_network
```

This network enables DNS resolution for database services using names like:
- `mongo` for MongoDB
- `mysql` for MySQL
- `postgresql` for PostgreSQL

### Step 2: Build the Image
Build the database manager image:

```bash
docker build -t database-manager:0.1.1 .
```

### Step 3: Verify Connectivity
Test the connection to your database service:

```bash
$ docker run --rm --network db_network database-manager:0.1.1 verify \
    --db-type mongo \
    --connection-string mongodb://root:root@mongo/
✓ Connection successful!
```

### Step 4: Create Database Users
Create users and databases with the following command:

```bash
docker run --rm --network db_network database-manager:0.1.1 create \
    --db-type mongo \
    --connection-string mongodb://root:root@mongo/ \
    --username appuser \
    --password mypassword
```

