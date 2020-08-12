
var max = 0;
var steps = 10;
var username = '';
var password = '';


var GetChartData = function () {
    $.ajax({
        url: '../vendorStats/',
        method: 'GET',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
        },
        success: function (d) {
           var labels = d.results.map(function(e) {
               return e.key;
           });
           var data = d.results.map(function(e) {
               return e.value;
           });
           var ctx = document.getElementById("myChart");
           var config = {
            type: 'doughnut',
           data: {
              labels: labels,
              datasets: [{
                 //label: 'Graph Line',
                 data: data,
                 backgroundColor: [
                    'rgba(25, 40, 166, 0.7)', //LGE
                    'rgba(83, 51, 237, 1)',
                    'rgba(25, 168, 98, 0.7)',
                    'rgba(220,20,60 ,0.7)',
                    'rgba(255,160,122 ,1)', //Samsung
                 ],
              }]
           }
        };

               var chart = new Chart(ctx, config);

               $('#VendorsTable').bootstrapTable({
                        data: [{
                            labels: labels[0],
                            data: data[0]
                          }, {
                            labels: labels[1],
                            data: data[1]

                          }, {
                            labels: labels[2],
                            data: data[2]

                          }, {
                            labels: labels[3],
                            data: data[3]
                          }, {
                            labels: labels[4],
                            data: data[4]

                        }]
               })
        }
    });
};

$(document).ready(function() {
    GetChartData();
});


var max = 0;
var steps = 10;
var username = '';
var password = '';

var GetChartDataNtw = function () {
    $.ajax({
        url: 'http://localhost:8000/myapp/networks/',
        method: 'GET',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
        },
        success: function (d) {
           var labels = d.results.map(function(n) {
               return n.key;
           });
           var data = d.results.map(function(n) {

                   return n.value;
           });


           var ctx = document.getElementById("ntwChart");
           var config = {
            type: 'pie',
           data: {
              labels: labels,
              datasets: [{

                  label: '',
                  data : data,
                  backgroundColor: [
                  "#f38b4a",
                  "rgba(220, 255, 30, 0.7)",
                  "#56d798",
                  "#6970d5"
                ],
              },

              ]
           }

        };

            var chart = new Chart(ctx, config);

             $('#NetworkTable').bootstrapTable({
                    data: [{
                        labels: labels[0],
                        data: data[0]
                      }, {
                        labels: labels[1],
                        data: data[1]

                      }, {
                        labels: labels[2],
                        data: data[2]

                      }, {
                        labels: labels[3],
                        data: data[3]

                    }]
             })

        }


    });
};

$(document).ready(function() {

    GetChartDataNtw();
});


var max = 0;
var steps = 10;
var username = '';
var password = '';


var GetChartDataStats = function () {
    $.ajax({
        url: '../levelStats/',
        method: 'GET',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
        },
        success: function (statistics) {
           var labels = statistics.results.map(function(s) {
               return s.key;
           });
           var avgData = statistics.results.map(function(s) {
               return s.avg;
           });
           var minData = statistics.results.map(function(s) {
               return s.min;
           });
           var maxData = statistics.results.map(function(s) {
               return s.max;
           });
           var ctx = document.getElementById("statChart");
           var config = {
                type: 'bar',
                data: {
                      labels: labels,
                      datasets: [{
                         label: 'Avg',
                         backgroundColor: 'rgba(0, 119, 204, 0.3)',
                         data: avgData,

                    }, { label: 'Min',
                         backgroundColor: 'rgba(255, 206, 86, 20)',
                         data : minData,
                    },
                       { label: 'Max',
                         backgroundColor: 'rgba(153, 102, 255, 15)',
                         data : maxData,
                    }]
                },
                 options: {
                    scales: {
                        yAxes: [{
                            display : true,
                            ticks: {
                                min: -150,
                                max: 100,
                                beginAtZero:true
                            }
                        }]
                    }
                 }
           }
            var chart = new Chart(ctx, config);

            $('#table').bootstrapTable({
                    data: [{
                        labels: labels[0],
                        avgData: avgData[0],
                        minData: minData[0],
                        maxData: maxData[0]
                      }, {
                        labels: labels[1],
                        avgData: avgData[1],
                        minData: minData[1],
                        maxData: maxData[1]
                      }, {
                        labels: labels[2],
                        avgData: avgData[2],
                        minData: minData[2],
                        maxData: maxData[2]
                      }, {
                        labels: labels[3],
                        avgData: avgData[3],
                        minData: minData[3],
                        maxData: maxData[3]
                      }]

                 })

        }
    });
};

$(document).ready(function () {
    GetChartDataStats();

});



// ======== Measurements with Date range and Network Type  ======= //
var max = 0;
var steps = 10;
var username = '';
var password = '';

