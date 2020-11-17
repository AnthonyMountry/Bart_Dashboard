function renderMeterReadings() {}

function testDataPoints() {
  return [
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
    { x: Math.random(), y: Math.random() },
  ];
}

function testGraph(ctx) {
  let config = {
    type: "scatter",
    options: {
      title: {
        display: true,
        text: "Yeeeet",
      },
    },
    data: {
      datasets: [
        {
          label: "red bois",
          borderColor: "rgb(225, 99, 132)",
          backgroundColor: Chart.helpers
            .color("rgb(225, 99, 132)")
            .alpha(0.2)
            .rgbString(),
          data: testDataPoints(),
        },
        {
          label: "blue bois",
          borderColor: "rgb(54, 162, 235)",
          backgroundColor: Chart.helpers
            .color("rgb(54, 162, 235)")
            .alpha(0.2)
            .rgbString(),
          data: testDataPoints(),
        },
      ],
    },
  };
  return new Chart(ctx, config);
}
