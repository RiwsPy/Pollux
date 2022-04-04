var where = document.getElementById('myTxt');

function showMyTxt(lines) {
    if (!where || !lines) {
        return;
    }

    for (line of lines) {
        if (line) {
            txt = '<p>' + line + '</p>';
        } else {
            txt = '<br>'
        }
        where.innerHTML += txt
    }
}