"use strict"

function renderBarchart(data, properties, init){

	// Domain of Y AXIS
	properties.heightScale.domain([0,properties.heightMax])

    const width_domain = []

    for (let i = 0; i < data.length; ++i)
        width_domain.push(data[i].column_name)

	// Domain of X AXIS
	properties.widthScale.domain(width_domain)

	// SET scales for each axis
	properties.xAxis.scale(properties.widthScale)
	properties.yAxis.scale(properties.heightScale)

	// tooltip that will pop up when mouseover columns
    const tip = d3.tip()
		.attr("class", "d3-tip")
		.offset([-10, 0])
		.html(d =>
            "<strong>Column name: </strong>" + d.column_name + "</br>" +
            "<strong>Value: </strong>" +  (
            	(Math.round(d.column_value*1000000)/1000000) *
					properties.curr_scoring_function.indexOf("_stats") !== -1 ||
                    properties.curr_scoring_function.indexOf("_p-value") !== -1 ?
					1 :
					100
			)
		)

    // Connect tooltip to SVG
    properties.svg.call(tip)

    // Create bars for each value
	const bar = properties.svg.selectAll(".bar")
		.data(data)

	bar.exit().remove()
	bar.enter()
		.append("rect").merge(bar)
		.attr("class", "bar")
		.attr("id", (d,i) => d.id = properties.curr_data_type+"_bar_" + i)
		.attr("pointer-events","all")
		.on("mouseover", function(d) {
			// Fade
			d3.select("#" + d.id)
				.transition()
				.style("opacity", 0.5)
			tip.show(d,this)
		})
		.on("mouseout", function(d) {
			// Fade
			d3.select("#" + d.id)
				.transition()
				.style("opacity", 1)
			tip.hide(d,this)
		})
		.transition("bar").duration(500)
		.attr("fill", "#158896")
		.attr("x", d => properties.margins.left + properties.widthScale(d.column_name))
		.attr("y", d => properties.margins.top + properties.heightScale(d.column_value))
		.attr("width", properties.widthScale.bandwidth())
		.attr("height",  d => properties.height - properties.heightScale(d.column_value))

	// If first render add the axes
	if (init) {
        properties.svg.append("g")
            .attr("id", "axis-x")
            .attr("class", "x axis")
            .style("font-size", "10px")
            .attr("transform", "translate(" + properties.margins.left + "," + (properties.height + properties.margins.top) + ")")
            .call(properties.xAxis)
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(45)")
            .style("text-anchor", "start")

        properties.svg.append("g")
            .attr("id", "axis-y")
            .attr("class", "y axis")
            .style("font-size", "14px")
            .attr("transform", "translate(" + properties.margins.left + "," + properties.margins.top + ")")
            .call(properties.yAxis)

    }
    // Else update current axis
	else {
		properties.svg.select("#axis-x").transition("xaxis_bar_"+properties.curr_data_type).duration(500).call(properties.xAxis)
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(45)")
            .style("text-anchor", "start")

		properties.svg.select("#axis-y").transition("yaxis_bar_"+properties.curr_data_type).duration(500).call(properties.yAxis)
        if(properties.displayingAll)
        	d3.select("#h3_"+properties.curr_data_type).text(properties.curr_data_type)
		else
			d3.select("h3").text(properties.curr_data_type)
	}
}
