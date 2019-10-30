"use strict"

function renderHistogram(properties, init){

    // append the svg object to the body of the page
    let svg = properties.svg

    // set the parameters for the histogram
    let histogram = d3.histogram()
        .domain(properties.widthScaleLinear.domain())
        .thresholds(properties.widthScaleLinear.ticks(40))
        .value(d => d)

    let max = 0
    for(let i = 0; i < properties.containerHistogram.hists_data.length; ++i){
        let x = properties.containerHistogram.hists_data[i]

        let bins = histogram(x)

        let temp = d3.max(bins, d => d.length)
        if(temp > max)
            max = temp

         // append the bars for series 1
        svg.selectAll("rect"+i)
            .data(bins)
            .enter()
            .append("rect")
            .attr("x", 1)
            .attr("transform", d =>
                "translate(" + (properties.margin.left + properties.widthScaleLinear(d.x0)) + "," + properties.containerHistogram.heightScale(d.length) + ")"
            )
            .attr("width", d => properties.widthScaleLinear(d.x1) - properties.widthScaleLinear(d.x0))
            .attr("height", d =>  properties.height - properties.containerHistogram.heightScale(d.length))
            .style("fill", "#69b3a2")
            .style("opacity", 0.6)
    }

    properties.containerHistogram.heightScale.domain([0,max])

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