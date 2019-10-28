"use strict"

function renderViolin(properties, init) {

    properties.containerViolin.svg.call(properties.containerViolin.tip)

    if (init) {
        properties.containerViolin.svg.append("g")
            .attr("id", "axis-x")
            .attr("class", "x axis")
            .style("font-size", "14px")
            .attr("transform", "translate(" + properties.margin.left + "," + properties.height + ")")
            .call(properties.containerViolin.xAxisLinear)

        properties.containerViolin.svg.append("g")
            .attr("id", "axis-y")
            .attr("class", "y axis")
            .style("font-size", "14px")
            .attr("transform", "translate(" + properties.margin.left + ",0)")
            .call(properties.containerViolin.yAxis)

    } else {
        properties.containerViolin.svg.select("#axis-x").transition("xaxis_violin").duration(500).call(properties.containerViolin.xAxisLinear)
        properties.containerViolin.svg.select("#axis-y").transition("yaxis_violin").duration(500).call(properties.containerViolin.yAxis)
    }

    let curr = 0

    const histoChart = d3.histogram()

    histoChart
        .domain([0, properties.containerViolin.max])
        .thresholds(properties.containerViolin.thresholds)
        .value(d => d)

    let max_ocur = 0
    const area = d3.area()
        .y0(d => -((d.length) / (max_ocur) * properties.containerViolin.heightScale.bandwidth() / 2))
        .y1(d => d.length / max_ocur * properties.containerViolin.heightScale.bandwidth() / 2)
        .x(d => properties.containerViolin.widthScaleLinear(d.x0))
        .curve(d3.curveCatmullRom)

    const violins_graphs = properties.containerViolin.svg.selectAll(".violins")
        .data(properties.containerViolin.data)

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
                let current_value = Math.round(d[x]*properties.containerViolin.threshold_multiplier)/properties.containerViolin.threshold_multiplier
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
            properties.containerViolin.tip.show(d)
        })
        .on("mouseout", (d, i) => {
            d3.select("#path_" + i)
                .transition()
                .style("opacity", 1)
            curr = i
            properties.containerViolin.tip.hide(d)
        })
        .transition("violin").duration(500)
        .attr("transform", (d, i) =>
            "translate(" +
            properties.margin.left +
            "," +
            (properties.containerViolin.heightScale(properties.containerViolin.height_domain[i]) + properties.containerViolin.heightScale.bandwidth() / 2) +
            ")"
        )
        .style("fill", "#238443")
}