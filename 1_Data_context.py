import streamlit as st
import numpy as np
import ast
import ast
import pandas as pd
import pm4py
import copy
import deprecation
import statisticslog
import query_selection
import os
import recommendations
import specification
from PIL import Image
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.transformation.log_to_features import algorithm as log_to_features
from pm4py.algo.filtering.dfg import dfg_filtering
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.statistics.rework.cases.log import get as cases_rework_get
from pm4py.statistics.start_activities.log.get import get_start_activities
from pm4py.statistics.end_activities.log.get import get_end_activities
import networkx as nx
from pm4py.statistics.rework.cases.log import get as rework_cases
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.algo.filtering.log.end_activities import end_activities_filter
from pm4py.statistics.rework.cases.log import get as rework_cases
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.filtering.log.attributes import attributes_filter
import json
import re
from datetime import date, time, datetime
from pm4py.visualization.dfg.variants.frequency import apply
from pm4py.visualization.dfg.variants import performance
import warnings
warnings.filterwarnings("ignore")
import time
from datetime import datetime
from PIL import Image
from io import StringIO
from pm4py.visualization.dfg import visualizer as dfg_visualizer
from streamlit import session_state as ss
from graphviz import Digraph
import metricas
import load_data
import manipulation
import dfg_creation
import dfg_properties
import positions_creation
import visualization


st.set_page_config(page_title="Main page", layout="wide")

pd.set_option("styler.render.max_elements", 2000000)


st.title("VISCoPro :mag_right::chart_with_downwards_trend:")
# st.markdown("""---""")


# --------------------------------------------------------------------------------------



if "generate_pressed" not in st.session_state:
    st.session_state.generate_pressed = False

if "save_pressed" not in st.session_state:
    st.session_state.save_pressed = False

if "filter_types" not in st.session_state:
        st.session_state["filter_types"] = {}

if "filter_type_group" not in st.session_state:
        st.session_state["filter_type_group"] = {}

if "attribute" not in st.session_state:
        st.session_state["attribute"] = {}

if "values" not in st.session_state:
        st.session_state["values"] = {}

if "act1" not in st.session_state:
        st.session_state["act1"] = {}

if "act2" not in st.session_state:
        st.session_state["act2"] = {}

if "actk" not in st.session_state:
        st.session_state["actk"] = {}

if "rango" not in st.session_state:
    st.session_state["rango"] = {}

if "number_values" not in st.session_state:
    st.session_state["number_values"] = {}

if "range_values" not in st.session_state:
    st.session_state["range_values"] = {}

if "modes" not in st.session_state:
    st.session_state["modes"] = {}

if "nrange" not in st.session_state:
    st.session_state["nrange"] = {}

if "rango2" not in st.session_state:
    st.session_state["rango2"] = {}

if "input_values" not in st.session_state:
    st.session_state["input_values"] = {}

if "group" not in st.session_state:
    st.session_state["group"] = {}

if "nfollow" not in st.session_state:
    st.session_state["nfollow"] = 1

if "lista_act" not in st.session_state:
    st.session_state["lista_act"] = {}

if 'original' not in st.session_state:
    st.session_state.original = pd.DataFrame()

if 'positions' not in st.session_state:
    st.session_state.positions = {}

if 'positions_edges' not in st.session_state:
    st.session_state.positions_edges = {}

if 'viz' not in st.session_state:
    st.session_state.viz = Digraph()

if 'mapeo' not in st.session_state:
    st.session_state.mapeo = {}

if 'sa' not in st.session_state:
    st.session_state.sa = []

if 'ea' not in st.session_state:
    st.session_state.ea = []

if 'unified' not in st.session_state:
    st.session_state.unified = pd.DataFrame()

if 'nodesDFG' not in st.session_state:
    st.session_state.nodesDFG = set()

if 'edgesDFG' not in st.session_state:
    st.session_state.edgesDFG = set()

if 'colores' not in st.session_state:
    st.session_state.colores={}

if 'delete_act' not in st.session_state:
    st.session_state.delete_act=[]

if 'viz_edges' not in st.session_state:
    st.session_state.viz_edges = set()

if 'viz_labels' not in st.session_state:
    st.session_state.viz_labels = {}

if 'viz_edge_labels' not in st.session_state:
    st.session_state.viz_edge_labels = {}

if 'reference_nodes' not in st.session_state:
    st.session_state.reference_nodes = set()

if 'reference_edges' not in st.session_state:
    st.session_state.reference_edges = set()

if 'reference_sa' not in st.session_state:
    st.session_state.reference_sa = set()

if 'reference_ea' not in st.session_state:
    st.session_state.reference_ea = set()

if "show_table" not in st.session_state:
    st.session_state.show_table = False

