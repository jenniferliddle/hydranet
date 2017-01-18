  jQuery('.hydranet_chart svg').each(function(i) {
    var graph_id = jQuery(this).data('id');
    var width = jQuery(this).data('width') || 650;
    var height = jQuery(this).data('height') || 300;
    var titleX = jQuery(this).data('xtitle') || '';
    var titleY = jQuery(this).data('ytitle') || '';
    var id = this;

  nv.addGraph(function() {
  var chart = nv.models.lineChart()
                .margin({left: 100})  //Adjust chart margins to give the x-axis some breathing room.
                .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                .color(d3.scale.category10().range())
                .duration(100)  //how fast do you want the lines to transition?
                .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
                .showYAxis(true)        //Show the y-axis
                .showXAxis(true)        //Show the x-axis
  ;

  chart.xAxis     //Chart x-axis settings
      .axisLabel(titleX)
      .tickFormat(function(d) { return d3.time.format('%H:%M')(new Date(d)); });

  chart.yAxis     //Chart y-axis settings
      .axisLabel(titleY)
      .tickFormat(d3.format('.02f'));

  /* Done setting the chart up? Time to render it!*/

    var graphData = [];

    d3.json("/data/"+graph_id, function(error, json) {
        if (error) throw error;
        var series = json.data;

        series.forEach(function(d) {
            var values = [];
            d.data.forEach(function(s) {
                values.push({x: s[0]*1000, y: s[1]});
            });

            graphData.push({values: values, key: d.legend});
        });


        d3.select(id)    //Select the <svg> element you want to render the chart in.   
            .datum(graphData)         //Populate the <svg> element with chart data...
            .call(chart);          //Finally, render the chart!

        // Update the chart when window resizes.
        nv.utils.windowResize(function() { chart.update() });
    });

  return chart;
});

});

