import streamlit as st
import pm4py
from pm4py.statistics.rework.cases.pandas import get as rework_cases

i=0
j=0

def small_text(text):
    return f"<p style='font-size:12px; color:grey; font-style:italic;'>{text}</p>"

def search_differences(keys, metric, nodes):

    df = st.session_state.original
    
    col11, col12 = st.columns(2)

    if(nodes=='org:resource'):
        if(metric in ["Median Cycle Time","Mean Cycle Time","StDev Cycle Time","Total Cycle Time"]):
            search = col11.selectbox('Action', ('Select an action...', 'Identify resources by duration', 'Identify transitions by duration',
                                            'Identify interchanged resources', 'Identify groups of resources',
                                            'Identify shared endpoint nodes', 'Identify missing endpoint nodes',  'Identify exclusive endpoint nodes',
                                            'Identify shared startpoint nodes', 'Identify missing startpoint nodes',  'Identify exclusive startpoint nodes', 
                                            'Identify shared control-flow elements', 'Identify exclusive control-flow elements', 'Identify missing control-flow elements'))                                        
        else:
            search = col11.selectbox('Action', ('Select an action...', 'Identify resources by frequency', 'Identify transitions by frequency',
                                            'Identify interchanged resources', 'Identify groups of resources',
                                            'Identify shared endpoint nodes', 'Identify missing endpoint nodes',  'Identify exclusive endpoint nodes',
                                            'Identify shared startpoint nodes', 'Identify missing startpoint nodes',  'Identify exclusive startpoint nodes', 
                                            'Identify shared control-flow elements', 'Identify exclusive control-flow elements', 'Identify missing control-flow elements'))
    else:
    
        if(metric in ["Median Cycle Time","Mean Cycle Time","StDev Cycle Time","Total Cycle Time"]):
            search = col11.selectbox('Action', ('Select an action...', 'Identify activities by duration', 'Identify transitions by duration',
                                            'Identify interchanged activities', 'Identify groups of activities',
                                            'Identify shared endpoint nodes', 'Identify missing endpoint nodes',  'Identify exclusive endpoint nodes',
                                            'Identify shared startpoint nodes', 'Identify missing startpoint nodes',  'Identify exclusive startpoint nodes', 
                                            'Identify shared control-flow elements', 'Identify exclusive control-flow elements', 'Identify missing control-flow elements'))                                        
        else:
            search = col11.selectbox('Action', ('Select an action...', 'Identify rework of activities', 'Identify the most frequent process fragment', 
                                            'Identify activities belonging to a process fragment',
                                            'Identify the most frequent activities', 'Identify infrequent activities',
                                            'Identify activities by frequency', 'Identify transitions by frequency',
                                            'Identify interchanged activities', 'Identify groups of activities',
                                            'Identify shared endpoint nodes', 'Identify missing endpoint nodes',  'Identify exclusive endpoint nodes',
                                            'Identify shared startpoint nodes', 'Identify missing startpoint nodes',  'Identify exclusive startpoint nodes', 
                                            'Identify shared control-flow elements', 'Identify exclusive control-flow elements', 'Identify missing control-flow elements'))
                                        
    explanations = {
                'Select an action...' : "",
                'Identify rework of activities' : "Highlights nodes corresponding to activities executed more than once within a case.",
                'Identify the most frequent process fragment': "Highlights nodes in orange that belong to the process fragment with the highest case frequency.", 
                'Identify activities belonging to a process fragment': "Highlights nodes in orange that belong to a specific part of the process between activity A and B.",
                'Identify the most frequent activities' : "Highlights nodes in orange that correspond to activities with the highest case frequency.",
                'Identify infrequent activities' : "Highlights nodes in orange that correspond to activities with the lowest case frequency.",
                'Identify interchanged resources': "Highlights pairs of resources that appear in opposite execution order compared to the reference model, excluding concurrent relations.",
                'Identify groups of resources' : "Highlights selected groups of resources with the same or different colors.",
                'Identify resources by duration': "Highlights nodes in light orange when their duration is lower than in the reference model, and in dark orange when it is higher.",
                'Identify activities by duration': "Highlights nodes in light orange when their duration is lower than in the reference model, and in dark orange when it is higher.",
                'Identify resources by frequency': "Highlights nodes in light orange when their frequency is lower than in the reference model, and in dark orange when it is higher.",
                'Identify groups of activities' : "Highlights selected groups of activities with the same or different colors.",
                'Identify interchanged activities': "Highlights pairs of activities that appear in opposite execution order compared to the reference model, excluding concurrent relations.",
                'Identify transitions by frequency': "Highlights edges in light orange when their frequency is lower than in the reference model, and in dark orange when it is higher.",
                'Identify transitions by duration': "Highlights edges in light orange when their duration is lower than in the reference model, and in dark orange when it is higher.",
                'Identify activities by frequency' : "Highlights nodes in light orange when their frequency is lower than in the reference model, and in dark orange when it is higher.",
                'Identify missing endpoint nodes': "Highlights missing endpoint nodes between DFGs using a reference model, which could be the entire process or a DFG from the collection.",
                'Identify exclusive endpoint nodes': "Highlights exclusive endpoint nodes between DFGs using a reference model, which could be the entire process or a DFG from the collection.",
                'Identify shared endpoint nodes': "Highlights common endpoint nodes between DFGs using a reference model, which could be the entire process or a DFG from the collection.",
                'Identify missing startpoint nodes': "Highlights missing startpoint nodes between DFGs using a reference model, which could be the entire process or a DFG from the collection.",
                'Identify exclusive startpoint nodes': "Highlights exclusive startpoint nodes between DFGs using a reference model, which could be the entire process or a DFG from the collection.",
                'Identify shared startpoint nodes': "Highlights common startpoint nodes between DFGs using a reference model, which could be the entire process or a DFG from the collection.",
                'Identify shared control-flow elements': "Highlights common nodes and edges between DFGs using a reference model, which could be the entire process or a DFG from the collection.",
                'Identify exclusive control-flow elements': "Highlights exclusive nodes and edges between DFGs using a reference model, which could be the entire process or a DFG from the collection.",
                'Identify missing control-flow elements': "Highlights missing nodes and edges between DFGs using a reference model, which could be the entire process or a DFG from the collection."
            }
    
    col11.markdown(small_text(explanations[search]), unsafe_allow_html=True)
    add = False

    # color_selectbox(2, 'green')

    if(search == 'Identify groups of activities'):
        mode = col12.selectbox('Mode',('All included', 'Some included'), label_visibility="hidden")
        values = col11.multiselect('Activities', df['concept:name'].unique(), label_visibility="hidden")
        color_mode = col11.radio('Color', ['Same color', 'Different color'], horizontal=True)
        explanations = {
                'Same color': "Use only one color for all the activities selected.",
                'Different color': "Use a different color to highlight each activity selected."
            }
        col11.markdown(small_text(explanations[color_mode]), unsafe_allow_html=True)
        search = 'Existence of activities'
    
    elif(search == 'Identify groups of resources'):
        mode = col12.selectbox('Mode',('All included', 'Some included'), label_visibility="hidden")
        values = col11.multiselect('Resources', df['org:resource'].unique(), label_visibility="hidden")
        color_mode = col11.radio('Color', ['Same color', 'Different color'], horizontal=True)
        explanations = {
                'Same color': "Use only one color for all the resources selected.",
                'Different color': "Use a different color to highlight each resource selected."
            }
        col11.markdown(small_text(explanations[color_mode]), unsafe_allow_html=True)
        search = 'Existence of activities'

    # elif(search == 'Stable parts'):
        # mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        # values = []
        # if(mode=='Whole process'):
        #     color_mode = col2.multiselect('Highlight', ['Similarities',  'Differences reference model'], 
        #                               placeholder='Choose some options')
        # else:
        #     color_mode = col2.multiselect('Highlight', ['Similarities', 'Differences DFG', 'Differences reference model'], 
        #                               placeholder='Choose some options')
        #     if('Similarities' in color_mode and 'Differences DFG' in color_mode and 'Differences reference model' in color_mode):
        #         add = col3.checkbox('Show the activities of the whole process')

    elif(search == 'Select an action...'):
        mode = []
        values = []
        color_mode = []
        search = 'Existence of activities'

    elif(search == 'Identify shared control-flow elements'):
        mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        values = []
        color_mode = 'Similarities'
        search = 'Stable parts'
        
    elif(search == 'Identify exclusive control-flow elements'):
        mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        values = []
        if(mode=='Whole process'):
            color_mode = ''
        else:
            color_mode = 'Differences DFG'
        search = 'Stable parts'
        
    elif(search == 'Identify missing control-flow elements'):
        mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        values = []
        color_mode = 'Differences reference model'
        search = 'Stable parts'

    elif(search == 'Identify shared startpoint nodes'):
        mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        values = []
        color_mode = 'Similarities'
        search='Identify startpoint nodes'

    elif(search == 'Identify exclusive startpoint nodes'):
        mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        values = []
        if(mode=='Whole process'):
            color_mode = ''
        else:
            color_mode = 'Differences DFG'
        search='Identify startpoint nodes'

    elif(search == 'Identify missing startpoint nodes'):
        mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        values = []
        color_mode = 'Differences reference model'
        search='Identify startpoint nodes'

    elif(search == 'Identify shared endpoint nodes'):
        mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        values = []
        color_mode = 'Similarities'
        search='Identify endpoint nodes'

    elif(search == 'Identify exclusive endpoint nodes'):
        mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        values = []
        if(mode=='Whole process'):
            color_mode = ''
        else:
            color_mode = 'Differences DFG'
        search='Identify endpoint nodes'

    elif(search == 'Identify missing endpoint nodes'):
        mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        values = []
        color_mode = 'Differences reference model'
        search='Identify endpoint nodes'

    elif(search == 'Identify activities by frequency'):
        mode = col12.selectbox('Reference model', ['Specific value' , 'Whole process'] + list(keys))
        if(mode=='Specific value'):
            values = col12.number_input("Insert a frequency value")
            values = [values]
        else:
            values = []
        color_mode = []

    elif(search == 'Identify activities by duration'):
        mode = col12.selectbox('Reference model', ['Specific value' , 'Whole process'] + list(keys))
        if(mode=='Specific value'):
            values = col12.number_input("Insert a time value in minutes")
            values = [values]
        else:
            values = []
        color_mode = []
        search = 'Identify activities by frequency'

    elif(search == 'Identify resources by frequency'):
        mode = col12.selectbox('Reference model', ['Specific value' , 'Whole process'] + list(keys))
        if(mode=='Specific value'):
            values = col12.number_input("Insert a frequency value")
            values = [values]
        else:
            values = []
        color_mode = []
        search = 'Identify activities by frequency'

    elif(search == 'Identify transitions by frequency'):
        mode = col12.selectbox('Reference model', ['Specific value' , 'Whole process'] + list(keys))
        if(mode=='Specific value'):
            values = col12.number_input("Insert a frequency value")
            values = [values]
        else:
            values = []
        color_mode = []

    elif(search == 'Identify the most frequent activities'):
        mode = col12.number_input('Top-k most frequent activities', step=1, min_value=1)
        values = top_k_activities_case_frequency(mode, False)
        st.markdown("**Most frequent activities:**")
        st.info(
            ", ".join(f"**{a}**" for a in values)
        )
        color_mode = []
        search = 'Identify activities by frequency'
    
    elif(search == 'Identify infrequent activities'):
        mode = col12.number_input('Top-k infrequent activities', step=1, min_value=1)
        values = top_k_activities_case_frequency(mode, True)
        st.markdown("**Less frequent activities:**")
        st.info(
            ", ".join(f"**{a}**" for a in values)
        )
        color_mode = []
        search = 'Identify activities by frequency'

    elif(search == 'Identify transitions by duration'):
        mode = col12.selectbox('Reference model', ['Specific value' , 'Whole process'] + list(keys))
        if(mode=='Specific value'):
            values = col12.number_input("Insert a time value in minutes")
            values = [values]
        else:
            values = []
        color_mode = []   
        search = 'Identify transitions by frequency'

    elif(search == 'Identify interchanged activities'):
        mode = col12.selectbox('Reference model', list(keys))
        values = []
        color_mode = []
    
    elif(search == 'Identify interchanged resources'):
        mode = col12.selectbox('Reference model', list(keys))
        values = []
        color_mode = []
        search = 'Identify interchanged activities'

    elif(search == 'Identify the most frequent process fragment'):
        mode = col12.number_input('Number of activities', step=1, min_value=3)
        values = most_frequent_fragments(mode)
        st.markdown("**Most frequent process fragment:**")
        st.info(
            " → ".join(f"**{a}**" for a in values)
        )
        color_mode = []
        # search = 'Identify activities by frequency' # incluir esto si quiero "Some included" en vez de "All includad"

    elif(search == 'Identify activities belonging to a process fragment'):
        mode = ''
        df = st.session_state.original
        act1 = col12.selectbox('From', df['concept:name'].unique(), key='from'+str(i))
        act2 = col12.selectbox('To', df['concept:name'].unique(), key='to'+str(i))
        values = [act1, act2]
        color_mode = [] 

    elif(search == 'Identify rework of activities'):
        # mode = col12.selectbox('Reference model', ['Whole process'] + list(keys))
        mode=''
        # rework = rework_log()
        values = []
        color_mode = []

    else:
        values = []
        mode=''
        color_mode=False
    
    # st.write(search, mode, values, color_mode)
    return (search, (mode,values), color_mode, add)

