$(document).ready(function () {
    $.getJSON('/api/potential_disks', function (resp) {
        let table = $('#available-disk-list > tbody');
        resp["data"].forEach(function (disk) {
            let row = $("<tr></tr>");
            [disk.name, humanFileSize(disk.used, true), humanFileSize(disk.free, true)]
                .forEach(function (value) {
                    $("<td class='mdl-data-table__cell--non-numeric'></td>")
                        .text(value)
                        .appendTo(row);
                });
            $("<td class='mdl-data-table__cell--non-numeric'></td>")
                .append(
                    $("<input type='checkbox' name='" + disk.name + "' value='is_source'>")
                        .prop('checked', disk.is_source)
                )
                .appendTo(row);
            $("<td class='mdl-data-table__cell--non-numeric'></td>")
                .append(
                    $("<input type='checkbox' name='" + disk.name + "' value='is_dest'>")
                        .prop('checked', disk.is_dest)
                )
                .appendTo(row);

            row.appendTo(table);
        });
    });
});