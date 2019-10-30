"use strict"

function initExploration(graphData){

    const properties = {}

    properties.data = graphData
    properties.margin = {
        top: 50,
        right: 100,
        bottom: 30,
        left: 100
    }

    properties.class_labels = ["complicação pós-cirúrgica", "classificação clavien-dindo"]
    properties.data_types = Object.keys(graphData)
    properties.visualizations = [
        {
            name:"Violin Charts",
            renderChart: (properties, init) => renderViolin(properties, init),
            prep: (properties, init) => preparationViolin(properties, init)
        },
        {
            name:"Histogram",
            renderChart: (properties, init) => renderHistogram(properties, init),
            prep: (properties) => preparationHistogram(properties)
        },
        {
            name:"Box Plot",
            renderChart: (properties, init) => renderBoxplot(properties, init),
            prep: (properties) => preparationBoxplot(properties)
        },
        {
            name: "Parallel Coordinates",
            renderChart: (properties, init) => renderParallelCoordinate(properties, init),
            prep: (properties) => preparationParallel(properties)
        }
    ]

    // Init with default values
    properties.curr_data_type = properties.data_types[1]
    properties.curr_visualization = properties.visualizations[0]
    properties.curr_class_label = properties.class_labels[0]
    properties.curr_attribute = Object.keys(properties.data[properties.curr_data_type])[0]
    // First data selected
    properties.curr_data = properties.data[properties.curr_data_type][properties.curr_attribute].dataset
    // SVG Setup
    const fullwidth = 1024
    const fullheight = 768
    properties.width = fullwidth - properties.margin.left - properties.margin.right
    properties.height = fullheight - properties.margin.top - properties.margin.bottom
    properties.svg = d3.select(".content-svgs")
        .append("div")
        .attr("class","row centered")
        .append("div")
        .attr("class","col-sm-12")
        .append("svg")
        .attr("width", properties.width + properties.margin.left + properties.margin.right)
        .attr("height", properties.height + properties.margin.top + properties.margin.bottom)
    // Axis for charts
    properties.yAxisDomain = {
        "complicação pós-cirúrgica": [],
        "classificação clavien-dindo": []
    }
    for(let i = 0; i<Object.keys(properties.yAxisDomain).length; ++i){
        const height_domain = []
        height_domain.push("All")
        if(Object.keys(properties.yAxisDomain)[i] === "complicação pós-cirúrgica")
            for(let i = 0; i < 2; ++i)
                height_domain.push(""+i)
        if(Object.keys(properties.yAxisDomain)[i] === "classificação clavien-dindo")
            for(let i = 0; i < 8; ++i)
                height_domain.push(""+i)
        properties.yAxisDomain[Object.keys(properties.yAxisDomain)[i]] = height_domain
    }
    properties.threshold_spacing = properties.curr_data_type === "Numerical_Continuous" ? 0.1 : 1
    // Initiate properties for each view
    // Common for each view
    properties.widthScaleLinear = d3.scaleLinear().range([0, properties.width])
    properties.heightScale = d3.scaleBand().rangeRound([properties.margin.top, properties.height]).padding(0.3)
    properties.xAxisLinear = d3.axisBottom(properties.widthScaleLinear)
    properties.yAxis = d3.axisLeft(properties.heightScale)
    properties.svg = d3.select(".content-svgs").select("svg")

    // Properties for violin
    properties.containerViolin = {}

    // Properties for Parallel
    properties.containerParallel = {}

    // Properties for Boxplot
    properties.containerBoxplot = {}

    // Properties for Histogram
    properties.containerHistogram = {}

    properties.containerHistogram.heightScale = d3.scaleLinear().range([properties.height, 0])
    properties.containerHistogram.yAxis = d3.axisLeft(properties.containerHistogram.heightScale)

    // Fill dropdowns
    dropdown(
        // List of functions for each dropdown
        [
            function(class_label){
                properties.curr_class_label = class_label
                properties.curr_data = properties.data[properties.curr_data_type][properties.curr_attribute].dataset
                properties.curr_visualization.prep(properties, false)
                properties.curr_visualization.renderChart(properties, false)
            },
            function(visualization){
                d3.select(".content-svgs").selectAll("svg > *").remove()
                properties.curr_visualization  = properties.visualizations.find(d => d.name === visualization)
                properties.curr_data = properties.data[properties.curr_data_type][properties.curr_attribute].dataset
                properties.curr_visualization.prep(properties, true)
                properties.curr_visualization.renderChart(properties, true)
            },
            function(data_type){
                properties.curr_data_type = data_type
                properties.curr_attribute = Object.keys(properties.data[properties.curr_data_type])[0]
                properties.curr_data = properties.data[properties.curr_data_type][properties.curr_attribute].dataset
                properties.threshold_spacing = properties.curr_data_type === "Numerical_Continuous" ? 0.01 : 1
                // Update attribute
                let dropdown_attributes = d3.select("#attribute_selector")

                dropdown_attributes.selectAll("select").remove()
                dropdown_attributes.selectAll("option").remove()

                dropdown_attributes
                    .append("select")
                    .selectAll("option")
                    .data(Object.keys(properties.data[properties.curr_data_type]))
                    .enter()
                    .append("option")
                    .attr("value", d  => d)
                    .text(d => d)
                // Render new vizualization
                properties.curr_visualization.prep(properties, false)
                properties.curr_visualization.renderChart(properties, false)
            },
            function(attribute){
                properties.curr_attribute = attribute
                properties.curr_data = properties.data[properties.curr_data_type][properties.curr_attribute].dataset
                properties.curr_visualization.prep(properties, false)
                properties.curr_visualization.renderChart(properties, false)
            }
        ],
        // List of html element id for each dropdown
        [
            "#class_label_dropdown",
            "#visualization",
            "#data_type",
            "#attribute_selector"
        ],
        // List of arrays for dropdown options
        [
            properties.class_labels,
            properties.visualizations.map((d) => d.name),
            properties.data_types,
            Object.keys(properties.data[properties.curr_data_type])
        ]
    )

    preparationViolin(properties, true)
    renderViolin(properties, true)
}

