# VISCoPro:  A Tool for Visual Insights Search from Collections of Directly-Follows Graphs

Process mining is a discipline that enables the analysis of business processes from event logs. The Directly-Follows Graph (DFG) is one of the most used visualization types employed in this domain. However, the extraction of valuable information from DFGs requires significant manual effort from users due to the limitations of current process mining tools. To address this challenge, we propose VISCoDFG, a visual query tool designed to ease the manipulation of event logs and the management of DFG collections. The system allows users to query these DFGs to uncover significant insights efficiently. The tool proposed has been developed with Streamlit (https://streamlit.io/), which is a framework that enables the conversion of data Python scripts into shareable web applications.

VISCoPro is available at https://viscopro.streamlit.app/.

### Use case: Find bottlenecks in the process 

Data source: Business Process Intelligence Challenge 2019 Event Log (https://icpmconference.org/2019/icpm-2019/contests-challenges/bpi-challenge-2019/). In this BPI Challenge, there is data from a large multinational company operating from the Netherlands in the field of paints and coatings. Specifically, the event log contains information about the purchasing document management process and four types of data flows. Due to the large size of this dataset, we selected only a subset of cases from this event dataset for the use case, considering only the central cases with less noise. This subset of data contains 50.000 traces, 318.272 events, and 21 attributes.
  
We focused on finding bottlenecks in the process, as this is one of the most studied analysis objectives in process time performance analysis.

1. We open the application and we go to the *Upload file* page and click the *Browse files* button.

![image](https://github.com/msurbano/VISCoPro/assets/92515344/68447597-36b5-4dcf-a709-2b7e64b68ce2)

2. We can examine the event log when it is uploaded.

![image](https://github.com/msurbano/VISCoPro/assets/92515344/4836934d-bca5-450c-b4f4-7245afb692b1)

3. Next we go to the ***Data context*** page where we can define the context of the data. 

![image](https://github.com/msurbano/VISCoPro/assets/92515344/8ba9961c-2858-4b08-840a-d14c1f8e9bb6)

4. To look for bottlenecks in the process, we can focus on identifying certain attribute values that influence the time performance of the process. In this case, we first focus on looking for differences between the 4 types of data flows. Therefore, to manipulate the event log and obtain a set of data subsets, it is necessary to apply one or more manipulation actions by clicking on *+ Number of manipulation actions*.

![image](https://github.com/msurbano/VISCoPro/assets/92515344/9651e6c4-fb58-402a-a957-6f30bfd71b3a)

5. When a manipulation action is added, all its properties are displayed: *Filter type* (in this case, by Attributes), *Filter mode* (in this case, Mandatory, to obtain the traces in which at least one event has a selected value), and the *Value* or values of this attribute. In addition, by clicking on *Group by*, we choose to group the event log by these values instead of filtering. We chose the *case:Item Category* attribute to look for differences between groups of documents according to the type of data flow to which they are linked. In addition, we choose the properties of the resulting collection of DFGs from this set of event log subset. In this case, we use the *concept:name* attribute for the nodes and the *Mean Cycle Time* (Mean CT) metric in the nodes and transitions. 

![image](https://github.com/msurbano/VISCoPro/assets/92515344/7bce3704-b61a-4df3-8378-4219caf54384)

6. Next, by clicking on *Show DFGs*, we can see the resulting collection of visualizations.

![image](https://github.com/msurbano/VISCoPro/assets/92515344/4cca2cc8-af59-4da8-9be6-cddd7d45da12)

7. We access the ***Pattern Specification*** page where the system provides a set of objectives and we select that we are interested in Identifying activities as bottlenecks. Furthermore, we customize the criteria by which the results will be obtained, indicating that we want to identify those DFGs that contain the activity execution with the longest duration of the entire process. The biggest delay in the process is in data flow *3-way match, invoice before GR*.

![image](https://github.com/msurbano/VISCoPro/assets/92515344/35a66402-31cd-4410-8c98-e85942fbd2ad)

8. In addition to the data flow, if we want to know in which type of document this bottleneck occurs, we can add this grouping on the ***Data Context*** page by adding a new manipulation action (*+ Number of manipulation actions*) to group by all values of the *case:Document Type* attribute. In this way, we obtain all the possible pairs of combinations between the two attributes (*case:Item Category* and *case:Document Type*).

![image](https://github.com/msurbano/VISCoPro/assets/92515344/66de6829-3d16-44e6-9551-aa2216898ba6)

9. Finally, if we go back to the ***Pattern Specification*** page, we can see how the execution of the activity with the longest duration is in data flow *3-way match, invoice before GR*, specifically in document type *Standard PO*.

![image](https://github.com/msurbano/VISCoPro/assets/92515344/256f15ea-c973-4d30-ae5d-71775ec41c31)

10. If we zoom in on this DFG, we can see how this delay occurs between activities *Vendor Creates Invoice* and *Create Purchase Order Item*, whose duration is about 7 months.

![image](https://github.com/msurbano/VISCoPro/assets/92515344/55947a9e-5d77-480f-9913-5742e102fcf8)

Furthermore, a video tutorial for this use case is accessible at ...
