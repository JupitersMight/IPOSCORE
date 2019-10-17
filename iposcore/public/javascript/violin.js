'use strict'

function fade(opacity, i) {
    d3.select('#path_' + i)
        .transition()
        .style('opacity', opacity)
}

function renderViolin(properties, init) {

    const widthScaleLinear = d3.scaleLinear().range([0, properties.width])
    const heightScale = d3.scaleBand().rangeRound([properties.margin.top, properties.height]).padding(0.3)
    const xAxisLinear = d3.axisBottom(widthScaleLinear)
    const yAxis = d3.axisLeft(heightScale)

    const height_domain = []
    height_domain.push("All")
    if(properties.curr_class_label === 'complicação pós-cirúrgica')
        for(let i = 0; i < 2; ++i)
            height_domain.push(''+i)
    if(properties.curr_class_label === 'classificação clavien-dindo')
        for(let i = 0; i < 8; ++i)
            height_domain.push(''+i)

    const dataset = properties.data[properties.curr_data_type][properties.curr_attribute].dataset
    const violins = []
    for(let x = 0; x < height_domain.length; ++x){
        violins.push([])
        const curr_data =  x === 0? dataset : dataset.filter(d => d[properties.curr_class_label] === height_domain[x])
        for (let i = 0; i < curr_data.length; ++i){
            violins[x].push(curr_data[i][properties.curr_attribute])
        }
        violins[x].sort((a, b) => a - b)
    }

    let min_ocur = null
    let max_ocur = 0

    let max = 0
    for (let i = 0; i < violins.length; ++i)
        if (max < violins[i][violins[i].length - 1])
            max = violins[i][violins[i].length - 1]

    let thresholds = []
    for (let i = 0; i <= max; ++i)
        thresholds.push(i)

    widthScaleLinear.domain([0, max])
    heightScale.domain(height_domain)
    xAxisLinear.scale(widthScaleLinear)
    yAxis.scale(heightScale)

    if (init) {
        properties.svg.append('g')
            .attr('id', 'axis-x')
            .attr('class', 'x axis')
            .style("font-size", "14px")
            .attr('transform', 'translate(' + properties.margin.left + ',' + properties.height + ')')
            .call(xAxisLinear)

        properties.svg.append('g')
            .attr('id', 'axis-y')
            .attr('class', 'y axis')
            .style("font-size", "14px")
            .attr('transform', 'translate(' + properties.margin.left + ',0)')
            .call(yAxis)

    } else {
        properties.svg.select('#axis-x').transition('xaxis_violin').duration(500).call(xAxisLinear)
        properties.svg.select('#axis-y').transition('yaxis_violin').duration(500).call(yAxis)
    }
    let curr = 0
    const tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(d => '<strong>' + 'Category: ' + shared_data.data[curr].category +
            '</br> Most common duration: ' + shared_data.data[curr].days + ' days</strong>')

    properties.svg.call(tip)

    const histoChart = d3.histogram()

    histoChart
        .domain([0, max])
        .thresholds(thresholds)
        .value(d => d)

    const area = d3.area()
        .y0(d => -((d.length - min_ocur) / (max_ocur - min_ocur) * heightScale.bandwidth() / height_domain.length))
        .y1(d => (d.length - min_ocur) / (max_ocur - min_ocur) * heightScale.bandwidth() / height_domain.length)
        .x(d => widthScaleLinear(d.x0))
        .curve(d3.curveCatmullRom)

    const violins_graphs = properties.svg.selectAll('.violins')
        .data(violins)

    violins_graphs.exit().remove()
    violins_graphs.enter()
        .append('path')
        .attr('id', (d, i) => 'path_' + i)
        .attr('class', 'violins')
        .merge(violins_graphs)
        .style('stroke-width', 0)
        .attr('d', (d) => {
            min_ocur = null
            max_ocur = 0
            let value = null
            let ocur = 0
            for (let x = 0; x < d.length; ++x) {
                let current_value = d[x]
                if (current_value !== value) {
                    if (ocur !== 1) {
                        if (min_ocur == null || min_ocur > ocur) min_ocur = ocur
                        if (max_ocur < ocur) max_ocur = ocur
                    }
                    ocur = 1
                    value = current_value
                } else ++ocur
            }
            if (min_ocur == null || min_ocur > ocur && ocur !== 0) min_ocur = ocur
            if (max_ocur < ocur) max_ocur = ocur
            return area(histoChart(d))
        })
        .on('mouseover', (d, i) => {
            fade(0.5, i)
            curr = i
            tip.show(d)
        })
        .on('mouseout', (d, i) => {
            fade(1, i)
            curr = i
            tip.hide(d)
        })
        .transition('violin').duration(500)
        .attr('transform', (d, i) =>
            'translate(' +
            properties.margin.left +
            ',' +
            (heightScale(height_domain[i]) + heightScale.bandwidth() / 2) +
            ')'
        )
        .style('fill', '#238443')
}