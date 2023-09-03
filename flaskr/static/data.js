
var datasets = [];

var datasets;
var init_data;

var myChart = {
  ctx: null,
  cfg: null,
  chart: null,

  update_chart() {
    this.chart.update();
  },

  update_data(new_data) {
    console.log(chart_data);
    console.log(new_data);
    var new_datasets = [];
    this.chart.data.datasets = [];

    for (const key in new_data) {
      this.chart.data.datasets.push({label: key, data: new_data[key]});
    }
  
  },

  init(chart_data) {
    for (const key in chart_data) {
      datasets.push({pointStyle: false, borderWidth: 2, label: key, data: chart_data[key]});
    }
    console.log(datasets);
    
    this.ctx = document.getElementById("myChart");
  
    this.cfg = {
      type: 'line',
      data: {
        datasets: datasets
      },
      options: {
        scales: {
          x: {
            // The axis for this scale is determined from the first letter of the id as `'x'`
            // It is recommended to specify `position` and / or `axis` explicitly.
            type: 'time',
            parsing: 'true',
            time: {
              displayFormats: {
                  hour: 'MMM d HH:mm:ss'
              }
            }
          }
        },
        plugins: {
          zoom: {
            pan: {
              enabled: true,
              modifierKey: "shift"
            },
            zoom: {
              wheel: {
                enabled: true
              }
              
              // zoom options and/or events
            }
          }
        }
      }
    }

    this.chart = new Chart(
      this.ctx,
      this.cfg
    );
  }

};

var dates = {
  start_date: null,
  to_date: null,

  get_start() {
    return this.start_date;
  },

  set_start(date) {
    this.start_date = date;
    document.querySelector('#sampled-date-start').setAttribute('value', date);
  }, 
  
  get_to() {
    return this.to_date;
  }, 

  set_to(date) {
    this.to_date = date;
    console.log(date);
    document.querySelector('#sampled-date-to').setAttribute('value', date);
  }, 

  init_dates() {
    console.log("initing dates");
    var now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    this.set_to(now.toISOString().replace(/\.\d\d\dZ/, ""));  // Set to date to now
    now.setDate(now.getDate()-7);
    this.set_start(now.toISOString().replace(/\.\d\d\dZ/, "")); // Set start date one week prior
  }
};

function get_get_url() {
  return  $(location).attr('href').concat("/api/data");
}

var get_arguments = {
  data_range_low: "",
  data_range_high: "",
  device_ids: [], 
  sensor_ids: [],
}
  
var get_args = {
  update_args() {
    get_arguments.data_range_low = null;
    get_arguments.data_range_high = null;
    get_arguments.device_ids = [];
    get_arguments.sensor_ids = [];

    get_arguments.data_range_low = dates.get_start();
    get_arguments.data_range_high = dates.get_to();

    console.log($("#sensors li.active").text());

    $("#sensors li.active").each(function() { 
      console.log(get_arguments);
      console.log(get_arguments.data_range_high);
      console.log(get_arguments.sensor_ids);
      console.log($(this).text());
      get_arguments.sensor_ids.push($(this).text()) 
    });
    $("#devices li.active").each(function() { get_arguments.device_ids.push($(this).text()) });
    get_arguments.sensor_ids = get_arguments.sensor_ids.join(',');
    get_arguments.device_ids = get_arguments.device_ids.join(',');
    console.log(get_arguments.sensor_ids);
  }, 

  get_query() {
    return Object.keys(get_arguments).map((key)=>encodeURIComponent(key) + '=' +get_arguments[key]).join('&');
  }
}


function update_chart() {
  get_args.update_args();
  var queryString = get_args.get_query();
  var url_with_params = get_get_url() + '?' + queryString;

  fetch(url_with_params)
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return response.json();
  })
  .then((data) => {
    console.log("data: ")
    console.log(data.data);
    myChart.update_data(data.data);
    console.log("data uploaded");
    myChart.update_chart();
  })
  .catch((error) => {
    // Handle errors
    console.error('Fetch error:', error);
  });
}

$( document ).ready(function() {
  dates.init_dates();

  console.log( "ready!" );
  myChart.init(chart_data);

  $(".graph-list li").on("click", function() {
    // Toggle the "active" class on the clicked item
    $(this).toggleClass("active inactive");
    update_chart();
  });

  $("#sampled-date-start").on("change",function() {
    dates.set_start($("#sampled-date-start").val());
    update_chart()
  });

  $("#sampled-date-to").on("change",function() {
    dates.set_to($("#sampled-date-to").val());
    update_chart();
  });

  $("#rst-btn").on("click", function() {
    $(this).addClass('clicked');
    myChart.chart.resetZoom();
    var button = $(this);
    setTimeout(function() {
      button.removeClass('clicked');
    }, 250);
    
  });

});

