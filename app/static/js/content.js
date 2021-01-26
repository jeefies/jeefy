var odata;
var ed;

function showContent(div) {
	let root = div;
	const es = new EventSource(evdurl);
	es.onmessage = function(e) {
		console.log(e.data);
		try {
			let line = JSON.parse(e.data);
			addLine(line, root);
		} catch(e) {}
	}
}

function addLine(line, root) {
	let div = document.createElement("div");
	div.className = 'main'

	let header = document.createElement('div');
	header.className = 'header';
	let name = document.createElement("p");
	name.innerText = line['user'];
	let time = document.createElement("time");
	stime = new Date(line['time'] * 1000);
	console.log(line['time']* 1000);
	console.log(stime);
	let s = stime.toLocaleDateString().split('/').join('-') + ' ' + stime.toTimeString().substr(0, 12);
	time.innerHTML = s;
	header.appendChild(name);
	header.appendChild(time);

	let br = document.createElement('br');
	let ctx = document.createElement("p");
	ctx.innerText = line['ctx'];
	ctx.className = 'ctx'

	div.appendChild(header);
	div.appendChild(br);
	div.appendChild(ctx);
	console.log(div.outerHTML);

	root.innerHTML = div.outerHTML + root.innerHTML;
}

function goBackMain() {
	window.location.href = mainurl
}

function Go(url) {
	location.href = url
}

function Submit() {
	const Line = document.getElementById('Line');
	$.post(suburl, {'line': Line.value}, function(res) {});
	Line.value = '';
	Line.focus()
}

function KeyPress(event) {
	console.log(event.key);
	if (event.key == "Enter") {
		Submit()
	}
}
