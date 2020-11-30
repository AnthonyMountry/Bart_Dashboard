const groupBy = (xs, key) =>
  xs.reduce((rv, x) => {
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;
  }, {});

const COLORS = [
  "rgb(255, 99, 132)",
  "rgb(132, 255, 99)",
  "rgb(99, 132, 255)",
  "rgb(255, 130, 75)",
  "rgb(255, 255, 0)",
  "rgb(0, 255, 255)",
  "rgb(0,128,0)",
  "rgb(128,0,128)",
  "rgb(0,128,128)",
  "rgb(0, 0, 128)",
];

function transparentize(color, opacity) {
  var alpha = opacity === undefined ? 0.5 : 1 - opacity;
  return Chart.helpers.color(color).alpha(alpha).rgbString();
}

function colorize(opaque, ctx) {
  var v = ctx.dataPoint.y;
  var c =
    v < -50 ? "#D60000" : v < 0 ? "#F46300" : v < 50 ? "#0358B6" : "#44DE28";
  return opaque ? c : transparentize(c, 1 - Math.abs(v / 150));
}

function renderBarGraph(ctx, assets) {
  let options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: false,
      tooltip: false,
    },
    elements: {
      bar: {
        backgroundColor: colorize.bind(null, false),
        borderColor: colorize.bind(null, true),
        borderWidth: 2,
      },
    },
  };

  let statuses = new Map();
  for (i in assets) {
    let asset = assets[i];
    if (statuses.has(asset.status)) {
      let count = statuses.get(asset.status);
      statuses.set(asset.status, count + 1);
    } else {
      statuses.set(asset.status, 1);
    }
  }

  var data = {
    labels: Array.from(statuses.keys()),
    datasets: [
      {
        //TODO change to real data
        backgroundColor: [
          "#2100fa",
          "#1ff502",
          "#f55702",
          "#c002f5",
          "#8abd99",
          "#2dcded",
        ],
        barPercentage: 1,
        barThickness: "flex",
        maxBarThickness: 50,
        minBarLength: 10,
        data: Array.from(statuses.values()),
      },
    ],
  };
  return new Chart(ctx, {
    type: "bar",
    data: data,
    options: options,
  });
}

function renderMeterReadings(ctx, readings) {
  let grouped = groupBy(readings, "name");
  let datasets = [];
  let colors = [...COLORS]; // copy the colors array
  for (const name in grouped) {
    let col = colors.pop();
    datasets.push({
      label: name,
      borderColor: col,
      backgroundColor: Chart.helpers.color(col).alpha(0.2).rgbString(),
      data: grouped[name],
      hidden: false,
    });
  }

  return new Chart(ctx, {
    type: "line",
    options: {
      responsive: true,
      title: { display: false, text: "" },
      scales: {
        xAxes: [
          {
            type: "time",
            display: true,
            scaleLabel: { display: true, labelString: "Date" },
          },
        ],
      },
    },
    data: {
      labels: readings.map((r) => r.x),
      datasets: datasets,
    },
  });
}

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
      responsive: true,
      maintainAspectRatio: false,
      title: {
        display: true,
        text: "Example",
      },
    },
    data: {
      datasets: [
        {
          label: "test",
          borderColor: "rgb(225, 99, 132)",
          backgroundColor: Chart.helpers
            .color("rgb(225, 99, 132)")
            .alpha(0.2)
            .rgbString(),
          data: testDataPoints(),
        },
        {
          label: "test",
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
