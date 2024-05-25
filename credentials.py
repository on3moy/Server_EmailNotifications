import os

# With this method you can store your credentials in a .env file (Which is highly not recommended)

# Read the .env file and assign the values to your os environment temporarily
with open('.env', 'r') as file:
    for line in file.readlines():
        os.environ[line.split('=')[0]] = line.split('=')[1].strip('\n')

# Print Out the values
print(os.getenv('sqlusername'))
print(os.getenv('sqlpassword'))

# Store the values into variables for later use
SQLUSERNAME = os.getenv('sqlusername')
SQLPASSWORD = os.getenv('sqlpassword')

'''
Note - The best way to store credentials locally is to store them manually into your system variables and note inside
a .env file.
'''