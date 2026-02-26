document.addEventListener("DOMContentLoaded", () => {
    const cy = cytoscape({
        container: document.getElementById("graph"),
        elements: [],
        style: [
            {
                selector: "node",
                style: {
                    "background-color": "#0074D9",
                    "label": "data(id)",
                    "color": "white",
                    "text-valign": "center",
                },
            },
            {
                selector: "edge[weight]",
                style: {
                    "width": 2,
                    "line-color": "#0074D9",
                    "target-arrow-color": "#0074D9",
                    "target-arrow-shape": "triangle",
                    "curve-style": "bezier",
                    "label": "data(weight)", // Display weight if specified
                    "text-rotation": "autorotate",
                    "font-size": "10px",
                    "text-background-color": "#ffffff",
                    "text-background-opacity": 0.7,
                },
            },
            {
                selector: "edge[!weight]",
                style: {
                    "width": 2,
                    "line-color": "#0074D9",
                    "curve-style": "bezier",
                    "target-arrow-shape": "none", // No arrow for edges without weight
                },
            },
        ],
    });

    let nodeId = 0;

    document.getElementById("add-node").addEventListener("click", () => {
        const id = `n${nodeId++}`;
        const viewportCenter = cy.extent();
        const x = (viewportCenter.x1 + viewportCenter.x2) / 2;
        const y = (viewportCenter.y1 + viewportCenter.y2) / 2;
        const newNode = cy.add({ data: { id }, position: { x, y } });

        // Pan and zoom to the new node
        cy.animate({
            fit: {
                eles: newNode,
                padding: 50,
            },
            duration: 500,
        });
    });

    document.getElementById("add-edge").addEventListener("click", (event) => {
        event.stopPropagation(); // Prevent duplicate event triggers

        const source = prompt("Enter source node ID:");
        const target = prompt("Enter target node ID:");
        let weight = prompt("Enter edge weight (optional):");

        if (cy.getElementById(source).length && cy.getElementById(target).length) {
            if (weight === null || weight.trim() === "") {
                weight = undefined; // No weight specified
            } else {
                weight = parseFloat(weight);
            }

            cy.add({
                data: {
                    id: `${source}-${target}`,
                    source,
                    target,
                    ...(weight !== undefined && { weight }), // Add weight only if specified
                },
            });
        } else {
            alert("Invalid node IDs");
        }
    });

    document.getElementById("run-algorithm").addEventListener("click", () => {
        const algorithm = document.getElementById("algorithm-selector").value;
        const source = document.getElementById("source-node").value;
        const graph = {};

        cy.nodes().forEach(node => {
            graph[node.id()] = [];
        });

        cy.edges().forEach(edge => {
            graph[edge.data("source")].push({ target: edge.data("target"), weight: edge.data("weight") });
        });

        fetch("/dsa/run-algorithm", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ graph, algorithm, source }),
        })
            .then(response => response.json())
            .then(data => {
                const outputLog = document.getElementById("output-log");
                if (data.error) {
                    outputLog.textContent = `Error: ${data.error}`;
                } else {
                    outputLog.textContent = `Result: ${JSON.stringify(data.result, null, 2)}`;
                }
            })
            .catch(error => {
                const outputLog = document.getElementById("output-log");
                outputLog.textContent = `Error: ${error.message}`;
            });
    });
});