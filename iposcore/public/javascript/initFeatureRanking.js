"use strict"

let curr = 0


function get_next_prev(value, properties){
    curr = (curr + value) % properties.data_types.length
    if(curr < 0)
        curr = properties.data_types.length - 1
    properties.curr_data_type = properties.data_types[curr]
    renderSingleBarchart(properties, false, undefined)
}

function init(graphData){
    const properties ={}

    properties.data = graphData

    properties.margins = {
            top: 30,
            right: 20,
            bottom: 30,
            left: 90
    }
    properties.MAX_LABEL_SIZE_Y = 200
    properties.MAX_LABEL_SIZE_X = 150
    properties.displayingAll = false

    properties.data_types = Object.keys(graphData)
    properties.scoring_functions = Object.keys(graphData[properties.data_types[0]])
    properties.class_labels = Object.keys(graphData[properties.data_types[0]][properties.scoring_functions[0]])

    properties.curr_class_label = properties.class_labels[0]
    properties.curr_scoring_function = properties.scoring_functions[0]
    properties.curr_data_type = properties.data_types[0]

    d3.select("#prev").on("click",()=>get_next_prev(-1, properties))
    d3.select("#next").on("click",()=>get_next_prev(1, properties))
    d3.select("#displayall").on("click",()=>renderMultipleBarcharts(properties, true))

    dropdowns_feature_ranking(properties)

    renderSingleBarchart(properties, true, undefined)
}
