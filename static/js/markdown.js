var setMarked = function () {
    marked.setOptions({
        breaks: true,
    })
}

var markContents = function () {
    var contents = document.querySelectorAll('.markdown-text')
    for (var i = 0; i < contents.length; i++) {
        var content = contents[i]
        content.innerHTML = marked(content.innerHTML.replace(/&gt;+/g, '>'))
    }
}

var __main = function () {
    setMarked()
    markContents()
}

__main()