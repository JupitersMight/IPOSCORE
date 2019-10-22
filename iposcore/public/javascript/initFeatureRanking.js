"use strict"


function get_next_prev(value, properties){
    let curr = properties.data_types.indexOf(properties.curr_data_type)
    curr = (curr + value) % properties.data_types.length
    if(curr < 0)
        curr = properties.data_types.length - 1
    properties.curr_data_type = properties.data_types[curr]
    d3.selectAll(".d3-tip").remove()
    renderSingleBarchart(properties, false, undefined)
}

/**
 * Main function called by HTML Script, initializes all the interactions of the page and visualizations
 * @param graphData contains the data received from the backend in JSON format (documented in Github)
 */
function init(graphData){
    //Initialization of main properties used by the visualizations
    const properties ={}

    properties.data = graphData

    properties.margins = {
            top: 30,
            right: 20,
            bottom: 30,
            left: 90
    }

    properties.MAX_LABEL_SIZE_Y = 200
    properties.MAX_LABEL_SIZE_X = 150
    properties.displayingAll = false

    properties.data_types = Object.keys(graphData)
    properties.scoring_functions = Object.keys(graphData[properties.data_types[0]])
    properties.class_labels = Object.keys(graphData[properties.data_types[0]][properties.scoring_functions[0]])

    properties.curr_class_label = properties.class_labels[0]
    properties.curr_scoring_function = properties.scoring_functions[0]
    properties.curr_data_type = properties.data_types[0]

    // On click functions for existing buttons
    d3.select("#prev").on("click",()=>get_next_prev(-1, properties))
    d3.select("#next").on("click",()=>get_next_prev(1, properties))
    d3.select("#displayall").on("click",()=>renderMultipleBarcharts(properties, true))

    // Fill dropdowns
    dropdown(
        // List of functions for each dropdown
        [
            function(class_label){
		        d3.selectAll(".d3-tip").remove()
                properties.curr_class_label =class_label
                properties.displayingAll ? renderMultipleBarcharts(properties, false) : renderSingleBarchart(properties, false, undefined)
            },
            function(score_function){
		        d3.selectAll(".d3-tip").remove()
                properties.curr_scoring_function  = score_function
                properties.displayingAll ? renderMultipleBarcharts(properties, false) : renderSingleBarchart(properties, false, undefined)
            }
        ],
        // List of html element id for each dropdown
        [
            "#class_label_dropdown",
            "#score_function_dropdown"
        ],
        // List of arrays for dropdown options
        [
            properties.class_labels,
            properties.scoring_functions
        ]
    )

    // Default view for single barchart
    renderSingleBarchart(properties, true, undefined)
}

/**
 * Function called to display a single bar chart in detail
 * @param properties object containing the information needed to render the visualizations
 * @param init flag to render extra components if it's the first rendering
 * @param clicked_data_type if user clicked from multiple bar chart visualization then this field has information
 */
function renderSingleBarchart(properties, init, clicked_data_type){

	if(!init)
		d3.select("div#slider-fill > *").remove()

    // If user clicked from multiple bar chart visualization then this field has information
    // Change the flag according to the information
	if(clicked_data_type)
		properties.curr_data_type = clicked_data_type

    // Change flag to inform the system that only one bar chart is displayed
    properties.displayingAll = false

    // Retrieve selected data according to flags
    const current_data = properties.data[properties.curr_data_type][properties.curr_scoring_function][properties.curr_class_label]

    // Width and Height of SVG
	const fullwidth = 1024
	const fullheight = 768

	if(init){
	    // Remove previous content inside content container
		d3.selectAll(".content-svgs>*").remove()
		d3.selectAll(".d3-tip").remove()

		let currRow = d3.select(".content-svgs").append("div").attr("class","row centered")
		currRow.append("div").attr("class", "col-sm-12").attr("id", "slider-div")
		// Create container for slider
		properties.slidderContainer = d3.select("#slider-div")
			.append("div")
			.attr("class", "row align-items-center")
		// Create container for value of slider
		properties.slidderContainer
			.append("div")
			.attr("class", "col-sm")
			.append("p")
			.attr("id", "value-fill")
			.style("border-style", "solid")
			.style("border-width", "thin")
		// Create container for slider
		properties.slidderContainer
			.append("div")
			.attr("class", "col-sm")
			.append("div")
			.attr("id", "slider-fill")
		//Create container where title and bar chart will appear
		properties.svg = currRow.append("div").attr("class","col-sm-12")
		//Add title for barchart
		properties.svg
			.append("h3")
			.attr("id","h3_"+ properties.curr_data_type)
			.attr("align", "center")
			.style("text-decoration", "underline")
			.text(properties.curr_data_type)
		// Define SVG
		properties.svg = properties.svg.append("svg")
			.attr("id", "svg_" + properties.curr_data_type)
			.attr("width", fullwidth)
			.attr("height", fullheight)
			.attr("class", "centered")
	}

	// Find out maximum value for the height scale
	let max = 0
	for(let i = 0; i < current_data.length; ++i)
		if(max < current_data[i].column_value)
			max = current_data[i].column_value

    // Change flags and objects of properties for single bar chart visualization
	properties.heightMax = max
	properties.width = fullwidth - properties.margins.left - properties.margins.right - properties.MAX_LABEL_SIZE_X
	properties.height = fullheight - properties.margins.top - properties.margins.bottom - properties.MAX_LABEL_SIZE_Y
	properties.heightScale = d3.scaleSqrt().range([properties.height, 0])
	properties.widthScale = d3.scaleBand().rangeRound([0, properties.width]).padding(0.3)
	properties.yAxis = d3.axisLeft(properties.heightScale).tickFormat(
		d3.format(
			properties.curr_scoring_function.indexOf("stats") !== -1 ||
			properties.curr_scoring_function.indexOf("p-value") !== -1 ?
				".4~s" :
				".1%"
		)
	)
	properties.xAxis = d3.axisBottom(properties.widthScale)
	properties.maxSlidderValue = current_data.length

	// Add the display all button and activate the prev and next buttons
	d3.select("#displayall").on("click",()=>renderMultipleBarcharts(properties, true)).text("Display All")
	d3.select("#prev").attr("disabled",null)
	d3.select("#next").attr("disabled",null)
	fillerSlider(properties, current_data)
	// Render barchart
	renderBarchart(current_data.slice(0, 10), properties, init)
}