from collections import defaultdict

def rework_log():
    df = st.session_state.original

    rework = rework_cases.apply(df, parameters={
        "case_id_key": "case:concept:name",
        "activity_key": "concept:name"
    })

    total_rework = sum(v.get("rework", 0) for v in rework.values())
    total_activities = sum(v.get("number_activities", 0) for v in rework.values())

    return total_rework / total_activities if total_activities > 0 else 0.0


def most_frequent_fragments(fragment_len):
    """
    Returns the top-k most frequent fragments (case frequency).
    A fragment is a contiguous sequence of activities.
    """
    df = st.session_state.original
    # case -> ordered list of activities
    traces = (
        df.sort_values("time:timestamp")
          .groupby("case:concept:name")["concept:name"]
          .apply(list)
    )

    fragment_cases = defaultdict(set)

    for case_id, trace in traces.items():
        seen_in_case = set()

        for i in range(len(trace) - fragment_len + 1):
            fragment = tuple(trace[i:i + fragment_len])
            seen_in_case.add(fragment)

        for fragment in seen_in_case:
            fragment_cases[fragment].add(case_id)

    # fragment with highest case frequency
    most_frequent = max(
        fragment_cases.items(),
        key=lambda x: len(x[1])
    )[0]

    return list(most_frequent)

