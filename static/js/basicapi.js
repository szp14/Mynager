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

window.dftFail = function (errno, errmsg, e) {
    var mes = errmsg.split(",");
    if(mes[0] == "(1062")
        alert("该账号已存在，请重新输入账户！");
};