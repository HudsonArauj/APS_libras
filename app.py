import streamlit as st
from streamlit import session_state as ss
from streamlit.components.v1 import html
from streamlit_folium import st_folium
import folium
from utils import get_data

cinemas = get_data('data/cinema.json')
teatros = get_data('data/teatro.json')
restaurantes = get_data('data/restaurante.json')
palestras = get_data('data/resultados.json')


options_cinemas = [cinema['title'] for cinema in cinemas]
options_teatros = [teatro['title'] for teatro in teatros]
options_restaurantes = [restaurante['title'] for restaurante in restaurantes]
options_palestras = [palestra['title'] for palestra in palestras]

def set_category(category):
    ss.selected_category = category
    ss.vlibras_text = category 


if 'selected_category' not in ss:
    ss.selected_category = 'Cinemas'  
    ss.vlibras_text = 'Cinema'  

col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("<h1 style='text-align: center; color: rgb(127, 107, 181);'>Localiza</h1>", unsafe_allow_html=True)

with col2:
    st.image('./img/icon_libras.png', width=100)

st.markdown("<h3 style='text-align: center; color: rgb(12, 189, 181);'>Localize eventos próximos de você</h3>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: rgb(127, 107, 181);'>Escolha uma categoria:</h4>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('Cinema'):
        set_category('Cinemas')

with col2:
    if st.button('Teatro'):
        set_category('Teatros')

with col3:
    if st.button('Restaurante'):
        set_category('Restaurantes')

with col4:
    if st.button('Palestras'):
        set_category('Palestras')


st.sidebar.markdown("<h1 style ='background-color: rgb(127, 107, 181); text-align: center; border-radius:0.8rem;'>Localiza</h1>", unsafe_allow_html=True)


options = {
    'Cinemas': options_cinemas,
    'Teatros': options_teatros,
    'Restaurantes': options_restaurantes,
    'Palestras': options_palestras
}

selected_option = st.sidebar.selectbox(ss.selected_category, options[ss.selected_category], key='selected_option')


# create columns streamlit
col1, col2 = st.columns([1, 1])


def show_location_details(location, category):
    
    with col1:
        if category == 'Palestras':
            st.markdown(f"### {location['title']}")
            st.write(f"**Data:** {location['date']['start_date']} - {location['date']['when']}")
            st.write(f"**Endereço:** {', '.join(location['address'])}")
            st.write(f"**Link:** [Clique aqui]({location['link']})")
            st.write(f"**Descrição:** {location['description']}")
            
            if 'thumbnail' in location:
                st.image(location['thumbnail'], caption=location['title'], use_container_width ="never", width= 150)
            
        
        if category == 'Cinemas':
            st.markdown(f"### {location['title']}")
            st.write(f"**Endereço:** {location['address']}")
            st.write(f"**Tipo:** {location['type']}")
            st.write(f"**Website:** [Clique aqui]({location['links']['website']})")
            st.write(f"**Direções:** [Clique aqui]({location['links']['directions']})")
            st.write(f"**Descrição:** {location['description']}")


            if "image" in location:
                st.image(location["image"], caption=location["title"], use_container_width =True, width=100)

            map_ = folium.Map(
                location=[location["gps_coordinates"]["latitude"], location["gps_coordinates"]["longitude"]],
                zoom_start=15
            )
            folium.Marker(
                [location["gps_coordinates"]["latitude"], location["gps_coordinates"]["longitude"]],
                popup=location["title"],
                tooltip="Clique para mais informações"
            ).add_to(map_)

            st_folium(map_, width=300, height=300)
            st.write("---")
        
        if category== "Teatros":
            st.markdown(f"### {location['title']}")
            st.write(f"**Endereço:** {location['address']}")
            st.write(f"**Tipo:** {location['type']}")
            st.write(f"**Descrição:** {location['description']}")

            
            if "thumbnail" in location:
                st.image(location["thumbnail"], caption=location["title"], use_container_width ="always", width=100)

            map_ = folium.Map(
                location=[location["gps_coordinates"]["latitude"], location["gps_coordinates"]["longitude"]],
                zoom_start=15
            )
            folium.Marker(
                [location["gps_coordinates"]["latitude"], location["gps_coordinates"]["longitude"]],
                popup=location["title"],
                tooltip="Clique para mais informações"
            ).add_to(map_)

            st_folium(map_, width=300, height=300)
            st.write("---")
            
        if category == 'Restaurantes':
            st.markdown(f"### {location['title']}")
            st.write(f"**Endereço:** {location['address']}")
            st.write(f"**Tipo:** {location['type']}")
            st.write(f"**Descrição:** {location['description']}")

            if "image" in location:
                st.image(location["image"], caption=location["title"], use_container_width =True, width=100)

            map_ = folium.Map(
                location=[location["gps_coordinates"]["latitude"], location["gps_coordinates"]["longitude"]],
                zoom_start=15
            )
            folium.Marker(
                [location["gps_coordinates"]["latitude"], location["gps_coordinates"]["longitude"]],
                popup=location["title"],
                tooltip="Clique para mais informações"
            ).add_to(map_)

            st_folium(map_, width=200, height=200)
            st.write("---")

if ss.selected_category == 'Cinemas':
    selected_cinema = next((cinema for cinema in cinemas if cinema['title'] == selected_option), None)
    if selected_cinema:
        show_location_details(selected_cinema, 'Cinemas')

elif ss.selected_category == 'Teatros':
    selected_teatro = next((teatro for teatro in teatros if teatro['title'] == selected_option), None)
    if selected_teatro:
        show_location_details(selected_teatro, 'Teatros')

elif ss.selected_category == 'Restaurantes':
    selected_restaurante = next((restaurante for restaurante in restaurantes if restaurante['title'] == selected_option), None)
    if selected_restaurante:
        show_location_details(selected_restaurante, 'Restaurantes')

elif ss.selected_category == 'Palestras':
    selected_palestra = next((palestra for palestra in palestras if palestra['title'] == selected_option), None)
    if selected_palestra:
        show_location_details(selected_palestra, 'Palestras')

with col2:
    html(
        """
        <style>
            .vw-plugin-top-wrapper {
                height: 100px; /* Ajuste a altura conforme necessário */
            }
        </style>
        <div vw class="enabled">
            <div vw-access-button class="active"></div>
            <div vw-plugin-wrapper>
                <div class="vw-plugin-top-wrapper"></div>
            </div>
        </div>
        <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
        <script>
            new window.VLibras.Widget('https://vlibras.gov.br/app');
        </script>
        """,
        height=500 
    )
