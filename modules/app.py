import streamlit as st
import pandas as pd
from neo4j import GraphDatabase
from streamlit_agraph import agraph, Node, Edge

import requests
import json
from AutoClean import AutoClean
from langchain.schema import Document
from langchain.document_loaders import CSVLoader 
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.llms import Ollama
from langchain_community.graphs import Neo4jGraph

class Config:
  def __init__(self, height=750, width=750, directed=True, physics=True, hierarchical=False, from_json=None, **kwargs):
    self.height = f"{height}px"
    self.width = f"{width}px"
    if not directed:
      self.edges = {"arrows":"none"}

    # https://visjs.github.io/vis-network/docs/network/physics.html#
    self.physics = {"enabled": physics,
                    "solver":kwargs.get("solver", "barnesHut"),
                    "minVelocity":kwargs.get("minVelocity", 1),
                    "maxVelocity":kwargs.get("maxVelocity", 100),
                    "stabilization":{
                      "enabled": kwargs.get("stabilization", True),
                      "fit":kwargs.get("fit", True),
                      },
                    "timestep":kwargs.get("timestep", 0.5),
                    }
    # https://visjs.github.io/vis-network/docs/network/layout.html
    self.layout = {
        "hierarchical": {
          "enabled":hierarchical,
          "levelSeparation": kwargs.get("levelSeparation", 150),
          "nodeSpacing": kwargs.get("nodeSpacing", 100),
          "treeSpacing": kwargs.get("treeSpacing", 200),
          "blockShifting": kwargs.get("blockShifting", True),
          "edgeMinimization": kwargs.get("edgeMinimization", True),
          "parentCentralization": kwargs.get("parentCentralization", True),
          "direction": kwargs.get("direction", "UD"),        # UD, DU, LR, RL
          "sortMethod": kwargs.get('sortMethod', "hubsize"),  # hubsize, directed
          "shakeTowards": kwargs.get('shakeTowards', 'roots')  # roots, leaves
      }
    }
    self.groups = kwargs.get("groups", None)

    self.__dict__.update(**kwargs)

    if from_json:
        self.from_json(from_json)

  def to_dict(self):
    return self.__dict__

  def save(self, path):
      config_json = json.dumps(self.__dict__, indent=2)
      if os.path.isabs(path):
          save_path = path
      else:
          directory = os.getcwd()
          save_path = os.path.join(directory, path)
      with open(save_path, "w") as file:
          file.write(config_json)

  def from_json(self, path):
        with open(path, "r") as f:
            config_json = f.read()
        self.__dict__ = json.loads(config_json)


