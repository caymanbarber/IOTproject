





const DATA_COUNT = 7;
const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};




const chart = new Chart("myChart", {
  type: 'line',
  data: data,
  labels: labels,
  config: config,
  actions: actions,
  options: {
    onClick: (e) => {
      const canvasPosition = getRelativePosition(e, chart);

      // Substitute the appropriate scale IDs
      const dataX = chart.scales.x.getValueForPixel(canvasPosition.x);
      const dataY = chart.scales.y.getValueForPixel(canvasPosition.y);
    }
  }
});


console.log("end");