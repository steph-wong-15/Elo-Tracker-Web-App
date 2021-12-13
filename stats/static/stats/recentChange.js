function recentChangeGraph(changes=[], currentRating = 1000, svgidentifier){


    height = $(svgidentifier).height()
    width =  $(svgidentifier).width()

    //Convert changes to absolute values

    ratings = []

    after = currentRating

    entries = 20

    rev = changes.slice().reverse()

    for(change in changes){
        before = after-rev[change]
        ratings = ratings.concat([[before, after]])
        after = before
    }
    ratings = ratings.reverse()
    //Come up with scales

    min = d3.min(ratings, val =>(d3.min(val)))
    max = d3.max(ratings, val =>(d3.max(val)))

    xScale = d3.scaleLinear()
        .domain([0,entries-1])
        .range([width*0.05, (width*0.95)])

    yScale = d3.scaleLinear()
        .domain([min, max])
        .range([height-10, 10])

    
    svg = d3.select(svgidentifier)

    svg.selectAll("rect")
        .data(ratings)
        .join("rect")

        .attr("x", function(d, i){
            return xScale(i);
        })

        .attr("y", function(d, i){
            return yScale(d3.max(d))
        })

        .attr("width", function(d){
            return width*0.9/entries/2
        })

        .attr("height", function(d){
            return Math.abs(yScale(d[1]) - yScale(d[0]))
        })

        .attr("fill", function(d){
            if(d[0] > d[1]) return "red"
            return "green"
        })


    
        // .each(function(){
        //     temp = this.parentNode
        //     a = document.createElementNS("http://www.w3.org/2000/svg","a")
        //     a.setAttribute("href", "/game/test/example/123")
        //     temp.replaceChild(a, this)
        //     a.appendChild(this)
            
        // })

        .append("title")
            .text(function(d){
                if(d[1] > d[0]) return "+" + (d[1] - d[0])
                return d[1] - d[0]
        });

    svg
        .append("g")
        .attr("transform", `translate(${width-10},0)`)
        .call(d3.axisLeft(yScale))

    //debugger
}