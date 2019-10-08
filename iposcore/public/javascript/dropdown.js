'use strict'

function dropdowns(properties){
    let class_label_dropdownChange = (properties) => {
        let class_label = d3.select(this).property('value')
        properties.curr_class_label = properties.class_labels[class_label]

        properties.displayingAll ? renderMultipleBarcharts(properties, false) : renderSingleBarchart(properties, false)
    }
    let score_functions_dropdownChange = (properties) => {
        let score_function = d3.select(this).property('value')
        properties.curr_scoring_functions  = properties.scoring_functions[score_function]

        properties.displayingAll ? renderMultipleBarcharts(properties, false) : renderSingleBarchart(properties, false)
    }

    let dropdown = d3.select("#class_label_dropdown")
        .insert("select", "svg")
        .on("change", class_label_dropdownChange(properties))

    dropdown.selectAll("option")
        .data(properties.class_labels)
        .enter().append("option")
        .attr("value", d  => d)
        .text(d => d[0].toUpperCase() + d.slice(1,d.length))// capitalize 1st letter

    dropdown = d3.select("#score_function_dropdown")
        .insert("select", "svg")
        .on("change", score_functions_dropdownChange(properties))

    dropdown.selectAll("option")
        .data(properties.scoring_functions)
        .enter().append("option")
        .attr("value", d  => d)
        .text(d => d[0].toUpperCase() + d.slice(1,d.length)) // capitalize 1st letter
}