from table import Table

database= []
database_running = True

def isRunning():
    return database_running
def exitDatabase():
    database_running=False