/*
	Makes cross-domain XMLHTTPRequest.	
*/
var posterXHR = {
	xhr : function (url, callback){
		try{
			chrome.extension.sendRequest({ 'type': 'xhr', 'term': url }, function(response) {
				callback(response.result);
		});
		} catch(e) {
			console.log('Chrome extension: ' + e.message);
		}
	}
};

document.getElementById('test_extension').onclick = function() {
	debugger;
	var text = document.getElementById('sndrcv');
	var url = text.innerText;
	posterXHR.xhr(url, function(ttt){
		text.innerText = ttt;
		document.getElementById('test_extension_answer').click();
	});
}