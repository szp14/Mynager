function login(username, password) {
  api.post('/api/u/login', {"username":username, "password":password}, function (data) {
    if (data == 1) {
      window.location.href = "/user/homepage";
    }
    else {
      alert("账户名或者密码不正确，请重新输入！");
    }
  }, dftFail);
}
