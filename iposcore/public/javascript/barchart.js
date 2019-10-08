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

function renderMultipleBarcharts(properties, init){
    properties.displayingAll = true

	let container = d3.select('.content-svgs')
	d3.select('.content-svgs').selectAll('svg').remove()
	d3.select('.content-svgs').selectAll('.col-sm-6').remove()
	d3.select('.content-svgs').selectAll('.row').remove()
	d3.selectAll('.d3-tip').remove()
	let currRow = container.append('div').attr('class','row')

	let max = 0
	for(let i = 0; i<properties.data_types.length; ++i){
		for(let x = 0; x<properties.data[properties.curr_class_label][properties.data_types[i]][properties.curr_scoring_functions].length; ++x){
			if(max < properties.data[properties.curr_class_label][properties.data_types[i]][properties.curr_scoring_functions][x].column_value)
				max = properties.data[properties.curr_class_label][properties.data_types[i]][properties.curr_scoring_functions].column_value
		}
	}

	properties.heightMax = max
	properties.width = 500 - properties.margins.left - properties.margins.right - properties.MAX_LABEL_SIZE_X
	properties.height = 500 - properties.margins.top - properties.margins.bottom - properties.MAX_LABEL_SIZE_Y
	properties.heightScale = d3.scaleLinear().range([properties.height, 0])
	properties.widthScale = d3.scaleBand().rangeRound([0, properties.width]).padding(0.3)
	properties.yAxis = d3.axisLeft(properties.heightScale).tickFormat(d3.format(".1%"))
	properties.xAxis = d3.axisBottom(properties.widthScale)

	for(let i = 0; i< data_types.length; ++i){
		properties.svg = currRow
            .append('div')
            .attr('class','col-sm-6')

		properties.svg.append('h3')
            .attr("align", "center")
            .style("text-decoration", "underline")
            .text(properties.data[properties.curr_class_label][properties.data_types[i]][properties.curr_scoring_functions])

        properties.svg =  properties.svg
            .append('svg')
            .attr('width', 500)
            .attr('height', 500)
            .attr('class','centered')

		properties.svg.on('click',()=>renderSingleBarchart(properties,true))
		render(
		    properties.data[properties.curr_class_label][properties.data_types[i]][properties.curr_scoring_functions],
            properties,
            init
        )
	}
	d3.select('#displayall').on('click',()=>renderSingleBarchart(properties,true)).text("Hide All")
	d3.select('#prev').attr('disabled','disabled')
	d3.select('#next').attr('disabled','disabled')
}

function renderSingleBarchart(properties, init){

    properties.displayingAll = false

    const current_data = properties.data[properties.curr_class_label][properties.curr_data_type][properties.curr_scoring_functions]

	const fullwidth = 1024
	const fullheight = 768

    let currRow
	if(init){
		d3.select('.content-svgs').selectAll('svg').remove()
		d3.select('.content-svgs').selectAll('.col-sm-6').remove()
		d3.select('.content-svgs').selectAll('.row').remove()
		d3.selectAll('.d3-tip').remove()
		currRow = d3.select('.content-svgs').append('div').attr('class','row centered')
	}
	else
		currRow = d3.select('.content-svgs').select('.row')

	let max = 0
	for(let i = 0; i < current_data.length; ++i)
		if(max < current_data[i].column_value)
			max = current_data[i].column_value

	properties.heightMax = max
	properties.width = fullwidth - margins.left - margins.right - properties.MAX_LABEL_SIZE_X
	properties.height = fullheight - margins.top - margins.bottom - properties.MAX_LABEL_SIZE_Y
	properties.heightScale = d3.scaleLinear().range([properties.height, 0])
	properties.widthScale = d3.scaleBand().rangeRound([0, properties.width]).padding(0.3)
	properties.yAxis = d3.axisLeft(properties.heightScale).tickFormat(d3.format(".1%"))
	properties.xAxis = d3.axisBottom(properties.widthScale)

	if(init) {
		properties.svg = currRow.append('div').attr('class','col-sm-12')
		properties.svg.append('h3').attr("align", "center").style("text-decoration", "underline").text(properties.curr_data_type)
		properties.svg = properties.svg.append('svg')
			.attr('width', fullwidth)
			.attr('height', fullheight)
			.attr('class', 'centered')
	}
	d3.select('#displayall').on('click',()=>renderMultipleBarcharts(properties, true)).text("Display All")
	d3.select('#prev').attr('disabled',null)
	d3.select('#next').attr('disabled',null)
	render(current_data, properties, init)
}
