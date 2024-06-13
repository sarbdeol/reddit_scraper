$(document).ready(function() {
    var socket = io();

    $('#scrape-form').on('submit', function(e) {
        e.preventDefault();
        var url = $('#url').val();
        socket.emit('scrape', { url: url });

        socket.on('progress', function(data) {
            var progress = data.progress;
            $('#progress-bar').css('width', progress + '%').attr('aria-valuenow', progress).text(progress + '%');
        });

        socket.on('completed', function(data) {
            var fileName = data.file_name;
            $('#download-link').show();
            $('#download-button').attr('href', '/download/' + fileName).text('Download Your File');
        });
    });
});
