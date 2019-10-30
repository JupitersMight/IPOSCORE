"use strict"

function renderHistogram(properties, init){
    init = true
    // append the svg object to the body of the page
    let svg = properties.svg

    // set the parameters for the histogram
    let histogram = d3.histogram()
        .domain(properties.widthScaleLinear.domain())
        .thresholds(properties.widthScaleLinear.ticks(40))
        .value(d => d)

    let max = 0
    for(let i = 0; i < properties.containerHistogram.hists_data.length; ++i)
        if(d3.max(histogram(properties.containerHistogram.hists_data[i]), d => d.length) > max)
            max = d3.max(histogram(properties.containerHistogram.hists_data[i]), d => d.length)

    properties.containerHistogram.heightScale.domain([0,max + Math.round(max/5)])

    const colors = ["PALETURQUOISE", "AQUAMARINE", "TURQUOISE", "MEDIUMTURQUOISE", "DARKTURQUOISE", "CADETBLUE", "STEELBLUE", "LIGHTSTEELBLUE", "POWDERBLUE"]
    for(let i = 0; i < properties.containerHistogram.hists_data.length; ++i){
        let bins = histogram(properties.containerHistogram.hists_data[i])
        // append the bars for series i
        let bars = svg.selectAll("rect"+i)
            .data(bins)

        bars.exit().remove()
        bars.enter()
            .append("rect").merge(bars)
            .attr("x", 1)
            .attr("transform", d =>
                "translate(" + (properties.margin.left + properties.widthScaleLinear(d.x0)) + "," + properties.containerHistogram.heightScale(d.length) + ")"
            )
            .attr("width", d => properties.widthScaleLinear(d.x1) - properties.widthScaleLinear(d.x0))
            .attr("height", d =>  properties.height - properties.containerHistogram.heightScale(d.length))
            .style("fill", colors[i])
            .style("opacity", 0.6)
        svg.append("circle").attr("cx",300).attr("cy",30 + i*30).attr("r", 6).style("fill", colors[i])
        svg.append("text").attr("x", 320).attr("y", 30 + i*30).text(i === 0 ? "All" : ""+i).style("font-size", "15px").attr("alignment-baseline","middle")
    }

    if(init) {
        svg.append("g")
            .attr("id", "axis-x")
            .attr("class", "x axis")
            .style("font-size", "14px")
            .attr("transform", "translate(" + properties.margin.left + "," + properties.height + ")")
            .call(properties.xAxisLinear)

        svg.append("g")
            .attr("id", "axis-y")
            .attr("class", "y axis")
            .style("font-size", "14px")
            .attr("transform", "translate(" + properties.margin.left + ",0)")
            .call(properties.containerHistogram.yAxis)
    }
    else {
        properties.svg.select("#axis-x").transition("xaxis_violin").duration(500).call(properties.xAxisLinear)
        properties.svg.select("#axis-y").transition("yaxis_violin").duration(500).call(properties.yAxis)
    }
}