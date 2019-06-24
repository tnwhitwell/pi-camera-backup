$(document).ready(function () {
    draw_disk_table();
});

function draw_disk_table() {
    $.getJSON('/api/potential_disks', function (resp) {
        let table = $('#available-disk-list > tbody');
        table.empty();
        resp["data"].forEach(function (disk) {
            let row = $("<tr></tr>");
            $("<td class='mdl-data-table__cell--non-numeric'></td>")
                .append(
                    $(`<a href=${disk.fb_url} target="_blank"></a>`)
                        .text(disk.name)
                )
                .appendTo(row);
            $("<td class='mdl-data-table__cell--non-numeric'></td>").text(
                `${humanFileSize(disk.used)}/${humanFileSize(disk.total)} (${disk.percent}%)`
            ).appendTo(row)
            $("<td class='mdl-data-table__cell--non-numeric'></td>").html(
                `<svg width="100" height="10">
                  <rect width="${disk.percent}" height="10" x=0 y=0 style="fill:rgba(248, 121, 121, 1)" />
                  <rect width="70" height="10" x="${disk.percent}" style="fill:rgba(121, 248, 121, 1)" />
                </svg>`
            ).appendTo(row);
            $("<td class='mdl-data-table__cell--non-numeric'></td>")
                .append(
                    $(`<label class="mdl-radio mdl-js-radio mdl-js-ripple-effect" for="${disk.name}-is_source">`).append(
                        $(`<input type="radio" class="mdl-radio__button" name="is_source" id="${disk.name}-is_source" value="${disk.name}-is_source">`)
                            .prop('checked', disk.is_source)
                    )
                )
                .appendTo(row);
            $("<td class='mdl-data-table__cell--non-numeric'></td>")
                .append(
                    $(`<label class="mdl-radio mdl-js-radio mdl-js-ripple-effect" for="${disk.name}-is_dest">`).append(
                        $(`<input type="radio" class="mdl-radio__button" name="is_dest" id="${disk.name}-is-dest" value="${disk.name}-is_dest">`)
                            .prop('checked', disk.is_dest)
                    )
                )
                .appendTo(row);
            $("<td class='mdl-data-table__cell--non-numeric'></td>")
                .append(
                    $(`<label class="mdl-radio mdl-js-radio mdl-js-ripple-effect" for="${disk.name}-is_unused">`).append(
                        $(`<input type="radio" class="mdl-radio__button" name="${disk.name}" id="${disk.name}-is_unused" value="${disk.name}-is_unused">`)
                            .prop('checked', (!disk.is_dest && !disk.is_source))
                    )
                )
                .appendTo(row);
            row.appendTo(table);
        });
        $('#available-disk-list input[type="radio"]').change(function () {
            let changed = this;
            let parent = $(this).closest("tr");
            $(parent)
                .find(`input[type='radio'][value!='${$(this).attr("value")}']`)
                .each(function () {
                    $(this).prop("checked", !$(changed).is(":checked"))
                });
            let table = $(this).closest("tbody");
            $(table).find("tr").each(function () {
                if ($(this).find("input:checked").length === 0) {
                    $(this)
                        .find("input[value$='is_unused']")
                        .first().prop("checked", true);
                }
            });
        });
    });
}