class ConfigBuilder(object):
    def __init__(self, nodes=None, edges=None, **kwargs):
        self.kwargs = kwargs
        self.nodes = nodes
        st.sidebar.write("Agraph Configurations")
        self.basic_widget = self.basic_widget()
        self.physics_widget = self.physics_widget()
        self.hierarchical_widget = self.hierarchical_widget()
        self.groups = self.group_widget()

    def basic_widget(self):
        basic_expander = st.sidebar.expander("Basic Config", expanded=True)
        with basic_expander:
            basic_expander.number_input("height",
                                        value=self.kwargs.get("height", 750),
                                        key="height")
            basic_expander.number_input("width",
                                        value=self.kwargs.get("width", 750),
                                        key="width")
            basic_expander.checkbox("directed",
                                    value=self.kwargs.get("directed", True),
                                    key="directed")
            self.kwargs["height"] = st.session_state.height
            self.kwargs["width"] = st.session_state.width
            self.kwargs["directed"] = st.session_state.directed

    def physics_widget(self):
        physics_expander = st.sidebar.expander("Physics Config", expanded=False)
        with physics_expander:
            physics_expander.checkbox("physics",
                                      value=self.kwargs.get("physics", True),
                                      key="physics")
            solvers = ["barnesHut",
                       "forceAtlas2Based",
                       "hierarchicalRepulsion",
                       "repulsion"]
            physics_expander.selectbox("Solver",
                                       options=solvers,
                                       index=self._get_index(solvers, "solver"),
                                       key="solver")
            physics_expander.number_input("minVelocity",
                                          value=self.kwargs.get("minVelocity", 1),
                                          key="minVelocity")
            physics_expander.number_input("maxVelocity",
                                          value=self.kwargs.get("maxVelocity",100),
                                          key="maxVelocity")
            physics_expander.checkbox("stabilize",
                                      value=self.kwargs.get("stabilization", True),
                                      key="stabilize")
            physics_expander.checkbox("fit",
                                      value=self.kwargs.get('fit', True),
                                      key="fit")
            physics_expander.number_input("timestep",
                                          value=self.kwargs.get("timestep", 0.5),
                                          key="timestep")

            self.kwargs["physics"] = st.session_state.physics
            self.kwargs["minVelocity"] = st.session_state.minVelocity
            self.kwargs["maxVelocity"] = st.session_state.maxVelocity
            self.kwargs["stabilization"] = st.session_state.stabilize
            self.kwargs["fit"] = st.session_state.fit
            self.kwargs["timestep"] = st.session_state.timestep
            self.kwargs["solver"] = st.session_state.solver

    def hierarchical_widget(self):
        hierarchical_expander = st.sidebar.expander("Hierarchical Config", expanded=False)
        with hierarchical_expander:

            def set_physics_off():
                if st.session_state.hierarchical:
                    st.session_state.physics = False

            hierarchical_expander.checkbox("hierarchical",
                                           value=self.kwargs.get("hierarchical", False),
                                           key="hierarchical",
                                           on_change=set_physics_off)
            hierarchical_expander.number_input("levelSeparation",
                                               value=self.kwargs.get("levelSeparation", 150),
                                               key="levelSeparation")
            hierarchical_expander.number_input("nodeSpacing",
                                               value=self.kwargs.get("nodeSpacing", 100),
                                               key="nodeSpacing")
            hierarchical_expander.number_input("treeSpacing",
                                               value=self.kwargs.get("treeSpacing", 200),
                                               key="treeSpacing")
            hierarchical_expander.checkbox("blockShifting",
                                           value=self.kwargs.get("blockShifting", True),
                                           key="blockShifting")
            hierarchical_expander.checkbox("edgeMinimization",
                                           value=self.kwargs.get("edgeMinimization", True),
                                           key="edgeMinimization")
            hierarchical_expander.checkbox("parentCentralization",
                                           value=self.kwargs.get("parentCentralization", True),
                                           key="parentCentralization")
            directions = ["UD", "DU", "LR", "RL"]
            hierarchical_expander.selectbox("direction",
                                            options=directions,
                                            index=self._get_index(directions, "direction"),
                                            key="direction")
            sortmethods = ["hubsize", "directed"]
            hierarchical_expander.selectbox("sortMethod",
                                            options=sortmethods,
                                            index=self._get_index(sortmethods, "sortMethod"),
                                            key="sortMethod")
            shaketowards = ["roots", "leaves"]
            hierarchical_expander.selectbox("shakeTowards",
                                            options=shaketowards,
                                            index=self._get_index(shaketowards, "shakeTowards"),
                                            key="shakeTowards")
            self.kwargs.update({
                           "hierarchical": st.session_state.hierarchical,
                           "levelSeparation": st.session_state.levelSeparation,
                           "nodeSpacing": st.session_state.nodeSpacing,
                           "treeSpacing": st.session_state.treeSpacing,
                           "blockShifting": st.session_state.blockShifting,
                           "edgeMinimization": st.session_state.edgeMinimization,
                           "parentCentralization": st.session_state.parentCentralization,
                           "direction": st.session_state.direction,
                           "sortMethod": st.session_state.sortMethod,
                           "shakeTowards": st.session_state.shakeTowards
                           }
                          )

    def group_widget(self):
        group_expander = st.sidebar.expander("Group Config", expanded=False)
        group_expander.checkbox("groups",
                                value=self.kwargs.get("groups", False),
                                key="groups")
        if st.session_state.groups:
            if self.nodes:
                groups = list(set([node.__dict__.get("group", None) for node in self.nodes]))
                if None in groups:
                    groups.remove(None)
                with group_expander:
                    groups_dict = {}
                    for group in groups:
                        st.write(f"Group: {group}")
                        group_expander.text_input(f"Color (hex)", value=" #fe8a71", key=f"group_{group}")
                        groups_dict[group] = {"color": st.session_state[f"group_{group}"]}
                    self.kwargs.update({"groups": groups_dict})

    def build(self, dictify=False):
        # self.physics_widget()
        # self.hierarchical_widget()
        if dictify:
            return self.kwargs
        else:
            self.config = Config(**self.kwargs)
        return self.config

    def _get_index(self, options, target):
        val = self.kwargs.get(target, None)
        if val is None:
            return 0
        try:
            index = options.index(val)
        except ValueError:
            index = 0
        return index

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
def show_page():
    def visualize_graph():
        nodes = []
        edges = []
        seen_nodes = set()
        with driver.session() as session:
            result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m")
            for record in result:
                node1_id = str(record["n"].id)
                node2_id = str(record["m"].id)
                rel_type = record["r"].type

                if node1_id not in seen_nodes:
                    nodes.append(Node(id=node1_id, label=record["n"].get("name", node1_id)))
                    seen_nodes.add(node1_id)
                if node2_id not in seen_nodes:
                    nodes.append(Node(id=node2_id, label=record["m"].get("name", node2_id)))
                    seen_nodes.add(node2_id)

                edges.append(Edge(source=node1_id, target=node2_id, label=rel_type))

        if not nodes:
            return None

        config_builder = ConfigBuilder(nodes=nodes, edges=edges)
        config = config_builder.build()

        return agraph(nodes=nodes, edges=edges, config=config)

    ollama_url = "https://1fe6-34-16-168-185.ngrok-free.app/"
    llm = Ollama(model="llama3", base_url=ollama_url)

    st.title("RAG Graph with Neo4j, Llama3 (Ollama), and CSV Upload")

    uploaded_file = st.file_uploader("Choose a file", type=['csv'])

    if uploaded_file is not None:
        dataset = pd.read_csv(uploaded_file)
        st.subheader("Uploaded file")
        with st.expander("View Uploaded Data"):
            st.dataframe(dataset)

        st.subheader("Deleting existing Neo4j nodes and relationships")
        with st.spinner("Deleting existing graph data..."):
            query = "MATCH (n) DETACH DELETE n"
            try:
                with driver.session() as session:
                    session.run(query)
                st.success("Successfully deleted all existing nodes and relationships in Neo4j.")
            except Exception as e:
                st.error(f"An error occurred while deleting nodes: {e}")

        st.subheader("Cleaned and converted data")
        with st.spinner("Cleaning and converting to schema..."):
            pipeline = AutoClean(dataset)
            txt_file = "cleaned_customers.csv"
            pipeline.output.to_csv(txt_file, sep=",", index=True, header=True)

            loader = CSVLoader(file_path="cleaned_customers.csv")
            docs = loader.load()
            documents = [Document(page_content=doc.page_content) for doc in docs]

            
            with st.expander("cleaned data"):
                for doc in documents[:10]:
                    st.write(doc.page_content)

        if 'graph_documents' not in st.session_state:
            st.session_state.graph_documents = None

        st.subheader("Graph Conversion")
        with st.spinner("Converting to graph document..."):
            if st.session_state.graph_documents is None:
                llm_transformer = LLMGraphTransformer(llm=llm)
                st.session_state.graph_documents = llm_transformer.convert_to_graph_documents(documents)
            graph_documents = st.session_state.graph_documents

        if graph_documents:
            with st.expander("Nodes and Relations"):
                st.subheader("Nodes")
                for node in graph_documents[0].nodes:
                    st.write(node)

                st.subheader("Relationships")
                for relation in graph_documents[0].relationships:
                    st.write(relation)

        st.subheader("Adding new graph documents to Neo4j")
        with st.spinner("Adding data to Neo4j..."):
            try:
                graph = Neo4jGraph(url="neo4j://localhost:7687", username="neo4j", password="password")
                graph.add_graph_documents(
                    graph_documents,
                    baseEntityLabel=True,
                    include_source=True
                )
                st.success("Successfully added new graph documents to Neo4j.")
            except Exception as e:
                st.error(f"An error occurred while adding graph documents: {e}")

        st.subheader("Graph Visualization")
        graph_visualization = visualize_graph()
        if graph_visualization:
            st.write(graph_visualization)
        else:
            st.warning("No data available for visualization.")