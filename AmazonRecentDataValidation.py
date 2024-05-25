import pandas as pd # For Dataframe creation
from SendEmail import send_email # Sends email
from Servers import get_CEPHX01BI1_data, get_dataconnect_data, insert_dataconnect # Connects to servers to get data.

# Global variables
NOWDATE = f'{pd.Timestamp.today().year}{pd.Timestamp.today().month:02d}{pd.Timestamp.today().day:02d}'
LOGFILENAME = 'AmazonValidationLogFile'
SENDER = 'PythonBIServer-noreply@somecompany.com'
TODAY = pd.Timestamp.date(pd.Timestamp.today())

# Query to get max carbon txn date
AmazonComDataSQLQuery = '''
    SELECT MAX(TxnDateTime) AS [MaxDate]
    FROM [amazon].[ComDataTxn]
'''

# Query to get max date from carbon server
CarbonComdataSQLQuery = '''
    SELECT MAX(TxnDateTime) AS [MaxDate]
    FROM [CARBONSQLDB].[DataXfer].[dbo].[vComdataReview]
    '''

# Query to check volume descrepencies
VolumeCheckSQLQuery = '''
	SELECT [Alert], [AlertMessage], [AlertDateTime]
	FROM [Staging].[validation].[comdatavolumecheck]
	WHERE [AlertDateTime] = (
		SELECT MAX([AlertDateTime])
		FROM [Staging].[validation].[comdatavolumecheck]
    )
'''
# Query to check most recent excel file date
ComDataEmailCheck = '''
	SELECT
		MAX([CreateDate]) AS [MaxCreateDate]
	FROM [CARBONSQLDB].[DataXfer].[dbo].[vComdataReview]
'''

# DataConnect Variables
DataConnectMaxDate = pd.Timestamp.date(get_dataconnect_data(AmazonComDataSQLQuery).iloc[0,0])
DataconnectPreviousDate = pd.Timestamp.date(TODAY - pd.DateOffset(days=1))
DataconnectDaysDiff = (TODAY - DataConnectMaxDate).days
DataconnectMatches = DataConnectMaxDate == TODAY or DataConnectMaxDate == DataconnectPreviousDate

# ComData Variables
ComDataEmailMaxDate = pd.Timestamp.date(get_CEPHX01BI1_data(ComDataEmailCheck).iloc[0,0])
ComDataEmailDaysDiff = (TODAY - ComDataEmailMaxDate).days

# Carbon Data Variables
CarbonMaxDate = pd.Timestamp.date(get_CEPHX01BI1_data(CarbonComdataSQLQuery).iloc[0,0])
CarbonPreviousDate = pd.Timestamp.date(TODAY - pd.DateOffset(days=1))
CarbonDaysDiff = (TODAY - CarbonMaxDate).days
CarbonMatches = CarbonMaxDate == TODAY or CarbonMaxDate == CarbonPreviousDate

# Carbon Data Volume Variables
volume_check_df = get_CEPHX01BI1_data(VolumeCheckSQLQuery)
ALERT = volume_check_df.loc[0,'Alert']
ALERT_MESSAGE = volume_check_df.loc[0,'AlertMessage']
ALERT_DATE = volume_check_df.loc[0,'AlertDateTime']

# Message Variables
MESSAGE_PASS = f'''
	Daily Email!

	[amazon].[ComDataTxn] has the most recent transactions.

	Amazon's latest transaction date: {DataConnectMaxDate}.
	Volume Alert Message: {ALERT_MESSAGE}.
	Volume Alert Date: {ALERT_DATE}.
	ComData latest create date: {ComDataEmailMaxDate}

	---
	Automated Python Generated Email Hosted on ServerA.
	---
	Source Data
	Server: ServerB
	Database: Dataconnect
	---
	Purpose of this email is to notify you when Amazon's transactions are not recent.
	Email Schedule: 9:15 AM & 7:00 PM Daily
	'''
MESSAGE_FAIL = f'''
	Daily Email!

	[amazon].[ComDataTxn] does not have the most recent transactions and Carbon Does!

		- Check Stored Procedure spLoadAmazonComDataToDataCONNECT on ServerA to confirm no issues.

	Amazon's latest transaction date: {DataConnectMaxDate}.
	Number of days off: {DataconnectDaysDiff}
	vComdataReview latest transaction date: {CarbonMaxDate}
	ComData latest create date: {ComDataEmailMaxDate}
	Volume Alert Message: {ALERT_MESSAGE}.
	Volume Alert Date: {ALERT_DATE}.
	---
	Automated Python Generated Email Hosted on ServerA.
	---
	Source Data
	Server: ServerB
	Database: Dataconnect
	---
	Purpose of this email is to notify you when Amazon's transactions are not recent.
	Email Schedule: 9:15 AM & 7:00 PM Daily
	'''
