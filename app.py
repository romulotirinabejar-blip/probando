import streamlit as st
import google.generativeai as genai

# Configuración de la ventana y el título de la app
st.set_page_config(page_title="Mi App de IA", page_icon="🤖")
st.title("🤖 Mi Asistente Gemini")

# Obtener la clave API guardada en la configuración de Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Por favor, configura tu GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Configurar el modelo con tu clave
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Inicializar el historial de conversación en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar en pantalla el historial de mensajes guardados
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada de texto para enviar mensajes
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Guardar y mostrar el mensaje que escribió el usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar y mostrar la respuesta de la IA
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ocurrió un error al consultar a Gemini: {e}")
