$(document).ready(function () {
    $("#trigger_backup").click(function (e) {
        e.preventDefault();
        $.post("/api/backup", {})
            .done(function () {
                console.log("backup started")
            });
    });
});