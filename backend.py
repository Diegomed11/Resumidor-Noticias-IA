from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import requests
from bs4 import BeautifulSoup
import torch

# Configuración inicial de Flask
app = Flask(__name__)
# Permitimos CORS para que el Frontend (React) pueda hablar con este Backend
CORS(app) 


print("⏳ Cargando modelos de IA... Por favor espera.")


try:
    model_name = "csebuetnlp/mT5_multilingual_XLSum"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    model_t5 = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cpu")
    
    summarizer_pipeline = pipeline("summarization", model=model_t5, tokenizer=tokenizer)
    print("✅ Modelo de Resumen cargado.")
except Exception as e:
    print(f"❌ Error cargando Resumidor: {e}")


try:
    sentiment_pipeline = pipeline("text-classification", model="pysentimiento/robertuito-sentiment-analysis")
    print("✅ Modelo de Sentimiento cargado.")
except Exception as e:
    print(f"❌ Error cargando Sentimiento: {e}")



def clean_text_from_url(url):
    """Descarga y limpia el texto de una noticia dado un URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Eliminar elementos no deseados
        for element in soup(["script", "style", "footer", "nav", "header", "aside", "form"]):
            element.decompose()

        # Extraer párrafos con contenido sustancial
        paragraphs = soup.find_all('p')
        clean_text = []
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 60: # Filtro para evitar menús o frases cortas
                clean_text.append(text)
        
        full_text = ' '.join(clean_text)
        return full_text if len(full_text) > 100 else None
    except Exception as e:
        print(f"Error scraping: {e}")
        return None



@app.route('/api/analyze', methods=['POST'])
def analyze_news():
    data = request.json
    source_type = data.get('type') # 'url' o 'text'
    content = data.get('content')

    if not content:
        return jsonify({"error": "No se proporcionó contenido"}), 400


    text_to_process = ""
    if source_type == 'url':
        extracted = clean_text_from_url(content)
        if not extracted:
            return jsonify({"error": "No se pudo extraer texto de la URL. Intenta pegar el texto manualmente."}), 400
        text_to_process = extracted
    else:
        text_to_process = content


    text_preview = text_to_process[:3000]

    try:
        # 2. Generar Resumen
        # Ajustamos parámetros para un resumen conciso
        summary_result = summarizer_pipeline(text_preview, max_length=130, min_length=40, do_sample=False)
        summary_text = summary_result[0]['summary_text']

        # 3. Analizar Sentimiento (sobre el resumen generado)
        sentiment_result = sentiment_pipeline(summary_text)
        sentiment_label = sentiment_result[0]['label'] # POS, NEG, NEU
        sentiment_score = sentiment_result[0]['score']

        return jsonify({
            "success": True,
            "original_length": len(text_to_process),
            "summary": summary_text,
            "sentiment": sentiment_label,
            "confidence": sentiment_score
        })

    except Exception as e:
        return jsonify({"error": f"Error interno del modelo: {str(e)}"}), 500

if __name__ == '__main__':
    # Corremos en el puerto 5000
    print("Servidor Backend listo en http://localhost:5000")
    app.run(debug=True, port=5000)