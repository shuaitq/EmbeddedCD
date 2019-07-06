function startTime() {
	var today = new Date();
	var h = today.getHours();
	var m = today.getMinutes();
	var s = today.getSeconds();
	m = checkTime(m);
	s = checkTime(s);
	document.getElementById('txt').innerHTML =
	h + ":" + m + ":" + s;
	var t = setTimeout(startTime, 1000);
}
	
function checkTime(i) {
	if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
	return i;
}

function update_tmp(){
	$.ajax({
		url: 'api/history?limit=1',
		success: function (data) {
			document.getElementById('temp').innerHTML = data[0][3].toFixed(1) + "°C";
			document.getElementById('hum').innerHTML = data[0][2].toFixed(1) + "%";
		}
	});
}

update_tmp();

window.setInterval(function(){
	update_tmp();
}, 10000);