from transformers import pipeline
import textwrap

# --- 1. CONFIGURACIÓN DE MODELOS ---

print("Cargando modelo de resumen T5 (Google Multilingual)...")
# Usamos mT5, un modelo moderno y estable que soporta español nativamente
resumidor = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")

print("Cargando modelo de análisis de sentimiento...")
analista_sentimiento = pipeline("text-classification", model="pysentimiento/robertuito-sentiment-analysis")

# --- 2. DATOS DE ENTRADA ---
articulo = """
La empresa OpenAI presentó este lunes su nuevo modelo de inteligencia artificial, GPT-4o. 
Según la compañía, esta nueva versión es mucho más rápida y tiene capacidades mejoradas 
para entender y generar texto, audio e imágenes en tiempo real. 
Durante la demostración en vivo, el modelo fue capaz de resolver ecuaciones matemáticas, 
contar chistes con diferentes tonos de voz y traducir idiomas instantáneamente. 
Expertos aseguran que este lanzamiento marca un hito en la competencia tecnológica 
entre Microsoft, Google y Apple por dominar el mercado de la IA generativa.
"""

print("\n" + "="*50)
print("ARTÍCULO ORIGINAL:")
print(textwrap.fill(articulo, width=80))
print("="*50)

# --- 3. EJECUTAR EL RESUMEN ---
print("\nGenerando resumen...")

# El modelo mT5 funciona mejor con textos cortos de entrada.
resumen = resumidor(articulo, max_length=80, min_length=20, do_sample=False)
texto_resumen = resumen[0]['summary_text']

print(f"\n📝 RESUMEN IA:\n{textwrap.fill(texto_resumen, width=80)}")

# --- 4. EJECUTAR EL ANÁLISIS DE SENTIMIENTO ---
print("\nAnalizando sentimiento...")
sentimiento = analista_sentimiento(texto_resumen)

etiqueta = sentimiento[0]['label']
score = sentimiento[0]['score']

print(f"\nbarómetro SENTIMENTAL: {etiqueta} (Confianza: {score:.4f})")