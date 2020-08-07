// https://github.com/nagix/chartjs-plugin-datasource
// https://stackoverflow.com/questions/53118166/how-to-set-time-scale-zoom-in-chartjs
// https://github.com/chartjs/chartjs-plugin-zoom

var charts = [];

function update_chart(id, csv) {
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  return new Chart(ctx, {
    type: "bar",
    plugins: [ChartDataSource],
    options: {
      plugins: {
        datasource: {
          type: "csv",
          url: csv,
          rowMapping: "index",
        },
      },
      scales: {
        xAxes: [
          {
            type: "time",
          },
        ],
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });
}

function set_text(id, text) {
  var ctx = document.getElementById(id);
  ctx.innerHTML = text;
}

function update(geo) {
  charts.forEach((chart) => chart.destroy());
  charts = ["case", "test", "death"].map((chart) =>
    update_chart(chart + "-chart", "data/" + geo + "_" + chart + ".csv")
  );
}

function clicked(e) {
  e = e || window.event;
  var targ = e.target || e.srcElement || e;
  if (targ.nodeType == 3) targ = targ.parentNode; // defeat Safari bug

  geo = targ.id;

  var geo_nav = document.getElementsByClassName("geo-nav");
  for (var i = 0; i < geo_nav.length; i++) {
    if (targ == geo_nav[i]) {
      geo_nav[i].classList.remove("active");
    } else {
      geo_nav[i].classList.add("active");
    }
  }

  var geo_header = document.getElementsByClassName("geo-header");
  for (var i = 0; i < geo_header.length; i++) {
    var inner = "";
    switch (geo) {
      case "local":
        inner = "Princeton Township";
        break;
      case "county":
        inner = "Mercer County";
        break;
      case "state":
        inner = "New Jersey";
        break;
      case "national":
        inner = "United States";
        break;
    }
    geo_header[i].innerHTML = inner;
  }

  update(geo);
}

window.onload = function initialize() {
  set_text("active-cases", 10);
  update("local");
};

