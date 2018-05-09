var linePlot;
var spiderPlot;
/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
// If changes are not being reflected in the webpage, press Ctrl+Shift+R(Linux)
// to fully reload the webpage without any caching.
function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = linePlot.series[0],
                shift = series.data.length > 200; // shift if the series is
                                                 // longer than 20
          //  console.log("point is : " + point)
            // format:
            //[a, d, h, n, sad, sur, frame]
            // add the points
            //line plot
            linePlot.series[0].addPoint([point[6], point[0]], true);
            linePlot.series[1].addPoint([point[6], point[1]], true);
            linePlot.series[2].addPoint([point[6], point[2]], true);
            linePlot.series[3].addPoint([point[6], point[3]], true);
            linePlot.series[4].addPoint([point[6], point[4]], true);
            linePlot.series[5].addPoint([point[6], point[5]], true);

            //spider plot
            spiderPlot.series[0].setData([point[0], point[1], point[2], point[3], point[4], point[5]],true)
     
            // call it again after one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
  //  console.log("Hello from highcharts")
    linePlot = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'line',
            zoomType: 'xy',
            panning: true,
            events: {
                load: requestData
            }
        },
        tooltip:{
            formatter:function(){
                return 'Frame: ' + this.key + ' Probability: ' + this.y;
            }
        },
        title: {
            text: 'Emotion plot- FaceRecog module'
        },
        xAxis: {
          //  tickPixelInterval: 150,
          //  maxZoom: 20 * 1000
          minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Frame',
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Probability',
                margin: 80
            }
        },
           // format:
            //[a, d, h, n, sad, sur, frame]
        series: [{
            name: 'Anger',
            data: []
        },
        {
            name: 'Disgust',
            data: []
        },
        {
            name: 'Happy',
            data: []
        },
        {
            name: 'Neutral',
            data: []
        },
        {
            name: 'Sad',
            data: []
        },
        {
            name: 'Surprise',
            data: []
        },
        ]
    });

    spiderPlot = new Highcharts.Chart({

        chart: {
            renderTo: 'data-container2',
            polar: true,
            type: 'area'
        },
    
        title: {
            text: 'Emotion probabilities (Spider plot)',
            x: -80
        },
    
        pane: {
            size: '80%'
        },
    
        xAxis: {
            // format:
            //[a, d, h, n, sad, sur, frame]
            categories: ['Angry', 'Disgusted', 'Happy', 'Neutral',
                'Sad', 'Surprise'],
            tickmarkPlacement: 'on',
            lineWidth: 0
        },
    
        yAxis: {
            gridLineInterpolation: 'polygon',
            lineWidth: 0,
            min: 0,
            max : 100
        },
    
        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>',
            hideDelay : 10
        },
    
        legend: {
            align: 'right',
            verticalAlign: 'top',
            y: 70,
            layout: 'vertical'
        },
    
        series: [{
            name: 'Probability of emotion',
            data: [],
            pointPlacement: 'on'
        }]
    
    });
});