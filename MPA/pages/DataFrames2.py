import streamlit as st
import pandas as pd
import uuid

# Configuración inicial de la página
st.set_page_config(layout="wide")

# Inicializar el DataFrame en el estado de la sesión
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["ID", "Nombre", "Cantidad"])


# Función para agregar una nueva fila
def add_row():
    new_id = str(uuid.uuid4())  # Generar un identificador único
    new_row = {"ID": new_id, "Nombre": "", "Cantidad": 0}
    st.session_state["data"] = pd.concat(
        [st.session_state["data"], pd.DataFrame([new_row])], ignore_index=True
    )


# Función para eliminar una fila
def remove_row(row_id):
    st.session_state["data"] = st.session_state["data"][
        st.session_state["data"]["ID"] != row_id
    ]


# Mostrar la tabla editable
st.title("Gestión de Filas en un DataFrame")

# Botón para agregar una nueva fila
st.button("Agregar Fila", on_click=add_row)

# Iterar sobre las filas del DataFrame
for index, row in st.session_state["data"].iterrows():
    # Crear columnas para cada fila
    cols = st.columns((3, 2, 1))

    # Inputs para editar "Nombre" y "Cantidad"
    st.session_state["data"].at[index, "Nombre"] = cols[0].text_input(
        "Nombre", value=row["Nombre"], key=f"nombre_{row['ID']}"
    )
    st.session_state["data"].at[index, "Cantidad"] = cols[1].number_input(
        "Cantidad", value=row["Cantidad"], step=1, key=f"cantidad_{row['ID']}"
    )

    # Botón para eliminar la fila
    cols[2].button(
        "🗑️", key=f"eliminar_{row['ID']}", on_click=remove_row, args=(row["ID"],)
    )

# Mostrar el DataFrame resultante
st.write("### DataFrame Actual")
st.dataframe(st.session_state["data"])
