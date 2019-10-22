"use strict"

function fillerSlider(properties){

    let values = d3.range(1, properties.maxSlidderValue)


    let sliderFill = d3.sliderBottom()
        .min(1)
        .max(properties.maxSlidderValue)
        .step(1)
        .width(500)
        .tickFormat(d3.format(""))
        .tickValues(values)
        .default(Math.round(properties.maxSlidderValue/3))
        .fill("#2196f3")
        .on("onchange", val => {
            d3.select("#value-fill").text(d3.format("")(val))
            d3.selectAll(".d3-tip").remove()
            renderBarchart(
                properties.data[properties.curr_data_type][properties.curr_scoring_function][properties.curr_class_label].slice(0,val),
                properties,
                false
            )
        })

    let gFill = d3
        .select("div#slider-fill")
        .append("svg")
        .attr("width", 600)
        .attr("height", 100)
        .append("g")
        .attr("transform", "translate(30,30)")

    gFill.call(sliderFill)

    d3.select("#value-fill").text(d3.format("")(sliderFill.value()))
}

/** play with transition
 * gTransition
      .transition()
      .duration(200)
      .call(sliderTransition);
 */
