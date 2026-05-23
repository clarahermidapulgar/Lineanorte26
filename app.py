import streamlit as st
from supabase import create_client
import os

st.set_page_config(page_title="CRM Línea Norte", page_icon="📇")

st.title("CRM Línea Norte")
st.write("Gestión de clientes y proveedores")

# Conexión a Supabase (las claves las añadiremos luego)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.success("Conectado a Supabase")
else:
    st.warning("Faltan las claves de Supabase. Las añadiremos más adelante.")

st.subheader("Clientes")
st.info("Aquí aparecerá la gestión de clientes.")

st.subheader("Proveedores")
st.info("Aquí aparecerá la gestión de proveedores.")
