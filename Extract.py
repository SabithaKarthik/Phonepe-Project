import os
import pandas as pd
from pathlib import Path

#aggregate Transaction
class agg_trans:
    def __init__(self,agg_trans_path):
        self.agg_trans_path=agg_trans_path
        self.agg_trans_data=pd.DataFrame({})
    
    def agg_Transaction(self,state,year,quarter,file):
        aggT_df=pd.read_json(file)
        for i in aggT_df['data']['transactionData']:
            rows={"Transaction_method":i['name'],"Transaction_Count":i['paymentInstruments'][0]['count'],"Transaction_Amount":i['paymentInstruments'][0]['amount'],"State":state,"Year":year,"Quarter":quarter}
            df_rows=pd.DataFrame.from_dict([rows])
            self.agg_trans_data=pd.concat([self.agg_trans_data,df_rows])
            self.agg_trans_data['Transaction_Amount']= self.agg_trans_data['Transaction_Amount'].apply(lambda x:int(x))
        self.agg_trans_data.reset_index(drop=True,inplace=True)
        
    def extractData(self):
        for state in os.listdir(self.agg_trans_path):
            statePath=os.path.join(self.agg_trans_path,state)
            for year in os.listdir(statePath):
                yearPath=os.path.join(statePath,year)
                for file in os.listdir(yearPath):
                    filePath=os.path.join(yearPath,file)
                    quarter=file.strip('.json')
                    self.agg_Transaction(state,year,quarter,filePath)
        return self.agg_trans_data

#aggregate User
class agg_usr:
    def __init__(self,agg_usr_path):
        self.agg_usr_path=agg_usr_path
        self.agg_usr_data=pd.DataFrame({})
    
    def agg_user(self,state,year,quarter,filePath):
        aggU_df=pd.read_json(filePath)
        usr_df=aggU_df['data']['usersByDevice']
        if usr_df:
            for i in usr_df:
                rows={'Device_Brand':i['brand'],'Brand_count':i['count'],'Percentage':i['percentage'],'State':state,'Year':year,'Quarter':quarter}
                df_rows=pd.DataFrame.from_dict([rows])
                self.agg_usr_data=pd.concat([self.agg_usr_data,df_rows])
            self.agg_usr_data.reset_index(drop=True,inplace=True)
    
    def extractData(self):
        for state in os.listdir(self.agg_usr_path):
            statePath=os.path.join(self.agg_usr_path,state)
            for year in os.listdir(statePath):
                yearPath=os.path.join(statePath,year)
                for file in os.listdir(yearPath):
                    filePath=os.path.join(yearPath,file)
                    quarter=file.strip('.json')
                    self.agg_user(state,year,quarter,filePath)
        return self.agg_usr_data

#map transaction
class map_trans:
    def __init__(self,map_trans_path):
        self.map_trans_path=map_trans_path
        self.map_trans_data=pd.DataFrame({})
    
    def map_Transaction(self,state,year,quarter,file):
        df=pd.read_json(file)
        df_hover=df['data']['hoverDataList']
        if df_hover:
            for i in df_hover:
                rows={'District':i['name'],'Transaction_Count':i['metric'][0]['count'],'Transaction_Amount':i['metric'][0]['amount'],'State':state,'Year':year,'Quarter':quarter}
                df_rows=pd.DataFrame.from_dict([rows])
                self.map_trans_data=pd.concat([self.map_trans_data,df_rows])
                self.map_trans_data['Transaction_Amount']= self.map_trans_data['Transaction_Amount'].apply(lambda x:int(x))
            self.map_trans_data.reset_index(drop=True,inplace=True)
            
    def extractData(self):
        for state in os.listdir(self.map_trans_path):
            statePath=os.path.join(self.map_trans_path,state)
            for year in os.listdir(statePath):
                yearPath=os.path.join(statePath,year)
                for file in os.listdir(yearPath):
                    filePath=os.path.join(yearPath,file)
                    quarter=file.strip('.json')
                    self.map_Transaction(state,year,quarter,filePath)
        return self.map_trans_data

