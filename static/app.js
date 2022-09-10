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
	const url = `${baseUrl}/api/google/calendar/connect`;
	openWindow(url, 'Authorize Zoom', 600, 700, 1);
}

/**
 * Disconnect Google Account Handler
 */
function disconnectGoogleCalendar(event) {
	setCookie('is_calendar_connected', '', 0);
	window.location.reload();
}

/**
 * Create Event
 */
function createEvent(event) {
	$.ajax('/api/google/calendar/events/insert', {
		type: 'GET',
		success: function (data, status, xhr) {
			window.createdEvent = data;
			$('#createEvent').hide();
			$('#eventCreated').show();
			$('#getEventSection').show();
			$('#deleteEventSection').show();
		},
		error: function (jqXhr, textStatus, errorMessage) {
			alert('err')
		}
	});
}

/**
 * Get Event
 */
function getCreatedEvent(event) {
	$.ajax(`/api/google/calendar/events/get?eventId=${window.createdEvent.id}`, {
		type: 'GET',
		success: function (data, status, xhr) {
			document.getElementById("createdEventInfo").textContent = JSON.stringify(data, undefined, 2);
		},
		error: function (jqXhr, textStatus, errorMessage) {
			alert('err')
		}
	});
}

/**
 * Delete Event
 */
function deleteCreatedEvent(event) {
	$.ajax(`/api/google/calendar/events/delete?eventId=${window.createdEvent.id}`, {
		type: 'GET',
		success: function (data, status, xhr) {
			$('#createEvent').show();
			$('#eventCreated').hide();
			$('#getEventSection').hide();
			$('#deleteEventSection').hide();
		},
		error: function (jqXhr, textStatus, errorMessage) {
			alert('err')
		}
	});
}

function init() {
	$('#connectGoogleCalendar').click(connectGoogleCalendar);
	$('#disconnectGoogleCalendar').click(disconnectGoogleCalendar);
	$('#createEvent').click(createEvent);
	$('#getCreatedEvent').click(getCreatedEvent);
	$('#deleteCreatedEvent').click(deleteCreatedEvent);
}

init();