function preparationViolin(properties, init){
    if(init) {
        d3.select(".content-svgs").selectAll("svg>*").remove()
    }
    properties.svg = d3.select(".content-svgs").select("svg")
    // Retrieve height domain of current label
    properties.containerViolin.height_domain = properties.yAxisDomain[properties.curr_class_label]

    // Current selected data
    const dataset = properties.data[properties.curr_data_type][properties.curr_attribute].dataset

    // Get data for each violin displayed
    properties.containerViolin.data = []
    for(let x = 0; x < properties.containerViolin.height_domain.length; ++x) {
        // Push an empty array to fill with values
        properties.containerViolin.data.push([])
        // Select the data based on height domain, if in the first position ("all") all the dataset
        const curr_data = x === 0 ? dataset : dataset.filter(d => d[properties.curr_class_label] === properties.containerViolin.height_domain[x])
        for (let i = 0; i < curr_data.length; ++i) {
            properties.containerViolin.data[x].push(curr_data[i][properties.curr_attribute])
        }
        // Sort inserted values for future use
        properties.containerViolin.data[x].sort((a, b) => a - b)
    }

    // Get the maximum value displayed of all violins for the X-Axis range setter
    properties.containerViolin.max = 0
    for (let i = 0; i <properties.containerViolin.data.length; ++i) {
        const max_value_of_index = properties.containerViolin.data[i][properties.containerViolin.data[i].length - 1]
        if (properties.containerViolin.max < max_value_of_index)
            properties.containerViolin.max = max_value_of_index
    }

    // Thresholds for bins in histogram
    properties.containerViolin.thresholds = []
    for (let i = 0; i <= properties.containerViolin.max; i += properties.threshold_spacing)
        properties.containerViolin.thresholds.push(i)

    // Threshold spacing for between each bin in histogram
    let temp = properties.threshold_spacing
    properties.containerViolin.threshold_multiplier = 1
    while(temp < 1){
        temp *= 10
        properties.containerViolin.threshold_multiplier *= 10
    }

    // Setters for domain and ranges of axis and scales
    properties.widthScaleLinear.domain([0, properties.containerViolin.max])
    properties.heightScale.domain(properties.containerViolin.height_domain)
    properties.xAxisLinear.scale(properties.widthScaleLinear)
    properties.yAxis.scale(properties.heightScale)

    // Tooltip displayed
    properties.containerViolin.tip = d3.tip()
        .attr("class", "d3-tip")
        .offset([-10, 0])
        .html(d => "<strong></strong>")
}

