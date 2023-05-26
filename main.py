from db import InMemoryDatabase

db = InMemoryDatabase()

def print_available_commands():
    print("Available commands:")
    print(" BEGIN: Open a new transaction block")
    print(" COMMIT: Close all open transaction blocks")
    print(" ROLLBACK: Undo all of the commands issued in the most recent transaction block")
    print(" SET [key] [value]: Set the variable name to the value value.")
    print(" GET [key]: Print out the value of the variable name")
    print(" UNSET [key]: Unset the variable name,")
    print(" NUMEQUALTO [value]: Print out the number of variables that are currently set to value")
    print(" END: Exit the program")

def process_command(command):
    tokens = command.split()
    if tokens[0] == 'BEGIN':
        db.begin_transaction()
    elif tokens[0] == 'COMMIT':
        db.commit_transaction()
    elif tokens[0] == 'ROLLBACK':
        db.rollback_transaction()
    elif tokens[0] == 'SET':
        db.set_record(tokens[1], tokens[2])
    elif tokens[0] == 'GET':
        print(db.get_record(tokens[1]))
    elif tokens[0] == 'UNSET':
        db.delete_record(tokens[1])
    elif tokens[0] == 'NUMEQUALTO':
        print(db.get_value_count(tokens[1]))
    elif tokens[0] == 'END':
        raise EndProcessException
    else:
        print("Invalid command")

class EndProcessException(Exception):
    pass

print_available_commands()
while True:
    try:
        command = input("> ")
        process_command(command)
    except EndProcessException:
        break