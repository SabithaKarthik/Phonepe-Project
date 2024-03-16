from Extract import all_df
import psycopg2
from sql_queries import queries

#files paths
agg_usr_path = 'C:/Users/kallai Karthi/Videos/Project/phonepe/pulse/data/aggregated/user/country/india/state/'
agg_tran_path = 'C:/Users/kallai Karthi/Videos/Project/phonepe/pulse/data/aggregated/transaction/country/india/state/'
map_tran_path = 'C:/Users/kallai Karthi/Videos/Project/phonepe/pulse/data/map/transaction/hover/country/india/state'
map_usr_path = 'C:/Users/kallai Karthi/Videos/Project/phonepe/pulse/data/map/user/hover/country/india/state'
top_usr_path = 'C:/Users/kallai Karthi/Videos/Project/phonepe/pulse/data/top/user/country/india/state'
top_trans_path = 'C:/Users/kallai Karthi/Videos/Project/phonepe/pulse/data/top/transaction/country/india/state'

agg_trans_df, agg_usr_df, map_trans_df, map_usr_df,top_trans_df,top_usr_df=all_df(agg_tran_path,agg_usr_path,map_tran_path,map_usr_path,top_trans_path,top_usr_path)

def createTables(access,client):
    for query in queries:
        access.execute(query)
        client.commit()

def insertData(access,client):
    for index,row in agg_trans_df.iterrows():
        query='''INSERT INTO aggregated_transaction (State,Year,Quarter,Transaction_Method,Transaction_Count,Transaction_Amount)
                values(%s,%s,%s,%s,%s,%s)'''
        values=(row['State'],row['Year'],row['Quarter'],row['Transaction_method'],row['Transaction_Count'],row['Transaction_Amount'])
        access.execute(query,values)
        client.commit()
    for index,row in agg_usr_df.iterrows():
        query='''INSERT INTO aggregated_user (State,Year,Quarter,Device_Brand,Brand_count,Percentage)
                values(%s,%s,%s,%s,%s,%s)'''
        values=(row['State'],row['Year'],row['Quarter'],row['Device_Brand'],row['Brand_count'],row['Percentage'])
        access.execute(query,values)
        client.commit()
    for index,row in map_trans_df.iterrows():
        query='''INSERT INTO map_transaction (State,Year,Quarter,District,Transaction_Count,Transaction_Amount)
                values(%s,%s,%s,%s,%s,%s)'''
        values=(row['State'],row['Year'],row['Quarter'],row['District'],row['Transaction_Count'],row['Transaction_Amount'])
        access.execute(query,values)
        client.commit()
    for index,row in map_usr_df.iterrows():
        query='''INSERT INTO map_user (State,Year,Quarter,District,Registered_Users,AppOpens)
                values(%s,%s,%s,%s,%s,%s)'''
        values=(row['State'],row['Year'],row['Quarter'],row['District'],row['Registered_Users'],row['AppOpens'])
        access.execute(query,values)
        client.commit()
    for index,row in top_trans_df.iterrows():
        query='''INSERT INTO top_transaction (State,Year,Quarter,District,Transaction_Count,Transaction_Amount)
                values(%s,%s,%s,%s,%s,%s)'''
        values=(row['State'],row['Year'],row['Quarter'],row['District'],row['Transaction_Count'],row['Transaction_Amount'])
        access.execute(query,values)
        client.commit()
    for index,row in top_usr_df.iterrows():
        query='''INSERT INTO top_user (State,Year,Quarter,District,Registered_Users)
                values(%s,%s,%s,%s,%s)'''
        values=(row['State'],row['Year'],row['Quarter'],row['District'],row['Registered_Users'])
        access.execute(query,values)
        client.commit()
    
def insertIntoSql():
    client=psycopg2.connect(host='localhost',user='postgres',password='12345',database='phonepe',port=5432)
    access=client.cursor()
    createTables(access,client)
    insertData(access,client)
    access.close()
    client.close()
    
try:
    insertIntoSql()
    print('Successfully inserted')
except Exception as e:
    print(e)
