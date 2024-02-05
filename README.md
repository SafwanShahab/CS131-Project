# CS131-Project
Phase 1: Proposal
<br> Team 30 Members: 
<br> Logan McGuire(SID:862307006)
<br> Safwan Shahab(SID:862203942)

Project description and use case:
The goal is to build an edge computing system that allows for the early autonomous detection of dangerous falls in elderly people. This could be a useful system to employ in the healthcare sector, and could be deployed in a care facility or in residence. The main challenges would be to construct a system that is competent at analyzing visual input data and accurately identifying a fall. 

Solution:
The system would include a network of cameras set up in the patient’s home or care facility. Each camera will be linked to a small edge device where visual data is recorded. The edge nodes take the recorded data and send relevant parameters to the cloud server. From there the cloud inputs the parameters into a deep learning model to detect falls. If a fall is detected, the cloud can notify family members, caregivers, or relevant authorities of the incident. 

Demo:
As a proof of concept we can make use of the equipment we have access to for labs, including the jetson nano and cameras. If necessary, we could set up a connection to a desktop server and transmit the data from the jetson device to this server. The jetson device would transmit the relative parameters to the server where the computing resources of the server would handle the analysis. In practice, the Jetson nano may be capable of performing all relevant tasks by itself. However, the actual implementation of this solution would probably involve edge devices with far less computational power. In the experiential phase however, it may be sufficient to perform everything on the jetson nano. 

Task distribution:
As previously mentioned, this system would collect data on the edge nodes and perform other relevant computation on the cloud server. More specifically, the edge nodes take in visual data and upload the relevant parameters to the cloud. From there the cloud uses a deep learning model to detect falls and identify if action is needed. 
