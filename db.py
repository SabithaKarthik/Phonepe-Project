
import pandas as pd
import psycopg2

client=psycopg2.connect(host='localhost',user='postgres',password='12345',database='phonepe',port=5432)
access=client.cursor()

access.execute("select * from aggregated_transaction")
pay=access.fetchall()
pay_df=pd.DataFrame(pay,columns=("State","Year","Quarter","TransactionMethod","TransactionCount","TransactionAmount"))

access.execute("select * from map_transaction")
trans=access.fetchall()
trans_df=pd.DataFrame(trans,columns=("State","Year","Quarter","District","TransactionCount","TransactionAmount"))

access.execute("select * from map_user")
user=access.fetchall()
user_df=pd.DataFrame(user,columns=("State","Year","Quarter","District","RegisteredUser","AppOpens"))
