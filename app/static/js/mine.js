function getDataInP(p) {
	$.get("/js/data", {}, function(res){
		console.log(res);
		let str = ""
		for (let k of Object.keys(res)) {
			str += k;
			str += ' = ';
			str += res[k];
			str += "\n"
		}
		p.innerText = str
	})
}
