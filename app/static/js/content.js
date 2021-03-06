function showContent(div) {
	let root = div;
	es = new EventSource(evdurl);
	es.onmessage = function(e) {
		let data = e.data;
		console.log(data);
		if (data == 'reset') {
			root.innerHTML = '';
			alert("Some one Reset All the Content!");
			return
		}
		if (data == 'destroy') {
			alert("Room destroyed!");
			goBackMain();
		}
		try {
			let line = JSON.parse(e.data);
			addLine(line, root);
		} catch(e) {}
	}
}

function addLine(line, root) {
	let div = document.createElement('div');
	div.className = "main";

	let left = document.createElement('div');
	left.className = "left"
	let img = document.createElement('img');
	left.appendChild(img);
	img.src = line['gravatar'];
	div.appendChild(left)

	let right = document.createElement("div");
	right.className = 'right'

	let header = document.createElement('div');
	header.className = 'header';
	let name = document.createElement("p");
	name.innerText = line['user'];
	let time = document.createElement("time");
	stime = new Date(line['time'] * 1000);
	let s = stime.toLocaleDateString().split('/').join('-') + ' ' + stime.toTimeString().substr(0, 12);
	time.innerHTML = s;
	header.appendChild(name);
	header.appendChild(time);

	let br = document.createElement('br');
	let ctx = document.createElement("p");
	ctx.innerText = line['ctx'];
	ctx.className = 'ctx'

	right.appendChild(header);
	right.appendChild(br);
	right.appendChild(ctx);

	div.appendChild(right)

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
