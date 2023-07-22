
var datasets = [];

for (const key in chart_data) {
  datasets.push({label: key, data: chart_data[key]})
}
console.log(datasets);

var ctx = document.getElementById("myChart");

  const cfg = {
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
          parsing: 'true'
        }
      }
    }
  }
  
  

  new Chart(
    ctx,
    cfg
  );

/*var labels = [1]
var ctx = document.getElementById('myChart')

console.log(chart_data[labels[0]])


const data = {
  datasets: [{
    data: [{
      x: 10,
      y: 20
    }, {
      x: 15,
      y: 10
    }]
      //data: chart_data[labels[0]]
  }]
}
const options = {
  //parsing: true,
  //scaleOverride: true,
  
}

const chart = new Chart(ctx, {
  type: 'line',
  data,
  options,
});
*/
