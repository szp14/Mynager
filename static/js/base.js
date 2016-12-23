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

window.api = {
    get: function (url, data, success, fail, complete) {
        success = success || $.noop;
        fail = fail || $.noop;
        complete = complete || $.noop;
        return $.get(url, data).done(function (response, status, xhr) {
            if (response.code != 0) {
                return fail(response.code, response.msg);
            } else {
                return success(response.data);
            }
        }).fail(function (xhr, errmsg, e) {
            return fail(-2, errmsg, e);
        }).always(complete);
    },
    post: function (url, data, success, fail, complete) {
        success = success || $.noop;
        fail = fail || $.noop;
        complete = complete || $.noop;
        return $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify(data),
            contentType: 'application/json'
        }).done(function (response, status, xhr) {
            if (response.code != 0) {
                return fail(response.code, response.msg);
            } else {
                return success(response.data);
            }
        }).fail(function (xhr, errmsg, e) {
            return fail(-2, errmsg, e);
        }).always(complete);
    }
};

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

function getQueryParams(qs) {
    qs = qs.split('+').join(' ');

    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
    }

    return params;
}

window.urlParam = getQueryParams(document.location.search);

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

window.dftFail = function (errno, errmsg, e) {
    var mes = errmsg.split(",");
    if(mes[0] == "(1062")
        alert("该账号已存在，请重新输入账户！");
    else
        alert(errmsg);
};

function GetLogStatus(fun0) {
    api.get('/api/u/login', {}, function (data) {
        fun0(data);
    }, dftFail);
}

function RenderTpl(tpl_id, data) {
    $("#" + tpl_id).html(swig.render($("#tpl-"+tpl_id).html(), data))
}

function GetUserDetail(fun) {
    api.get("/api/u/user/detail", {}, fun, dftFail);
}

function DeleteMeeting(meet_id, fun) {
    api.get("/api/u/meeting/create", { "meeting_id": meet_id }, fun, dftFail);
}

function CreateNotice(touser_ids, content, fun) {
    api.post("/api/u/notice/create/", { "to_ids": touser_ids, "content": content }, fun, dftFail);
}

function GetMeeting(meet_id, fun) {
    api.get("/api/u/meeting/detail", { "meeting_id": meet_id }, fun, dftFail);
}

function WithMeeting(meet_id, type) {
    api.get("/api/u/relation/change", { "meet_id": meet_id, "relation": type }, function () {
        GetAllList(page_index);
    });
}