import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import pandas as pd
import pickle
import base64
from copy import deepcopy
import plotly.express as px
import sqlite3
from datetime import datetime
import os

# Set page config to use full width
st.set_page_config(
    page_title="R&D AI Improvements",
    layout="wide"
)

# Add custom CSS for DM Sans font
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
        
        /* Apply DM Sans to all text */
        html, body, [class*="st-"] {
            font-family: 'DM Sans', sans-serif !important;
        }
        
        /* Style for the title */
        h1 {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 700 !important;
        }
        
        /* Style for regular text */
        p, div {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 400 !important;
        }
    </style>
""", unsafe_allow_html=True)

def create_sdlc_graph():
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes with their levels
    nodes = [
        ("SDLC Process", 0),
        ("Planning", 1),
        ("Requirements Gathering", 2),
        ("Stakeholder Analysis", 3),
        ("Identify Key Stakeholders", 4),
        ("Internal Stakeholders", 5),
        ("External Stakeholders", 5),
        ("Requirements Documentation", 4),
        ("Functional Requirements", 5),
        ("Non-Functional Requirements", 5),
        ("Feasibility Study", 3),
        ("Technical Feasibility", 4),
        ("Technology Assessment", 5),
        ("Resource Evaluation", 5),
        ("Design", 1),
        ("System Architecture", 2),
        ("High-Level Design", 3),
        ("Component Design", 4),
        ("Module Specification", 5),
        ("Interface Design", 5),
        ("Implementation", 1),
        ("Coding", 2),
        ("Development", 3),
        ("Code Implementation", 4),
        ("Unit Testing", 5),
        ("Code Review", 5),
        ("Testing", 1),
        ("Quality Assurance", 2),
        ("Testing Phases", 3),
        ("Test Planning", 4),
        ("Test Cases", 5),
        ("Test Environment", 5),
        ("Deployment", 1),
        ("Release Management", 2),
        ("Deployment Planning", 3),
        ("Release Strategy", 4),
        ("Rollout Plan", 5),
        ("Rollback Plan", 5),
        ("Maintenance", 1),
        ("Operations", 2),
        ("Support", 3),
        ("Monitoring", 4),
        ("Performance Tracking", 5),
        ("Issue Resolution", 5)
    ]
    
    # Add nodes to graph
    for node, level in nodes:
        G.add_node(node, level=level, ai_percentage=0)  # Initialize with 0
    
    # Add edges
    edges = [
        ("SDLC Process", "Planning"),
        ("Planning", "Requirements Gathering"),
        ("Requirements Gathering", "Stakeholder Analysis"),
        ("Stakeholder Analysis", "Identify Key Stakeholders"),
        ("Identify Key Stakeholders", "Internal Stakeholders"),
        ("Identify Key Stakeholders", "External Stakeholders"),
        ("Stakeholder Analysis", "Requirements Documentation"),
        ("Requirements Documentation", "Functional Requirements"),
        ("Requirements Documentation", "Non-Functional Requirements"),
        ("Requirements Gathering", "Feasibility Study"),
        ("Feasibility Study", "Technical Feasibility"),
        ("Technical Feasibility", "Technology Assessment"),
        ("Technical Feasibility", "Resource Evaluation"),
        ("SDLC Process", "Design"),
        ("Design", "System Architecture"),
        ("System Architecture", "High-Level Design"),
        ("High-Level Design", "Component Design"),
        ("Component Design", "Module Specification"),
        ("Component Design", "Interface Design"),
        ("SDLC Process", "Implementation"),
        ("Implementation", "Coding"),
        ("Coding", "Development"),
        ("Development", "Code Implementation"),
        ("Code Implementation", "Unit Testing"),
        ("Code Implementation", "Code Review"),
        ("SDLC Process", "Testing"),
        ("Testing", "Quality Assurance"),
        ("Quality Assurance", "Testing Phases"),
        ("Testing Phases", "Test Planning"),
        ("Test Planning", "Test Cases"),
        ("Test Planning", "Test Environment"),
        ("SDLC Process", "Deployment"),
        ("Deployment", "Release Management"),
        ("Release Management", "Deployment Planning"),
        ("Deployment Planning", "Release Strategy"),
        ("Release Strategy", "Rollout Plan"),
        ("Release Strategy", "Rollback Plan"),
        ("SDLC Process", "Maintenance"),
        ("Maintenance", "Operations"),
        ("Operations", "Support"),
        ("Support", "Monitoring"),
        ("Monitoring", "Performance Tracking"),
        ("Monitoring", "Issue Resolution")
    ]
    
    G.add_edges_from(edges)
    
    return G

def calculate_parent_ai_percentage(G, node):
    children = list(G.successors(node))
    if not children:
        return G.nodes[node]['ai_percentage']
    
    total_percentage = sum(G.nodes[child]['ai_percentage'] for child in children)
    return total_percentage / len(children)

def update_parent_ai_percentages(G):
    # Get all nodes in reverse level order (from bottom to top)
    nodes_by_level = sorted(G.nodes(), key=lambda x: G.nodes[x]['level'], reverse=True)
    
    for node in nodes_by_level:
        if G.nodes[node]['level'] < 5:  # Only update non-leaf nodes
            G.nodes[node]['ai_percentage'] = calculate_parent_ai_percentage(G, node)

def serialize_graph(G):
    """Serialize a NetworkX graph to a base64 string"""
    return base64.b64encode(pickle.dumps(G)).decode('utf-8')

def deserialize_graph(graph_str):
    """Deserialize a base64 string back to a NetworkX graph"""
    if isinstance(graph_str, str):
        return pickle.loads(base64.b64decode(graph_str.encode('utf-8')))
    elif isinstance(graph_str, dict):
        # If it's already a dict, convert it back to a NetworkX graph
        G = nx.DiGraph()
        for node, attrs in graph_str.get('nodes', {}).items():
            G.add_node(node, **attrs)
        for source, targets in graph_str.get('edges', {}).items():
            for target in targets:
                G.add_edge(source, target)
        return G
    elif isinstance(graph_str, list):
        # If it's a list, try to reconstruct the graph from the list data
        G = nx.DiGraph()
        for item in graph_str:
            if isinstance(item, dict):
                if 'id' in item:  # Node data
                    G.add_node(item['id'], **{k: v for k, v in item.items() if k != 'id'})
                elif 'source' in item and 'target' in item:  # Edge data
                    G.add_edge(item['source'], item['target'])
        return G
    else:
        raise ValueError("Invalid graph data format")

def format_number(num):
    if num >= 1_000_000_000:
        return f"${num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"${num/1_000:.2f}K"
    else:
        return f"${num:,.2f}"

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         email TEXT,
         notes TEXT,
         timestamp DATETIME)
    ''')
    conn.commit()
    conn.close()

# Function to get all notes
def get_all_notes():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM notes ORDER BY timestamp DESC')
    notes = c.fetchall()
    conn.close()
    return notes

# Function to add a new note
def add_note(email, notes):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('INSERT INTO notes (email, notes, timestamp) VALUES (?, ?, ?)',
              (email, notes, datetime.now()))
    conn.commit()
    conn.close()

# Initialize database
if not os.path.exists('notes.db'):
    init_db()

def main():
    st.title("R&D AI Improvements")
    
    # Initialize session state for graph data if not exists
    if 'graph_data' not in st.session_state:
        G = create_sdlc_graph()
        st.session_state.graph_data = serialize_graph(G)
    
    # Get the graph data from session state
    try:
        G = deserialize_graph(st.session_state.graph_data)
    except Exception as e:
        st.error(f"Error loading graph data: {str(e)}")
        G = create_sdlc_graph()
        st.session_state.graph_data = serialize_graph(G)
    
    # Add controls for graph modification
    with st.sidebar:
        st.title("Graph Controls")
        
        # Node controls in expander
        with st.expander("Node Controls", expanded=True):
            node_action = st.radio("Node Action", ["Add", "Delete", "Rename", "Set AI Percentage"])
            
            if node_action == "Add":
                new_node_name = st.text_input("New Node Name")
                parent_node = st.selectbox("Connect to Node", [""] + list(G.nodes()))
                if st.button("Add Node"):
                    if new_node_name and parent_node:
                        # Add new node
                        new_level = G.nodes[parent_node]['level'] + 1
                        G.add_node(new_node_name, level=new_level, ai_percentage=0)
                        # Add new edge
                        G.add_edge(parent_node, new_node_name)
                        st.session_state.graph_data = serialize_graph(G)
                        st.experimental_rerun()
            
            elif node_action == "Delete":
                node_to_delete = st.selectbox("Select Node to Delete", [""] + list(G.nodes()))
                if st.button("Delete Node"):
                    if node_to_delete:
                        # Remove node and its edges
                        G.remove_node(node_to_delete)
                        st.session_state.graph_data = serialize_graph(G)
                        st.experimental_rerun()
            
            elif node_action == "Rename":
                node_to_rename = st.selectbox("Select Node to Rename", [""] + list(G.nodes()))
                new_name = st.text_input("New Name")
                if st.button("Rename Node"):
                    if node_to_rename and new_name:
                        # Update node name
                        G = nx.relabel_nodes(G, {node_to_rename: new_name})
                        st.session_state.graph_data = serialize_graph(G)
                        st.experimental_rerun()
            
            elif node_action == "Set AI Percentage":
                # Get only leaf nodes (level 5)
                leaf_nodes = [node for node in G.nodes() if G.nodes[node]['level'] == 5]
                node_to_update = st.selectbox("Select Leaf Node", [""] + leaf_nodes)
                if node_to_update:
                    ai_percentage = st.slider("AI Augmentation Percentage", 0, 100, 
                                            G.nodes[node_to_update]['ai_percentage'])
                    if st.button("Update AI Percentage"):
                        # Update AI percentage
                        G.nodes[node_to_update]['ai_percentage'] = ai_percentage
                        # Recalculate parent percentages
                        update_parent_ai_percentages(G)
                        st.session_state.graph_data = serialize_graph(G)
                        st.experimental_rerun()
        
        # Edge controls in expander
        with st.expander("Edge Controls", expanded=True):
            edge_action = st.radio("Edge Action", ["Add", "Delete"])
            
            if edge_action == "Add":
                source_node = st.selectbox("Source Node", [""] + list(G.nodes()))
                target_node = st.selectbox("Target Node", [""] + list(G.nodes()))
                if st.button("Add Edge"):
                    if source_node and target_node:
                        # Add new edge
                        G.add_edge(source_node, target_node)
                        st.session_state.graph_data = serialize_graph(G)
                        st.experimental_rerun()
            
            elif edge_action == "Delete":
                edges = list(G.edges())
                edge_to_delete = st.selectbox("Select Edge to Delete", 
                                            [""] + [f"{source} → {target}" for source, target in edges])
                if st.button("Delete Edge"):
                    if edge_to_delete:
                        source, target = edge_to_delete.split(" → ")
                        # Remove edge
                        G.remove_edge(source, target)
                        st.session_state.graph_data = serialize_graph(G)
                        st.experimental_rerun()
    
    # Convert graph to JSON format for D3.js
    nodes_data = [{
        "id": node, 
        "level": G.nodes[node]["level"],
        "ai_percentage": G.nodes[node]["ai_percentage"]
    } for node in G.nodes()]
    
    links_data = [{"source": source, "target": target} 
                 for source, target in G.edges()]
    
    graph_data = {"nodes": nodes_data, "links": links_data}
    
    # Create the D3.js visualization HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{ 
                margin: 0; 
                padding: 0; 
                background-color: transparent; 
                width: 100%;
                height: 100%;
                font-family: 'DM Sans', sans-serif;
            }}
            #visualization {{
                width: 100%;
                height: 800px;
                margin: 0;
                padding: 0;
                background-color: transparent;
            }}
            svg {{
                width: 100%;
                height: 100%;
                background-color: transparent;
            }}
            .node {{ cursor: pointer; }}
            .node text {{
                pointer-events: none;
                font-family: 'DM Sans', sans-serif;
                font-size: 12px;
                text-anchor: middle;
                dominant-baseline: middle;
                fill: white;
                font-weight: 600;
            }}
            .link {{ 
                stroke: #999; 
                stroke-opacity: 0.6;
                stroke-width: 2;
            }}
            .node circle {{ 
                transition: r 0.2s, fill 0.2s, stroke 0.2s;
                stroke-width: 2px;
                stroke: white;
            }}
            .node text {{ transition: font-size 0.2s; }}
            .link {{ transition: stroke-opacity 0.2s; }}
            .controls {{
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(255, 255, 255, 0.9);
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .tooltip {{
                position: absolute;
                background: rgba(255, 255, 255, 0.9);
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
                pointer-events: none;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div id="visualization"></div>
        <div class="tooltip"></div>
        <script>
            // Wait for the DOM to be fully loaded
            document.addEventListener('DOMContentLoaded', function() {{
                const data = {graph_data};
                
                // Get container dimensions
                const container = document.getElementById('visualization');
                const width = container.clientWidth;
                const height = 800;
                
                // Create SVG
                const svg = d3.select("#visualization")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .attr("viewBox", "0 0 " + width + " " + height)
                    .attr("preserveAspectRatio", "xMidYMid meet")
                    .style("background-color", "transparent");
                
                const g = svg.append("g");
                
                // Create a map of connected nodes for quick lookup
                const connectedNodes = {{}};
                data.links.forEach(link => {{
                    if (!connectedNodes[link.source]) connectedNodes[link.source] = new Set();
                    if (!connectedNodes[link.target]) connectedNodes[link.target] = new Set();
                    connectedNodes[link.source].add(link.target);
                    connectedNodes[link.target].add(link.source);
                }});
                
                // Initialize positions based on level
                data.nodes.forEach(node => {{
                    node.x = width / 2 + (node.level - 2) * 150;
                    node.y = height / 2 + (node.level % 2 ? 80 : -80);
                }});
                
                const simulation = d3.forceSimulation(data.nodes)
                    .force("link", d3.forceLink(data.links)
                        .id(function(d) {{ return d.id; }})
                        .distance(function(d) {{
                            // Increase distance based on level difference
                            return 400 + (Math.abs(d.source.level - d.target.level) * 150);
                        }}))
                    .force("charge", d3.forceManyBody().strength(function(d) {{
                        // Stronger repulsion for better spacing
                        return d.id === "SDLC Process" ? -10000 : -3000;
                    }}))
                    .force("center", d3.forceCenter(width / 2, height / 2))
                    .force("collision", d3.forceCollide().radius(function(d) {{
                        // Larger collision radius to prevent node overlap
                        return 150 + (d.level * 25);
                    }}))
                    .force("x", d3.forceX().strength(0.3).x(function(d) {{
                        // Strong horizontal force to maintain clear hierarchy
                        return (d.level * 250) + (width / 4);
                    }}))
                    .force("y", d3.forceY().strength(0.2).y(function(d) {{
                        // Vertical force to spread nodes
                        return height / 2 + (d.level % 2 ? 150 : -150);
                    }}))
                    .force("radial", d3.forceRadial(function(d) {{
                        // Radial force to maintain circular layout
                        return d.level * 250;
                    }}, width/2, height/2).strength(0.4))
                    .alphaDecay(0.03)  // Slower decay for more stable layout
                    .velocityDecay(0.8);  // Higher velocity decay for smoother movement
                
                // Create links with initial opacity 0
                const link = g.append("g")
                    .selectAll("line")
                    .data(data.links)
                    .enter().append("line")
                    .attr("class", "link")
                    .attr("stroke-width", 2)
                    .style("opacity", 0)
                    .attr("marker-end", "url(#arrowhead)");  // Add arrowhead to links
                
                // Add arrowhead definition
                svg.append("defs").append("marker")
                    .attr("id", "arrowhead")
                    .attr("viewBox", "0 -5 10 10")
                    .attr("refX", 15)
                    .attr("refY", 0)
                    .attr("orient", "auto")
                    .attr("markerWidth", 6)
                    .attr("markerHeight", 6)
                    .append("path")
                    .attr("d", "M0,-5L10,0L0,5")
                    .attr("fill", "#999");
                
                // Create nodes with initial opacity 0
                const node = g.append("g")
                    .selectAll("g")
                    .data(data.nodes)
                    .enter().append("g")
                    .attr("class", "node")
                    .style("opacity", 0)
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));
                
                node.append("circle")
                    .attr("r", function(d) {{ 
                        const textLength = d.id.length;
                        const textSize = textLength * 0.8;
                        const levelSize = (5 - d.level) * 10;
                        return Math.max(30 + textSize, 40 + levelSize);
                    }})
                    .attr("fill", function(d) {{
                        if (d.ai_percentage > 0) {{
                            return "black";
                        }} else {{
                            return d3.schemeCategory10[d.level % 10];
                        }}
                    }})
                    .attr("stroke", "white")
                    .attr("stroke-width", 2)
                    .on("mouseover", function(event, d) {{
                        const connected = connectedNodes[d.id] || new Set();
                        node.selectAll("circle")
                            .style("opacity", function(node) {{
                                return connected.has(node.id) || node.id === d.id ? 1 : 0.3;
                            }});
                        node.selectAll("text")
                            .style("opacity", function(node) {{
                                return connected.has(node.id) || node.id === d.id ? 1 : 0.3;
                            }});
                        link.style("opacity", function(l) {{
                            return l.source.id === d.id || l.target.id === d.id ? 1 : 0.3;
                        }});
                        
                        // Show tooltip with AI percentage
                        const tooltip = d3.select(".tooltip");
                        tooltip
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 10) + "px")
                            .style("opacity", 1)
                            .html(`<strong>${{d.id}}</strong><br>AI Augmentation: ${{d.ai_percentage.toFixed(1)}}%`);
                    }})
                    .on("mousemove", function(event) {{
                        const tooltip = d3.select(".tooltip");
                        tooltip
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 10) + "px");
                    }})
                    .on("mouseout", function() {{
                        node.selectAll("circle").style("opacity", 1);
                        node.selectAll("text").style("opacity", 1);
                        link.style("opacity", 1);
                        
                        // Hide tooltip
                        d3.select(".tooltip").style("opacity", 0);
                    }});
                
                node.append("text")
                    .attr("dy", 0)
                    .attr("text-anchor", "middle")
                    .attr("font-size", function(d) {{
                        return 12 + (5 - d.level) * 2;
                    }})
                    .text(function(d) {{ return d.id; }});
                
                simulation.on("tick", function() {{
                    link
                        .attr("x1", function(d) {{ return d.source.x; }})
                        .attr("y1", function(d) {{ return d.source.y; }})
                        .attr("x2", function(d) {{ return d.target.x; }})
                        .attr("y2", function(d) {{ return d.target.y; }});
                    
                    node.filter(function(d) {{ return d3.select(this).style("opacity") === "1" }})
                        .attr("transform", function(d) {{ return "translate(" + d.x + "," + d.y + ")"; }});
                }});
                
                // Function to reveal nodes level by level
                function revealLevel(level) {{
                    node.filter(d => d.level === level)
                        .attr("transform", function(d) {{ 
                            return "translate(" + d.x + "," + d.y + ") scale(0)"; 
                        }})
                        .transition()
                        .duration(800)
                        .style("opacity", 1)
                        .attr("transform", function(d) {{ 
                            return "translate(" + d.x + "," + d.y + ") scale(1)"; 
                        }});
                    
                    link.filter(d => d.source.level === level || d.target.level === level)
                        .transition()
                        .duration(800)
                        .style("opacity", 1);
                    
                    if (level < 5) {{
                        setTimeout(() => revealLevel(level + 1), 1000);
                    }}
                }}
                
                // Start revealing from level 0
                setTimeout(() => revealLevel(0), 500);
                
                function dragstarted(event, d) {{
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }}
                
                function dragged(event, d) {{
                    d.fx = event.x;
                    d.fy = event.y;
                }}
                
                function dragended(event, d) {{
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }}
                
                // Add zoom behavior
                const zoom = d3.zoom()
                    .scaleExtent([0.1, 4])
                    .on("zoom", function(event) {{
                        g.attr("transform", event.transform);
                    }});
                
                svg.call(zoom);
                
                // Initial zoom to fit all nodes
                setTimeout(function() {{
                    const bounds = g.node().getBBox();
                    const fullWidth = bounds.width;
                    const fullHeight = bounds.height;
                    const midX = bounds.x + fullWidth / 2;
                    const midY = bounds.y + fullHeight / 2;
                    
                    const scale = 0.8 / Math.max(fullWidth / width, fullHeight / height);
                    const translate = [width / 2 - scale * midX, height / 2 - scale * midY];
                    
                    svg.call(zoom.transform, d3.zoomIdentity
                        .translate(translate[0], translate[1])
                        .scale(scale));
                }}, 1000);
            }});
        </script>
    </body>
    </html>
    """
    
    # Display the visualization with full width
    components.html(html, height=800, width=None, scrolling=True)

    # Add calculator section
    st.markdown("---")
    st.subheader("AI Impact Calculator")
    
    # Create main columns for the calculator
    col1, col2 = st.columns(2)
    
    with col1:
        # Team and Project Metrics Section
        st.markdown("### Team & Project Metrics")
        team_size = st.number_input("Team Size", min_value=1, value=10, help="Number of team members")
        avg_salary = st.number_input("Average Developer Salary (USD/year)", min_value=0, value=120000, help="Average annual salary of team members")
        
        # Project Performance Metrics
        st.markdown("#### Project Performance")
        current_cycle_time = st.number_input("Current Cycle Time (days)", min_value=1, value=14, help="Average time to complete a feature from start to finish")
        current_velocity = st.number_input("Current Velocity (story points/sprint)", min_value=1, value=20, help="Current team velocity in story points per sprint")
        sprint_duration = st.number_input("Sprint Duration (weeks)", min_value=1, value=2, help="Duration of each sprint in weeks")
        features_per_sprint = st.number_input("Features per Sprint", min_value=1, value=3, help="Average number of features completed per sprint")
        
        # Financial Parameters
        st.markdown("#### Financial Parameters")
        discount_rate = st.slider("Discount Rate (%)", min_value=0.0, max_value=20.0, value=8.0, step=0.1,
                                help="Annual discount rate for NPV calculation")
        project_duration = st.slider("Project Duration (years)", min_value=1, max_value=10, value=5,
                                   help="Duration of the project for NPV and IRR calculations")
        
    with col2:
        # AI Impact Metrics Section
        st.markdown("### AI Impact Metrics")
        ai_percentage = st.slider("AI Augmentation Percentage", min_value=0, max_value=100, value=30, 
                                help="Overall AI augmentation percentage across the SDLC process")
        
        # Efficiency Metrics
        st.markdown("#### Efficiency Metrics")
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            efficiency_gain = st.slider("Efficiency Gain (%)", min_value=0, max_value=100, value=25, 
                                      help="Expected efficiency gain from AI tools")
            error_reduction = st.slider("Error Reduction (%)", min_value=0, max_value=100, value=30, 
                                      help="Expected reduction in errors/bugs")
        with col2_2:
            time_savings = st.slider("Time Savings (%)", min_value=0, max_value=100, value=20, 
                                   help="Expected time savings in development tasks")
            maintenance_reduction = st.slider("Maintenance Reduction (%)", min_value=0, max_value=100, value=15,
                                            help="Expected reduction in maintenance efforts")
        
        # AI Implementation Costs
        st.markdown("#### AI Implementation Costs")
        
        # Initial Setup Costs
        with st.expander("Initial Setup Costs", expanded=True):
            col2_3, col2_4 = st.columns(2)
            with col2_3:
                initial_ai_cost = st.number_input("AI Tool License Cost (USD)", min_value=0, value=50000, 
                                                help="One-time cost for AI tool licenses")
                infrastructure_cost = st.number_input("Infrastructure Setup Cost (USD)", min_value=0, value=20000,
                                                    help="Cost for setting up required infrastructure")
            with col2_4:
                integration_cost = st.number_input("Integration Cost (USD)", min_value=0, value=15000,
                                                help="Cost for integrating AI tools with existing systems")
                data_migration_cost = st.number_input("Data Migration Cost (USD)", min_value=0, value=10000,
                                                    help="Cost for migrating and preparing data for AI tools")
        
        # Training & Development Costs
        with st.expander("Training & Development Costs", expanded=True):
            col2_5, col2_6 = st.columns(2)
            with col2_5:
                ai_training_cost = st.number_input("AI Training Cost (USD)", min_value=0, value=10000, 
                                                 help="Cost for team training on AI tools")
                developer_training = st.number_input("Developer Training Hours", min_value=0, value=40,
                                                   help="Number of training hours per developer")
            with col2_6:
                training_rate = st.number_input("Training Rate (USD/hour)", min_value=0, value=100,
                                              help="Cost per hour for training")
                documentation_cost = st.number_input("Documentation Cost (USD)", min_value=0, value=5000,
                                                  help="Cost for creating documentation and guidelines")
        
        # Ongoing Operational Costs
        with st.expander("Ongoing Operational Costs", expanded=True):
            col2_7, col2_8 = st.columns(2)
            with col2_7:
                annual_ai_maintenance = st.number_input("Annual AI Maintenance Cost (USD)", min_value=0, value=20000, 
                                                     help="Annual cost for AI tool maintenance and updates")
                cloud_service_cost = st.number_input("Cloud Service Cost (USD/month)", min_value=0, value=1000,
                                                   help="Monthly cost for cloud services")
            with col2_8:
                api_usage_cost = st.number_input("API Usage Cost (USD/month)", min_value=0, value=500,
                                              help="Monthly cost for API usage")
                support_contract = st.number_input("Support Contract Cost (USD/year)", min_value=0, value=15000,
                                                help="Annual cost for technical support")
        
        # Additional Costs
        with st.expander("Additional Costs", expanded=True):
            col2_9, col2_10 = st.columns(2)
            with col2_9:
                model_retraining = st.number_input("Model Retraining Cost (USD/year)", min_value=0, value=10000,
                                                help="Annual cost for model retraining and updates")
                productivity_loss = st.number_input("Productivity Loss During Transition (days)", min_value=0, value=5,
                                                 help="Estimated days of productivity loss during transition")
            with col2_10:
                transition_support = st.number_input("Transition Support Cost (USD)", min_value=0, value=8000,
                                                  help="Cost for additional support during transition period")
                risk_mitigation = st.number_input("Risk Mitigation Cost (USD)", min_value=0, value=5000,
                                               help="Cost for risk mitigation measures")
        
        # Compliance & Security Costs
        with st.expander("Compliance & Security Costs", expanded=True):
            col2_11, col2_12 = st.columns(2)
            with col2_11:
                security_audit = st.number_input("Security Audit Cost (USD)", min_value=0, value=12000,
                                              help="Cost for security audit and compliance checks")
                data_privacy = st.number_input("Data Privacy Implementation Cost (USD)", min_value=0, value=8000,
                                            help="Cost for implementing data privacy measures")
            with col2_12:
                compliance_certification = st.number_input("Compliance Certification Cost (USD)", min_value=0, value=10000,
                                                        help="Cost for obtaining necessary certifications")

    # Calculate metrics
    if st.button("Calculate Impact") or st.session_state.get('show_results', False):
        # Calculate total costs
        total_initial_cost = (initial_ai_cost + infrastructure_cost + integration_cost + 
                            data_migration_cost + security_audit + data_privacy + 
                            compliance_certification)
        
        total_training_cost = (ai_training_cost + (developer_training * training_rate * team_size) + 
                             documentation_cost)
        
        total_annual_cost = (annual_ai_maintenance + (cloud_service_cost * 12) + 
                           (api_usage_cost * 12) + support_contract + model_retraining)
        
        total_indirect_cost = ((productivity_loss * team_size * (avg_salary/260)) + 
                             transition_support + risk_mitigation)
        
        total_ai_cost = total_initial_cost + total_training_cost + total_annual_cost + total_indirect_cost
        
        # Calculate costs and time metrics
        annual_team_cost = team_size * avg_salary
        sprints_per_month = 4 / sprint_duration
        features_per_month = features_per_sprint * sprints_per_month
        
        # Calculate new cycle time with AI impact
        new_cycle_time = current_cycle_time * (1 - (efficiency_gain / 100))
        cycle_time_reduction = current_cycle_time - new_cycle_time
        
        # Calculate savings
        efficiency_savings = annual_team_cost * (efficiency_gain / 100)
        error_reduction_savings = annual_team_cost * (error_reduction / 100) * 0.3  # Assuming 30% of time spent on fixing errors
        time_savings_amount = annual_team_cost * (time_savings / 100)
        maintenance_savings = annual_team_cost * (maintenance_reduction / 100) * 0.2  # Assuming 20% of time spent on maintenance
        
        total_savings = efficiency_savings + error_reduction_savings + time_savings_amount + maintenance_savings
        net_savings = total_savings - total_annual_cost  # Subtract annual AI costs
        
        # Calculate productivity metrics
        new_velocity = current_velocity * (1 + (efficiency_gain / 100))
        productivity_gain = (new_velocity - current_velocity) / current_velocity * 100
        additional_features_per_month = features_per_month * (efficiency_gain / 100)
        
        # Calculate ROI and payback period
        roi = ((net_savings - total_ai_cost) / total_ai_cost) * 100
        payback_period = total_ai_cost / net_savings  # in years

        # Calculate NPV and IRR
        initial_investment = total_initial_cost + total_training_cost + total_indirect_cost
        annual_cash_flow = net_savings - total_annual_cost
        
        # Calculate NPV
        npv = -initial_investment
        for year in range(1, project_duration + 1):
            npv += annual_cash_flow / ((1 + discount_rate/100) ** year)
        
        # Calculate IRR using trial and error method
        def calculate_npv(rate, initial_investment, annual_cash_flow, years):
            npv = -initial_investment
            for year in range(1, years + 1):
                npv += annual_cash_flow / ((1 + rate) ** year)
            return npv
        
        def find_irr(initial_investment, annual_cash_flow, years):
            # Start with a reasonable range
            low_rate = 0.0
            high_rate = 1.0
            precision = 0.0001
            
            while high_rate - low_rate > precision:
                mid_rate = (low_rate + high_rate) / 2
                npv = calculate_npv(mid_rate, initial_investment, annual_cash_flow, years)
                
                if npv > 0:
                    low_rate = mid_rate
                else:
                    high_rate = mid_rate
            
            return (low_rate + high_rate) / 2 * 100
        
        irr = find_irr(initial_investment, annual_cash_flow, project_duration)
        
        # Calculate Profitability Index
        profitability_index = (npv + initial_investment) / initial_investment
        
        # Calculate Discounted Payback Period
        cumulative_discounted_cash_flow = 0
        discounted_payback_period = project_duration  # Default to project duration if not achieved
        for year in range(1, project_duration + 1):
            discounted_cash_flow = annual_cash_flow / ((1 + discount_rate/100) ** year)
            cumulative_discounted_cash_flow += discounted_cash_flow
            if cumulative_discounted_cash_flow >= initial_investment:
                discounted_payback_period = year
                break
        
        # Calculate additional financial metrics
        # Free Cash Flow (FCF)
        free_cash_flow = net_savings - total_annual_cost

        # ROI per Employee
        roi_per_employee = (net_savings - total_ai_cost) / team_size

        # Cost Savings Ratio
        cost_savings_ratio = total_savings / total_ai_cost

        # AI Investment Efficiency Ratio
        ai_investment_efficiency = net_savings / total_ai_cost

        # Annual Savings per Employee
        annual_savings_per_employee = net_savings / team_size

        # Feature Cost Reduction
        current_feature_cost = annual_team_cost / (features_per_month * 12)
        new_feature_cost = annual_team_cost / ((features_per_month + additional_features_per_month) * 12)
        feature_cost_reduction = ((current_feature_cost - new_feature_cost) / current_feature_cost) * 100

        # AI Cost per Feature
        ai_cost_per_feature = total_ai_cost / (additional_features_per_month * 12)

        # Break-even Features
        break_even_features = total_ai_cost / (current_feature_cost - new_feature_cost)

        # AI Impact Score (composite metric)
        ai_impact_score = (
            (efficiency_gain * 0.3) +
            (error_reduction * 0.2) +
            (time_savings * 0.2) +
            (maintenance_reduction * 0.1) +
            (productivity_gain * 0.2)
        )
        
        # Display results in a more organized way
        st.markdown("---")
        st.markdown("### Results")
        
        # Create results columns
        results_col1, results_col2, results_col3, results_col4 = st.columns(4)
        
        # Basic Metrics
        with results_col1:
            st.markdown("#### Basic Metrics")
            st.metric("Annual Team Cost", format_number(annual_team_cost), 
                     help="Formula: Team Size × Average Salary")
            st.metric("Total AI Cost", format_number(total_ai_cost), 
                     help="Sum of all AI-related costs")
            st.metric("Total Savings", format_number(total_savings), 
                     help="Sum of all savings components")
            st.metric("Net Savings", format_number(net_savings), 
                     help="Formula: Total Savings - Total Annual Cost")
        
        # Investment Metrics
        with results_col2:
            st.markdown("#### Investment Metrics")
            st.metric("ROI", f"{roi:.1f}%", 
                     help="Formula: ((Net Savings - Total AI Cost) / Total AI Cost) × 100")
            st.metric("NPV", format_number(npv), 
                     help="Net Present Value of the investment")
            st.metric("IRR", f"{irr:.1f}%", 
                     help="Internal Rate of Return")
            st.metric("Profitability Index", f"{profitability_index:.2f}", 
                     help="Ratio of present value of future cash flows to initial investment")
        
        # Time Metrics
        with results_col3:
            st.markdown("#### Time Metrics")
            st.metric("Payback Period", f"{payback_period:.1f} years", 
                     help="Formula: Total AI Cost / Net Savings")
            st.metric("Discounted Payback Period", f"{discounted_payback_period:.1f} years", 
                     help="Time to recover initial investment considering time value of money")
            st.metric("Current Cycle Time", f"{current_cycle_time} days")
            st.metric("New Cycle Time", f"{new_cycle_time:.1f} days")
        
        # Productivity Metrics
        with results_col4:
            st.markdown("#### Productivity Metrics")
            st.metric("Current Velocity", f"{current_velocity:.1f} points/sprint")
            st.metric("New Velocity", f"{new_velocity:.1f} points/sprint")
            st.metric("Velocity Improvement", f"{(new_velocity - current_velocity)/current_velocity*100:.1f}%")
            st.metric("Features per Month", f"{features_per_month + additional_features_per_month:.1f}")
        
        # Additional Metrics
        st.markdown("---")
        st.markdown("### Additional Metrics")
        
        add_metrics_col1, add_metrics_col2, add_metrics_col3, add_metrics_col4 = st.columns(4)
        
        with add_metrics_col1:
            st.metric("Free Cash Flow", format_number(free_cash_flow), 
                     help="Net savings minus annual costs")
            st.metric("ROI per Employee", format_number(roi_per_employee), 
                     help="Net ROI divided by team size")
        
        with add_metrics_col2:
            st.metric("Cost Savings Ratio", f"{cost_savings_ratio:.2f}", 
                     help="Ratio of total savings to total AI cost")
            st.metric("AI Investment Efficiency", f"{ai_investment_efficiency:.2f}", 
                     help="Ratio of net savings to total AI cost")
        
        with add_metrics_col3:
            st.metric("Annual Savings per Employee", format_number(annual_savings_per_employee), 
                     help="Net savings divided by team size")
            st.metric("Feature Cost Reduction", f"{feature_cost_reduction:.1f}%", 
                     help="Percentage reduction in cost per feature")
        
        with add_metrics_col4:
            st.metric("AI Cost per Feature", format_number(ai_cost_per_feature), 
                     help="Total AI cost divided by additional features per year")
            st.metric("Break-even Features", f"{break_even_features:.1f}", 
                     help="Number of features needed to break even")
        
        # Add detailed breakdowns
        st.markdown("---")
        st.markdown("### Detailed Breakdowns")
        
        # Cost Breakdown
        st.markdown("#### Cost Breakdown")
        cost_data = {
            'Category': ['Initial Setup', 'Training', 'Annual Operational', 'Indirect', 'Compliance & Security'],
            'Amount': [total_initial_cost, total_training_cost, total_annual_cost, total_indirect_cost, 
                      security_audit + data_privacy + compliance_certification]
        }
        
        # Create a DataFrame for the cost breakdown
        cost_df = pd.DataFrame(cost_data)
        cost_df['Percentage'] = (cost_df['Amount'] / cost_df['Amount'].sum() * 100).round(1)
        
        # Display cost breakdown as a bar chart
        st.bar_chart(cost_df.set_index('Category')['Amount'])
        
        # Display cost breakdown as a table with formatted values
        cost_df['Amount'] = cost_df['Amount'].apply(lambda x: f"${x:,.0f}")
        cost_df['Percentage'] = cost_df['Percentage'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(cost_df, hide_index=True)
        
        # Savings Breakdown
        st.markdown("#### Savings Breakdown")
        savings_data = {
            'Category': ['Efficiency Savings', 'Error Reduction Savings', 'Time Savings', 'Maintenance Savings'],
            'Amount': [efficiency_savings, error_reduction_savings, time_savings_amount, maintenance_savings]
        }
        
        # Create a DataFrame for the savings breakdown
        savings_df = pd.DataFrame(savings_data)
        savings_df['Percentage'] = (savings_df['Amount'] / savings_df['Amount'].sum() * 100).round(1)
        
        # Display savings breakdown as a bar chart
        st.bar_chart(savings_df.set_index('Category')['Amount'])
        
        # Display savings breakdown as a table with formatted values
        savings_df['Amount'] = savings_df['Amount'].apply(lambda x: f"${x:,.0f}")
        savings_df['Percentage'] = savings_df['Percentage'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(savings_df, hide_index=True)
        
        # Add ROI Trend Chart
        st.markdown("#### ROI Trend Over Time")
        
        # Calculate ROI for each year
        years = list(range(1, project_duration + 1))
        roi_trend = []
        cumulative_investment = initial_investment
        
        for year in years:
            annual_roi = (annual_cash_flow * year - cumulative_investment) / cumulative_investment * 100
            roi_trend.append(annual_roi)
            cumulative_investment += total_annual_cost
        
        # Create ROI trend DataFrame
        roi_df = pd.DataFrame({
            'Year': years,
            'ROI': roi_trend
        })
        
        # Display ROI trend as a line chart
        st.line_chart(roi_df.set_index('Year')['ROI'])
        
        # Display ROI trend as a table with formatted values
        roi_df['ROI'] = roi_df['ROI'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(roi_df, hide_index=True)

        # Set show_results to True after calculation
        st.session_state.show_results = True

    # Add custom notes section
    st.markdown("---")
    st.markdown("### Notes")
    
    # Initialize session state for notes if not exists
    if 'notes' not in st.session_state:
        st.session_state.notes = ""
    
    # Notes text area
    notes = st.text_area("Add your notes or observations here", 
                       value=st.session_state.notes,
                       help="Use this space to add any additional notes, observations, or context about the calculations")
    
    # Update session state when notes change
    if notes != st.session_state.notes:
        st.session_state.notes = notes
    
    # Email submission form
    if notes.strip():  # Only show email form if there are notes
        st.markdown("---")
        st.markdown("### Submit Your Notes")
        email = st.text_input("Enter your email to submit notes", 
                            help="Your email will be used to identify your notes")
        
        submit_button = st.button("Submit Notes")
        if submit_button:
            if email.strip():
                # Add note to database
                add_note(email, notes)
                st.success("Notes submitted successfully!")
                # Clear the notes after successful submission
                st.session_state.notes = ""
                # Preserve the results section
                st.session_state.show_results = True
            else:
                st.error("Please enter your email to submit notes")
    
    # Display notes history
    st.markdown("---")
    st.markdown("### Notes History")
    
    # Get all notes from database
    all_notes = get_all_notes()
    
    if all_notes:
        # Create a DataFrame for better display
        notes_df = pd.DataFrame(all_notes, columns=['ID', 'Email', 'Notes', 'Timestamp'])
        notes_df['Timestamp'] = pd.to_datetime(notes_df['Timestamp'])
        
        # Display each note in a card-like format
        for _, note in notes_df.iterrows():
            with st.expander(f"Notes from {note['Email']} ({note['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')})"):
                st.write(note['Notes'])
    else:
        st.info("No notes have been submitted yet.")

    # Add download button for results
    if st.session_state.get('show_results', False):
        results = {
            "Annual Team Cost": annual_team_cost,
            "Total Initial Cost": total_initial_cost,
            "Total Training Cost": total_training_cost,
            "Total Annual Cost": total_annual_cost,
            "Total Indirect Cost": total_indirect_cost,
            "Total AI Cost": total_ai_cost,
            "Current Cycle Time": current_cycle_time,
            "New Cycle Time": new_cycle_time,
            "Cycle Time Reduction": cycle_time_reduction,
            "Cycle Time Improvement": (cycle_time_reduction/current_cycle_time)*100,
            "Efficiency Savings": efficiency_savings,
            "Error Reduction Savings": error_reduction_savings,
            "Time Savings": time_savings_amount,
            "Maintenance Savings": maintenance_savings,
            "Total Savings": total_savings,
            "Net Savings": net_savings,
            "Monthly Savings": net_savings/12,
            "Daily Savings": net_savings/365,
            "ROI": roi,
            "Payback Period": payback_period,
            "NPV": npv,
            "IRR": irr,
            "Profitability Index": profitability_index,
            "Discounted Payback Period": discounted_payback_period,
            "Free Cash Flow": free_cash_flow,
            "ROI per Employee": roi_per_employee,
            "Cost Savings Ratio": cost_savings_ratio,
            "AI Investment Efficiency": ai_investment_efficiency,
            "Annual Savings per Employee": annual_savings_per_employee,
            "Feature Cost Reduction": feature_cost_reduction,
            "AI Cost per Feature": ai_cost_per_feature,
            "Break-even Features": break_even_features,
            "AI Impact Score": ai_impact_score,
            "Current Velocity": current_velocity,
            "New Velocity": new_velocity,
            "Velocity Improvement": (new_velocity - current_velocity)/current_velocity*100,
            "Current Features per Month": features_per_month,
            "Additional Features per Month": additional_features_per_month,
            "Total Features per Month": features_per_month + additional_features_per_month,
            "Cost per Feature": total_ai_cost/(additional_features_per_month*12),
            "Notes": notes
        }
        
        # Convert results to CSV
        df = pd.DataFrame([results])
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="ai_impact_calculator_results.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main() 