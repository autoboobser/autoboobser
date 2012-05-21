(function(){
	// DOM constants
	var IS_DEBUG = false;
	var TEXTAREA_ID = 'sndrcv';
	var REQUEST_ID = 'send_request';
	var RESPONSE_ID = 'pass_request';
	
	//	Makes cross-domain XMLHTTPRequest.
	var posterXHR = {
		xhr : function (url, callback){
			try{
				chrome['extension']['sendRequest']({ 'type': 'xhr', 'term': url }, function(response) {
					callback(response.result);
			});
			} catch(e) {
				if(IS_DEBUG) {
					console.log('Chrome extension XHR error: ' + e.message);
					callback(0);
				}
			}
		}
	};
	
	// Create element to pass data between extension and page
	var area = document.createElement('textarea'); // sendind data via TEXTAREA
	if(area) {
		area.id = TEXTAREA_ID;
		area.style.display = 'none';
		area.setAttribute('cols', 0);
		area.setAttribute('rows', 0);
		document.body.appendChild(area);
	}
	// Button to return response XHR
	var respose = document.createElement('input');
	if(respose) {
		respose.id = RESPONSE_ID;
		respose.type = 'button';
		respose.value = 'resp';
		respose.style.display = 'none';
		document.body.appendChild(respose);
	}
	// Button to get XHR parameters
	var request = document.createElement('input');
	if(request) {
		request.id = REQUEST_ID;
		request.type = 'button';
		respose.value = 'request';
		request.style.display = 'none';
		document.body.appendChild(request);
		request.addEventListener("click", function(){
		
			var data = area.value;
			if(IS_DEBUG) {
				console.log("Request called with data: " + data);
			}
			
			posterXHR.xhr(data, function(res) {
				if(IS_DEBUG) {
					console.log("XHR Return value: " + res);
				}
			
				if(res)	area.value = res;
				else area.value = "";
				// Send response
				respose.click();
			});
		}, false);
	}	
})();

