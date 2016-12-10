var meeting_num = 6;

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

window.location.pathname_with_query_string = function(){
    return this.href.substring(this.origin.length);
 };

window.loginRequired = function (cb) {
    api.get('/api/a/login', {}, cb, function () {
        window.location.href = '/a/login?' + $.param({
            next: window.location.pathname_with_query_string()
        });
    });
};

window.logout = function () {
    api.post('/api/a/logout', {}, null, dftFail, function () {
        window.location.href = '/a/login?' + $.param({
            next: window.location.pathname_with_query_string()
        });
    });
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

window.updateObj = function (obj, newObj) {
    for (var key in newObj) {
        obj[key] = newObj[key];
    }
};

function GetAllList(page_index, fun0) {
    api.get('/api/u/meeting/list', {"meeting_num": meeting_num, "page_index": page_index}, function (data) {
        //status:状态, total_page:总页数, list:会议信息列表
        fun0(data);
    }, dftFail);
}

function SearchMeeting(key_word, page_index, fun0) {
    api.post('/api/u/meeting/list', {"key_word": key_word, "meeting_num": meeting_num, "page_index": page_index}, function (data) {
        fun0(data);
    }, dftFail);
}

$(function () {
    GetAllList(1, function(data){
        console.log(data["list"]);
    });
    //SearchMeeting("那些年", 2);
    //console.log(GetLogStatus());
});