MESSAGE_FAIL_CARBON = f'''
	Daily Email!

		- [amazon].[ComDataTxn] does not have the most recent transactions.
		- [CARBONSQLDB].[DataXfer].[dbo].[vComdataReview] does not have the most recent transactions.

	Ted, please investigate comdata on your end!

	Amazon's latest transaction date: {DataConnectMaxDate}.
	Number of days off: {DataconnectDaysDiff}
	vComdataReview latest transaction date: {CarbonMaxDate}
	Number of days off: {CarbonDaysDiff}
	ComData latest create date: {ComDataEmailMaxDate}
	Volume Alert Message: {ALERT_MESSAGE}.
	Volume Alert Date: {ALERT_DATE}.

	Thank you!
	---
	Automated Python Generated Email Hosted on ServerA.
	---
	Source Data
	Server1: ServerB
	Database1: Dataconnect
	Server2: CARBONSQLDB
	Database2: DataXfer
	---
	Purpose of this email is to notify you when Amazon's transactions are not recent.
	Email Schedule: 9:15 AM & 7:00 PM Daily
	'''
MESSAGE_FAIL_CARBON_VOLUME = f'''
	Daily Email!

		- Most Recent data on Carbonsqldb.D365.dbo.ComdataReview has Volume Discrepancies!

	Ted, please investigate comdata on your end!

	Amazon's latest transaction date: {DataConnectMaxDate}.
	Number of days off: {DataconnectDaysDiff}
	vComdataReview latest transaction date: {CarbonMaxDate}
	Number of days off: {CarbonDaysDiff}
	Volume Alert Message: {ALERT_MESSAGE}.
	Volume Alert Date: {ALERT_DATE}.
	ComData latest create date: {ComDataEmailMaxDate}
	
	Thank you!
	---
	Automated Python Generated Email Hosted on ServerA.
	---
	Source Data
	Server1: ServerB
	Database1: Dataconnect
	Server2: CARBONSQLDB
	Database2: DataXfer
	---
	Purpose of this email is to notify you when Amazon's transactions are not recent.
	Email Schedule: 9:15 AM & 7:00 PM Daily
	'''

MESSAGE_FAIL_COMDATA = f'''
	Daily Email!

		- Recent Daily Email from Comdata is missing.

	Ted, please investigate comdata on your end!

	Amazon's latest transaction date: {DataConnectMaxDate}.
	Number of days off: {DataconnectDaysDiff}
	vComdataReview latest transaction date: {CarbonMaxDate}
	Number of days off: {CarbonDaysDiff}
	Volume Alert Message: {ALERT_MESSAGE}.
	Volume Alert Date: {ALERT_DATE}.
	ComData latest create date: {ComDataEmailMaxDate}
	
	Thank you!
	---
	Automated Python Generated Email Hosted on ServerA.
	---
	Source Data
	Server1: ServerB
	Database1: Dataconnect
	Server2: CARBONSQLDB
	Database2: DataXfer
	---
	Purpose of this email is to notify you when Amazon's transactions are not recent.
	Email Schedule: 9:15 AM & 7:00 PM Daily
	'''

# Creates a Log file with comments as input
def logfile(text):
	'''
	Takes a comment or text and add a datetime stamp on it
	'''
	comment = str(text)
	with open(LOGFILENAME + ".log", mode='a') as log:
		log.write(f'{comment}: {pd.Timestamp.today()}')
		log.write('\n')

def main(test=False):
	'''
	Runs SQL Query to see whether Amazon data has current data
	'''
	if test == True:
		recipient = ['moy.patel@company.com']
	else:
		recipient = ['moy.patel@company.com', 'justin.carlisto@company.com', 'randy.curran@company.com', 'ted.baskin@company.com']
	# Check if Comdata has recent data from emails
	if ComDataEmailDaysDiff >= 1:
		logfile(f'Error: Daily Comdata Email Fail')
		subject = 'Amazon Data Pipeline Refresh Validation | Fail'
		send_email(sender=SENDER, recipient=recipient, subject=subject, message=MESSAGE_FAIL_COMDATA)
		insert_dataconnect('Error: Daily Comdata Email Fail')
	else:
		# Check if DataConnect has recent Data.
		if DataconnectMatches:
			logfile('Info: Passed')
			subject = 'Amazon Data Pipeline Refresh Validation | Pass'
			send_email(sender=SENDER, recipient=recipient, subject=subject, message=MESSAGE_PASS)
		else:
			# If Dataconnect does not have recent data, check carbon to see if it has recent data.
			subject = 'Amazon Data Pipeline Refresh Validation | Fail'
			recipient = ['moy.patel@company.com', 'justin.carlisto@company.com', 'randy.curran@company.com', 'ted.baskin@company.com','mike.tewksbury@company.com']
			if CarbonMatches:
				logfile(f'Error: DataConnect Fail')
				send_email(sender=SENDER, recipient=recipient, subject=subject, message=MESSAGE_FAIL)
				insert_dataconnect('Error: DataConnect Fail')
			else:
				logfile(f'Critical: Carbon Fail')
				send_email(sender=SENDER, recipient=recipient, subject=subject, message=MESSAGE_FAIL_CARBON)
				insert_dataconnect('Critical: Carbon Fail')
		if ALERT == 'True':
			subject = 'Amazon Data Pipeline Refresh Validation | Fail'
			recipient = ['moy.patel@company.com', 'justin.carlisto@company.com', 'randy.curran@company.com', 'ted.baskin@company.com','mike.tewksbury@company.com']
			logfile(f'Critical: Carbon Volume Discrepancy')
			send_email(sender=SENDER, recipient=recipient, subject=subject, message=MESSAGE_FAIL_CARBON_VOLUME)
			insert_dataconnect('Critical: Carbon Volume Discrepancy')

if __name__ == '__main__':
	main(True)