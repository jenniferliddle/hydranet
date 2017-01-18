  jQuery('.hydranet_chart').each(function(i) {
    var id = jQuery(this).data('id');
    var w = jQuery(this).data('width') || 650;
    var h = jQuery(this).data('height') || 300;
    var t = jQuery(this).data('title') || id;
    var chart = drawChart({'id': id, 'width': w, 'height': h, 'title': t});
    if (chart != null) {
      if (chart.svg != null) {
        div = document.createElement("div");
        jQuery(div).append(function() { return chart.svg.node(); } );
        jQuery(div).addClass('chart');
        jQuery(div).css('width',w);
        jQuery(div).css('height',h);
        jQuery(this).append(div);
      }
    }
  });

function drawChart(config)
{
    var id = config.id;
    var width = config.width;
    var height = config.height;
    var title = config.title || 'Graph';

    var padding = {
      top: 50,
      right: 25,
      bottom: 25,
      left: 50
    };

var series = [[ [1,1], [2,4], [3,9], [4,16], [5,25] ]];

    var bare_svg = document.createElementNS(d3.ns.prefix.svg, 'svg');
    var svg = d3.select(bare_svg)
            .attr("width", width + padding.left + padding.right)
            .attr("height", height + padding.top + padding.bottom);

    var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;
//    var x = d3.time.scale().range([0, width]);
    var x = d3.scale.linear().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    x.domain(d3.extent(series, function(d) { return d.date; }));
    y.domain(d3.extent(series, function(d) { return d.value; }));

    var xAxis = d3.svg.axis().scale(x).orient("bottom");
    var yAxis = d3.svg.axis().scale(y).orient("left");

    var line = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.value); });

//    d3.json("/data/"+id, function(error, json) {
//        if (error) throw error;
//        var series = json.data;

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
      .append("text")
      .attr("dy", ".71em")
      .attr("text-anchor", "middle")
      .attr("transform", "translate(" + (width / 2) + "," + padding.bottom / 2 + ")")
      .attr("style", "font-size: 12; font-family: Helvetica, sans-serif")
      .text('Date');


        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
        .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Price ($)");

        svg.append('text')
            .attr("transform", "translate(" + padding.left + ", " + padding.top / 4 + ")")
            .style('font-size', padding.top / 4)
            .text(title);

        series.forEach(function(d) {
 //           var sd = d.data;
var sd = d;
            var legend = d.legend;
            var n = 0;
            var datum = [];
            sd.forEach(function(s) {
                var p={};
                //p.date = parseDate(s[0]);
                p.date = n; n=n+1;
                p.value = +s[1];
                datum.push(p);
            });

            svg.append("path")
             .data(datum)
             .attr("class", "line")
             .attr("d", line);

        });
//    });

    return {
      'svg': svg
    };

}

