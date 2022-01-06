#%%
#Kirjastot
import streamlit as st
#%%
import pandas as pd
import plotly.express as px
from pyjstat import pyjstat
#%%
#Statfin-haku funktio
def SFhaku(URL):
    jsondata = pyjstat.Dataset.read(URL)
    df =jsondata.write('dataframe')
    return(df)
#%% TK 
# Asuntotuotanto
#Valmistuneet asunnot käyttötarkoituksen mukaan, liukuva vuosisumma 
VA_DF =SFhaku('https://pxnet2.stat.fi:443/PXWeb/sq/52fcfd4e-db48-487f-8529-fad589819176')
VA_DF['Vuosi']=VA_DF.Kuukausi.str.slice(0,4)
VA_DF['Vuosi']=VA_DF['Vuosi'].astype(int)
VA_DF=VA_DF[(VA_DF['Vuosi']>1999)]
VA_DF=VA_DF[(VA_DF["Tiedot"]=='Asunnot (kpl), liukuva vuosisumma')]
VA_DF=VA_DF.rename(columns = {'value':'Asunnot (kpl), liukuva vuosisumma'})
Fig_VA_DF= px.line(VA_DF, x='Kuukausi', y='Asunnot (kpl), liukuva vuosisumma', color='Käyttötarkoitus')
Fig_VA_DF.update_layout(
    title='Valmistuneet asunnot, liukuva vuosisumma (Tilastokeskus)',
    plot_bgcolor="white")
Fig_VA_DF.update_xaxes(showline=True, linecolor='grey')
Fig_VA_DF.update_yaxes(showline=True, linecolor='grey')    

#Valmistuneet asunnot kuukausittain yhteensä
VA_DF_yht=SFhaku('https://pxnet2.stat.fi:443/PXWeb/sq/87982d1e-61ab-4635-9e4e-f0443f96350d')
VA_DF_yht=VA_DF_yht[(VA_DF_yht["Rakennusvaihe"]=='Valmistuneet rakennushankkeet')]
#Lasketaan likuva keskiarvo
VA_DF_yht['Liukuva keskiarvo 12kk']=VA_DF_yht.value.rolling(12, min_periods=1).mean()
VA_DF_yht['Liukuva keskiarvo 12kk']=VA_DF_yht['Liukuva keskiarvo 12kk'].astype(int)
VA_DF_yht['Vuosi']=VA_DF_yht.Kuukausi.str.slice(0,4)
VA_DF_yht['Vuosi']=VA_DF_yht['Vuosi'].astype(int)
VA_DF_yht=VA_DF_yht[(VA_DF_yht['Vuosi']>1999)]
VA_DF_yht=VA_DF_yht.rename(columns = {'value':'Asunnot (kpl)'})
#Tehdään kuvio
Fig_VA_DF_yht=px.line(VA_DF_yht, x='Kuukausi',y= ['Asunnot (kpl)','Liukuva keskiarvo 12kk'])
Fig_VA_DF_yht.update_layout(
    title='Valmistuneet asunnot kuukausittain (Tilastokeskus)',
    yaxis_title='Asunnot (kpl)',
    legend_title='Arvo',
    plot_bgcolor="white"
)
Fig_VA_DF_yht.update_xaxes(showline=True, linecolor='grey')
Fig_VA_DF_yht.update_yaxes(showline=True, linecolor='grey')
#%%
#Hinnat ja vuokrat
#Hintaindeksi
HI_DF=SFhaku('https://pxnet2.stat.fi:443/PXWeb/sq/04087e49-670e-4a5e-a062-d548a2fcdc45')
HI_DF=HI_DF.rename(columns ={'value': 'Indeksi (2015=100)'})
Fig_HI_DF=px.line(HI_DF, x='Kuukausi', y='Indeksi (2015=100)', color='Alue')
Fig_HI_DF.update_layout(
    title='Vanhojen osakeasuntojen hintaindeksi (Tilastokeskus)',
    yaxis_title='Indeksi (2015=100)',
    legend_title='Alue',
    plot_bgcolor="white"
)
Fig_HI_DF.update_xaxes(showline=True, linecolor='grey')
Fig_HI_DF.update_yaxes(showline=True, linecolor='grey')
#%%
#Vuokraindeksi
VI_DF=SFhaku('https://pxnet2.stat.fi:443/PXWeb/sq/e67d5de5-8579-4705-aaab-1cbfc7b67804')
VI_DF=VI_DF.rename(columns ={'value': 'Indeksi (2015=100)'})
Fig_VI_DF=px.line(VI_DF, x='Vuosineljännes', y='Indeksi (2015=100)', color='Alue')
Fig_VI_DF.update_layout(
    title='Vuokraindeksi (Tilastokeskus)',
    legend_title='Alue',
    plot_bgcolor="white"
)
Fig_VI_DF.update_xaxes(showline=True, linecolor='grey')
Fig_VI_DF.update_yaxes(showline=True, linecolor='grey')
#%%
print(VI_DF)
#%%
#Ulkoasu
st.set_page_config(
     page_title="Asumisen ja rakentamisen tilannekuva V0.1",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help'
     }
 )

st.title('Asumisen ja rakentamisen yleiskuva v0.1')
st.text('Laajenna kuvio klikkaamalla oikeasta yläkulmasta.')
st.markdown('[Tilastokeskuksen tiedot Statfin-tietokannasta](https://pxnet2.stat.fi/PXWeb/pxweb/fi/StatFin/)')
col1, col2 = st.columns(2)
with col1:
    st.subheader("Hinnat ja vuokrat")
    st.plotly_chart(Fig_HI_DF, use_container_width=True)
    st.plotly_chart(Fig_VI_DF, use_container_width=True)
with col2:
    st.subheader("Asuntotuotanto")
    st.plotly_chart(Fig_VA_DF, use_container_width=True)
    st.plotly_chart(Fig_VA_DF_yht, use_container_width=True)

#Kela scrape
#http://raportit.kela.fi/linkki/39070756

#Kartat
#https://towardsdatascience.com/lets-make-a-map-using-geopandas-pandas-and-matplotlib-to-make-a-chloropleth-map-dddc31c1983d

#st.dataframe(data=VA_DF)



