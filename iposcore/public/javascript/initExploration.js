"use strict"

function initExploration(graphData){

    const properties = {}

    properties.data = graphData
    properties.margin = {
        top: 50,
        right: 100,
        bottom: 30,
        left: 100
    }

    properties.class_labels = ["complicação pós-cirúrgica", "classificação clavien-dindo"]
    properties.data_types = Object.keys(graphData)
    properties.visualizations = [
        {
            name:"Violin Charts",
            renderChart: (properties, init) => renderViolin(properties, init)
        },
        /*{
            name:"Box Plot",
            renderChart: (properties, init) => renderBoxplot(properties, init)
        },*/
        {
            name: "Parallel Coordinates",
            renderChart: (properties, init) => renderParallelCoordinate(properties, init)
        }
    ]

    //Init with default values
    properties.curr_data_type = properties.data_types[0]
    properties.curr_visualization = properties.visualizations[0]
    properties.curr_class_label = properties.class_labels[0]
    properties.curr_attribute = Object.keys(properties.data[properties.curr_data_type])[0]

    properties.curr_data = properties.data[properties.curr_data_type][properties.curr_attribute].dataset

    const fullwidth = 1024
    const fullheight = 768
    properties.width = fullwidth - properties.margin.left - properties.margin.right
    properties.height = fullheight - properties.margin.top - properties.margin.bottom

    properties.svg = d3.select(".content-svgs").append("svg")
        .attr("width", properties.width + properties.margin.left + properties.margin.right)
        .attr("height", properties.height + properties.margin.top + properties.margin.bottom)

    properties.violinChartHeightDomains = {
        "complicação pós-cirúrgica": [],
        "classificação clavien-dindo": []
    }
    for(let i = 0; i<Object.keys(properties.violinChartHeightDomains).length; ++i){
        const height_domain = []
        height_domain.push("All")
        if(Object.keys(properties.violinChartHeightDomains)[i] === "complicação pós-cirúrgica")
            for(let i = 0; i < 2; ++i)
                height_domain.push(""+i)
        if(Object.keys(properties.violinChartHeightDomains)[i] === "classificação clavien-dindo")
            for(let i = 0; i < 8; ++i)
                height_domain.push(""+i)
        properties.violinChartHeightDomains[Object.keys(properties.violinChartHeightDomains)[i]] = height_domain
    }

    // Fill dropdowns
    dropdown(
        // List of functions for each dropdown
        [
            function(class_label){
                properties.curr_class_label = class_label
                properties.curr_visualization.renderChart(properties, false)
            },
            function(visualization){
                d3.select(".content-svgs").selectAll("svg > *").remove()
                properties.curr_visualization  = properties.visualizations.find(d => d.name === visualization)
                properties.curr_visualization.renderChart(properties, true)
            },
            function(data_type){
                properties.curr_data_type = data_type
                // Update attribute
                let dropdown_attributes = d3.select("#attribute_selector")

                dropdown_attributes.selectAll("select").remove()
                dropdown_attributes.selectAll("option").remove()

                dropdown_attributes
                    .append("select")
                    .selectAll("option")
                    .data(Object.keys(properties.data[properties.curr_data_type]))
                    .enter()
                    .append("option")
                    .attr("value", d  => d)
                    .text(d => d)
                // Render new vizualization
                properties.curr_visualization.renderChart(properties, false)
            },
            function(attribute){
                properties.curr_attribute = attribute
                properties.curr_data = properties.data[properties.curr_data_type][properties.curr_attribute].dataset
                properties.curr_visualization.renderChart(properties, false)
            }
        ],
        // List of html element id for each dropdown
        [
            "#class_label_dropdown",
            "#visualization",
            "#data_type",
            "#attribute_selector"
        ],
        // List of arrays for dropdown options
        [
            properties.class_labels,
            properties.visualizations.map((d) => d.name),
            properties.data_types,
            Object.keys(properties.data[properties.curr_data_type])
        ]
    )

    renderViolin(properties, true)
}