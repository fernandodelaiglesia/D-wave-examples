# Requiere: boto3, amazon-braket-sdk, dwave-ocean-sdk, amazon-braket-ocean-plugin
# boto3:OK
# amazon-braket-sdk: OK
# dwave-ocean-sdk: OK
# amazon-braket-ocean-plugin: OK

import boto3

# Import Braket SDK
from braket.aws import AwsDevice
from braket.ocean_plugin import BraketSampler, BraketDWaveSampler

import os

os.environ['AWS_DEFAULT_REGION'] = "us-west-2"
#aws_account_id = boto3.client("sts", **sessiona).get_caller_identity()["Account"]

# Import DWave stuff
import matplotlib.pyplot as plt
# magic word for producing visualizations in notebook
#%matplotlib inline
import networkx as nx
import dwave_networkx as dnx
from dwave.system.composites import EmbeddingComposite
import neal # Para el simulador


# Please enter the S3 bucket you created during onboarding in the code below
my_bucket = f"yourbucket" # the name of the bucket
my_prefix = "YourFolder" # the name of the folder in the bucket
s3_folder = (my_bucket, my_prefix)

device = AwsDevice("arn:aws:braket:::device/qpu/d-wave/DW_2000Q_6")
print('Device:', device)


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

###sampler = neal.SimulatedAnnealingSampler() # Usando el simulador

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