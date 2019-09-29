'use strict'

function render(data, properties){

    const svg = d3.select(".content-svgs").append('div').attr('class','centered_svg').append('svg'),
        width = properties.width - properties.left - properties.right - properties.MAX_LABEL_SIZE_X,
        height = properties.height - properties.top - properties.bottom - properties.MAX_LABEL_SIZE_Y

    svg.attr('width',properties.width).attr('height',properties.height)
    // set the ranges
    let x = d3.scaleBand().rangeRound([0, width]).paddingInner(0.1),
        y = d3.scaleLinear().rangeRound([height, 0])

    x.domain(data.map(d => d.column_name))
    y.domain([0, 100])

    let g = svg.append("g")
        .attr("transform", "translate(" + properties.left + "," + properties.top + ")")

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
        .call(d3.axisLeft(y).ticks(10))
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
        .attr("x", d => x(d.column_name))
        .attr("y", d => y(d.column_value))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.column_value))

}
