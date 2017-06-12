var dom_cpu = document.getElementById("cpu_paint");
var dom_memory = document.getElementById("memory_paint");
var dom_io = document.getElementById("io_paint");
var dom_net = document.getElementById("net_paint");

var myChart = echarts.init(dom_cpu);
var myChart2 = echarts.init(dom_memory);
var myChart3 = echarts.init(dom_io);
var myChart4 = echarts.init(dom_net);

// var oneDay = 24 * 3600 * 1000;
var ylabel=[];
var data = [];
// function addData(shift) {
  // var now = new Date();
  // now = [now.getHours(), now.getMinutes(), now.getSeconds()].join(':');
  // date.push(now);
  // if (shift) {
    // date.shift();
    // data.shift();
  // }
  // now = new Date(+new Date(now) + oneDay);
// }


option = {
  // legend: {
    // data: "data"
  // },
  xAxis: {
    type: 'category',
    // boundaryGap: false,
    data: ylabel
  },
  yAxis: {
  //   boundaryGap: [0, '50%'],
  //   type: 'value'
  },
  grid:{
    x:40,
  },
  series: [{
    name: 'info',
    type: 'line',
    smooth: true,
    symbol: 'none',
    stack: 'a',
    areaStyle: {
      normal: {}
    },
    data: data
  }]
};

if (option && typeof option === "object") {
  myChart.setOption(option, true);
  // myChart.setOption({xAxis: {data:["CPU"]}});
  myChart.setOption({yAxis: {axisLabel:{formatter: '{value} %'},type: 'value'}});
  myChart2.setOption(option, true);
  myChart2.setOption({yAxis: {axisLabel: {formatter: '{value} %'},type: 'value'}});
  // myChart2.setOption({xAxis: {data:["MEMORY"]}});
  myChart3.setOption(option, true);
  // myChart3.setOption({xAxis: {data:["CPU"]}});
  myChart4.setOption(option, true);
  // myChart4.setOption({xAxis: {data:["CPU"]}})
};


$(function() {
  $("#button").click(function(event) {
    $.ajax({
      url: 'test2/',
      type: 'GET',
      dataType: 'json',
      success: function(data) {
        // data=data.replace(/\(/g,"").replace(/\)/g,"").split(",");
        // data.pop();
        var json = eval('(' + data + ')');
        cpu=[];
        memory=[]
        for(var i=0;i<=json.length-1;i++){
          cpu[i]=json[i].fields.cpu;
          memory[i]=json[i].fields.memory;
        }
        alert(cpu);
      }
    });
  });
});

$(function() {
  $("#button2").click(function() {
    //      $(this).button('loading').delay(1000).queue(function() {
    //        $(this).button('reset');
    setInterval(dick_io, 500);
  });
});

function dick_io() {
  // addData();
  $.ajax({
    url: 'test2/',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      var json=eval('('+data+')');
      cpu=[],memory=[]
      for (var i=0;i<json.length-1;i++){
        cpu[i]=json[i].fields.cpu;
        memory[i]=json[i].fields.memory;
      }
      // alert(cpu);
      // alert(data['fields']);
      // data=data.replace(/\(/g,"").replace(/\)/g,"").split(",");
      // data.pop();
      myChart.setOption({
        series: [{
          name: 'CPU',
          data: cpu
        }]
      }),
      myChart2.setOption({
        series: [{
          name: 'memory',
          data: memory
        }]
      })
    }
  });
}
