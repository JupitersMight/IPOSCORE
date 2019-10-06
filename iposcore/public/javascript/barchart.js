'use strict'

function fade(opacity, d) {
	d3.select('#' + d.id)
		.transition()
		.style('opacity', opacity)
}

function render(data, properties, init){

	properties.heightScale.domain([0,properties.heightMax])

    const width_domain = []

    for (let i = 0; i < data.length; ++i)
        width_domain.push(data[i].column_name)

	properties.widthScale.domain(width_domain)
	properties.xAxis.scale(properties.widthScale)
	properties.yAxis.scale(properties.heightScale)

    const tip = d3.tip()
		.attr('class', 'd3-tip')
		.offset([-10, 0])
		.html(d =>
            '<strong>Column name: </strong>' + d.column_name + '</br>' +
            '<strong>Value: </strong>' + (Math.round(d.column_value * 10000)/100)
        )

    properties.svg.call(tip)

	const bar = properties.svg.selectAll('.bar')
		.data(data)

	bar.exit().remove()
	bar.enter()
		.append('rect').merge(bar)
		.attr('class', 'bar')
		.attr('id', (d,i) => d.id = properties.chartName+'_bar_' + i)
		.attr('pointer-events','all')
		.on('mouseover', function(d) {
			fade(0.5, d)
			tip.show(d,this)
		})
		.on('mouseout', function(d) {
			fade(1, d)
			tip.hide(d,this)
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
        d3.select('.content-svgs').select('h3').text(properties.chartName)
	}
}
