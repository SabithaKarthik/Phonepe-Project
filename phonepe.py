import json
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from db import pay_df,trans_df,user_df

def mcrores(number):
            return '₹'+'{:,.0f} Cr'.format(round(number / 10000000))
        
def formated(number):
    number_str = str(number)
    length = len(number_str)
    formatted_number = ""
    comma_counter = 0
    for i in range(length - 1, -1, -1):
        formatted_number = number_str[i] + formatted_number
        comma_counter += 1
        if comma_counter == 2 and i != 0:
            formatted_number = "," + formatted_number
            comma_counter = 0
        elif comma_counter == 3 and i != 0:
            formatted_number = "," + formatted_number
            comma_counter = 0
    return formatted_number

st.set_page_config(layout='wide')
c1,c2=st.columns([8,4])
col1,col2=st.columns([8,4])
with st.container():
    original_title = '''<p style="font-weight: bold; color:Green; font-size: 30px;text-align: center">
    ₹PhonePe Pulse Data Analysis</p>'''
    c1.markdown(original_title,unsafe_allow_html=True)
    option=["**Explore Data**", "**Insights**"]
    #c2.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;}</style>', unsafe_allow_html=True)
    tabs = c2.radio("Select", option,format_func=lambda x: x,horizontal=True,label_visibility="hidden")
    
