var Isuseful_personal = 1;
var Isuseful_admin = 1;

function openwindow(window) {
    if (Isuseful_personal) {
        window.style.display = "block";
    }
    Isuseful_personal = 0;
}

function closewindow(window) {
    window.style.display = "none";
    Isuseful_personal = 1;
}

function open_rejectwindow(window) {
	window.children[0].children[1].textContent = "";
	window.children[0].children[1].value = "";
	if (Isuseful_admin) {
        window.style.display = "block";
    }
    Isuseful_admin = 0;
}

function close_rejectwindow(window) {
	window.style.display = "none";
    Isuseful_admin = 1;
}

function open_iamge(){
	window.open ('image.jpg', 'newwindow', 
		'height=100, width=400, top=0, left=0, toolbar=no, menubar=no, scrollbars=no, resizable=no,location=no, status=no')
}

window.api.form = function (form, success, fail, before, complete) {
    before = before || $.noop;
    success = success || $.noop;
    fail = fail || $.noop;
    complete = complete || $.noop;
    form.submit(function () {
        var data = {};
        $.each($(this).serializeArray(), function (i, input) {
            data[input.name] = input.value;
        });
        if (before(data) === false) {
            return false;
        }
        api.post($(this).attr('action'), data, success, fail, complete);
        return false;
    })
};

window.api.postForm = function (url, data, success, fail, complete) {
    success = success || $.noop;
    fail = fail || $.noop;
    complete = complete || $.noop;
    return $.ajax({
        type: 'POST',
        url: url,
        data: data,
        contentType: false,
        processData: false
    }).done(function (response, status, xhr) {
        if (response.code != 0) {
            return fail(response.code, response.msg);
        } else {
            return success(response.data);
        }
    }).fail(function (xhr, errmsg, e) {
        return fail(-2, errmsg, e);
    }).always(complete);
};