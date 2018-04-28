var chart;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 200; // shift if the series is
                                                 // longer than 20
          //  console.log("point is : " + point)
            // format:
            //[a, d, h, n, sad, sur, frame]
            // add the points
            chart.series[0].addPoint([point[6],point[0]], true);
            chart.series[1].addPoint([point[6],point[1]], true);
            chart.series[2].addPoint([point[6],point[2]], true);
            chart.series[3].addPoint([point[6],point[3]], true);
            chart.series[4].addPoint([point[6],point[4]], true);
            chart.series[5].addPoint([point[6],point[5]], true);


            // call it again after one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
  //  console.log("Hello from highcharts")
    chart = new Highcharts.Chart({
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
                return 'Frame: ' + this.key + 'Probability: ' + this.y;
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
});