import streamlit as st
import requests

st.set_page_config(page_title="Network Calculator", layout="centered")

st.title("🌐 Gestionnaire de Réseau IP")

with st.form("network_form"):
    col1, col2 = st.columns(2)
    with col1:
        ip_input = st.text_input("Adresse Réseau", value="192.168.10.0")
    with col2:
        mask_input = st.number_input("Masque (CIDR)", min_value=0, max_value=32, value=26)
    
    submit_button = st.form_submit_button("Calculer")

if submit_button:
    # Appel de l'API FastAPI (assurez-vous que le serveur tourne sur le port 8000)
    api_url = f"http://127.0.0.1:8000/network/info?address={ip_input}&mask={mask_input}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            
            # Affichage des informations générales
            st.subheader("Informations Réseau")
            c1, c2, c3 = st.columns(3)
            c1.metric("Hôtes utilisables", data["num_hosts"])
            c2.metric("Passerelle (Gtw)", data["gateway"])
            c3.metric("Broadcast", data["broadcast"])
            
            st.info(f"Masque de sous-réseau : {data['netmask']}")

            # Liste des hôtes
            with st.expander("Voir la liste complète des adresses IP disponibles"):
                st.write(data["hosts"])
        else:
            st.error(f"Erreur API : {response.json().get('detail')}")
    except Exception as e:
        st.error(f"Impossible de contacter l'API. Vérifiez qu'elle est lancée. {e}")