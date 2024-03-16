
agg_trans='''CREATE TABLE if not exists aggregated_transaction (State varchar(50),
                                                                Year int,
                                                                Quarter int,
                                                                Transaction_Method varchar(50),
                                                                Transaction_Count bigint,
                                                                Transaction_Amount bigint
                                                                )'''

agg_usr='''CREATE TABLE if not exists aggregated_user (State varchar(50),
                                                                Year int,
                                                                Quarter int,
                                                                Device_Brand varchar(50),
                                                                Brand_count bigint,
                                                                Percentage float
                                                                )'''
                                                                
map_trans='''CREATE TABLE if not exists map_transaction (State varchar(50),
                                                                Year int,
                                                                Quarter int,
                                                                District varchar(50),
                                                                Transaction_Count bigint,
                                                                Transaction_Amount float)'''

map_usr='''CREATE TABLE if not exists map_user (State varchar(50),
                                                        Year int,
                                                        Quarter int,
                                                        District varchar(50),
                                                        Registered_Users bigint,
                                                        AppOpens bigint)'''
                                                        
top_trans='''CREATE TABLE if not exists top_transaction (State varchar(50),
                                                                Year int,
                                                                Quarter int,
                                                                District varchar(50),
                                                                Transaction_Count bigint,
                                                                Transaction_Amount bigint)'''

top_usr='''CREATE TABLE if not exists top_user (State varchar(50),
                                                        Year int,
                                                        Quarter int,
                                                        District varchar(50),
                                                        Registered_Users bigint
                                                        )'''

queries=[agg_trans,agg_usr,map_trans,map_usr,top_trans,top_usr]