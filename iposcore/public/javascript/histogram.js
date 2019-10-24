"use strict"

function renderHistogram(properties, init){

    d3.select(".content-svgs").selectAll("svg>*").remove()
    properties.widthScaleLinear = d3.scaleLinear().range([0, properties.width])
    properties.heightScale = d3.scaleLinear().range([properties.height, 0]);
    properties.xAxisLinear = d3.axisBottom(properties.widthScaleLinear)
    properties.yAxis = d3.axisLeft(properties.heightScale)
    properties.svg = d3.select(".content-svgs").select("svg")

    const dataset = properties.data[properties.curr_data_type][properties.curr_attribute].dataset

    const hists_data = []
    for(let x = 0; x < properties.yAxisDomain[properties.curr_class_label].length; ++x) {
        hists_data.push([])
        const curr_data = x === 0 ? dataset : dataset.filter(d => d[properties.curr_class_label] === properties.yAxisDomain[properties.curr_class_label][x])
        for (let i = 0; i < curr_data.length; ++i) {
            hists_data[x].push(curr_data[i][properties.curr_attribute])
        }
        hists_data[x].sort((a, b) => a - b)
    }
    let max_occur = 0
    let temp = {}
    for(let i = 0; i < hists_data[0].length; ++i){
        if(temp[hists_data[0][i]]) temp[hists_data[0][i]]++
        else temp[hists_data[0][i]] = 1
    }
    for(let i = 0; i < Object.keys(temp).length; ++i){
        if(max_occur < temp[Object.keys(temp)[i]]) max_occur = temp[Object.keys(temp)[i]]
    }
    properties.heightScale.domain([0, max_occur])

    // append the svg object to the body of the page
    let svg = properties.svg
        .append("g")
        .attr("transform", "translate(" + properties.margin.left + ", 0)")

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

    // set the parameters for the histogram
    let histogram = d3.histogram()
        .value(function(d) { return +d.value; })   // I need to give the vector of value
        .domain(properties.heightScale.domain())  // then the domain of the graphic
        .thresholds( properties.heightScale.ticks(40)); // then the numbers of bins

    for(let i = 0; i < hists_data.length; ++i){

        let bins = histogram(hists_data[i]);

         // append the bars for series 1
        svg.selectAll("rect"+i)
            .data(bins)
            .enter()
            .append("rect")
            .attr("x", 1)
            .attr("transform", function(d) { return "translate(" + properties.widthScaleLinear(d.x0) + "," + properties.heightScale(d.length) + ")"; })
            .attr("width", function(d) { return properties.widthScaleLinear(d.x1) - properties.widthScaleLinear(d.x0) })
            .attr("height", function(d) { return properties.heightScale(d.length) + properties.height })
            .style("fill", "#69b3a2")
            .style("opacity", 0.6)
    }

    // Handmade legend
    svg.append("circle").attr("cx",300).attr("cy",30).attr("r", 6).style("fill", "#69b3a2")
    svg.append("circle").attr("cx",300).attr("cy",60).attr("r", 6).style("fill", "#404080")
    svg.append("text").attr("x", 320).attr("y", 30).text("variable A").style("font-size", "15px").attr("alignment-baseline","middle")
    svg.append("text").attr("x", 320).attr("y", 60).text("variable B").style("font-size", "15px").attr("alignment-baseline","middle")

}