# Python Email Notification Work Project

## Details
This project connects to multiple servers and runs queries for data validation. If there is a flag, an email will be sent out to notify stake holders.

## Flags
1. There is a volume discrepancy of more than 10%
2. Data pipeline does not show recent transactions

## How to run this
These scripts live on any computer/server and uses Window's Task Scheduler to Activate a .bat file we created on a certain frequency.

### Libraries used
- pandas
- SQLAlchemy
- pyodbc
- smtplib