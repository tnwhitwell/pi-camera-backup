$(document).ready(function () {
    $("#trigger_backup").click(function (e) {
        e.preventDefault();
        $.post("/api/backup", {})
            .fail(function () {
                trigger_snackbar({
                    message: "Backup failed to start"
                })
            })
    });
});