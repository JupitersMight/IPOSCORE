"use strict"

function renderBoxplot(properties, init){

    let barWidth = 30;


    // Prepare the data for the box plots
    let boxPlotData = [];
    for (let x = 0; x< groupCounts; ++x){

        let record = {};
        let localMin = d3.min(groupCount[x]);
        let localMax = d3.max(groupCount[x]);

        record["key"] = x;
        record["counts"] = groupCounts[x].sort((a, b) => a - b);
        record["quartile"] = boxQuartiles(groupCount[x]);
        record["whiskers"] = [localMin, localMax];

        boxPlotData.push(record);
    }
    let height_domain = ["All"]
     if(properties.curr_class_label === "complicação pós-cirúrgica")
        for(let i = 0; i < 2; ++i)
            height_domain.push(""+i)
    if(properties.curr_class_label === "classificação clavien-dindo")
        for(let i = 0; i < 8; ++i)
            height_domain.push(""+i)

    // Compute an ordinal xScale for the keys in boxPlotData
    let yScale = d3.scalePoint()
        .domain(height_domain)
        .rangeRound([0, width])
        .padding([0.5]);

    let max = 0
    for (let i = 0; i < boxPlotData.length; ++i)
        if (max < boxPlotData[i].counts[boxPlotData[i].counts.length - 1])
            max = boxPlotData[i].counts[boxPlotData[i].counts.length - 1]

    // Compute a global y scale based on the global counts
    let xScale = d3.scaleLinear()
    .domain([0, max])
    .range([0, height])

    // Setup the svg and group we will draw the box plot in
    let svg = properties.svg.append("g")
    .attr("transform", "translate(" + properties.margin.left + "," + properties.margin.top + ")");

    // Move the left axis over 25 pixels, and the top axis over 35 pixels
    let axisG = svg.append("g").attr("transform", "translate(25,0)");
    let axisTopG = svg.append("g").attr("transform", "translate(35,0)");

    // Setup the group the box plot elements will render in
    let g = svg.append("g")
    .attr("transform", "translate(20,5)");

    // Draw the box plot vertical lines
    let verticalLines = g.selectAll(".verticalLines")
    .data(boxPlotData)
    .enter()
    .append("line")
    .attr("x1", function(datum) {
    let whisker = datum.whiskers[0];
    return xScale(whisker);
    }
    )
    .attr("y1", function(datum) {
    return yScale(datum.key) + barWidth/2;
    }
    )
    .attr("x2", function(datum) {
    let whisker = datum.whiskers[1];
    return xScale(whisker);
    }
    )
    .attr("y2", function(datum) {
    return yScale(datum.key) + barWidth/2;
    }
    )
    .attr("stroke", "#000")
    .attr("stroke-width", 1)
    .attr("fill", "none");

    // Draw the boxes of the box plot, filled in white and on top of vertical lines
    let rects = g.selectAll("rect")
    .data(boxPlotData)
    .enter()
    .append("rect")
    .attr("width", barWidth)
    .attr("height", function(datum) {
    let quartiles = datum.quartile;
    let height = yScale(quartiles[2]) - yScale(quartiles[0]);
    return height;
    }
    )
    .attr("x", function(datum) {
    return xScale(datum.quartile[0])
    }
    )
    .attr("y", function(datum) {
    return yScale(datum.key)
    }
    )
    .attr("fill", "#238443")
    .attr("stroke", "#000")
    .attr("stroke-width", 1);

    // Now render all the horizontal lines at once - the whiskers and the median
    let horizontalLineConfigs = [
    // Top whisker
    {
    x1: function(datum) { return xScale(datum.whiskers[0]) },
    y1: function(datum) { return yScale(datum.key) },
    x2: function(datum) { return xScale(datum.whiskers[0]) },
    y2: function(datum) { return yScale(datum.key) + barWidth }
    },
    // Median line
    {
    x1: function(datum) { return xScale(datum.quartile[1]) },
    y1: function(datum) { return yScale(datum.key) },
    x2: function(datum) { return xScale(datum.quartile[1]) },
    y2: function(datum) { return yScale(datum.key) + barWidth },
    },
    // Bottom whisker
    {
    x1: function(datum) { return xScale(datum.whiskers[1]) },
    y1: function(datum) { return yScale(datum.key) },
    x2: function(datum) { return xScale(datum.whiskers[1]) },
    y2: function(datum) { return yScale(datum.key) + barWidth }
    }
    ];

    for(let i=0; i < horizontalLineConfigs.length; i++) {
    let lineConfig = horizontalLineConfigs[i];

    // Draw the whiskers at the min for this series
    let horizontalLine = g.selectAll(".whiskers")
    .data(boxPlotData)
    .enter()
    .append("line")
    .attr("x1", lineConfig.x1)
    .attr("y1", lineConfig.y1)
    .attr("x2", lineConfig.x2)
    .attr("y2", lineConfig.y2)
    .attr("stroke", "#000")
    .attr("stroke-width", 1)
    .attr("fill", "none");
    }

    // Setup a scale on the left
    var axisLeft = d3.axisLeft(yScale);
    axisG.append("g")
    .call(axisLeft);

    // Setup a series axis on the top
    var axisTop = d3.axisBottom(xScale);
    axisTopG.append("g")
    .call(axisTop);

    function boxQuartiles(d) {
    return [
    d3.quantile(d, .25),
    d3.quantile(d, .5),
    d3.quantile(d, .75)
    ];
    }

}