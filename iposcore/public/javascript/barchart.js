'use strict'

function render(data, properties, init){

	properties.heightScale.domain([0,100])

    const width_domain = []

    for (let i = 0; i < data.length; ++i)
        width_domain.push(data[i].column_name)

	properties.widthScale.domain(width_domain)
	properties.xAxis.scale(properties.widthScale)
	properties.yAxis.scale(properties.heightScale)

	if (init)
		properties.svg.append('text')
		.attr('x', (properties.width / 2) + properties.left)
		.attr("y", properties.top / 2)
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
		.transition('bar').duration(500)
		.attr('fill', d => d.selected ? '#ec7014' : '#238443')
		.attr('x', d => properties.left + properties.widthScale(d.column_name))
		.attr('y', d => properties.heightScale(d.column_value))
		.attr('width', properties.widthScale.bandwidth())
		.attr('height',  d => properties.height-  properties.heightScale(d.column_value))

	// Add the axes
	if (init) {
		properties.svg.append('g')
			.attr('id', 'axis-y')
			.attr('class', 'y axis')
			.style("font-size", "14px")
			.attr('transform', 'translate(' + properties.left + ',' + properties.height + ')')
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
			.attr('transform', 'translate(' + properties.left + ',0)')
			.call(properties.yAxis)

		properties.svg.append('text')
			.attr('id', 'usd')
			.attr('class', 'xlabel')
			.attr('transform', 'translate(' + (properties.left + properties.width / 2) + ' ,' + (properties.height + properties.bottom + 30) + ')')
			.style('text-anchor', 'middle')
			.attr('dy', '12')
			.style("font-size", "16px")
			.style('fill', '#b3b3b3')
			.text('Descriptive percentage')

	} else {
		properties.svg.select('#axis-x').transition('xaxis_bar').duration(500).call(properties.xAxis)
		properties.svg.select('#axis-y').transition('yaxis_bar').duration(500).call(properties.yAxis)
	}
}
