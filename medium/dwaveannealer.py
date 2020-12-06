# AWS import Boto3
import boto3

import os

# Each device is loacated in a specific region. us-west-2 is where Dwave device is located
os.environ['AWS_DEFAULT_REGION'] = "us-west-2"

# AWS imports: Import Braket SDK modules
from braket.ocean_plugin import BraketSampler, BraketDWaveSampler
from braket.aws import AwsDevice

# Import D-Wave stuff
import networkx as nx
import dwave_networkx as dnx
from dwave.system.composites import EmbeddingComposite
# Import the popular matplotlib for graphics
import matplotlib.pyplot as plt

# When running in real QPU you must enter the S3 bucket you created during onboarding to Braket in the code as follows
my_bucket = f"amazon-braket-your-bucket" # the name of the bucket
my_folder = "YourFolder" # the name of the folder in the bucket
s3_folder = (my_bucket, my_folder)

# set up device
device = AwsDevice("arn:aws:braket:::device/qpu/d-wave/DW_2000Q_6")

execution_windows = device.properties.service.executionWindows
print(f'{device.name} availability windows are:\n{execution_windows}\n')

# Define the graph
# Create empty graph
G = nx.Graph()

# Add edges to graph - this also adds the nodes
G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (6, 7)])

# Visualize the original graph
pos = nx.spring_layout(G)
plt.figure()
nx.draw_networkx(G, pos=pos, with_labels=True)
plt.show()

#Instanciate the sampler and do the magic
sampler = BraketDWaveSampler(s3_folder,'arn:aws:braket:::device/qpu/d-wave/DW_2000Q_6')
sampler = EmbeddingComposite(sampler)

# Find the maximum independent set, S
S = dnx.maximum_independent_set(G, sampler=sampler, num_reads=10)


# Print the solution for the user
print('Maximum independent set size found is', len(S))
print(S)

# Visualize the results
k = G.subgraph(S)
notS = list(set(G.nodes()) - set(S))
othersubgraph = G.subgraph(notS)
plt.figure()
nx.draw_networkx(G, pos=pos, with_labels=True)
nx.draw_networkx(k, pos=pos, with_labels=True, node_color='r', font_color='k')
nx.draw_networkx(othersubgraph, pos=pos, with_labels=True, node_color='b', font_color='w')
plt.show()
