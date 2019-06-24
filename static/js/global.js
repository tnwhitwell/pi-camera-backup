const socket = io.connect('http://' + document.domain + ':' + location.port);
$(document).ready(function () {
    if (socket.connected) {
        socket_connected()
    }
    socket.on('connect', socket_connected());

    socket.on('disconnect', function () {
        $("#status_chip")
            .removeClass("mdl-color--green")
            .addClass("mdl-color--red")
        $("#status_chip span")
            .text("Disconnected")
    });
    socket.on('backup started', function (msg) {
        console.log(msg);
        trigger_snackbar({message: "Backup Started"});
    });
    socket.on('backup already running', function (msg) {
        console.log(msg);
        trigger_snackbar({message: "Backup already running"});
    });
    socket.on('backup complete', function (msg) {
        console.log(msg);
        let dirname = msg["destination"].split('/').last();
        trigger_snackbar({
                message: "Backup to " + dirname + " complete",
                actionText: "View",
                actionHandler: function () {
                    window.location.href = filebrowser_base + msg["filebrowser_uri"]
                },
                timeout: 10000,
            }
        )
        ;
    });
    $("#header-shutdown").click(function (e) {
        e.preventDefault();
        trigger_dialog({
            title: "Shutdown?",
            message: "Are you sure you wish to shut down?",
            buttons: [
                {
                    caption: "No",
                    class: "close",
                    action: function () {
                        document.querySelector('dialog').close()
                    }
                },
                {
                    caption: "Yes",
                    class: "accept",
                    action: function () {
                        $.post("/api/power", {action: "poweroff"})
                            .done(function () {
                                trigger_snackbar({message: "Shutdown Triggered"});
                            })
                            .fail(function () {
                                trigger_snackbar({message: "Shutdown Failed"});
                            });
                        document.querySelector('dialog').close()
                    }
                }
            ]
        });
    });

    $("#header-restart").click(function (e) {
        e.preventDefault();
        trigger_dialog({
            title: "Restart?",
            message: "Are you sure you wish to restart?",
            buttons: [
                {
                    caption: "No",
                    class: "close",
                    action: function () {
                        document.querySelector('dialog').close()
                    }
                },
                {
                    caption: "Yes",
                    class: "accept",
                    action: function () {
                        $.post("/api/power", {action: "reboot"})
                            .done(function () {
                                trigger_snackbar({message: "Restart Triggered"});
                            })
                            .fail(function () {
                                trigger_snackbar({message: "Restart Failed"});
                            });
                        document.querySelector('dialog').close()
                    }
                }
            ]
        });
    });
});

function socket_connected() {
    $("#status_chip")
        .removeClass("mdl-color--red")
        .addClass("mdl-color--green")
    $("#status_chip span")
        .text("Connected")
}

function trigger_snackbar(data) {
    // var data = {
    //     message: 'Message Sent',
    //     actionHandler: function (event) {
    //     },
    //     actionText: 'Undo',
    //     timeout: 10000
    // };
    let snackbarContainer = document.querySelector('#pibackup-snackbar');
    snackbarContainer
        .MaterialSnackbar
        .showSnackbar(data)
}

function trigger_dialog(data) { // input: data
    // let data={
    //     title: "some title",
    //     message: "This is a message",
    //     buttons: [{
    //         caption: "No",
    //         class: "close",
    //         action: function () {
    //             document.querySelector('dialog').close()
    //         }
    //     }]
    // };
    $("dialog > .mdl-dialog__title").text(data.title)
    $("dialog > .mdl-dialog__content p").text(data.message)
    $("dialog > .mdl-dialog__actions").empty()
    data.buttons.forEach(function (buttondata) {
        let button = $("<button type='button' class='mdl-button " + buttondata.class + "'></button>)");
        button.text(buttondata.caption);
        button.click(buttondata.action);
        $("dialog > .mdl-dialog__actions").append(button);
    });
    document.querySelector('dialog').showModal();
}

// if (!Array.prototype.last) {
//     Array.prototype.last = function () {
//         return this[this.length - 1];
//     };
// }
// ;

function humanFileSize(bytes, si) {
    let thresh = si ? 1000 : 1024;
    if (Math.abs(bytes) < thresh) {
        return bytes + ' B';
    }
    let units = si
        ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
    let u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while (Math.abs(bytes) >= thresh && u < units.length - 1);
    return bytes.toFixed(1) + ' ' + units[u];
}