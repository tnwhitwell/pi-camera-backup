$( document ).ready(function() {
    $.getJSON('/api/chartdata', function(resp) {
        resp.forEach(function(item, idx){
            let ctx = $('#' + item["name"]);
            let data = {
                datasets: [{
                    data: item["value"],
                    backgroundColor: [
                        'rgba(248, 121, 121, 1)',
                        'rgba(121, 248, 121, 1)',
                    ]
                }],
                labels: [
                    'Used',
                    'Free'
                ],
            };
            let myDoughnutChart = new Chart(ctx, {
                type: 'doughnut',
                data: data,
                options: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: item["title"]
                    }
                }
            });
        });
    });
});