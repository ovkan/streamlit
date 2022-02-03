#Kirjastot
import plotly.express as px
import streamlit as st
import pandas as pd
from pyjstat import pyjstat
import plotly.graph_objects as go 

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
#Asuinolot
AO_DF=SFhaku('https://pxnet2.stat.fi:443/PXWeb/sq/15911bc7-eb59-4fce-bde5-f3e57e7425f9')
#Asuntokunnan keskikoko
kk=round(AO_DF['value'][1]/AO_DF['value'][0],2)
t=AO_DF['Vuosi'][0]
#%%
AO_DF2=SFhaku('https://pxnet2.stat.fi:443/PXWeb/sq/385143c3-93ae-4803-9f2f-47da51e932e0')
#AO_DF2
#%%
#Tunnuslukujen muutokset
Delta_ph=round(AO_DF2['value'][7]-AO_DF2['value'][6],2)
Delta_pa=round(AO_DF2['value'][5]-AO_DF2['value'][4],2)
Delta_av=int(AO_DF2['value'][1]-AO_DF2['value'][0])
Delta_kk=round(AO_DF2['value'][3]/AO_DF2['value'][1]-AO_DF2['value'][2]/AO_DF2['value'][0],2)

#Sankey
#Asuntokunnat ja asuntoväestö muuttujina Vuosi, Tiedot, Alue, Huoneiden lkm keittiö pl. ja Hallintaperuste
HH_DF=SFhaku('https://pxnet2.stat.fi:443/PXWeb/sq/26fe9793-08b0-4849-8268-232532d32693')
#HH_DF   
#%%
# override gray link colors with 'source' colors
fig_HH = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 5,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["Omistusasunnot", "Vuokra-asunnot", "1h", "2h", "3h", "4h+"],
      color = ["#80D4FF","#FF8080","#E6FFCC","#D9FFB3","#CCFF99","#B3FF66"]
    ),
    link = dict(
      source = [0, 0, 0, 0, 1, 1, 1, 1], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = [2, 3, 4, 5, 2, 3, 4, 5],
      value = [HH_DF['value'][0], HH_DF['value'][2],HH_DF['value'][4],HH_DF['value'][6],
      HH_DF['value'][1], HH_DF['value'][3],HH_DF['value'][5],HH_DF['value'][7]
      ],
      color =['#a6cee3', '#a6cee3','#a6cee3', '#a6cee3','#fb9a99','#fb9a99','#fb9a99','#fb9a99']
  ))])

fig_HH.update_layout(title_text="Vuokra- ja omistusasunnot huoneluvun mukaan (Tilastokeskus)",font_size=15)
#fig
fig_HH.update_layout(margin_b=40, margin_t=40, margin_l=0, margin_r=80)
fig_HH.update_layout(title_font_size=18)


#%%
#Ulkoasu
st.set_page_config(
     page_title="Asumisen ja rakentamisen yleiskuva",
     layout="wide"
)
st.title('Asumisen ja rakentamisen yleiskuva')
st.markdown('[Tilastokeskuksen tiedot Statfin-tietokannasta](https://pxnet2.stat.fi/PXWeb/pxweb/fi/StatFin/)')
st.text('TK:n tietoja visualisoiva epävirallinen harrasteprojekti, twitter @OttoKannisto')
st.header("Suhdannetiedot")
st.subheader("Asuntotuotanto")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(Fig_VA_DF, use_container_width=True) 
with col2:
    st.plotly_chart(Fig_VA_DF_yht, use_container_width=True)
st.subheader("Hinnat ja vuokrat")
col1, col2 = st.columns(2)  
with col1:      
    st.plotly_chart(Fig_VI_DF, use_container_width=True)
with col2:  
    st.plotly_chart(Fig_HI_DF, use_container_width=True) 

st.header("Vuositiedot")
st.subheader("Tunnuslukuja "+t+" ja muutos edellisvuodesta (Tilastokeskus)")
col1,col2,col3, col4=st.columns(4)
with col1:
    st.metric(label="Pinta-ala/asuntokunta, m2", value=AO_DF['value'][2], delta=Delta_pa)
with col2:
    st.metric(label="Pinta-ala/henkilö, m2", value=AO_DF['value'][3], delta=Delta_ph)
with col3:
    st.metric(label="Asuntokuntia", value=int(AO_DF['value'][0]), delta=Delta_av)
with col4:   
    st.metric(label="Asuntokunnan keskikoko", value=kk, delta=Delta_kk)
with st.container():
    st.plotly_chart(fig_HH, use_container_widht=True) 


