function humanFileSize(bytes, si) {
    let thresh = si ? 1000 : 1024;
    if(Math.abs(bytes) < thresh) {
        return bytes + ' B';
    }
    let units = si
        ? ['kB','MB','GB','TB','PB','EB','ZB','YB']
        : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
    let u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while(Math.abs(bytes) >= thresh && u < units.length - 1);
    return bytes.toFixed(1)+' '+units[u];
}

$( document ).ready(function() {
    $.getJSON('/api/backups', function(resp) {
        let table = $('#backup-list');
        let table_rows = [$("<thead></thead>"), $("<tbody></tbody>")];
        let columns = [];
        resp["meta"]["headers"].forEach(function (header) {
            let type_prefix = header.numeric ? "" : "non-";
            $("<th class=\"mdl-data-table__cell--" + type_prefix + "numeric\"></th>")
                .text(header.name)
                .appendTo(table_rows[0]);
        });
        resp["data"].forEach(function (backup, name) {
            let row = $("<tr></tr>");
            resp["meta"]["headers"].forEach(function (header) {
                let type_prefix = header.numeric ? "" : "non-";
                $("<td class=\"mdl-data-table__cell--" + type_prefix + "numeric\"></td>")
                    .text(backup[header["key"]])
                    .appendTo(row);
            });
            row.appendTo(table_rows[1]);
        });
        table.append(...table_rows);

    });
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
            let options = {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: item["title"]
                },
                tooltips: {
                    callbacks: {
                        label: function(tooltipItem, data) {
                            let label = data.labels[tooltipItem.index];
                            let value = data.datasets[tooltipItem.datasetIndex]["data"][tooltipItem.index];
                            let hrValue = humanFileSize(value, true)
                            return label + ': ' + hrValue;
                        }
                    }
                }
            };
            let myDoughnutChart = new Chart(ctx, {
                type: 'doughnut',
                data: data,
                options: options
            });
        });
    });
});