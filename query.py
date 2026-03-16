import pandas as pd
import streamlit as st

# Detectar recarga de la página
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.query = []  # Reinicia la query
    dic = {}  # Reinicia el diccionario


dic = {}

if "query" not in st.session_state:
    st.session_state.query = []

def query_table(row, nodes, metric, perc_act, perc_path, manip, cont):
    global dic

    if 'f' + str(row) not in dic:
        dic['f' + str(row)] = {}

    dic['f' + str(row)][cont] = {"Action": manip}

    new_entry = {
        "Name": 'f' + str(row),
        "Nodes": nodes,
        "Metrics": metric,
        "%P": perc_path,
        "%A": perc_act,
        "Selection": ""
    }

    for action_key, action_data in dic['f' + str(row)].items():
        new_entry[f"Filter{action_key}"] = str(action_data["Action"])  # Asegura compatibilidad

    existing_entry = next((row for row in st.session_state.query if row["Name"] == new_entry["Name"]), None)

    if existing_entry:
        existing_entry.update(new_entry)
    else:
        st.session_state.query.append(new_entry)

    df_query = pd.DataFrame(st.session_state.query)

    for col in df_query.columns:
        df_query[col] = df_query[col].apply(lambda x: str(x) if isinstance(x, (list, tuple)) else x)

    # st.write("Diccionario actualizado:")
    # st.write(dic)
    # st.write("Tabla generada:")
    st.data_editor(df_query, num_rows="dynamic")