function preparationParallel(properties){
    d3.select(".content-svgs").select("svg>*").remove()
    properties.svg = d3.select(".content-svgs")
        .select("svg")
        .append("g")
        .attr("transform", "translate(" + properties.margin.left + "," + properties.margin.top + ")")
}

function preparationBoxplot(properties){
    properties.svg = d3.select(".content-svgs").select("svg")
    d3.select(".content-svgs").selectAll("svg>*").remove()

    properties.containerBoxplot.height_domain = properties.yAxisDomain[properties.curr_class_label]

    const dataset = properties.data[properties.curr_data_type][properties.curr_attribute].dataset

    const boxs_data = []
    for(let x = 0; x < properties.containerBoxplot.height_domain.length; ++x) {
        boxs_data.push([])
        const curr_data = x === 0 ? dataset : dataset.filter(d => d[properties.curr_class_label] === properties.containerBoxplot.height_domain[x])
        for (let i = 0; i < curr_data.length; ++i) {
            boxs_data[x].push(curr_data[i][properties.curr_attribute])
        }
        boxs_data[x].sort((a, b) => a - b)
    }

    // Prepare the data for the box plots
    properties.containerBoxplot.boxPlotData = []
    for (let x = 0; x< boxs_data.length; ++x){

        let record = {}
        boxs_data[x] = boxs_data[x].sort((a, b) => a - b)
        let localMin = boxs_data[x][0]
        let localMax = boxs_data[x][boxs_data[x].length-1]

        record["key"] = x == 0 ? "All" : ""+x
        record["counts"] = boxs_data[x]
        record["quartile"] = [
            d3.quantile(boxs_data[x], 0.25),
            d3.quantile(boxs_data[x], 0.5),
            d3.quantile(boxs_data[x], 0.75)
        ]
        record["whiskers"] = [localMin, localMax]

        properties.containerBoxplot.boxPlotData.push(record)
    }

    let max = 0
    for (let i = 0; i < properties.containerBoxplot.boxPlotData.length; ++i)
        if (max < properties.containerBoxplot.boxPlotData[i].counts[properties.containerBoxplot.boxPlotData[i].counts.length - 1])
            max = properties.containerBoxplot.boxPlotData[i].counts[properties.containerBoxplot.boxPlotData[i].counts.length - 1]


    properties.widthScaleLinear.domain([0, max])
    properties.heightScale.domain(properties.containerBoxplot.height_domain)
    properties.xAxisLinear.scale(properties.widthScaleLinear)
    properties.yAxis.scale(properties.heightScale)

    // Tooltip displayed
    properties.containerBoxplot.tip = d3.tip()
        .attr("class", "d3-tip")
        .offset([-10, 0])
        .html(d => "<strong></strong>")

}

function preparationHistogram(properties){
    d3.select(".content-svgs").selectAll("svg>*").remove()
    properties.svg = d3.select(".content-svgs").select("svg")

    const dataset = properties.data[properties.curr_data_type][properties.curr_attribute].dataset

    properties.containerHistogram.hists_data = []
    for(let x = 0; x < properties.yAxisDomain[properties.curr_class_label].length; ++x) {
        properties.containerHistogram.hists_data.push([])
        const curr_data = x === 0 ? dataset : dataset.filter(d => d[properties.curr_class_label] === properties.yAxisDomain[properties.curr_class_label][x])
        for (let i = 0; i < curr_data.length; ++i) {
            properties.containerHistogram.hists_data[x].push(curr_data[i][properties.curr_attribute])
        }
        properties.containerHistogram.hists_data[x].sort((a, b) => a - b)
    }

    properties.containerHistogram.max = 0
    for (let i = 0; i < properties.containerHistogram.hists_data.length; ++i)
        if (properties.containerHistogram.max < properties.containerHistogram.hists_data[i][properties.containerHistogram.hists_data[i].length - 1])
            properties.containerHistogram.max = properties.containerHistogram.hists_data[i][properties.containerHistogram.hists_data[i].length - 1]

    properties.widthScaleLinear.domain([-1, properties.containerHistogram.max])

}

