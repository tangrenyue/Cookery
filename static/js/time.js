var formatTime = function () {
    var times = document.querySelectorAll('.time-stamp')
    for (var i = 0; i < times.length; i++) {
        var time = times[i]
        time.innerHTML = moment.unix(time.innerHTML).fromNow()
    }
}

var __main = function () {
    formatTime()
}

__main()