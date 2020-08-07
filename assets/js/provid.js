// https://github.com/nagix/chartjs-plugin-datasource
// https://stackoverflow.com/questions/53118166/how-to-set-time-scale-zoom-in-chartjs
// https://github.com/chartjs/chartjs-plugin-zoom

var charts = [];
var cards = {};

function numberWithCommas(x) {
  if (x == 0) {
    return "0.00";
  }
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function set_change(el, val) {
  val = parseFloat(val);
  el.classList.remove("text-success");
  el.classList.remove("text-danger");
  if (val < 0) {
    el.classList.add("text-success");
    el.innerHTML = "<i class='fa fa-arrow-down'></i>";
    el.innerHTML += " " + val + "%";
  } else if (val == 0) {
    el.classList.add("text-failure");
    el.innerHTML = "No change";
  } else if (isNaN(val)) {
    el.classList.add("text-failure");
    el.innerHTML = "N/A";
  } else {
    el.classList.add("text-danger");
    el.innerHTML = "<i class='fa fa-arrow-up'></i>";
    el.innerHTML += " " + val + "%";
  }
}

function update_cards(geo) {
  card_values = document.getElementsByClassName("card-value");
  card_changes = document.getElementsByClassName("card-change");

  values = [
    "total_active",
    "per_10k_active",
    "new_cases",
    "new_tests",
    "new_deaths",
    "pct_positive",
  ];
  changes = [
    "increase_active",
    "increase_active",
    "increase_cases",
    "increase_tests",
    "increase_deaths",
    "increase_pct_positive",
  ];

  for (var i = 0; i < card_values.length; i++) {
    card_values[i].innerHTML = numberWithCommas(cards[geo][values[i]]);
    set_change(card_changes[i], cards[geo][changes[i]]);
  }
}

function update_chart(id, csv) {
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");

  if (id == "test-chart") {
    console.log("set");
    return new Chart(ctx, {
      type: "bar",
      plugins: [ChartDataSource],
      data: {
        datasets: [
          {
            type: "bar",
            yAxisID: "new_tests",
          },
          {
            type: "line",
            yAxisID: "positive_test_rate",
          },
        ],
      },
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
              id: "new_tests",
              position: "left",
              ticks: {
                beginAtZero: true,
                userCallback: function (value, index, values) {
                  value = value.toString();
                  value = value.split(/(?=(?:...)*$)/);
                  value = value.join(",");
                  return value;
                },
              },
            },
            {
              id: "positive_test_rate",
              position: "right",
              scaleLabel: {
                display: true,
                labelString: "Positive test rate (%)",
              },
            },
          ],
        },
      },
    });
  }
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
              userCallback: function (value, index, values) {
                value = value.toString();
                value = value.split(/(?=(?:...)*$)/);
                value = value.join(",");
                return value;
              },
            },
          },
        ],
      },
    },
  });
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

  update_cards(geo);

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

update("local");
$.getJSON("data/cards.json", function (json) {
  cards = json;
  update_cards("local");
}).fail(function (jqxhr, textStatus, error) {
  console.log(error);
});

