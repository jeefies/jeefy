function Main() {
	editer = document.getElementById('Content');
	text = editer.innerText;
	
	const btn1 = document.getElementById('Butt1');
	const btn2 = document.getElementById('Butt2');
	const btn3 = document.getElementById('Butt3');
	function uploadEdition() {
		let text = editer.innerText;
		$.post(uplurl, {'ctx': text}, function(j) {
			if (j['code'] != 200) {
				alert("Upload Failed!\n" + j['error']);
			} else {
				alert('Upload success!');
			}
		})}

	function startEdit() {
		editer.contentEditable = true;
		btn1.innerText = "End Edit";
		btn1.removeEventListener('click', startEdit);
		btn1.addEventListener('click', endEdit);
	}

	function endEdit() {
		editer.contentEditable = false;
		if (editer.innerText == text) {
			btn2.style.display = 'none';
			btn3.style.display = "none";
		} else {
			btn2.style.display = "inline";
			btn3.style.display = "inline";
		}
		btn1.innerText = "Edit";
		btn1.removeEventListener('click', endEdit);
		btn1.addEventListener('click', startEdit);
	}

	function downloadEdited() {
		let text = editer.innerText;
		let blob = new Blob([text], {type: "application/octet-stream"});
		let src = URL.createObjectURL(blob);
		a = document.createElement("a");
		document.body.appendChild(a);
		a.href = src;
		a.download = filename;
		a.click();
		console.log('clicked!');
	}
	
	btn1.addEventListener('click', startEdit);
	btn2.addEventListener('click', uploadEdition);
	btn3.addEventListener('click', downloadEdited);
}

function Download() {
	a = document.createElement('a');
	a.style.display = "none";
	document.body.appendChild(a);
	a.href = dlurl;
	a.click();
	document.body.removeChild(a);
}

function Rename() {
	let result = prompt("Change Your File Name to?", filename);
	if (result !== null) {
		if (result == filename) {
			alert('Nothing Changed');
			return
		}else if (result.length > 31) {
			alert("Too Long File Name");
			R.click();
		} else {
			$.post(renurl, {'name': result}, (res) => {
				if (res['reload']) {
					location.href = res['url'];
				} else {
					alert('Nothing Changed..');
				}
			});
		}
	}
}

function Delete() {
    $.get(delurl, {}, (res) => {
    if (res['code'] == 200) {
        alert("Delete Success\nRedirect To Index Page!");
        location.href = indexurl;
    } else {
        alert("Delete Failed");
    }
    }
         )
}

function ToPublic() {
    $.post(puburl, {"method": "Change Pub"}, function(res) {
        if (res['code'] == 200) {
            if (res['public']) {
                alert("Success Change to a public File!\nEvery One can");
            } else {
                alert("Success Cahnge to a private File!\nOnly You Can See it now!");
            }
        } else {
            alert("Change Failed")
        }
    })
}
