'use strict'

function render(graphData){
    let data = []

    for(let i = 0; i< graphData[0].length; ++i){
        data.push({
            column_name : graphData[0][i],
            column_value : graphData[1][i]
        })
    }

    const svg = d3.select("svg"),
        margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 500 - margin.left - margin.right - 50,
        height = 500 - margin.top - margin.bottom - 150

    // set the ranges
    let x = d3.scaleBand().rangeRound([0, width]).paddingInner(0.1),
        y = d3.scaleLinear().rangeRound([height, 0])


    x.domain(data.map(function(d) { return d.column_name; }));
    y.domain([0, 100]);

    let g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("dy", ".35em")
        .attr("transform", "rotate(60)")
        .style("text-anchor", "start")

    g.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y).ticks(10, ""))
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("Frequency")

    g.selectAll(".bar")
      .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.column_name); })
        .attr("y", function(d) { return y(d.column_value); })
        .attr("width", x.bandwidth())
        .attr("height", function(d) { return height - y(d.column_value); })

}