with st.container():
    if tabs=="**Explore Data**":
        c1,c2,c3=col1.columns(3)
        selectType=c1.selectbox("Mode",("Transactions", "Users"))
        year=c2.selectbox("Year",("2018", "2019","2020","2021","2022","2023"))
        quarter=c3.selectbox("Quarter",("1", "2","3","4"))
        
        if selectType == "Transactions":
            ## Transaction button data
            pay_map = pay_df.copy()
            map_df = pay_map.loc[(pay_map['Quarter']==int(quarter)) & (pay_map['Year']==int(year))]
            map_df1 = map_df.groupby('State').agg({'TransactionCount':'sum','TransactionAmount':'sum'}).reset_index()
            fst = map_df1.copy()
            
            fst['All Transactions'] = fst['TransactionCount'].apply(lambda x: round(x)).apply(lambda x: formated(x))
            fst['Total Payment Values'] = fst['TransactionAmount'].apply(lambda x: round(x)).apply(lambda x: mcrores(x))
            fst['Avg.Transaction Value'] = fst['TransactionAmount'] / fst['TransactionCount']
            fst['Avg.Transaction Value'] = fst['Avg.Transaction Value'].apply(lambda x: round(x)).apply(lambda x: "₹{:,.0f}".format(x))
            ## Transaction map
            url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response= requests.get(url)
            india_states= json.loads(response.content)
            states_name_tra= [feature["properties"]["ST_NM"] for feature in india_states["features"]]
            states_name_tra.sort()
            fig1 = px.choropleth(
                fst,
                locations="State",
                geojson=india_states,
                featureidkey= "properties.ST_NM",
                color="TransactionAmount",
                range_color= (fst["TransactionAmount"].min(),fst["TransactionAmount"].max()),
                hover_name="State",
                hover_data={'All Transactions':True,'Total Payment Values':True,'Avg.Transaction Value':True,'TransactionAmount':False},
                title=f"PhonePe Amounts Transactions in Q {quarter}-{year}",
                color_continuous_scale='Blues', width=800, height=800
            )
            fig1.update_geos(fitbounds="locations", visible=False,projection_type="orthographic")
            col1.plotly_chart(fig1)
            with col2:
                ### Transaction values
                tr = trans_df.copy()
                filter_tr = tr.loc[(tr['Year']==int(year)) & (tr['Quarter']==int(quarter))]
                gr_tr = filter_tr.groupby('Year').sum()
                All_transactions = gr_tr['TransactionCount'].to_list()[0]
                Total_payments =gr_tr['TransactionAmount'] 
                Total_payments1 =gr_tr['TransactionAmount'].to_list()[0]
                def format_number(number):
                    return "{:,}".format(number)
                atl = format_number(All_transactions)
                Avg_Transaction = round(Total_payments1/All_transactions)
                av_form = '₹{:,}'.format(Avg_Transaction)
                # Set the locale to Indian English
                sf1 = Total_payments.apply(lambda x: "₹" + "{:,.0f}".format(x/10000000) + "Cr")
                trvalue1 = sf1.to_list()[0] # ***Total payments 
                st.write(f'#### {selectType}')
                st.write('#### :green[All Transactions (UPI+Cards+Wallets)]')
                st.write(f'#### {atl}')## values
                st.write('')
                
                #payments method groupby
                at = pay_df.copy()
                atr = at.loc[(at['Year']==int(year)) & (at['Quarter']==int(quarter))]
                atr1 = atr.groupby(['Year', 'TransactionMethod']).sum()
                df1a = atr1.reset_index().sort_values(by='TransactionCount', ascending=False).reset_index(drop=True).drop(['Year', 'Quarter', 'TransactionAmount'], axis=1)

                df1a = pd.concat([df1a[df1a['TransactionMethod']!='Others'], df1a[df1a['TransactionMethod']=='Others']]).reset_index(drop=True)
                df1a['TransactionCount'] = df1a['TransactionCount'].apply(lambda x: format_number(x))# this will be dataframe that inserted into
                df1a = df1a.reset_index(drop=True)
                df1a.index += 1
                
                rc1,rc2 = st.columns([1,1])
                with rc1:
                    st.write('##### :green[Total payment value]')
                    st.write(f'#### {trvalue1}')## values
                with rc2:
                    st.write('##### :green[Avg.transaction value]')
                    st.write(f'#### {av_form}')## values
                st.markdown('<hr>', unsafe_allow_html=True)
                st.subheader('Categories')
                #st.dataframe(df1a, width=800,use_container_width=True)
                #st.table(df1a.style.set_table_attributes("style='height:1000000%;'"))
                fc1,fc2 = st.columns([1.3,0.45])
                with fc1:
                    mrch = df1a['TransactionMethod'][1]
                    st.write(f'#### :green[{mrch}]')
                    st.write('')
                    peer = df1a['TransactionMethod'][2]
                    st.write(f'#### :green[{peer}]')
                    st.write('')
                    rech = df1a['TransactionMethod'][3]
                    st.write(f'#### :green[{rech}]')
                    st.write('')
                    fin = df1a['TransactionMethod'][4]
                    st.write(f'#### :green[{fin}]')
                    st.write('')
                    oth = df1a['TransactionMethod'][5]
                    st.write(f'#### :green[{oth}]')
                with fc2:
                    val1 = df1a['TransactionCount'][1]
                    st.write(f'#### {val1}')
                    st.write('')
                    val2 = df1a['TransactionCount'][2]
                    st.write(f'#### {val2}')
                    st.write('')
                    val3 = df1a['TransactionCount'][3]
                    st.write(f'#### {val3}')
                    st.write('')
                    
                    val4 = df1a['TransactionCount'][4]
                    st.write(f'#### {val4}')
                    st.write('')
                    
                    val5 = df1a['TransactionCount'][5]
                    st.write(f'#### {val5}')
        elif selectType == "Users":
            ## User button data
            ur_df = user_df.copy()
            map_df2 = ur_df.loc[(ur_df['Quarter']==int(quarter)) & (ur_df['Year']==int(year))].sort_values(by='State') 
            map_df2['AppOpens'] = map_df2['AppOpens'].astype(float)

            map_df3 = map_df2.groupby('State').agg({'RegisteredUser':'sum','AppOpens':'sum'}).reset_index()
            map_df3['Registered User'] = map_df3['RegisteredUser'].apply(lambda x: formated(round(x)) if pd.notnull(x) else '')
            map_df3['App Opens'] = map_df3['AppOpens'].apply(lambda x: formated(round(x)) if pd.notnull(x) else '')
            snd = map_df3.copy()
            ## User map
            url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response= requests.get(url)
            india_states= json.loads(response.content)
            states_name_tra= [feature["properties"]["ST_NM"] for feature in india_states["features"]]
            states_name_tra.sort()
            fig1 = px.choropleth(
                snd,
                locations="State",
                geojson=india_states,
                featureidkey= "properties.ST_NM",
                color="RegisteredUser",
                range_color= (snd["RegisteredUser"].min(),snd["RegisteredUser"].max()),
                hover_name="State",
                hover_data={'Registered User':True,'App Opens':True,'RegisteredUser':False},
                title=f"PhonePe Total Users in Q {quarter}-{year}",
                color_continuous_scale='Blues', width=800, height=800
            )
            fig1.update_geos(fitbounds="locations", visible=False,projection_type="orthographic")
            col1.plotly_chart(fig1)
            with col2:
                ### User values
                def format_number1(number):
                    number_str = "{:,.0f}".format(number)
                    return number_str.replace(",", ",")

                ur = user_df.copy()
                ur['AppOpens'] = ur['AppOpens'].astype(float)
                filter_ur = ur.loc[(ur['Year']==int(year)) & (ur['Quarter']==int(quarter))]
                gr_ur = filter_ur.groupby('Year').sum()
                Registered_users = gr_ur['RegisteredUser'].to_list()[0] #****Registered users****
                reg_usr = format_number1(Registered_users)
                App_opens = int(gr_ur['AppOpens'].to_list()[0]) #****App opens****
                app_on = format_number1(App_opens)

                ## Top 10 values
                a = user_df.copy()
                def crores(number):
                    return '{:.2f}Cr'.format(number / 10000000)
                #Top 10 district
                filter_ds = a.loc[(a['Year']==int(year)) & (a['Quarter']==int(quarter))]
                pin_d = filter_ds.groupby(['Year','District']).sum().reset_index()
                top_10_dist = pin_d.nlargest(10, 'RegisteredUser')[['District', 'RegisteredUser']]
                df_d = top_10_dist.copy()
                df_d['District'] = df_d['District'].apply(lambda x: x.title())
                df_d['RegisteredUser'] = df_d['RegisteredUser'].apply(lambda x: crores(x)) # top 10 districts
                df_d = df_d.reset_index(drop=True)
                df_d.index += 1
                #-----
                #Top 10 states
                filter_st = a.loc[(a['Year']==int(year)) & (a['Quarter']==int(quarter))]
                pin_s = filter_st.groupby(['Year','State']).sum().reset_index()
                top_10_sts = pin_s.nlargest(10, 'RegisteredUser')[['State', 'RegisteredUser']]
                df_s = top_10_sts.copy()
                df_s['State'] = df_s['State'].apply(lambda x: x.title())
                df_s['RegisteredUser'] = df_s['RegisteredUser'].apply(lambda x: crores(x)) # top 10 states
                df_s = df_s.reset_index(drop=True)
                df_s.index += 1
                
                st.write(f'#### {selectType}')
                st.subheader(f":green[Registered Users Till Q{quarter}-{year}] ")
                st.write(f'#### {reg_usr}')## values
                st.write('')
                st.subheader(f':green[ App Opens in Q{quarter}-{year}]')
                st.write(f'#### {app_on}')## values
                st.markdown('<hr>', unsafe_allow_html=True)
                tb10 = st.selectbox('', ('Top 10 States','Top 10 Districts'),key='top10')
                if tb10 == 'Top 10 Districts':
                    st.dataframe(df_d, width=800)
                elif tb10 == 'Top 10 States':
                    st.dataframe(df_s, width=800)
            
    else:
        st.subheader("Some intersting facts about Phonepe")
        questions=st.selectbox("Questions: ", ["Please select one",
                                        "The year which has the most no of Transactions?",
                                        "The most prominent payment type of Phonepe across years",
                                        "A district who loves the phonepe app the most",
                                        "An effective payment method during the Covid-19 Lockdown period(2019-2020)",
                                        "The Quarter which tops the transaction list very often across years",
                                        "The Quarter which tops the transaction value list very often across years",
                                        "The State which has most the PhonePe Registered users All time",
                                        "The year which recorded most no of Appopens across India",
                                        "The year which recorded highest no of Registered users across India",
                                        "The States which were unaware about Phonepe"])
        if (questions=="Please select one"):
            st.text("Please Choose any one Query")
        elif(questions=="The year which has the most no of Transactions?"):
            df=pay_df.loc[:,['Year','TransactionCount']]
            df1=df.groupby('Year').sum()
            df1=df1.reset_index()
            df1["Year"]=df1["Year"].astype(str)
            fig=px.bar(df1,x="Year",y="TransactionCount",width=600)
            st.plotly_chart(fig)
            st.success("2023 has the most no of Transactions so far")
        elif(questions=="The most prominent payment type of Phonepe across years"):
            df=pay_df.loc[:,['TransactionAmount','TransactionMethod']]
            df1=df.groupby('TransactionMethod').sum() 
            df1=df1.reset_index()
            fig=px.bar(df1,x="TransactionMethod",y="TransactionAmount",labels={"TransactionMethod":"Category"},width=600)
            st.plotly_chart(fig)
            st.success("Peer to Peer payments was the most prominent Payment type across people over Years")
        elif(questions=="A district who loves the phonepe app the most"):
            df=trans_df.loc[:,['District','TransactionCount']]
            df1=df.groupby('District').sum() 
            df1=df1.reset_index()
            df1=df1.sort_values(by=['TransactionCount'],ascending=False).head(5)
            fig=px.bar(df1,x="District",y="TransactionCount",width=600)
            st.plotly_chart(fig)
            st.success("bengularu Urban made the most use of PhonePe very often")
        elif(questions=="An effective payment method during the Covid-19 Lockdown period(2019-2020)"):
            df=pay_df[(pay_df.Year==2019)|(pay_df.Year==2020)]
            df=df.loc[:,['TransactionMethod','TransactionAmount']]
            df1=df.groupby('TransactionMethod').sum()
            df1=df1.reset_index()
            fig=px.bar(df1,x="TransactionMethod",y="TransactionAmount",labels={"TransactionMethod":"Category"},width=600)
            st.plotly_chart(fig)
            st.success("Peer to Peer payments was the most prominent Payment type during Covid-19")
        elif(questions=="The Quarter which tops the transaction list very often across years"):
            df=pay_df.loc[:,['TransactionCount','Quarter']]
            df1=df.groupby(['Quarter']).sum()
            df1=df1.reset_index()
            df1["Quarter"]=df1["Quarter"].astype(str)
            fig=px.bar(df1,x="Quarter",y="TransactionCount",width=600)
            st.plotly_chart(fig)
            st.success("Fourth Quarter tops in the transaction list")
        elif(questions=="The Quarter which tops the transaction value list very often across years"):
            df=pay_df.loc[:,['TransactionAmount','Quarter']]
            df1=df.groupby(['Quarter']).sum()
            df1=df1.reset_index()
            df1["Quarter"]=df1["Quarter"].astype(str)
            fig=px.bar(df1,x="Quarter",y="TransactionAmount",width=600)
            st.plotly_chart(fig)
            st.success("Fourth Quarter tops in the transaction value")
        elif(questions=="The State which has most the PhonePe Registered users All time"):
            df=user_df.loc[:,['State','RegisteredUser']]
            df1=df.groupby('State').sum() 
            df1=df1.reset_index()
            df1=df1.sort_values(by=['RegisteredUser'],ascending=False).head(5)
            fig=px.bar(df1,x="State",y="RegisteredUser",width=600)
            st.plotly_chart(fig)
            st.success("Maharastra has more phonepe users than other state in INDIA.")
        elif(questions=="The year which recorded most no of Appopens across India"):
            df=user_df.loc[:,['Year','AppOpens']]
            df1=df.groupby('Year').sum() 
            df1=df1.reset_index()
            df1["Year"]=df1["Year"].astype(str)
            fig=px.bar(df1,x="Year",y="AppOpens",width=600)
            st.plotly_chart(fig)
            st.success("Current year(2023) wins the chart with even a quarter less to its tally")
        elif(questions=="The year which recorded highest no of Registered users across India"):
            df=user_df.loc[:,['Year','RegisteredUser']]
            df1=df.groupby('Year').sum() 
            df1=df1.reset_index()
            df1["Year"]=df1["Year"].astype(str)
            fig=px.bar(df1,x="Year",y="RegisteredUser",width=600)
            st.plotly_chart(fig)
            st.success("Current year(2023) had more success among other years")
        elif(questions=="The States which were unaware about Phonepe"):
            df=user_df.loc[:,['State','AppOpens']]
            df1=df.groupby('State').sum() 
            df1=df1.reset_index()
            df1=df1.sort_values(by=['AppOpens'],ascending=True).head(5)
            fig=px.bar(df1,x="State",y="AppOpens",width=600)
            st.plotly_chart(fig)
            st.success("Lakshadeep island are unfamiliar about Phonepe in INDIA.")