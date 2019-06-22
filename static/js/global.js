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

if (!Array.prototype.last){
    Array.prototype.last = function(){
        return this[this.length - 1];
    };
};