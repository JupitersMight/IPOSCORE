'use strict'

function dropdowns(properties){
    let class_label_change = function(class_label){
        properties.curr_class_label =class_label
        properties.displayingAll ? renderMultipleBarcharts(properties, false) : renderSingleBarchart(properties, false)
    }
    let scoring_function_change = function(score_function){
        properties.curr_scoring_functions  = score_function
        properties.displayingAll ? renderMultipleBarcharts(properties, false) : renderSingleBarchart(properties, false)
    }

    let dropdown_class = d3.select("#class_label_dropdown")

    dropdown_class
        .append("select")
        .selectAll("option")
        .data(properties.class_labels)
        .enter()
        .append("option")
        .attr("value", d  => d)
        .text(d => d[0].toUpperCase() + d.slice(1,d.length))// capitalize 1st letter

    dropdown_class.on("change", function(){
        let class_label = d3.select(this).select('select').property('value')
        class_label_change(class_label)
    })

    let dropdown_score = d3.select("#score_function_dropdown")

    dropdown_score
        .append("select")
        .selectAll("option")
        .data(properties.scoring_functions)
        .enter()
        .append("option")
        .attr("value", d  => d)
        .text(d => d[0].toUpperCase() + d.slice(1,d.length))// capitalize 1st letter

    dropdown_score.on("change", function(){
        let score_function = d3.select(this).select('select').property('value')
        scoring_function_change(score_function)
    })

}