var getChartDataSelection = function () {
    $.ajax({
        url: 'http://localhost:8000/myapp/' + $('#iMeasurements').val() + '/' + $('#daterange').val() + '/' + $('#iNetworkType').val() + '/',
        method: 'GET',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
        },
        success: function (statistics) {
           var labels = statistics.results.map(function(s) {
               return s.key;
           });
           var avgData = statistics.results.map(function(s) {
               return s.avg;
           });
           var minData = statistics.results.map(function(s) {
               return s.min;
           });
           var maxData = statistics.results.map(function(s) {
               return s.max;
           });
           var ctx = document.getElementById("statChart");

           var config = {
                type: 'bar',
                data: {
                      labels: labels,
                      datasets: [{
                         label: 'Avg',
                         backgroundColor: 'rgba(0, 119, 204, 0.3)',
                         data: avgData,

                    }, { label: 'Min',
                         backgroundColor: 'rgba(255, 206, 86, 20)',
                         data : minData,
                    },
                       { label: 'Max',
                         backgroundColor: 'rgba(153, 102, 255, 15)',
                         data : maxData,
                    }]
                },
                 options: {
                    scales: {
                        yAxes: [{
                            display : true,
                            ticks: {

                                beginAtZero:true
                            }
                        }]
                    }
                 }
           }

            var chart = new Chart(ctx, config);

                $('#table').bootstrapTable({
                    data: [{
                        labels: labels[0],
                        avgData: avgData[0],
                        minData: minData[0],
                        maxData: maxData[0]
                      }, {
                        labels: labels[1],
                        avgData: avgData[1],
                        minData: minData[1],
                        maxData: maxData[1]
                      }, {
                        labels: labels[2],
                        avgData: avgData[2],
                        minData: minData[2],
                        maxData: maxData[2]
                      }, {
                        labels: labels[3],
                        avgData: avgData[3],
                        minData: minData[3],
                        maxData: maxData[3]
                      }]

                 })

        }

    });
    $('#table').bootstrapTable('destroy');
};

// ======== Measurements with only Date range ======= //
var max = 0;
var steps = 10;
var username = '';
var password = '';

var getDateRangeChart = function () {
    $.ajax({
        url: 'http://localhost:8000/myapp/' + $('#iMeasurements').val() + '/' + $('#daterange').val() + '/',
        method: 'GET',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
        },
        success: function (statistics) {
           var labels = statistics.results.map(function(s) {
               return s.key;
           });
           var avgData = statistics.results.map(function(s) {
               return s.avg;
           });
           var minData = statistics.results.map(function(s) {
               return s.min;
           });
           var maxData = statistics.results.map(function(s) {
               return s.max;
           });
           var ctx = document.getElementById("statChart");

           var config = {
                type: 'bar',
                data: {
                      labels: labels,
                      datasets: [{
                         label: 'Avg',
                         backgroundColor: 'rgba(0, 119, 204, 0.3)',
                         data: avgData,

                    }, { label: 'Min',
                         backgroundColor: 'rgba(255, 206, 86, 20)',
                         data : minData,
                    },
                       { label: 'Max',
                         backgroundColor: 'rgba(153, 102, 255, 15)',
                         data : maxData,
                    }]
                },
                 options: {
                    scales: {
                        yAxes: [{
                            display : true,
                            ticks: {

                                beginAtZero:true
                            }
                        }]
                    }
                 }
           }

            var chart = new Chart(ctx, config);

                $('#table').bootstrapTable({
                    data: [{
                        labels: labels[0],
                        avgData: avgData[0],
                        minData: minData[0],
                        maxData: maxData[0]
                      }, {
                        labels: labels[1],
                        avgData: avgData[1],
                        minData: minData[1],
                        maxData: maxData[1]
                      }, {
                        labels: labels[2],
                        avgData: avgData[2],
                        minData: minData[2],
                        maxData: maxData[2]
                      }, {
                        labels: labels[3],
                        avgData: avgData[3],
                        minData: minData[3],
                        maxData: maxData[3]
                      }]

                 })

        }

    });
    $('#table').bootstrapTable('destroy');
};


// ==== Date Range picker ==== //
$('#daterange').daterangepicker({
    startDate: new Date(),
    startDate: '2012-01-01',
    locale: {
        format: 'YYYY-MM-DD' // format change to sync with DB
    },
    opens: 'right'
});

// === Button submit ==== //
function update(){

if (($('#iMeasurements').val() == "levelStats" || $('#iMeasurements').val() == "uplinkStats"
   || $('#iMeasurements').val() == "downlinkStats") && ($('#iNetworkType').val() == 'all')) {

   getDateRangeChart();
 }
 else if ($('#iMeasurements').val() == "levelStats" || $('#iMeasurements').val() == "uplinkStats"
      || $('#iMeasurements').val() == "downlinkStats" && ($('#iNetworkType').val() == '2g'
      || $('#iNetworkType').val() == '3g' || $('#iNetworkType').val() == '4g')) {

      getChartDataSelection();
 }
};


var max = 0;
var steps = 10;
var username = '';
var password = '';

var GetChartDataOS = function () {
    $.ajax({
        url: '../osStats/',
        method: 'GET',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
        },
        success: function (os) {
           var labels = os.results.map(function(osSystem) {
               return osSystem.key;
           });
           var data = os.results.map(function(osSystem) {
               return osSystem.value;
           });
           var ctx = document.getElementById("chartOS");
           var config = {
            type: 'doughnut',
           data: {
              labels: labels,
              datasets: [{
                 label: "",
                 data: data,
                 backgroundColor: [
                    'rgba(153, 102, 255, 1)',
                    'rgba(0, 181, 204, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(0, 128, 0, 0.7)',
                    'rgba(255, 0, 0, 0.7)',
                    'rgba(255, 0, 255, 1)',

                 ],
              }]
           }
        };

            var chart = new Chart(ctx, config);

            $('#OsTable').bootstrapTable({
                    data: [{
                        labels: labels[0],
                        data: data[0]
                      }, {
                        labels: labels[1],
                        data: data[1]

                      }, {
                        labels: labels[2],
                        data: data[2]

                      }, {
                        labels: labels[3],
                        data: data[3]
                      }, {
                        labels: labels[4],
                        data: data[4]

                    }]
            })


        }
    });
};

$(document).ready(function() {
    GetChartDataOS();
});
