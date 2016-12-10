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