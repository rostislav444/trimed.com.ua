function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function XHR(method, url, data, func, params) {
    let csrf = getCookie("csrftoken")
    let request = new XMLHttpRequest();
        request.open(method, url, true);
        request.setRequestHeader("Content-Type", "application/json");
        request.setRequestHeader("X-CSRFToken", csrf);
        request.send(data)
        request.onload = () => {
            func(JSON.parse(request.responseText), params)
        }
}

function XHR_SYNC(method, url, data={}) {
    let csrf = getCookie("csrftoken")
    let request = new XMLHttpRequest();
        request.open(method, url, false);
        request.setRequestHeader("Data-Type", "json");
        request.setRequestHeader("Content-Type", "application/json");
        request.setRequestHeader("X-CSRFToken", csrf);
        request.send(JSON.stringify(data))
        if (request.status === 200) {
            let response = JSON.parse(request.responseText);
            return response
        } else {
            console.log(request.status)
            return false
        }

}