def top_k_activities_case_frequency(k, bool):
    """
    Returns the top-k activities by case frequency.
    """

    df = st.session_state.original
    case_freq = (
        df.groupby("concept:name")["case:concept:name"]
          .nunique()
          .sort_values(ascending=bool)
           .head(k)
            .index
             .tolist() # false: most freq
    )

    return case_freq


def zoom_fragment(col1, dic):
    df = st.session_state.original
    filtered_dataframe={}
    # col1, col2, col3, col4 = st.columns(4)


    z = col1.selectbox('Fragment focusing', ('Whole process','Select fragment'))
    if(z=='Select fragment'):
        z='Zoom subprocess'
    col11, col12 = col1.columns(2)
    if(z=='Zoom subprocess'):

        # col12, col22 = col2.columns(2)
        activityFROM = col11.selectbox('From', df['concept:name'].unique())
        # ("visible", "hidden", or "collapsed"))
        activityTO = col12.selectbox('To', df['concept:name'].unique(), index=len(df['concept:name'].unique())-1)

        for key,group in dic.items():
                    
            filt = pm4py.filter_between(group, 
                        activityFROM,activityTO, activity_key='concept:name', 
                                case_id_key='case:concept:name', timestamp_key='time:timestamp')
            if(len(filt)!=0):
                if(key==''):
                    filtered_dataframe[str(activityFROM) + " -- " + str(activityTO)] = filt
                else:
                    filtered_dataframe[key + " " + str(activityFROM) + " -- " + str(activityTO)] = filt
    else:
        filtered_dataframe = dic


    return filtered_dataframe
                
def show_activities(col2, df):
    delete_act = set()
    # col1, col2, col3, col4 = st.columns(4)
    z = col2.selectbox('Activity hiding', ('All activities', 'Hide activities', 'Filter events by activities'), key='act_delete')
    if(z=='Hide activities'):
        delete_act = col2.multiselect('Activities to hide', df['concept:name'].unique(), label_visibility="hidden", key='delete')
    # elif(z=='Filter events by activities'):
    #     delete_act = col2.multiselect('Activities to keep', df['concept:name'].unique(), label_visibility="hidden", key='delete')

    return z, delete_act

def filter_events(dic, act):
    filtered_subsets = {}
    
    for key,subset in dic.items():
        grupo = pm4py.filter_event_attribute_values(subset, 'concept:name', act, retain=False, level='event')
        if(len(grupo)!=0):
            filtered_subsets[key] = grupo

    return filtered_subsets, []



    
    

    









