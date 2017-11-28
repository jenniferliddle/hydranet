  jQuery('.hydranet_chart svg').each(function(i) {
//    var id = this;
//    drawChart(id, 1);
  });


function drawChart(id, period, loading) {
    var graph_id = jQuery(id).data('id');
    var titleX = jQuery(id).data('xtitle') || '';
    var titleY = jQuery(id).data('ytitle') || '';

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
      .tickFormat(function(d) { 
          fmt = '%H:%M';
          if (period>1) { fmt = '%d/%m'; }
          return d3.time.format(fmt)(new Date(d)); 
      });

  chart.yAxis     //Chart y-axis settings
      .axisLabel(titleY)
      .tickFormat(d3.format('.02f'));

  /* Done setting the chart up? Time to render it!*/

    var graphData = [];

    d3.json("/data/"+graph_id+"/"+period, function(error, json) {
        if (error) throw error;
        var series = json.data;

        series.forEach(function(d) {
            var values = [];
            d.data.forEach(function(s) {
                values.push({x: s[0]*1000, y: s[1]});
            });

            graphData.push({values: values, key: d.legend, color: d.colour});
        });


        d3.select("#chart_"+graph_id)    //Select the <svg> element you want to render the chart in.   
            .datum(graphData)         //Populate the <svg> element with chart data...
            .call(chart);          //Finally, render the chart!

        // Update the chart when window resizes.
        nv.utils.windowResize(function() { chart.update() });
    });

  return chart;
});

}

function showChart(id, period) 
{
    //$('#chart_'+id).fadeOut(400);
    //$('#loading_'+id).show(400);
    drawChart($('#chart_'+id),period,$('#loading_'+id)); 
    //$('#loading_'+id).fadeOut(400);
    //$('#chart_'+id).show(400);
}

