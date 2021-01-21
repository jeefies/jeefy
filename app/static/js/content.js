var odata;

function showContent(div) {
	let root = div;
	$.get("{{ u }}", {}, function(data){
		let datas = JSON.parse(data);
		if (data != odata) {
			div.innerHTML = '';
			for (const line of datas) {
				addLine(line, root);
			};
			odata = data;
		}
	}
	)
	setTimeout(() => showContent(div), 3000)
}

function addLine(line, root) {
	let div = document.createElement("div");
	div.className = 'main'

	let header = document.createElement('div');
	header.className = 'header';
	let name = document.createElement("p");
	name.innerText = line['user'];
	let time = document.createElement("time");
	stime = new Date(line['time']);
	s = stime.toLocaleDateString().split('/').join('-') + ' ' + stime.toTimeString().substr(0, 12);
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

	root.appendChild(div);
}

function goBackMain() {
	window.location.href = "{{ url_for('room.index' )}}"
}

function Go(url) {
	location.href = url
}
