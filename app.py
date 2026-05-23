import streamlit as st
from supabase import create_client
import os

st.set_page_config(page_title="CRM Línea Norte", page_icon=":office:")

st.title("CRM Línea Norte")
st.write("Gestión de clientes y proveedores")

# Conexión a Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.success("Conectado a Supabase")
else:
    st.warning("Faltan las claves de Supabase. Las añadiremos luego.")

# -------------------------
# FORMULARIO DE ALTA
# -------------------------

st.subheader("Alta de cliente")

with st.form("form_clientes"):
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    telefono = st.text_input("Teléfono")
    notas = st.text_area("Notas")

    submitted = st.form_submit_button("Guardar cliente")

    if submitted:
        if not nombre:
            st.error("El nombre es obligatorio.")
        else:
            data = {
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "notas": notas
            }

            try:
                supabase.table("clientes").insert(data).execute()
                st.success("Cliente guardado correctamente.")
            except Exception as e:
                st.error(f"Error al guardar: {e}")

# -------------------------
# FILTROS
# -------------------------

st.subheader("Filtrar clientes")

filtro_nombre = st.text_input("Filtrar por nombre")
filtro_email = st.text_input("Filtrar por email")
filtro_telefono = st.text_input("Filtrar por teléfono")
filtro_notas = st.text_input("Filtrar por notas")

# -------------------------
# LISTADO + EDITAR + ELIMINAR
# -------------------------

st.subheader("Listado de clientes")

try:
    clientes = supabase.table("clientes").select("*").order("fecha_alta", desc=True).execute()
    data = clientes.data

    # Aplicar filtros
    if filtro_nombre:
        data = [c for c in data if filtro_nombre.lower() in c["nombre"].lower()]

    if filtro_email:
        data = [c for c in data if c["email"] and filtro_email.lower() in c["email"].lower()]

    if filtro_telefono:
        data = [c for c in data if c["telefono"] and filtro_telefono in c["telefono"]]

    if filtro_notas:
        data = [c for c in data if c["notas"] and filtro_notas.lower() in c["notas"].lower()]

    # Mostrar tabla con botones de acción
    if data:
        for cliente in data:
            st.write("---")
            cols = st.columns([3, 1, 1])

            with cols[0]:
                st.write(f"**{cliente['nombre']}**")
                st.write(f"📧 {cliente['email']}")
                st.write(f"📱 {cliente['telefono']}")
                st.write(f"📝 {cliente['notas']}")

            # Botón editar
            with cols[1]:
                if st.button("✏️ Editar", key=f"edit_{cliente['id']}"):
                    st.session_state["edit_cliente"] = cliente

            # Botón eliminar
            with cols[2]:
                if st.button("🗑️ Eliminar", key=f"del_{cliente['id']}"):
                    try:
                        supabase.table("clientes").delete().eq("id", cliente["id"]).execute()
                        st.success("Cliente eliminado.")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error al eliminar: {e}")

    else:
        st.info("No hay clientes que coincidan con los filtros.")

except Exception as e:
    st.error(f"Error al cargar clientes: {e}")

# -------------------------
# FORMULARIO DE EDICIÓN
# -------------------------

if "edit_cliente" in st.session_state:
    cliente = st.session_state["edit_cliente"]

    st.subheader(f"Editar cliente: {cliente['nombre']}")

    nuevo_nombre = st.text_input("Nombre", cliente["nombre"])
    nuevo_email = st.text_input("Email", cliente["email"])
    nuevo_telefono = st.text_input("Teléfono", cliente["telefono"])
    nuevas_notas = st.text_area("Notas", cliente["notas"])

    if st.button("Guardar cambios"):
        try:
            supabase.table("clientes").update({
                "nombre": nuevo_nombre,
                "email": nuevo_email,
                "telefono": nuevo_telefono,
                "notas": nuevas_notas
            }).eq("id", cliente["id"]).execute()

            st.success("Cliente actualizado correctamente.")
            del st.session_state["edit_cliente"]
            st.experimental_rerun()

        except Exception as e:
            st.error(f"Error al actualizar: {e}")

    if st.button("Cancelar edición"):
        del st.session_state["edit_cliente"]
        st.experimental_rerun()

# -------------------------
# PROVEEDORES (vacío por ahora)
# -------------------------

st.subheader("Proveedores")
st.info("Aquí aparecerá la gestión de proveedores.")
