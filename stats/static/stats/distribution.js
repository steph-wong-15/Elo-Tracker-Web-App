function distributionGraph(data=[], svgidentifier){

    svg = d3.select(svgidentifier)

    divCount = d3.min([8, data.length])


    min = d3.min(data)
    max = d3.max(data)

    height = $(svgidentifier).height()
    width =  $(svgidentifier).width()

    divSize = (max-min)/divCount

    slots = [...Array(divCount).keys()]
    slots = slots.map(val => val*divSize + min)
    groups = slots.map(val => data.filter( function(dat){ return ( (dat >= val) && (dat < val + divSize))} ) )
    groups[groups.length-1] =  groups[groups.length-1].concat(d3.max(data))

    
    yScale = d3.scaleLinear()
        .domain([0,d3.max(groups.map(val => val.length))])
        //.range([height,height*0.05])
        .range([height,height*0.05])
    xScale = d3.scaleLinear()
        .domain([0, slots.length])
        .range([width*0.05, width])
 
    xAxis = d3.scaleLinear()
        .domain([min - (max-min)*(0.05/0.95), max])
        .range([0, width])

    // xAxis = d3.scaleLinear()
    //     .domain([min, max])
    //     .range([width*0.05, width])

    points = slots.map(val => [xScale(slots.indexOf(val)), yScale(groups[slots.indexOf(val)].length)])
    points = points.concat([[width, height-20]])
    points.unshift([0,height-20])

    ////
    //curveShape = d3.line().curve(d3.curveNatural);
    curveShape = d3.line().curve(d3.curveBasis)
    svg
        .append('path')
        .attr('d', curveShape(points))
        .attr('stroke', 'black')
        .attr('fill', 'none');
    svg
        .append("g")
        .attr("transform", `translate(0,${height-20})`)
        .call(d3.axisBottom(xAxis))
        //.attr()
        
    //ToDo

    //Add horizontal line (+ red fill for selected area?) that gives precise values for ELO and
    //How many users have up and including that rating (white background)

    // svg
    //     .on("mouseover", function(){
    //         console.log("mousing over")
    //         // recip = this.children[0].innerHTML
    //         // mtotal = _radialData.filter(o => o.recipient == recip)[0].messageCount
            
    //         // $("#htmlrecip").text("Recipient: " + recip)
    //         // $("#htmltotal").text("Total message count: " + mtotal)
    
    //         // d3.select(this)
    //         // .attr("stroke", "red")
    //         // .raise()
    //     })
    //     .on("mouseout", function(){
    //         d3.select(this)
    //         .attr("stroke", null)
        //})

    return 0
}