/**
 * Function called to display all the bar chart of all data types
 * @param properties object containing the information needed to render the visualizations
 * @param init flag to render extra components if it's the first rendering
 */
function renderMultipleBarcharts(properties, init){
    // Change flag to inform the system that multiple bar charts are displayed
    properties.displayingAll = true

	let currRow
	if(init){
	    // Remove previous content inside content container
	    d3.selectAll(".content-svgs>*").remove()
		d3.selectAll(".d3-tip").remove()
		currRow = d3.select(".content-svgs").append("div").attr("class","row centered")
	}

	// Find out maximum value for the height scale
	let max = 0
	for(let i = 0; i<properties.data_types.length; ++i){
		for(let x = 0; x<properties.data[properties.data_types[i]][properties.curr_scoring_function][properties.curr_class_label].length; ++x){
			const currentValue = properties.data[properties.data_types[i]][properties.curr_scoring_function][properties.curr_class_label][x]
			if(max < currentValue.column_value)
				max = currentValue.column_value
		}
	}

	// Change flags and objects of properties for multiple barchart visualization
	properties.heightMax = max
	properties.width = 500 - properties.margins.left - properties.margins.right - properties.MAX_LABEL_SIZE_X
	properties.height = 700 - properties.margins.top - properties.margins.bottom - properties.MAX_LABEL_SIZE_Y
	properties.heightScale = d3.scaleSqrt().range([properties.height, 0])
	properties.widthScale = d3.scaleBand().rangeRound([0, properties.width]).padding(0.3)
	properties.yAxis = d3
		.axisLeft(properties.heightScale)
		.tickFormat(
		    d3.format(
		        properties.curr_scoring_function.indexOf("_stats") !== -1 ||
                    properties.curr_scoring_function.indexOf("_p-value") !== -1?
                    ".4~s" :
                    ".1%"
            )
        )
	properties.xAxis = d3.axisBottom(properties.widthScale)

    // Render a bar chart for each data type
	for (let i = 0; i < properties.data_types.length; ++i) {
		properties.curr_data_type = properties.data_types[i]
        // If first render then render additional components
		if(init) {
			properties.svg = currRow
				.append("div")
				.attr("class", "col-sm-6")

			properties.svg.append("h3")
				.attr("id","h3_"+ properties.data_types[i])
				.attr("align", "center")
				.style("text-decoration", "underline")
				.text(properties.curr_data_type)

			properties.svg = properties.svg
				.append("svg")
				.attr("id", "svg_" + properties.data_types[i])
				.attr("width", 500)
				.attr("height", 700)
				.attr("class", "centered")

			properties.svg.on("click", () => renderSingleBarchart(properties, true, properties.data_types[i]))
			renderBarchart(
				properties.data[properties.data_types[i]][properties.curr_scoring_function][properties.curr_class_label].slice(0,10),
				properties,
				init
			)
		}
		// Else update existing
		else{
			properties.svg = d3.select("#svg_"+properties.data_types[i])
			renderBarchart(
				properties.data[properties.data_types[i]][properties.curr_scoring_function][properties.curr_class_label].slice(0,10),
				properties,
				init
			)
		}
	}
	// If first render then disable buttons and change existing buttons
	if(init) {
        d3.select("#displayall")
            .on("click",
                () => renderSingleBarchart(
                    properties,
                    true,
                    properties.data_types[properties.data_types.indexOf(properties.curr_data_type)]
                )
            ).text("Hide All")
        d3.select("#prev").attr("disabled", "disabled")
        d3.select("#next").attr("disabled", "disabled")
    }
}
