from databases.mongodb_strategy import MongoDBStrategy

def main():
    # Prompt the user for input.
    db_type = input("Enter the database type (mongo, mysql, postgresql): ").strip().lower()
    username = input("Enter the username: ").strip()
    user_password = input("Enter the user password: ").strip()

    # Factory for selecting the proper database strategy.
    strategies = {
        "mongo": MongoDBStrategy(),
    }

    if db_type not in strategies:
        print("Invalid database type selected. Please choose from 'mongo'")
        return

    strategy = strategies[db_type]

    # Create user and corresponding database (or update privileges if already exists).
    strategy.create_user_and_db(username, user_password)

    # Generate and display the connection string.
    connection_string = strategy.get_connection_string(username, user_password)
    print(f"Connection string: {connection_string}")

if __name__ == "__main__":
    main()
