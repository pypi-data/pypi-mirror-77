# model_vis

Dynamic Visualization tool for machine learning models that displays the models

## For Users
### Graph Visualization Usage Documentation

#### Usage
`pip install model-vis`<br/>

`python -m graph_visualization.plot_graph`<br/>`--pb_graph_path=`_`path_to_protobuf/protobuf.`_`pb`


Required Parameter:
-- pb_graph_path (str , path to the protobuf file on the system)

[_NOTE : ONLY PASS PROTOBUFS THAT ARE CONVERTED FROM TF_ ]

Optional Parameters :

-- port (int, default port is 5000).

-- pb_graph_type (str , currently only supports "tf" and is default. Other types like .onnx to be supported in future)

#### Interpreting Graph

A graph is created from the protobuf file passed as a parameter and is served on the given _port_no_ .

The nodes are interactive and can be moved around as per convenience.

Edges show name , port, dtype and shape on hover.

Nodes show node types by default and hovering over nodes shows node name and ohter attribute info.

All the information in the graph is contained in graph.json file which can be accessed by going to the URL: **localhost/:_port_no_/graph.json**


#### Features

##### Search

The search bar below the graph window provides a functionality to search for a particular node. The auto suggest drop down appears as you type to help you find the node quicker.  
The search is activated after the 'Highlight Node' button is clicked.
As the node is found, the window auto pans to the particular node being in the centre and it starts a pulse animation to disambiguate the searched node from the cluster.  
Use the 'Shrink Node' button to stop the animation.

##### Find Neighbors

Double click on any node to highlight it's neighboring nodes and respective edges.


##### Control bar

The control bar is present on the top right corner of the page. It can be minimized by clicking the close controls button at the bottom of the control bar. Once the graph becomes static (which is after interacting with a particular node/edge) "Link Distance" , "Link Strength" and "Node Strength" features become unavaialable.

The following configurations can be changed from the control bar which makes live changes to the graph.

###### Link Distance

It specifies how far apart should 2 nodes be from each other.  
The value ranges from 0 to 400. It is better to have a higher value for huge complex graphs.

##### Link Strength

It specifies how strongly the link pulls the other nodes. The value ranges from 0 (repulsion) to 1 (pull).

##### Node Strength

Works similar to Link Strength.  
It specifies how strongly nodes pull each other. The value ranges from -500 (low pull value therefore higher repel) to -1 (Maximum pull).

##### Lazy Load

Only the nodes whose current positions lie in the viewing window are loaded, other node information is known (present in the .json file) but no additional overhead is caused as none of these node or link related elements are shown.

While zooming out , if the zoom out reaches a value where the current window holds more than 500 nodes, the nodes are hidden but the links are visible. This is done to reduce the load.

Conversely, upon zooming in, if the viewing window has < 500 nodes, all the respective node and link elements are shown.

##### Show / Hide Node Labels

A functionality to turn off the node labelling.

##### Color Nodes By

A filter to visualize the nodes based on

1. Error Values
2. None (Same color to all nodes)

##### Restart

Restarts the given graph by reloading.

#### Libraries Used

The graph visualization is based on Node JS and the visualization library [D3](https://d3js.org).

## For Developers/ Contributors

### Requirements

#### 1. Clone the repo from github

#### 2. Conda (using Miniconda)

###### Setup Miniconda

Install Miniconda3 using [these instructions](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html)

Create the virtual environment and activate it

```
model_vis$ conda env create -f environment.yml
model_vis$ conda activate vis-env
(vis-env) model_vis $
```

#### 3. Bazel
[Bazel](https://www.bazel.build) can be installed with [Bazelisk](https://docs.bazel.build/versions/master/install-bazelisk.html) , it downloads the appropriate bazel version for the current working directory.

###### Create symbolic link to use bazelisk whenever "bazel" is called
```ln -s $(which bazelisk) bazel```

### Running the file (thorugh bazel)
`bazel run //graph_visualization:plot_graph`<br/>` -- --pb_graph_path=`_`abs_path_to_protobuf/protobuf.`_`pb`<br/>`--port=`_`port_no`<br/>_

Required Parameters:
-- pb_graph_path (str , path to the protobuf file on the system)

[_NOTE : ONLY PASS PROTOBUFS THAT ARE CONVERTED FROM TF_ ]

Optional Parameters :

-- port (int, default port is 5000).

-- pb_graph_type (str , currently only supports "tf" and is default. Other types like .onnx to be supported in future)