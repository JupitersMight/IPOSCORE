'use strict'

function fade(opacity, d) {
	d3.select('#bar_' + d.id)
		.transition()
		.style('opacity', opacity)
}

function render(data, properties, init){

	properties.heightScale.domain([0,1])

    const width_domain = []

    for (let i = 0; i < data.length; ++i)
        width_domain.push(data[i].column_name)

	properties.widthScale.domain(width_domain)
	properties.xAxis.scale(properties.widthScale)
	properties.yAxis.scale(properties.heightScale)

	if (init)
		properties.svg.append('text')
		.attr('x', (properties.width / 2) + properties.margins.left)
		.attr("y", (properties.margins.top / 2) - properties.margins.top)
		.attr("text-anchor", "middle")
		.style("font-size", "20px")
		.style('fill', '#b3b3b3')
		.style('text-decoration', 'underline')
		.text('Attributes')

	const bar = properties.svg.selectAll('.bar')
		.data(data)

	bar.exit().remove()
	bar.enter()
		.append('rect').merge(bar)
		.attr('class', 'bar')
		.attr('id', d => 'bar_' + d.column_name)
		.on('mouseover', d => {
			fade(0.5, d)
			//tip.show(d)
		})
		.on('mouseout', d => {
			fade(1, d)
			//tip.hide(d)
		})
		.transition('bar').duration(500)
		.attr('fill', '#158896')
		.attr('x', d => properties.margins.left + properties.widthScale(d.column_name))
		.attr('y', d => properties.margins.top + properties.heightScale(d.column_value))
		.attr('width', properties.widthScale.bandwidth())
		.attr('height',  d => properties.height - properties.heightScale(d.column_value))

	// Add the axes
	if (init) {
		properties.svg.append('g')
			.attr('id', 'axis-x')
			.attr('class', 'x axis')
			.style("font-size", "10px")
			.attr('transform', 'translate(' + properties.margins.left + ',' + (properties.height + properties.margins.top) + ')')
			.call(properties.xAxis)
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(45)")
            .style("text-anchor", "start")

		properties.svg.append('g')
			.attr('id', 'axis-y')
			.attr('class', 'y axis')
			.style("font-size", "14px")
			.attr('transform', 'translate(' + properties.margins.left + ',' + properties.margins.top+')')
			.call(properties.yAxis)

	} else {
		properties.svg.select('#axis-x').transition('xaxis_bar').duration(500).call(properties.xAxis)
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(45)")
            .style("text-anchor", "start")
		properties.svg.select('#axis-y').transition('yaxis_bar').duration(500).call(properties.yAxis)
	}
}