if "collections" not in st.session_state:
    st.session_state.collections = {}

if "variables" not in st.session_state:
    st.session_state.variables = {}

if "id_col" not in st.session_state:
    st.session_state.id_col = 0

if "run_pattern" not in st.session_state:
    st.session_state.run_pattern = False

if "selected_ids" not in st.session_state:
    st.session_state.selected_ids = []

if "rework_act" not in st.session_state:
    st.session_state.rework_act = []

if "selected_coll" not in st.session_state:
    st.session_state.selected_coll = {}

if "res_vars" not in st.session_state:
    st.session_state.res_vars = {}

if "var_cont" not in st.session_state:
    st.session_state.var_cont = 0

if "var_cont_table" not in st.session_state:
    st.session_state.var_cont_table = 0


# ------------------------------------------------------------------------------------------------

mensaje_container = st.empty()
sample_data = []
df = load_data.cargar_datos(mensaje_container, sample_data)
dic_original = {}
i=0


# Función helper inline para manejar Selection y memoria
def update_selection(collection_id, new_value, pattern, v_asociada, param="", num=None, second_id=None):
    row_sel = st.session_state.collections[collection_id].get("selection", "")
    
    if row_sel:  # ya hay algo → extraer var_id existente
        var_id = row_sel.split("<-")[0].strip()
    else:  # crear nueva variable
        var_id = f"v{st.session_state.var_cont_table}"
        st.session_state.var_cont_table += 1
        st.session_state.var_cont += 1

    # st.write(var_id)

    # actualizar memoria
    st.session_state.res_vars[var_id] = new_value

    # construir texto de Selection según si hay segunda colección
    if second_id is None:
        st.session_state.collections[collection_id]["selection"] = f"{var_id} <- {param}_{v_asociada} (n={num}) {pattern}(f{collection_id})"
    else:
        st.session_state.collections[collection_id]["selection"] = (
            f"{var_id} <- {param}_{v_asociada} (n={num}) {pattern} (f{collection_id},f{second_id})"
        )   


