"use strict"

function renderBoxplot(properties, init){

    const height_domain = properties.yAxisDomain[properties.curr_class_label]

    const dataset = properties.data[properties.curr_data_type][properties.curr_attribute].dataset

    const boxs_data = []
    for(let x = 0; x < height_domain.length; ++x) {
        boxs_data.push([])
        const curr_data = x === 0 ? dataset : dataset.filter(d => d[properties.curr_class_label] === height_domain[x])
        for (let i = 0; i < curr_data.length; ++i) {
            boxs_data[x].push(curr_data[i][properties.curr_attribute])
        }
        boxs_data[x].sort((a, b) => a - b)
    }

    // Prepare the data for the box plots
    let boxPlotData = []
    let tmp = {}
    let localMin = d3.min(boxs_data[0])
    let localMax = d3.max(boxs_data[0])

    tmp["key"] = "All"
    tmp["counts"] = boxs_data[0].sort((a, b) => a - b)
    tmp["quartile"] = boxQuartiles(boxs_data[0])
    tmp["whiskers"] = [localMin, localMax]

    boxPlotData.push(tmp)

    for (let x = 1; x< boxs_data.length; ++x){

        let record = {}
        let localMin = d3.min(boxs_data[x])
        let localMax = d3.max(boxs_data[x])

        record["key"] = ""+x
        record["counts"] = boxs_data[x].sort((a, b) => a - b)
        record["quartile"] = boxQuartiles(boxs_data[x])
        record["whiskers"] = [localMin, localMax]

        boxPlotData.push(record)
    }

    let max = 0
    for (let i = 0; i < boxPlotData.length; ++i)
        if (max < boxPlotData[i].counts[boxPlotData[i].counts.length - 1])
            max = boxPlotData[i].counts[boxPlotData[i].counts.length - 1]


    properties.widthScaleLinear.domain([0, max])
    properties.heightScale.domain(height_domain)
    properties.xAxisLinear.scale(properties.widthScaleLinear)
    properties.yAxis.scale(properties.heightScale)

    let barWidth = properties.heightScale.bandwidth() / 2

    // Setup the svg and group we will draw the box plot in
    let svg = properties.svg.append("g").attr("transform", "translate(" + properties.margin.left + ", 0 )")

    // Draw the box plot vertical lines
    let verticalLines = svg.selectAll(".verticalLines")
        .data(boxPlotData)
        .enter()
        .append("line")
        .attr("x1",(datum) => properties.widthScaleLinear(datum.whiskers[0]))
        .attr("y1", (datum, i) => properties.heightScale(height_domain[i]) + barWidth)
        .attr("x2", (datum) => properties.widthScaleLinear(datum.whiskers[1]))
        .attr("y2", (datum, i) => properties.heightScale(height_domain[i]) + barWidth)
        .attr("stroke", "#000")
        .attr("stroke-width", 1)
        .attr("fill", "none")

    // Draw the boxes of the box plot, filled in white and on top of vertical lines
    let rects = svg.selectAll("rect")
        .data(boxPlotData)
        .enter()
        .append("rect")
        .attr("height", barWidth)
        .attr("width", (datum) => properties.widthScaleLinear(datum.quartile[2]) - properties.widthScaleLinear(datum.quartile[0]))
        .attr("x", (datum) => properties.widthScaleLinear(datum.quartile[0]))
        .attr("y", (datum, i) => properties.heightScale(height_domain[i]) + barWidth / 2)
        .attr("fill", "#238443")
        .attr("stroke", "#000")
        .attr("stroke-width", 1)

    // Now renderBarchart all the horizontal lines at once - the whiskers and the median
    let horizontalLineConfigs = [
        // Top whisker
        {
            x1: function(datum, i) { return properties.widthScaleLinear(datum.whiskers[0]) },
            y1: function(datum, i) { return properties.heightScale(height_domain[i]) + barWidth - barWidth / 2 },
            x2: function(datum, i) { return properties.widthScaleLinear(datum.whiskers[0]) },
            y2: function(datum, i) { return properties.heightScale(height_domain[i]) + barWidth + barWidth / 2 }
        },
        // Median line
        {
            x1: function(datum, i) { return properties.widthScaleLinear(datum.quartile[1]) },
            y1: function(datum, i) { return properties.heightScale(height_domain[i]) + barWidth - barWidth / 2},
            x2: function(datum, i) { return properties.widthScaleLinear(datum.quartile[1]) },
            y2: function(datum, i) { return properties.heightScale(height_domain[i]) + barWidth + barWidth / 2}
        },
        // Bottom whisker
        {
            x1: function(datum, i) { return properties.widthScaleLinear(datum.whiskers[1]) },
            y1: function(datum, i) { return properties.heightScale(height_domain[i]) + barWidth - barWidth / 2 },
            x2: function(datum, i) { return properties.widthScaleLinear(datum.whiskers[1]) },
            y2: function(datum, i) { return properties.heightScale(height_domain[i]) + barWidth + barWidth / 2 }
        }
    ]

    for(let i=0; i < horizontalLineConfigs.length; i++) {
        let lineConfig = horizontalLineConfigs[i]

        // Draw the whiskers at the min for this series
        let horizontalLine = svg.selectAll(".whiskers")
            .data(boxPlotData)
            .enter()
            .append("line")
            .attr("x1", lineConfig.x1)
            .attr("y1", lineConfig.y1)
            .attr("x2", lineConfig.x2)
            .attr("y2", lineConfig.y2)
            .attr("stroke", "#000")
            .attr("stroke-width", 1)
            .attr("fill", "none")
    }

    function boxQuartiles(d) {
        return [
            d3.quantile(d, .25),
            d3.quantile(d, .5),
            d3.quantile(d, .75)
        ]
    }

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

}