# Real_Time_System
Real_Time_System project: Build Content-Centric Networking (CCN)

project1: Build Network topology construction

project2: Build a simple CCN which contains simulator:interest,data,forward,ps,pit table:PS,PIT

project3: Optimize the project2 by adding CS and FIB, then optimize the Interest_queue and Data_queue

For Interest_queue: 
Using DFS to check which package has shortest distance for this node, if queue is full then remove it

For Data_queue: 
Build the table to check the data_hop, if queue is full then remove the max one (just like aging)
