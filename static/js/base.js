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