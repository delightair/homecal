/**
 * Opens Popup window as the current window as parent
 */
function openWindow(url, winName, w, h, scroll) {
	LeftPosition = (screen.width) ? (screen.width - w) / 2 : 0;
	TopPosition = (screen.height) ? (screen.height - h) / 2 : 0;
	settings =
		'height=' + h + ',width=' + w + ',top=' + TopPosition + ',left=' + LeftPosition + ',scrollbars=' + scroll + ',resizable'
	window.open(url, winName, settings)
}

/**
 * Set Cookie in the browser
 */
function setCookie(cname, cvalue, exMins) {
	var d = new Date();
	d.setTime(d.getTime() + (exMins * 60 * 1000));
	var expires = "expires=" + d.toUTCString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

/**
 * Connect Google Account Handler
 */
function connectGoogleCalendar(event) {
	const url = `http://cal.the-etheridges.com:5000/api/google/calendar/connect`;
	openWindow(url, 'Authorize Zoom', 600, 700, 1);
}

/**
 * Disconnect Google Account Handler
 */
function disconnectGoogleCalendar(event) {
	setCookie('is_calendar_connected', '', 0);
	window.location.reload();
}

function init() {
	$('#connectGoogleCalendar').click(connectGoogleCalendar);
	$('#disconnectGoogleCalendar').click(disconnectGoogleCalendar);
}

init();
