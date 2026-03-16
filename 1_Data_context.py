import streamlit as st
import numpy as np
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

if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame({
        "Name": [""],
        "Filter": [""],
        "Nodes": [""],
        "Metrics": [""],
        "%P": [0.0],
        "%A": [0.0],
        "Selection": [""]
    })

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


# ------------------------------------------------------------------------------------------------

mensaje_container = st.empty()
sample_data = []
df = load_data.cargar_datos(mensaje_container, sample_data)
dic_original = {}


#  ------------------------------------------------------------------------------------------------
# Elementos de la interfaz
#  ------------------------------------------------------------------------------------------------
    
# tab1, tab2 = st.tabs(["Comparative features", "Queries"])

# with tab1:


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

        st.markdown("""---""")


        dic_initial = {}
        dic_initial['Initial'] = original

        dfg_initial = positions_creation.df_to_dfg(dic_initial,nodes,'Absolute frequency')
        # positions_creation.nodes_edges(dfg_initial, 'Absolute frequency', 100, 100, nodes)
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
        else:
            while (cont < n):
                try:
                    manip = manipulation.manipulation_options(dataframe, original, cont)
                    filtered = manipulation.apply_manipulation(dataframe, original, manip)
                    
                except Exception as e:
                    st.error(e)
                    break

                dataframe = filtered
                cont = cont+1



        # col1, col2, col3, col4 = st.columns(4)
        col1, col2 = st.columns(2)
        filtered = visualization.zoom_fragment(col1, filtered)
    
        left_column, right_column = st.columns([1, 6])

        if( st.sidebar.button('Generate collection of DFGs', type='primary')):
            st.session_state.generate_pressed = True
            st.session_state.run_pattern = False
        
        
        if st.session_state.generate_pressed :

            tupla = visualization.search_differences(filtered.keys(), metric, nodes)
            colores = dfg_creation.asignar_colores(tupla[1][1])
            st.session_state.colores = colores

            z, delete_act = visualization.show_activities(col2, original)

            # filtered = visualization.zoom_fragment(filtered)

            if (filtered == {}):
                st.error('No results (no event log subset matches the specified manipulation actions).')
                st.session_state.generate_pressed = False
            else:

                st.markdown("""---""")
                
                dfgs = dfg_creation.df_to_dfg(filtered,nodes,metric)
                # st.write(dfgs.items())
                st.session_state.dataframe = dfgs
                copia_dict = copy.deepcopy(dfgs)

                # if( st.button('Save collection of DFGs', type='primary')):
                #     st.session_state.collections[st.session_state.id_col] = dfgs
                #     st.success(f"Saved collection with ID {st.session_state.id_col}")
                #     st.session_state.id_col += 1

                left_column, right_column = st.columns(2)
                order_options = ['By the search', "Mean case duration", "Median cycle time", "Number of events", "Number of traces", "Number of activities", "Number of variants", "Rework of cases"]
                order_by = left_column.selectbox("Order by:", order_options, index=6, key='context_order') 
                
                
                stats = dfg_creation.threshold(copia_dict, metric, perc_act, perc_path, nodes, tupla, delete_act)
                # st.write(stats)
                # for g in stats:
                #     g["svg_path"]
                dfg_creation.show_DFGs(stats, order_by, metric)


                i=0
                with st.expander(" **Pattern recommendation**  :bulb:"):

                    recommendations.pattern_recommendations(filtered, nodes, metric, perc_act, perc_path)
                with st.expander(" **Pattern specification** :memo:"):
                    
                    specification.pattern(original, dfgs, nodes, metric, perc_act, perc_path,i)
                i+=1
            
            # if st.session_state.save_pressed :
                # st.session_state.collections[id_col] = dfgs
            
        st.subheader("Collections in memory")

        description = st.text_input(
            "Collection description",
            placeholder="e.g. High throughput variants"
        )

        if( st.button('Save collection of DFGs', type='primary')):
            st.session_state.collections[st.session_state.id_col] = {
                        "dfgs": dfgs,
                        "description": description
                    }
            st.success(f"Saved collection with ID {st.session_state.id_col}")
            st.session_state.id_col += 1

        if st.session_state.collections:
            summary = []
            for cid, data in st.session_state.collections.items():
                summary.append({
                    "Collection ID": cid,
                    "Number of DFGs": len(data["dfgs"]),
                    "Description": data.get("description", "")
                })

            df_summary = pd.DataFrame(summary)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)

            st.markdown("---")

            # -------- Select collections (0–2) --------
            options = {
                f"{cid} – {data['description']}": cid
                for cid, data in st.session_state.collections.items()
            }

            selected_labels = st.multiselect(
                "Select up to 2 collections for pattern specification",
                options=list(options.keys()),
                max_selections=2,
                key="collection_multiselect"
            )

            # Guardamos la selección en session_state
            st.session_state.selected_ids = [options[label] for label in selected_labels]

            # -------- Run button --------
            if st.button("Run pattern specification", type="primary"):
                if not st.session_state.selected_ids:
                    st.warning("Please select at least one collection.")
                else:
                    st.session_state.run_pattern = True

            if st.session_state.run_pattern:
                if(len(st.session_state.selected_ids) == 1):
                    for i, col_id in enumerate(st.session_state.selected_ids):
                        selected_dfgs = st.session_state.collections[col_id]["dfgs"]

                        dfgs = query_selection.pattern(
                            original,
                            selected_dfgs,
                            nodes,
                            metric,
                            perc_act,
                            perc_path,
                            i, col_id
                        )  

                        if dfgs:
                            description = st.text_input(
                                "Collection description",
                                placeholder="e.g. High throughput variants", key='text_'+str(i)
                            )

                            if( st.button('Save resulted collection of DFGs', type='primary')):
                                st.session_state.collections[st.session_state.id_col] = {
                                            "dfgs": dfgs,
                                            "description": description
                                        }
                                st.success(f"Saved collection with ID {st.session_state.id_col}")
                                st.session_state.id_col += 1
                            
                                st.rerun()
                            
                elif(len(st.session_state.selected_ids) == 0):
                    st.write("")
                
                else:
                    dfgs = query_selection.pattern_arguments(
                            original,
                            nodes,
                            metric,
                            perc_act,
                            perc_path,
                            i
                        )    
        

                    if dfgs:
                        description = st.text_input(
                            "Collection description",
                            placeholder="e.g. High throughput variants", key='text_'+str(i)
                        )

                        if( st.button('Save resulted collection of DFGs', type='primary')):
                            st.session_state.collections[st.session_state.id_col] = {
                                        "dfgs": dfgs,
                                        "description": description
                                    }
                            st.success(f"Saved collection with ID {st.session_state.id_col}")
                            st.session_state.id_col += 1
                        
                            st.rerun()
                                
            
        else:
            st.info("No collections stored yet.")  


                    
                
