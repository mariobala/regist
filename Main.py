import streamlit as st
import geopandas as gpd
import pandas as pd
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import folium
import geopandas as gpd
import branca.colormap as cm
import os
import geocoder
from fiona.drvsupport import supported_drivers
from shapely.geometry import Point
import time
from PIL import Image
import googlemaps
import shapely.wkt

class Main(object):

    def __init__(self):
        st.set_page_config(layout='wide', 
                            page_title='Buscador de endereço',
                            initial_sidebar_state='auto')
        
        supported_drivers['LIBKML'] = 'rw'

        if 'ENDERECO' not in st.session_state:
            st.session_state['ENDERECO'] = ''

        if 'ENDERECO_MULTIPLOS' not in st.session_state:
            st.session_state['ENDERECO_MULTIPLOS'] = []

        if 'BASE_ENDERECOS' not in st.session_state:
            st.session_state['BASE_ENDERECOS'] = []

    def carregar_estilo(self):

        endereco_completo = os.getcwd() + "\\Estilos\\Estilo.css"
        with open(endereco_completo) as f:
            st.markdown("<script>document.getElementById('styles').disable=true;</script>", unsafe_allow_html=True)
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    @st.cache_resource
    def carregar_poligonos(_self):
        mapa = gpd.read_file(os.getcwd() + "\\Dados\\CACHOEIRINHA ZONAS.kml")
        mapa["geometry"] = mapa["geometry"].apply(lambda x: shapely.wkt.loads(shapely.wkt.dumps(x, rounding_precision=4)))
        return mapa
    
    def salvar_dados(self, dados):

        try:
            dados.to_csv(os.getcwd() + "\\Dados\\base_dados.csv", 
                         index=False,
                         mode='a',
                         header=not os.path.exists(os.getcwd() + "\\Dados\\base_dados.csv"))
        except:
            pass

    @st.cache_resource
    def carregar_dados(_self, tempo):

        dados = pd.read_csv(os.getcwd() + "\\Dados\\base_dados.csv")
        return dados.drop_duplicates()
    
    @st.cache_resource
    def verificador_endereco(_self, endereco, _mapa):

        endereco_ajustado = ''
        resultado = ''
        ponto = None
        mapa_ = _mapa.copy()
        fronteira = False

        fronteiras = ['frederico augusto ritter',
                      'ary rosa dos santos',
                      'capitão garibaldi pinto dos santos',
                      'azaléia',
                      'silvério manoel da silva',
                      ' caí',
                      'missões',
                      'flores da Cunha']

        if ('cachoeirinha' not in endereco.lower()):
            endereco_ajustado = endereco + ",  cachoeirinha - RS"
        else:
            endereco_ajustado = endereco

        for front in fronteiras:
            if (front in endereco.lower()):
                fronteira = True
                break

        if (fronteira):
            try:
                gmaps = googlemaps.Client(key='AIzaSyA0xZENQb9tgGIIaHVsfXmvQFhHpYV4CSw')

                geocode_result = gmaps.geocode(endereco_ajustado)

                ponto = Point(geocode_result[0]['geometry']['location']['lng'], 
                            geocode_result[0]['geometry']['location']['lat'])

                mapa_['resultado'] = mapa_['geometry'].map(lambda x: x.distance(ponto))

                #mapa_selecionado = mapa_[mapa_['resultado'] == True]
                mapa_selecionado = mapa_[mapa_['resultado'] == mapa_['resultado'].min()]

                if (len(mapa_selecionado) > 0):

                    return ponto, mapa_selecionado['Name'].values[0]
                else:
                    return ponto, None
                    
            except:
                return None, None
        else:
            try:
                if (len(st.session_state['BASE_ENDERECOS'][st.session_state['BASE_ENDERECOS']['ENDERECO'] == endereco]) == 0):

                    resultado = geocoder.arcgis(endereco_ajustado)

                    if (len(resultado.latlng) == 2):
                        ponto = Point(resultado.lng, resultado.lat)

                        mapa_['resultado'] = mapa_['geometry'].map(lambda x: x.distance(ponto))

                        #mapa_selecionado = mapa_[mapa_['resultado'] == True]
                        mapa_selecionado = mapa_[mapa_['resultado'] == mapa_['resultado'].min()]

                        if (len(mapa_selecionado) > 0):

                            return ponto, mapa_selecionado['Name'].values[0]
                        else:
                            try:
                                gmaps = googlemaps.Client(key='AIzaSyA0xZENQb9tgGIIaHVsfXmvQFhHpYV4CSw')

                                geocode_result = gmaps.geocode(endereco_ajustado)
                                
                                ponto = Point(geocode_result[0]['geometry']['location']['lng'], 
                                            geocode_result[0]['geometry']['location']['lat'])

                                mapa_['resultado'] = mapa_['geometry'].map(lambda x: x.distance(ponto))

                                #mapa_selecionado = mapa_[mapa_['resultado'] == True].copy()
                                mapa_selecionado = mapa_[mapa_['resultado'] == mapa_['resultado'].min()]

                                if (len(mapa_selecionado) > 0):

                                    return ponto, mapa_selecionado['Name'].values[0]
                                else:
                                    return ponto, None
                                
                            except:
                                return None, None

                    else:
                        try:
                            gmaps = googlemaps.Client(key='AIzaSyA0xZENQb9tgGIIaHVsfXmvQFhHpYV4CSw')

                            geocode_result = gmaps.geocode(endereco_ajustado)
                            
                            ponto = Point(geocode_result[0]['geometry']['location']['lng'], 
                                        geocode_result[0]['geometry']['location']['lat'])

                            mapa_['resultado'] = mapa_['geometry'].map(lambda x: x.distance(ponto))

                            #mapa_selecionado = mapa_[mapa_['resultado'] == True].copy()
                            mapa_selecionado = mapa_[mapa_['resultado'] == mapa_['resultado'].min()]

                            if (len(mapa_selecionado) > 0):

                                return ponto, mapa_selecionado['Name'].values[0]
                            else:
                                return ponto, None
                            
                        except:
                            return None, None
                else:
                    return True, True
            except:
                resultado = geocoder.arcgis(endereco_ajustado)

                if (len(resultado.latlng) == 2):
                    ponto = Point(resultado.lng, resultado.lat)

                    mapa_['resultado'] = mapa_['geometry'].map(lambda x: x.distance(ponto))

                    #mapa_selecionado = mapa_[mapa_['resultado'] == True]
                    mapa_selecionado = mapa_[mapa_['resultado'] == mapa_['resultado'].min()]

                    if (len(mapa_selecionado) > 0):

                        return ponto, mapa_selecionado['Name'].values[0]
                    else:
                        try:
                            gmaps = googlemaps.Client(key='AIzaSyA0xZENQb9tgGIIaHVsfXmvQFhHpYV4CSw')

                            geocode_result = gmaps.geocode(endereco_ajustado)
                            
                            ponto = Point(geocode_result[0]['geometry']['location']['lng'], 
                                        geocode_result[0]['geometry']['location']['lat'])
                            
                            mapa_['resultado'] = mapa_['geometry'].map(lambda x: x.distance(ponto))

                            mapa_selecionado = mapa_[mapa_['resultado'] == True].copy()

                            if (len(mapa_selecionado) > 0):
                                return ponto, mapa_selecionado['Name'].values[0]
                            else:
                                return ponto, None
                            
                        except:
                            return None, None

                else:
                    try:
                        gmaps = googlemaps.Client(key='AIzaSyA0xZENQb9tgGIIaHVsfXmvQFhHpYV4CSw')

                        geocode_result = gmaps.geocode(endereco_ajustado)

                        ponto = Point(geocode_result[0]['geometry']['location']['lng'], 
                                    geocode_result[0]['geometry']['location']['lat'])

                        mapa_['resultado'] = mapa_['geometry'].map(lambda x: x.distance(ponto))

                        #mapa_selecionado = mapa_[mapa_['resultado'] == True]
                        mapa_selecionado = mapa_[mapa_['resultado'] == mapa_['resultado'].min()]

                        if (len(mapa_selecionado) > 0):

                            return ponto, mapa_selecionado['Name'].values[0]
                        else:
                            return ponto, None
                        
                    except:
                        return None, None


            

    def plotar_mapa(self, mapa_, colunas_disponiveis, geometria, zoom):

        mymap = folium.Map(location=[mapa_['geometry'].centroid.y.mean(), mapa_[
                            'geometry'].centroid.x.mean()], zoom_start=zoom, tiles=None, zoom_control=False)
        folium.TileLayer(control=False).add_to(mymap)
        
        mapa_plot = mapa_[(mapa_['Name'] == '1ª Zona') | (mapa_['Name'] == '2ª Zona')][['Name','geometry']]
        
        def style_function(x):
            if (x['properties']['Name'] == '1ª Zona'):
                return {"weight": 1,
                        'color': 'white',
                        'fillColor': '#F3D384',
                        'fillOpacity': 0.75}
            else:
                return {"weight": 1,
                        'color': 'white',
                        'fillColor': '#F9C7D9',
                        'fillOpacity': 0.75}

        def highlight_function(x):
            return {'fillColor': '#000000',
                    'color': 'white',
                    'fillOpacity': 0.50,
                    'weight': 1}
        

        for i in mapa_plot.index:
            mapa = gpd.GeoDataFrame(pd.DataFrame(
                mapa_plot.loc[i]).transpose())
            mapa.set_crs(epsg=4326, inplace=True)

            NIL = folium.features.GeoJson(
                mapa,
                zoom_on_click=False,
                style_function=style_function,
                control=False,
                highlight_function=highlight_function,
                tooltip=folium.features.GeoJsonTooltip(fields=colunas_disponiveis,
                                                        aliases=colunas_disponiveis,
                                                        style=(
                                                            "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                                                        sticky=False)
            )
            mymap.add_child(NIL)

            try:
                for geo in geometria:
                    folium.Marker( location=[geo.y, geo.x], fill_color='#43d9de', radius=8 ).add_to(mymap)
            except:
                pass

        folium_static(mymap)


    def exibir(self):
        self.carregar_estilo()
        mapa = self.carregar_poligonos()

        with st.sidebar:

            st.sidebar.image(Image.open(os.getcwd() + "\\Imagens\\logo.png"))

            endereco = st.text_input('', 
                                     value="", 
                                     type="default", 
                                     placeholder='Digite o endereço a ser pesquisado', 
                                     label_visibility="collapsed")
            
            st.text('Ou faça o upload de um arquivo csv')

            file = st.file_uploader('', type='csv', disabled=len(endereco) > 0, label_visibility="collapsed")

            with st.form("Fomulário", border=False):               
                
                submitted = st.form_submit_button("Buscar")
                if submitted:
                    st.session_state['ENDERECO'] = endereco

                    try:
                        if (file is not None):
                            df = pd.read_csv(file, header=None)

                            if (len(df) > 0 and df.shape[1] > 0):
                                st.session_state['ENDERECO_MULTIPLOS'] = df[df.index < 10]
                            else:
                                st.caption('O arquivo upado contém erros. Tente novamente.')
                    except:
                        st.session_state['ENDERECO_MULTIPLOS'] = []


        if (len(st.session_state['ENDERECO']) > 5):
            geometria, zona = self.verificador_endereco(st.session_state['ENDERECO'], mapa)
            
            if (geometria == True and zona == True):
                st.sidebar.text('Endereço já pesquisado')
            elif (geometria == None):
                st.sidebar.text('Não foi possível encontrar o endereço na cidade de Cachoeirinha - RS')
            elif (zona == None):
                st.sidebar.text('Não foi possível identificar a zona do endereço especificado')
            else:
                dt_final = pd.DataFrame({'ENDERECO': [st.session_state['ENDERECO']]})
                dt_final.loc[0, ['ZONA', 'GEOMETRIA']] = [zona, geometria]


                st.sidebar.markdown(f"<p style='font-weight: bold;'>Endereço {st.session_state['ENDERECO']}.<br>Este endereço pertence a {zona} </p>", unsafe_allow_html=True)
                            
                self.salvar_dados(dt_final)
                self.plotar_mapa(mapa, ['Name'], [geometria], 13)
        

        elif (len(st.session_state['ENDERECO_MULTIPLOS']) > 0):

                enderecos = st.session_state['ENDERECO_MULTIPLOS'][st.session_state['ENDERECO_MULTIPLOS'].columns[0]].values

                dt_final = pd.DataFrame({'ENDERECO': enderecos})

                for i in dt_final.index:
                    geometria, zona = self.verificador_endereco(dt_final['ENDERECO'][i], mapa)

                    dt_final.loc[i, ['ZONA', 'GEOMETRIA']] = [zona, geometria]

                    time.sleep(10)

                self.salvar_dados(dt_final)
                self.plotar_mapa(mapa, ['Name'], dt_final['GEOMETRIA'], 13)


        else:
            self.plotar_mapa(mapa, ['Name'], [], 13)




        # Janela de análises
        with st.expander("Dados históricos"):
            st.write("Dados históricos")
            try:
                st.session_state['BASE_ENDERECOS'] = self.carregar_dados(os.path.getmtime(os.getcwd() + "\\Dados\\base_dados.csv"))[['ENDERECO', 'ZONA']]
                st.dataframe(st.session_state['BASE_ENDERECOS'],
                             use_container_width=True,
                             hide_index=True)
            except:
                pass
            
obj = Main()
obj.exibir()