#map user
class map_usr:
    def __init__(self,map_usr_path):
        self.map_usr_path=map_usr_path
        self.map_usr_data=pd.DataFrame({})
    
    def map_user(self,state,year,quarter,filePath):
        df=pd.read_json(filePath)
        usr_df=df['data']['hoverData']
        if usr_df:
            for i in usr_df:
                rows={'District':i,'Registered_Users':usr_df[i]['registeredUsers'],'AppOpens':usr_df[i]['appOpens'],'State':state,'Year':year,'Quarter':quarter}
                df_rows=pd.DataFrame.from_dict([rows])
                self.map_usr_data=pd.concat([self.map_usr_data,df_rows])
            self.map_usr_data.reset_index(drop=True,inplace=True)
    
    def extractData(self):
        for state in os.listdir(self.map_usr_path):
            statePath=os.path.join(self.map_usr_path,state)
            for year in os.listdir(statePath):
                yearPath=os.path.join(statePath,year)
                for file in os.listdir(yearPath):
                    filePath=os.path.join(yearPath,file)
                    quarter=file.strip('.json')
                    self.map_user(state,year,quarter,filePath)
        return self.map_usr_data

#top transaction
class top_trans:
    def __init__(self,top_trans_path):
        self.top_trans_path=top_trans_path
        self.top_trans_data=pd.DataFrame({})
    
    def top_transaction(self,state,year,quarter,filePath):
        df=pd.read_json(filePath)
        df_hover=df['data']['districts']
        if df_hover:
            for i in df_hover:
                rows={'District':i['entityName'],'Transaction_Count':i['metric']['count'],'Transaction_Amount':i['metric']['amount'],'State':state,'Year':year,'Quarter':quarter}
                df_rows=pd.DataFrame.from_dict([rows])
                self.top_trans_data=pd.concat([self.top_trans_data,df_rows])
                self.top_trans_data['Transaction_Amount']= self.top_trans_data['Transaction_Amount'].apply(lambda x:int(x))
            self.top_trans_data.reset_index(drop=True,inplace=True)
            
    def extractData(self):
        for state in os.listdir(self.top_trans_path):
            statePath=os.path.join(self.top_trans_path,state)
            for year in os.listdir(statePath):
                yearPath=os.path.join(statePath,year)
                for file in os.listdir(yearPath):
                    filePath=os.path.join(yearPath,file)
                    quarter=file.strip('.json')
                    self.top_transaction(state,year,quarter,filePath)
        return self.top_trans_data

#top user
class top_usr:
    def __init__(self,top_usr_path):
        self.top_usr_path=top_usr_path
        self.top_usr_data=pd.DataFrame({})
    
    def top_user(self,state,year,quarter,filePath):
        df=pd.read_json(filePath)
        usr_df=df['data']['districts']
        if usr_df:
            for i in usr_df:
                rows={'District':i['name'],'Registered_Users':i['registeredUsers'],'State':state,'Year':year,'Quarter':quarter}
                df_rows=pd.DataFrame.from_dict([rows])
                self.top_usr_data=pd.concat([self.top_usr_data,df_rows])
            self.top_usr_data.reset_index(drop=True,inplace=True)
    
    def extractData(self):
        for state in os.listdir(self.top_usr_path):
            statePath=os.path.join(self.top_usr_path,state)
            for year in os.listdir(statePath):
                yearPath=os.path.join(statePath,year)
                for file in os.listdir(yearPath):
                    filePath=os.path.join(yearPath,file)
                    quarter=file.strip('.json')
                    self.top_user(state,year,quarter,filePath)
        return self.top_usr_data

def cleanData(df):
    df["State"] = df["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    df['State'] = df['State'].str.replace("dadra-&-nagar-haveli-&-daman-&-diu", "Dadra and Nagar Haveli and Daman and Diu")
    df["State"] = df["State"].str.replace("-"," ")
    df["State"] = df["State"].str.title()
    if 'District' in df.columns:
        df["District"] = df["District"].str.replace("-"," ")
        df["District"] = df["District"].str.title()

def all_df(agg_tran_path,agg_usr_path,map_trans_path,map_usr_path,top_trans_path,top_usr_path):
    a = agg_trans(agg_tran_path)
    agg_trans_df = a.extractData()
    cleanData(agg_trans_df)
    b = agg_usr(agg_usr_path)
    agg_usr_df = b.extractData()
    cleanData(agg_usr_df)
    c = map_trans(map_trans_path)
    map_trans_df = c.extractData()
    cleanData(map_trans_df)
    d = map_usr(map_usr_path)
    map_usr_df = d.extractData()
    cleanData(map_usr_df)
    e = top_trans(top_trans_path)
    top_trans_df = e.extractData()
    cleanData(top_trans_df)
    f = top_usr(top_usr_path)
    top_usr_df = f.extractData()
    cleanData(top_usr_df)
    return agg_trans_df, agg_usr_df, map_trans_df, map_usr_df,top_trans_df,top_usr_df