if len(st.session_state.original):
    dataframe = st.session_state.original

    if 'inicial' not in st.session_state:
        st.session_state.inicial = dataframe

    if dataframe is not None:


        if st.checkbox('Show Event log :page_facing_up:'):
            dataframe


        nodes, metric, perc_act, perc_path = dfg_properties.dfg_options(dataframe)

        cont = 0        

        n = st.sidebar.number_input('Number of manipulation actions :pick:', step=1, min_value=0)
        filtered = pd.DataFrame()
        original = dataframe

        # st.markdown("""---""")


        dic_initial = {}
        dic_initial['Initial'] = original

        dfg_initial = positions_creation.df_to_dfg(dic_initial,nodes,'Absolute frequency')
        positions_creation.threshold(dfg_initial, 'Absolute frequency', 100, 100, nodes)
        

        viz = st.session_state.viz

        # st.write('Initial DFG to fix node positions (DOT engine)')
        # viz



        activity_value = {}


        for line in viz.body:
            if "->" in line or "@@startnode" in line or "@@endnode" in line:
                continue

            match = re.search(r'label="(.+?) \((\d+)\)"', line)
            if match:
                name = match.group(1)
                value = int(match.group(2))
                activity_value[name] = value
        
        st.session_state.viz_labels = activity_value


        id_to_activity = {}

        for line in viz.body:
            line = line.strip()   

            match = re.search(r'^(\S+)\s+\[label="(.+?) \(\d+\)"', line)
            if match:
                node_id = match.group(1)
                activity = match.group(2)
                id_to_activity[node_id] = activity

        edge_dict = {}

        for line in viz.body:
            if "->" not in line:
                continue

            if "@@startnode" in line or "@@endnode" in line:
                continue

            match = re.search(r'(\S+)\s+->\s+(\S+).*label=(\d+)', line)
            if match:

                src_id = match.group(1)
                tgt_id = match.group(2)
                value = int(match.group(3))

                src = id_to_activity.get(src_id)
                tgt = id_to_activity.get(tgt_id)

                if src and tgt:
                    edge_dict[src + ', ' + tgt] = value

        
        st.session_state.viz_edge_labels = edge_dict


        if(n==0):
            filtered={}
            filtered['Initial'] = dataframe
            all_manip = []
        else:
            all_manip = []
            while (cont < n):
                try:
                    manip = manipulation.manipulation_options(dataframe, original, cont)
                    filtered = manipulation.apply_manipulation(dataframe, original, manip, cont+1)
                    all_manip.append(manip)
                    
                except Exception as e:
                    st.error(e)
                    break

                dataframe = filtered
                cont = cont+1
                # st.session_state.var_cont = st.session_state.var_cont+1

                

        st.subheader("Collections of DFGs in memory")
        if st.session_state.collections:

            max_manips = 0
            for data in st.session_state.collections.values():
                max_manips = max(max_manips, len(data.get("manipulation", [])))

            summary = []

            for cid, data in st.session_state.collections.items():

                row_dict = {
                    "Collection ID": f"f{cid}",
                    "Description": data.get("description", ""),
                    "Number of DFGs": len(data["dfgs"])
                }


                manip_list = data.get("manipulation", [])



                if not manip_list:
                    # No hay manipulaciones → celda vacía
                    row_dict["Data Manipulation 1"] = ""
                else:
                    # Hay manipulaciones → agregamos con varID
                    for i, manip in enumerate(manip_list):
                        col_name = f"Data Manipulation {i+1}"   # ahora i varía
                        valor = manip[2]      # valor real
                        var_id = manip[3]     # ID persistente guardado
                        row_dict[col_name] = f"{var_id} <- {manip[0]} {manip[1]} {manip[2]}"
                
                row_dict["Selection"] = data.get("selection", "")



                summary.append(row_dict)

            df_summary = pd.DataFrame(summary)

            cols = [c for c in df_summary.columns if c != "Selection"] + ["Selection"]
            df_summary = df_summary[cols]

            column_config = {col: st.column_config.TextColumn(disabled=True) 
                 for col in df_summary.columns if col != "Description"}
            
            column_config["Description"] = st.column_config.TextColumn()

 
            edited_df = st.data_editor(df_summary, use_container_width=True, hide_index=True, column_config=column_config)


            if st.button("Save descriptions"):
                for _, row in edited_df.iterrows():
                    cid = int(row["Collection ID"][1:])  # quitar la 'f'
                    st.session_state.collections[cid]["description"] = row["Description"]


        else:
            st.info("No collections stored yet.")

        # Mostrar tabla de variables
        if(st.session_state.res_vars):
            st.dataframe(st.session_state.res_vars)



        if( st.sidebar.button('Generate collection of DFGs', type='primary')):
            st.session_state.generate_pressed = True
            st.session_state.run_pattern = False


            if (filtered == {}):
                st.error('No results (no event log subset matches the specified manipulation actions).')
                st.session_state.generate_pressed = False
            else:
                dfgs = dfg_creation.df_to_dfg(filtered,nodes,metric)

                st.session_state.dataframe = dfgs

                st.session_state.collections[st.session_state.id_col] = {
                "dfgs": dfgs,
                "manipulation": all_manip,
                "description": "",
                "datos": filtered
                }


                if(all_manip!=[]):
                    for accion in all_manip:
                        valor = accion[2]
                        var_id = f"v{st.session_state.var_cont_table}"
                        st.session_state.res_vars[var_id] = ", ".join(valor)
                        # st.session_state.res_vars[var_id] = valor
                        st.session_state.var_cont += 1
                        accion.append(var_id)
                        st.session_state.var_cont_table += 1
                st.session_state.id_col += 1
                st.rerun()

        
        st.subheader("Search for specific DFGs")

        options = {
            f"f{cid} {data['description']}": cid
            for cid, data in st.session_state.collections.items()
        }



        selected1 = st.selectbox("Select the collection of interest",
            options=list(options.keys()),key='first_collection',index=None,placeholder="Choose a Collection ID...")
        
        selected2 = st.selectbox("Select an optional collection for comparison",
            options=list(options.keys()),key='second_collection', index=None,placeholder="Choose a Collection ID...")
        
        selected_labels=[selected1, selected2]
        
        # if(len(selected_labels) >= 1):
        selected_ids = [
            options[label]
            for label in selected_labels
            if label is not None
        ]
        
        st.session_state.selected_ids = selected_ids
        # [options[label] for label in selected_labels]
        # -----------------------------------------------


            # if (filtered == {}):
            #     st.error('No results (no event log subset matches the specified manipulation actions).')
            #     st.session_state.generate_pressed = False
            # else:
                # dfgs = dfg_creation.df_to_dfg(filtered,nodes,metric)


                # i=0
                # with st.expander(" **Pattern recommendation**  :bulb:"):

                #     recommendations.pattern_recommendations(filtered, nodes, metric, perc_act, perc_path)
                # with st.expander(" **Pattern specification** :memo:"):
                    
                #     specification.pattern(original, dfgs, nodes, metric, perc_act, perc_path,i)
                # i+=1



        if st.session_state.collections:
            

            if not st.session_state.selected_ids:
                st.warning("Please select at least one collection.")
            else:
                
                if(len(st.session_state.selected_ids) == 1):
                    for i, col_id in enumerate(st.session_state.selected_ids):
                        dfgs = st.session_state.collections[col_id]["dfgs"]

                        selected_dfgs, filtered, pattern, num, param = query_selection.pattern(
                            original,
                            dfgs,
                            nodes,
                            metric,
                            perc_act,
                            perc_path,
                            i, col_id
                        )  

                        # all_manip = st.session_state.collections[col_id]["manipulation"] + "  Result: " + str(list(filtered.keys()))

                elif(len(st.session_state.selected_ids) == 0):
                    st.write("")
                
                else:
                    selected_dfgs, filtered, pattern, num, param = query_selection.pattern_arguments(
                            original,
                            nodes,
                            metric,
                            perc_act,
                            perc_path,
                            i
                        )  

                if("Minimum" in param) or (param=='Minimize'):
                    param="min"
                elif("Maximum" in param) or (param=='Maximize'):
                    param='max'
                    

                if selected_dfgs:
                    # st.subheader("Visualization options")

                    # col1, col2 = st.columns(2)

                    # selected_dfgs = visualization.zoom_fragment(col1, selected_dfgs)
                    # tupla = visualization.search_differences(filtered.keys(), metric, nodes)
                    # colores = dfg_creation.asignar_colores(tupla[1][1])
                    # st.session_state.colores = colores

                    # z, delete_act = visualization.show_activities(col2, original)
                    
                    tupla = ('Existence of activities', ([], []), [], False)
                    delete_act = []

                    copia_dict = copy.deepcopy(selected_dfgs)

                    order_options = ["Mean case duration", "Median cycle time", "Events", "Traces", "Activities", "Variants"]

                    order_by = st.selectbox("Order by:", order_options, index=0, key='order_'+str(0))
                    
                    stats = dfg_creation.threshold(copia_dict, metric, perc_act, perc_path, nodes, tupla, delete_act)
                    dfg_creation.show_DFGs(stats, order_by, metric)


                    first_col_id = st.session_state.selected_ids[0] # la de interes

                    manip_list = st.session_state.collections[first_col_id].get("manipulation", [])


                    if len(manip_list) <= 1:

                        v_asociada = manip_list[0][3]
                        # claves = [", ".join(ast.literal_eval(k)) for k in filtered.keys()]
                        claves = [element for k in filtered.keys() for element in ast.literal_eval(k)]

                        # st.write(v_asociada,claves)

                    else:
                        atributo_to_v = {}
                        atributos = []
                        # atributos = [manip[1][0] for manip in manip_list]
                        atributos = sorted(list(set([manip[1][0] for manip in manip_list])))

                        if "atributo_select_v_estable" not in st.session_state:
                            st.session_state.atributo_select_v_estable = atributos[0]

                        # atributos = list(dict.fromkeys(atributos))  # evita duplicados

                        variables = [manip[3] for manip in manip_list]


                        atributo_seleccionado = st.selectbox(
                            "Select which attribute you want to store in v:",
                            options=atributos, key='atribute_select'
                        )
                        
                        attr_index = atributos.index(atributo_seleccionado)
                        v_asociada = variables[attr_index]

                        # claves = []

                        # for k in filtered.keys():
                        #     parts = k.split(";")
                        #     st.write(parts) 
                        #     parsed_parts = [ast.literal_eval(p.strip()) for p in parts]
                        #     valor = parsed_parts[attr_index]
                        #     claves.append(", ".join(valor))

                        claves = []
                        for k in filtered.keys():
                            parts = k.split(";")
                            parsed_parts = []

                            for p in parts:
                                # Asegurarnos que es string
                                if not isinstance(p, str):
                                    p = str(p)

                                # buscar listas dentro del string
                                listas = re.findall(r"\[.*?\]", p)
                                listas_parseadas = []
                                for l in listas:
                                    try:
                                        listas_parseadas.extend(ast.literal_eval(l))
                                    except Exception as e:
                                        print(f"Error evaluando {l}: {e}")
                                parsed_parts.append(listas_parseadas)

                            valor = parsed_parts[attr_index]  # el índice que necesitas
                            claves.append(", ".join(valor))


                    valor_final = ", ".join(claves)
                
                    if( st.button('Save resulted collection of DFGs', type='primary')):


                        if len(st.session_state.selected_ids) == 1:
                            update_selection(first_col_id, valor_final, pattern, v_asociada, param=param, num=num)
                        else:
                            second_col_id = st.session_state.selected_ids[1]
                            update_selection(first_col_id, valor_final, pattern, v_asociada, param=param, num=num, second_id=second_col_id)

                        st.rerun()
                        st.success(f"Saved collection with ID {st.session_state.id_col}")
                           

                    i=0
                    with st.expander(" **Pattern recommendation**  :bulb:"):

                        recommendations.pattern_recommendations(selected_dfgs, nodes, metric, perc_act, perc_path)      
