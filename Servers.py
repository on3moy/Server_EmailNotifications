from sqlalchemy import create_engine, make_url, text # For SQL Connection
import pandas as pd # For Dataframe creation
from credentials import SQLUSERNAME, SQLPASSWORD # Credentials for SQL Server

# Function created to query ServerA server
def get_dataconnect_data(SQL_QUERY):
    '''
    Returns t query as a dataframe
    '''

    SERVER = 'ServerA'
    DATABASE = 'DataConnect'
    DRIVER = '{ODBC Driver 18 for SQL Server}'
    UID = f'{SQLUSERNAME}'
    PWD = '{' + f'{SQLPASSWORD}'+ '}'
    ENCRYPT = 'yes'
    MSSQL = f'mssql+pyodbc:///?odbc_connect='
    ODBC_STR = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};ENCRYPT={ENCRYPT};UID={UID};PWD={PWD}'
    CONN_STR = make_url(MSSQL +  ODBC_STR)
    ENGINE = create_engine(CONN_STR, echo=True)
    raw = pd.read_sql(text(SQL_QUERY), ENGINE.connect())
    return raw

# Function created to query carbon server from ServerB as a linked server
def get_ServerB_data(SQL_QUERY):
    '''
    Returns t query as a dataframe
    '''

    SERVER = 'ServerB.enrginc.com'
    DATABASE = 'Staging'
    DRIVER = '{ODBC Driver 18 for SQL Server}'
    ENCRYPT = 'no'
    MSSQL = f'mssql+pyodbc:///?odbc_connect='
    ODBC_STR = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};ENCRYPT={ENCRYPT};Trusted_Connection=yes'
    CONN_STR = make_url(MSSQL +  ODBC_STR)
    ENGINE = create_engine(CONN_STR, echo=True)
    raw = pd.read_sql(text(SQL_QUERY), ENGINE.connect())
    return raw

def insert_dataconnect(description='Python Script Fail Detection'):
    '''
    Inserts a log into DataConnect's AmazonDataValidationLog. Takes in a string comment and puts marks it as a 
    description within log table.
    '''

    SERVER = 'ServerA'
    DATABASE = 'DataConnect'
    DRIVER = '{ODBC Driver 18 for SQL Server}'
    UID = f'{SQLUSERNAME}'
    PWD = '{' + f'{SQLPASSWORD}'+ '}'
    ENCRYPT = 'yes'
    MSSQL = f'mssql+pyodbc:///?odbc_connect='
    ODBC_STR = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};ENCRYPT={ENCRYPT};UID={UID};PWD={PWD}'
    CONN_STR = make_url(MSSQL +  ODBC_STR)
    ENGINE = create_engine(CONN_STR, echo=True)
    SCHEMA = 'errors'
    TABLE = 'AmazonDataValidationLog'
    description = description
    AmazonDataValidationLog = {
        'Server': [SERVER]
        ,'Database': [DATABASE]
        ,'Schema': [SCHEMA]
        ,'Table': [TABLE]
        ,'Description': [description]
        ,'Datetime':[pd.Timestamp.today()]
        }
    INSERT = pd.DataFrame(data=AmazonDataValidationLog).to_sql(schema=SCHEMA, name=TABLE ,con=ENGINE, index=False, if_exists='append')
    return INSERT

if __name__ == '__main__':
    print('\n')
    print('Starting Connection Process')
    print('\n')
    print('Getting Carbons Max Date')
    # print(get_carbon_data())
    print('\n')
    print('Getting Dataconnects Max Date')
    # print(get_dataconnect_data())
    print('\n')
    print('Getting all errors')
    print(insert_dataconnect('TEST Insert'))
    print('\n')
    print('Ending Connection Process')