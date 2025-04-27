// SDLC Process Data Structure
let sdlcData = {
    name: "SDLC Process",
    children: [
        {
            name: "Planning",
            level: 1,
            children: [
                {
                    name: "Requirements Gathering",
                    level: 2,
                    children: [
                        {
                            name: "Stakeholder Analysis",
                            level: 3,
                            children: [
                                {
                                    name: "Identify Key Stakeholders",
                                    level: 4,
                                    children: [
                                        { name: "Internal Stakeholders", level: 5 },
                                        { name: "External Stakeholders", level: 5 }
                                    ]
                                },
                                {
                                    name: "Requirements Documentation",
                                    level: 4,
                                    children: [
                                        { name: "Functional Requirements", level: 5 },
                                        { name: "Non-Functional Requirements", level: 5 }
                                    ]
                                }
                            ]
                        },
                        {
                            name: "Feasibility Study",
                            level: 3,
                            children: [
                                {
                                    name: "Technical Feasibility",
                                    level: 4,
                                    children: [
                                        { name: "Technology Assessment", level: 5 },
                                        { name: "Resource Evaluation", level: 5 }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            name: "Design",
            level: 1,
            children: [
                {
                    name: "System Architecture",
                    level: 2,
                    children: [
                        {
                            name: "High-Level Design",
                            level: 3,
                            children: [
                                {
                                    name: "Component Design",
                                    level: 4,
                                    children: [
                                        { name: "Module Specification", level: 5 },
                                        { name: "Interface Design", level: 5 }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            name: "Implementation",
            level: 1,
            children: [
                {
                    name: "Coding",
                    level: 2,
                    children: [
                        {
                            name: "Development",
                            level: 3,
                            children: [
                                {
                                    name: "Code Implementation",
                                    level: 4,
                                    children: [
                                        { name: "Unit Testing", level: 5 },
                                        { name: "Code Review", level: 5 }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            name: "Testing",
            level: 1,
            children: [
                {
                    name: "Quality Assurance",
                    level: 2,
                    children: [
                        {
                            name: "Testing Phases",
                            level: 3,
                            children: [
                                {
                                    name: "Test Planning",
                                    level: 4,
                                    children: [
                                        { name: "Test Cases", level: 5 },
                                        { name: "Test Environment", level: 5 }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            name: "Deployment",
            level: 1,
            children: [
                {
                    name: "Release Management",
                    level: 2,
                    children: [
                        {
                            name: "Deployment Planning",
                            level: 3,
                            children: [
                                {
                                    name: "Release Strategy",
                                    level: 4,
                                    children: [
                                        { name: "Rollout Plan", level: 5 },
                                        { name: "Rollback Plan", level: 5 }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            name: "Maintenance",
            level: 1,
            children: [
                {
                    name: "Operations",
                    level: 2,
                    children: [
                        {
                            name: "Support",
                            level: 3,
                            children: [
                                {
                                    name: "Monitoring",
                                    level: 4,
                                    children: [
                                        { name: "Performance Tracking", level: 5 },
                                        { name: "Issue Resolution", level: 5 }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
};

// Initialize the visualization
const width = window.innerWidth - 40;
const height = 800;
const margin = { top: 20, right: 20, bottom: 20, left: 20 };

const svg = d3.select("#visualization")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .call(d3.zoom()
        .scaleExtent([0.1, 4])
        .on("zoom", zoomed));

const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Create the force simulation
const simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(d => Math.max(5, 15 - d.level) * 2))
    .alphaDecay(0.01) // Slower decay for continuous movement
    .velocityDecay(0.4); // Less friction for smoother movement

// Zoom handler function
function zoomed(event) {
    g.attr("transform", event.transform);
}

// Animation functions
function animateNodes(nodes) {
    nodes
        .transition()
        .duration(2000)
        .attr("r", d => Math.max(5, 15 - d.level))
        .style("fill", d => {
            const colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"];
            return colors[d.level - 1] || "#e377c2";
        })
        .on("end", function() {
            d3.select(this)
                .transition()
                .duration(2000)
                .attr("r", d => Math.max(5, 10 - d.level))
                .style("fill", d => {
                    const colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"];
                    return colors[d.level - 1] || "#e377c2";
                })
                .on("end", function() {
                    animateNodes(d3.select(this));
                });
        });
}

function animateLinks(links) {
    links
        .transition()
        .duration(2000)
        .style("stroke-width", 2)
        .style("stroke", "#999")
        .on("end", function() {
            d3.select(this)
                .transition()
                .duration(2000)
                .style("stroke-width", 1)
                .style("stroke", "#ccc")
                .on("end", function() {
                    animateLinks(d3.select(this));
                });
        });
}

// Function to update the visualization
function update(data) {
    // Clear existing elements
    g.selectAll("*").remove();

    // Create links
    const links = g.append("g")
        .selectAll("line")
        .data(data.links)
        .enter()
        .append("line")
        .attr("class", "link")
        .style("stroke", "#ccc")
        .style("stroke-width", 1);

    // Create nodes
    const nodes = g.append("g")
        .selectAll(".node")
        .data(data.nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    // Add circles to nodes
    nodes.append("circle")
        .attr("r", d => Math.max(5, 10 - d.level))
        .style("fill", d => {
            const colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"];
            return colors[d.level - 1] || "#e377c2";
        });

    // Add text to nodes
    nodes.append("text")
        .text(d => d.name)
        .attr("dy", 4)
        .attr("text-anchor", "middle");

    // Update simulation
    simulation.nodes(data.nodes);
    simulation.force("link").links(data.links);

    // Add continuous animation
    simulation.on("tick", () => {
        // Update link positions with smooth transitions
        links
            .transition()
            .duration(50)
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        // Update node positions with smooth transitions
        nodes
            .transition()
            .duration(50)
            .attr("transform", d => `translate(${d.x},${d.y})`);

        // Add continuous random forces to keep the visualization moving
        nodes.each(function(d) {
            d.vx += (Math.random() - 0.5) * 0.2;
            d.vy += (Math.random() - 0.5) * 0.2;
        });

        // Periodically restart the simulation to maintain energy
        if (Math.random() < 0.1) {
            simulation.alpha(0.3).restart();
        }
    });

    // Add click handler for nodes
    nodes.on("click", (event, d) => {
        if (d.children) {
            const newData = convertToGraph(d);
            update(newData);
        }
    });

    // Update parent node dropdown
    updateParentNodeDropdown(data.nodes);
}

// Convert hierarchical data to graph format
function convertToGraph(root) {
    const nodes = [];
    const links = [];
    let id = 0;

    function traverse(node, parent = null) {
        const currentId = id++;
        nodes.push({
            id: currentId,
            name: node.name,
            level: node.level,
            children: node.children
        });

        if (parent !== null) {
            links.push({
                source: parent,
                target: currentId
            });
        }

        if (node.children) {
            node.children.forEach(child => traverse(child, currentId));
        }
    }

    traverse(root);
    return { nodes, links };
}

// Update parent node dropdown
function updateParentNodeDropdown(nodes) {
    const parentNodeSelect = d3.select("#parentNode");
    parentNodeSelect.selectAll("option")
        .data(nodes)
        .enter()
        .append("option")
        .attr("value", d => d.id)
        .text(d => d.name);
}

// Add new node
function addNode() {
    const name = document.getElementById("nodeName").value;
    const level = parseInt(document.getElementById("nodeLevel").value);
    const parentId = document.getElementById("parentNode").value;

    if (!name || !level) return;

    const newNode = {
        name: name,
        level: level,
        children: []
    };

    if (parentId) {
        // Find parent node and add child
        function addChildToParent(node, targetId) {
            if (node.id === targetId) {
                if (!node.children) node.children = [];
                node.children.push(newNode);
                return true;
            }
            if (node.children) {
                for (let child of node.children) {
                    if (addChildToParent(child, targetId)) return true;
                }
            }
            return false;
        }
        addChildToParent(sdlcData, parentId);
    } else {
        // Add as top-level node
        if (!sdlcData.children) sdlcData.children = [];
        sdlcData.children.push(newNode);
    }

    update(convertToGraph(sdlcData));
}

// Remove node
function removeNode() {
    const name = document.getElementById("nodeName").value;
    if (!name) return;

    function removeNodeFromParent(node, targetName) {
        if (node.children) {
            node.children = node.children.filter(child => {
                if (child.name === targetName) return false;
                removeNodeFromParent(child, targetName);
                return true;
            });
        }
    }

    removeNodeFromParent(sdlcData, name);
    update(convertToGraph(sdlcData));
}

// Search node
function searchNode() {
    const searchTerm = document.getElementById("searchNode").value.toLowerCase();
    if (!searchTerm) return;

    const graphData = convertToGraph(sdlcData);
    const matchingNodes = graphData.nodes.filter(node => 
        node.name.toLowerCase().includes(searchTerm)
    );

    // Highlight matching nodes
    g.selectAll(".node")
        .style("opacity", d => 
            matchingNodes.some(n => n.id === d.id) ? 1 : 0.3
        );
}

// Generate shareable link
function generateShareLink() {
    const dataString = encodeURIComponent(JSON.stringify(sdlcData));
    return window.location.origin + window.location.pathname + "?data=" + dataString;
}

// Load data from URL if present
function loadDataFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const dataParam = urlParams.get('data');
    if (dataParam) {
        sdlcData = JSON.parse(decodeURIComponent(dataParam));
    }
}

// Event listeners
document.getElementById("addNode").addEventListener("click", addNode);
document.getElementById("removeNode").addEventListener("click", removeNode);
document.getElementById("searchButton").addEventListener("click", searchNode);
document.getElementById("copyLink").addEventListener("click", () => {
    const shareLink = document.getElementById("shareLink");
    shareLink.value = generateShareLink();
    shareLink.select();
    document.execCommand("copy");
});

// Initialize
loadDataFromUrl();
update(convertToGraph(sdlcData));
document.getElementById("shareLink").value = generateShareLink();

// Drag functions
function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
}

function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
}

function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
} 