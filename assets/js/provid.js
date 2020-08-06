// https://github.com/nagix/chartjs-plugin-datasource
// https://stackoverflow.com/questions/53118166/how-to-set-time-scale-zoom-in-chartjs
// https://github.com/chartjs/chartjs-plugin-zoom

function update_chart(id, geo) {
  var ctx = document.getElementById(id).getContext("2d");
  return new Chart(ctx, {
    type: "bar",
    plugins: [ChartDataSource],
    options: {
      plugins: {
        datasource: {
          type: "csv",
          url: "timeseries/local_case.csv",
          rowMapping: "index",
        },
      },
      scales: {
        xAxes: [
          {
            type: "time",
            time: {
              //parser: "YYYY-MM-DD",
              //unit: "day",
              //displayFormats: {
                //day: "MMM D",
              //},
            },
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

update_chart("case-chart", "timeseries/local_new_cases.csv");
update_chart("test-chart", [12, 19, 3, 5, 2, 3]);
update_chart("death-chart", [12, 19, 3, 5, 2, 3]);
set_text("active-cases", 10);

function clicked(e) {
  e = e || window.event;
  var targ = e.target || e.srcElement || e;
  if (targ.nodeType == 3) targ = targ.parentNode; // defeat Safari bug

  var geo = targ.id;

  var geo_nav = targ.parentNode.parentNode.getElementsByTagName("img");

  for (var i = 0; i < geo_nav.length; i++) {
    if (geo_nav[i] != targ) {
      geo_nav[i].classList.remove("bg-gradient-orange");
    } else {
      geo_nav[i].classList.add("bg-gradient-orange");
    }
  }

  var geo_header = document.getElementsByClassName("geo-header");
  for (var i = 0; i < geo_header.length; i++) {
    var inner = ""
    switch (geo) {
      case "local":
        inner = "Princeton Township"
        break;
      case "county":
        inner = "Mercer County"
        break;
      case "state":
        inner = "New Jersey"
        break;
      case "national":
        inner = "United States"
        break;
    }
    geo_header[i].innerHTML = inner
  }
}

