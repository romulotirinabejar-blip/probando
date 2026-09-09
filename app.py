import streamlit as st
from google import genai

st.title("🤖 Mi Asistente Gemini")

# Obtener clave de API desde los Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Por favor, configura tu GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Inicializar cliente oficial
client = genai.Client(api_key=api_key)

# Inicializar historial en session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ocurrió un error al consultar a Gemini: {e}")
