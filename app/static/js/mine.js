var selfurl;
var dataurl;

/*
$.get('/urls', {}, function(result) {
	selfurl = result["self"];
	dataurl = result["data"];
	console.log(selfurl, dataurl);
})
*/

function logcookie() {
	console.log(document.cookie);
}

/*
class CookieUtil {
	static get(name) {
		let cookieName = `name=`,
		    cookieStart = document.cookie.indexOf(cookieName),
		    cookieValue = null;

		if (cookieStart > -1) {
			let cookieEnd = document.cookie.indexOf(";", cookieStart);
			if (cookieEnd == -1) {
				cookieEnd = document.cookie.length;
			}
			cookieValue = document.cookie.substring(cookieStart + cookieName.length, cookieEnd);
		}

		return cookieValue;
	}
	static getAll() {
		let cookieList = document.cookie.split(';');
		let cookieKws = new Array(cookieList.length);
		for (let index in cookieList) {
			let kw = cookieList[index].split('=');
			cookieKws[index] = kw;
			index += 1;
		}

		return cookieKws
	}
}
*/

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
