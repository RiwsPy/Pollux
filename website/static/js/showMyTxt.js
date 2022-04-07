var where = document.getElementById('myTxt');

function showMyTxt(textContent) {
    if (!where || !textContent) {
        return;
    }
    let txt = '<br>'
    txt += showParagraph(textContent.intro)

    for (QR of textContent.QR) {
        // question
        txt += "<hr class='divider'><br><br><strong>"
        txt += showParagraph(QR.Q)
        txt += "</strong>"

        // response
        txt += showParagraph(QR.R)
    }
    where.innerHTML += txt
}

function showParagraph(paragraph) {
    let txt = '';
    console.log(paragraph)
    for (line of paragraph.split('\n')) {
        console.log(line)
        if (line != "") {
            txt += '<p>' + line + '</p>';
        } else {
            txt += '<br>';
        }
    }
    return txt
}