# with tab2:

#     i=0
#     res_queries = {}
#     vars = {}

#     if len(st.session_state.original):
#         dataframe = st.session_state.original

#         if 'inicial' not in st.session_state:
#             st.session_state.inicial = dataframe



#         if dataframe is not None:

#             if st.button("Create query"):
#                 st.session_state.show_table = True

#             if st.session_state.show_table:
#                 edited_df = st.data_editor(
#                     st.session_state.table_data,
#                     num_rows="dynamic",
#                     use_container_width=True,
#                     key="editor"
#                 )


#             if st.session_state.show_table:
#                 if st.button("Run query"):
#                     st.session_state.table_data = edited_df
#                     st.success("Saved")

#                     tabla = st.session_state.table_data

#                     for index, row in tabla.iterrows():
                        
#                         nombre = row['Name']
#                         filtro = row['Filter']
#                         nodos = row['Nodes']
#                         metrica = row['Metrics']
#                         perc_p = row['%P']
#                         perc_a = row['%A']
#                         selection = row['Selection']

#                         mode  = re.search(r'\[(.*?)\]', filtro)
#                         mode = mode.group(1) if mode else None

#                         if("<-" in filtro):
#                             atributo = re.search(r'[\"“”]([^\"“”]+)[\"“”]', filtro)
#                             atributo = atributo.group(1) if atributo else None

#                             valores = re.search(r'\.\s*(.+)$', filtro)
#                             valores = valores.group(1) if valores else None

#                             var_filtro = re.search(r'(\w+)\s*<-', filtro)
#                             var_filtro = var_filtro.group(1) if var_filtro else None

#                             vars[var_filtro] = (atributo, valores)

#                         else:
#                             var_filtro = re.search(r'\]\s*(\w+)', filtro)
#                             var_filtro = var_filtro.group(1) if var_filtro else None

#                             tupla = vars.get(var_filtro)
#                             atributo = tupla[0]
#                             valores = tupla[1]


#                         if (valores == "*"):
#                             valores = "* All values"
#                             agrup = True
#                         else:
#                             agrup = True


#                         if isinstance(valores, list):
#                             manip = [mode, [atributo, agrup], valores]
#                         else:
#                             manip = [mode, [atributo, agrup], [valores]]

#                         if(nodos == "" or nodos==None):
#                             nodos = "concept:name"


#                         try:
#                             filtered = manipulation.apply_manipulation(dataframe, dataframe, manip)
                                    
#                         except Exception as e:
#                             st.error(e)
                    
#                         try:
#                             dfgs = dfg_creation.df_to_dfg(filtered,nodos,metrica)
#                             st.session_state.collections[nombre] = dfgs
#                         except Exception as e:
#                             st.error(f"Error: '{nodos}' is not one of the attributes.")

#                         res_queries[nombre] = dfgs


#                         if(selection != "" and selection is not None):

#                             parts = selection.split("<-", 1)
#                             var_selection = parts[0].strip()
                            
#                             resto = parts[1].strip()

#                             idx_par = resto.index("(")
#                             operador_var = resto[:idx_par] 
#                             operador, var_entrada = operador_var.split("_", 1)

#                             atributo,valor = vars[var_entrada.strip()]

#                             resto = resto[idx_par:]

#                             m = re.match(r'\(([^)]*)\)(.*)', resto)
#                             parametros = m.group(1)
#                             resto = m.group(2)

#                             m = re.search(r'(\w+)\s*\(([^)]*)\)', resto)
#                             funcion = m.group(1)
#                             id_coll = m.group(2)

                    #         if(funcion == 'numberOfNodes'):
                    #             selected, selected_data = query_selection.function_numberOfNodes(dfgs, operador, parametros)
                    #         else:
                    #             st.error('Incorrect function name. try with: numberOfNodes, ...')

                    #         keys = [
                    #             ast.literal_eval(k)[0]
                    #             for k in selected_data.keys()
                    #         ]       
                            
                    #         vars[var_selection] = (atributo, keys)
                            
                    #     if("*" in nombre):
                    #         # i=i+1
                    #         copia_dict = copy.deepcopy(dfgs)
                            
                    #         stats = query_selection.threshold(copia_dict, metric, perc_act, perc_path, nodes)
                    #         query_selection.show_DFGs(stats, "Activities", metric, selected_data)
                            
                    # st.session_state.collections = res_queries
                    # st.session_state.variables = vars



