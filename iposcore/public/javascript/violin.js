"use strict"

function renderViolin(properties, init) {

    const height_domain = properties.yAxisDomain[properties.curr_class_label]

    const dataset = properties.data[properties.curr_data_type][properties.curr_attribute].dataset

    const violins = []
    for(let x = 0; x < height_domain.length; ++x) {
        violins.push([])
        const curr_data = x === 0 ? dataset : dataset.filter(d => d[properties.curr_class_label] === height_domain[x])
        for (let i = 0; i < curr_data.length; ++i) {
            violins[x].push(curr_data[i][properties.curr_attribute])
        }
        violins[x].sort((a, b) => a - b)
    }

    let max = 0
    for (let i = 0; i < violins.length; ++i)
        if (max < violins[i][violins[i].length - 1])
            max = violins[i][violins[i].length - 1]

    let thresholds = []
    for (let i = 0; i <= max; i += properties.threshold_spacing)
        thresholds.push(i)

    let temp = properties.threshold_spacing
    let threshold_multiplier = 1
    while(temp < 1){
        temp *= 10
        threshold_multiplier *= 10
    }

    properties.widthScaleLinear.domain([0, max])
    properties.heightScale.domain(height_domain)
    properties.xAxisLinear.scale(properties.widthScaleLinear)
    properties.yAxis.scale(properties.heightScale)

    if (init) {
        properties.svg.append("g")
            .attr("id", "axis-x")
            .attr("class", "x axis")
            .style("font-size", "14px")
            .attr("transform", "translate(" + properties.margin.left + "," + properties.height + ")")
            .call(properties.xAxisLinear)

        properties.svg.append("g")
            .attr("id", "axis-y")
            .attr("class", "y axis")
            .style("font-size", "14px")
            .attr("transform", "translate(" + properties.margin.left + ",0)")
            .call(properties.yAxis)

    } else {
        properties.svg.select("#axis-x").transition("xaxis_violin").duration(500).call(properties.xAxisLinear)
        properties.svg.select("#axis-y").transition("yaxis_violin").duration(500).call(properties.yAxis)
    }
    let curr = 0
    const tip = d3.tip()
        .attr("class", "d3-tip")
        .offset([-10, 0])
        .html(d => "<strong>" + "Category: " + shared_data.data[curr].category +
            "</br> Most common duration: " + shared_data.data[curr].days + " days</strong>")

    properties.svg.call(tip)

    const histoChart = d3.histogram()

    histoChart
        .domain([0, max])
        .thresholds(thresholds)
        .value(d => d)

    let max_ocur = 0
    const area = d3.area()
        .y0(d => -((d.length) / (max_ocur) * properties.heightScale.bandwidth() / 2))
        .y1(d => d.length / max_ocur * properties.heightScale.bandwidth() / 2)
        .x(d => properties.widthScaleLinear(d.x0))
        .curve(d3.curveCatmullRom)

    const violins_graphs = properties.svg.selectAll(".violins")
        .data(violins)

    violins_graphs.exit().remove()
    violins_graphs.enter()
        .append("path")
        .attr("id", (d, i) => "path_" + i)
        .attr("class", "violins")
        .merge(violins_graphs)
        .style("stroke-width", 0)
        .attr("d", (d) => {
            max_ocur = 0
            let value = null
            let ocur = 0
            for (let x = 0; x < d.length; ++x) {
                let current_value = Math.round(d[x]*threshold_multiplier)/threshold_multiplier
                if (current_value !== value) {
                    if (ocur !== 1)
                        if (max_ocur < ocur) max_ocur = ocur
                    ocur = 1
                    value = current_value
                } else ++ocur
            }
            if (max_ocur < ocur) max_ocur = ocur
            return area(histoChart(d))
        })
        .on("mouseover", (d, i) => {
            d3.select("#path_" + i)
                .transition()
                .style("opacity", 0.5)
            curr = i
            tip.show(d)
        })
        .on("mouseout", (d, i) => {
            d3.select("#path_" + i)
                .transition()
                .style("opacity", 1)
            curr = i
            tip.hide(d)
        })
        .transition("violin").duration(500)
        .attr("transform", (d, i) =>
            "translate(" +
            properties.margin.left +
            "," +
            (properties.heightScale(height_domain[i]) + properties.heightScale.bandwidth() / 2) +
            ")"
        )
        .style("fill", "#238443")
}