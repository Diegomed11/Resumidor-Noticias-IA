import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import requests
from bs4 import BeautifulSoup
import torch

# configuracion de la pagina
st.set_page_config(page_title="Resumidor de Noticias IA", page_icon="📰", layout="wide")

st.title("📰 Analista de Noticias con IA 📰")
st.markdown("""
Esta herramienta utiliza **Deep Learning (Google mT5)** para leer, entender y resumir noticias en español.
""")

st.markdown("""
Herramienta desarrollada por Diego Medina Medina 
- [GitHub]-->https://github.com/diegomed11
"""
)

# carga modelos 
@st.cache_resource
def load_models():
    # Usamos mT5, el estándar para resumen multilingüe
    model_name = "csebuetnlp/mT5_multilingual_XLSum"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cpu")
    
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    sentiment = pipeline("text-classification", model="pysentimiento/robertuito-sentiment-analysis")
    
    return summarizer, sentiment

with st.spinner('Iniciando modelos de IA...'):
    try:
        resumidor, analista_sentimiento = load_models()
        st.success("Modelos de IA listos para usarse")
    except Exception as e:
        st.error(f"Error cargando modelos: {e}")

# script to extract 
def extraer_texto_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ELIMINAR BASURA: Quitamos scripts, estilos, pies de página y navegación
        for element in soup(["script", "style", "footer", "nav", "header", "aside"]):
            element.decompose()

        # EXTRAER PÁRRAFOS
        paragraphs = soup.find_all('p')
        
        
        # Esto elimina menús, "leé también", "copyright", etc.
        clean_text = []
        for p in paragraphs:
            if len(p.get_text()) > 50:
                clean_text.append(p.get_text())
        
        full_text = ' '.join(clean_text)
        return full_text.strip()

    except Exception as e:
        return None

# interface de usuario

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Ingresa la Noticia")
    tab1, tab2 = st.tabs(["🔗 Pegar URL", "📝 Pegar Texto Manual"])
    
    texto_a_procesar = ""

    with tab1:
        url_input = st.text_input("URL de la noticia:", placeholder="https://elpais.com/...")
        if st.button("Extraer Texto de URL"):
            if url_input:
                with st.spinner('Extrayendo contenido...'):
                    extracted = extraer_texto_url(url_input)
                    if extracted:
                        st.session_state['texto_final'] = extracted
                        st.success("Texto extraído correctamente.")
                    else:
                        st.error("No se pudo leer la página. Intenta pegar el texto manualmente en la otra pestaña.")

    with tab2:
        text_input = st.text_area("Pega aquí el cuerpo de la noticia:", height=300, placeholder="Copia y pega el texto completo del artículo aquí...")
        if st.button("Usar Texto Manual"):
            st.session_state['texto_final'] = text_input
            st.success("Texto manual cargado.")

with col2:
    st.subheader("2. Resultados de la IA")
    
    # Verificamos si hay texto cargado en la memoria de la sesión
    if 'texto_final' in st.session_state and len(st.session_state['texto_final']) > 50:
        
        texto_real = st.session_state['texto_final']
        
        # Mostrar el texto que la IA va a leer (para que tú verifiques si es basura o no)
        with st.expander("Ver qué texto se esta leyendo"):
            st.write(texto_real)

        if st.button("✨ Generar Resumen y Análisis"):
            with st.spinner('La IA está leyendo y pensando...'):
                try:
                    # RESUMEN
                    input_corto = texto_real[:3000] 
                    
                    resumen = resumidor(input_corto, max_length=130, min_length=30, do_sample=False)
                    texto_resumen = resumen[0]['summary_text']
                    
                    st.info(f"**Resumen:** {texto_resumen}")
                    
                    # SENTIMIENTO
                    sentimiento = analista_sentimiento(texto_resumen)
                    etiqueta = sentimiento[0]['label']
                    score = sentimiento[0]['score']
                    
                    st.divider()
                    col_a, col_b = st.columns(2)
                    col_a.metric("Sentimiento", etiqueta)
                    col_b.metric("Confianza", f"{score:.2%}")
                    
                except Exception as e:
                    st.error(f"Error en el procesamiento: {e}")
    else:
        st.info("👈 Primero extrae una URL o pega texto manualmente.")