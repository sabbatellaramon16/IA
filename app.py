import os
import requests
import streamlit as st
from dotenv import load_dotenv



load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")


st.write("Token:", HF_TOKEN)


API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

st.set_page_config(
    page_title="Corrector de Textos con IA",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Corrector de Textos con IA")

st.write(
    "Escribe un texto y la inteligencia artificial corregirá la ortografía, la gramática y mejorará la redacción."
)

texto = st.text_area(
    "Escribe tu texto:",
    height=250
)

if st.button("Corregir texto"):

    if texto.strip() == "":
        st.warning("Por favor escribe un texto.")
    else:

        prompt = f"""
Eres un profesor experto en lengua española.

Corrige el siguiente texto.

Debes:
- Corregir ortografía.
- Corregir gramática.
- Mejorar la redacción.
- Mantener el significado.
- No agregar información nueva.

Responde con este formato:

## Texto corregido

(texto corregido)

## Cambios realizados

- Cambio 1
- Cambio 2
- Cambio 3

Texto:

{texto}
"""

        payload = {
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 700
        }

        with st.spinner("Corrigiendo texto..."):

            respuesta = requests.post(
                API_URL,
                headers=headers,
                json=payload
            )

        if respuesta.status_code == 200:

            resultado = respuesta.json()

            st.success("¡Corrección realizada!")

            st.markdown(resultado["choices"][0]["message"]["content"])

        else:

            st.error("Ocurrió un error al conectar con la IA.")

            st.code(respuesta.text)