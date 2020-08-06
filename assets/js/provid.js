// https://github.com/nagix/chartjs-plugin-datasource
// https://stackoverflow.com/questions/53118166/how-to-set-time-scale-zoom-in-chartjs
// https://github.com/chartjs/chartjs-plugin-zoom

function update_chart(id, data) {
  var ctx = document.getElementById(id).getContext("2d");
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datasets: [
        {
          label: "# of Votes",
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
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

update_chart("case-chart", [12, 19, 3, 5, 2, 3]);
update_chart("test-chart", [12, 19, 3, 5, 2, 3]);
update_chart("death-chart", [12, 19, 3, 5, 2, 3]);
set_text("active-cases", 10);

function clicked(e) {
  e = e || window.event;
  var targ = e.target || e.srcElement || e;
  if (targ.nodeType == 3) targ = targ.parentNode; // defeat Safari bug

  ids = targ.id.split("-")
  chart = ids[0]
  geo = ids[2]

  var ul = targ.parentNode.parentNode.getElementsByTagName("img")

  for (var i = 0; i < ul.length; i++) {
    if (ul[i] != targ) {
      ul[i].style.color = "blue"
      ul[i].classList.remove("active")
    } else {
      ul[i].classList.add("active")
    }
  }
}

