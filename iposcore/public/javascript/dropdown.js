'use strict'

function dropdowns_feature_ranking(properties){
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


function dropdowns_exploration(properties){
    let class_label_change = function(class_label){
        properties.curr_class_label = class_label
        properties.curr_visualization.renderChart(properties, false)
    }
    let visualization_change = function(visualization){
        d3.select('.content-svgs').selectAll("svg > *").remove()
        properties.curr_visualization  = properties.visualizations.find(d => d.name === visualization)
        properties.curr_visualization.renderChart(properties, true)
    }
    let data_type_change = function(data_type){
        properties.curr_data_type = data_type
        update_attributes()
        properties.curr_visualization.renderChart(properties, false)
    }
    let attribute_change = function(attribute){
        properties.curr_attribute = attribute
        properties.curr_data = properties.data[properties.curr_data_type][properties.curr_attribute].dataset
        properties.curr_visualization.renderChart(properties, false)
    }

    let dropdown_class = d3.select("#class_label_dropdown")

    dropdown_class
        .append("select")
        .selectAll("option")
        .data(properties.class_labels)
        .enter()
        .append("option")
        .attr("value", d  => d)
        .text(d => d)

    dropdown_class.on("change", function(){
        let class_label = d3.select(this).select('select').property('value')
        class_label_change(class_label)
    })

    let dropdown_visualization = d3.select("#visualization")

    dropdown_visualization
        .append("select")
        .selectAll("option")
        .data(properties.visualizations)
        .enter()
        .append("option")
        .attr("value", d  => d.name)
        .text(d => d.name)

    dropdown_visualization.on("change", function(){
        let visualization = d3.select(this).select('select').property('value')
        visualization_change(visualization)
    })

    let dropdown_data_types = d3.select("#data_type")

    dropdown_data_types
        .append("select")
        .selectAll("option")
        .data(properties.data_types)
        .enter()
        .append("option")
        .attr("value", d  => d)
        .text(d => d)

    dropdown_data_types.on("change", function(){
        let data_type = d3.select(this).select('select').property('value')
        data_type_change(data_type)
    })

    let dropdown_attributes = d3.select("#attribute_selector")

    dropdown_attributes.selectAll('option').remove()

    dropdown_attributes
        .append("select")
        .selectAll("option")
        .data(Object.keys(properties.data[properties.curr_data_type]))
        .enter()
        .append("option")
        .attr("value", d  => d)
        .text(d => d)

    dropdown_attributes.on("change", function(){
        let attribute = d3.select(this).select('select').property('value')
        attribute_change(attribute)
    })

    function update_attributes(){
        let dropdown_attributes = d3.select("#attribute_selector")

        dropdown_attributes.selectAll('select').remove()
        dropdown_attributes.selectAll('option').remove()

        dropdown_attributes
            .append("select")
            .selectAll("option")
            .data(Object.keys(properties.data[properties.curr_data_type]))
            .enter()
            .append("option")
            .attr("value", d  => d)
            .text(d => d)
    }
}