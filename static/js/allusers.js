$(document).ready( function(){
	if (document.URL.indexOf('phone') != -1) {
		selotd();
		if (window.sessionStorage) {
			if (sessionStorage.getItem('typelink') != null) {
				sessionStorage.removeItem('typelink');
			}
		}		
	} else if (document.URL.indexOf('admin/links') != -1) {
		if (document.URL.indexOf('admin/links/link') == -1) {
			get_links();
			if (window.sessionStorage) {
				if (sessionStorage.getItem('idotdclick') != null) {
					sessionStorage.removeItem('idotdclick');
				}		
				if (sessionStorage.getItem('fil') != null) {
					sessionStorage.removeItem('fil');
				}		
				if (sessionStorage.getItem('typeotd') != null) {
					sessionStorage.removeItem('typeotd');
				}		
			}	
		} else {
			if (window.sessionStorage && sessionStorage.getItem('typelink') != null && sessionStorage.getItem('typelink') != '' && $('#typelink').length > 0) {
				document.getElementById('typelink').value = sessionStorage.getItem('typelink');
			}
		}
	} else {
		if (window.sessionStorage) {
			if (sessionStorage.getItem('idotdclick') != null) {
				sessionStorage.removeItem('idotdclick');
			}		
			if (sessionStorage.getItem('fil') != null) {
				sessionStorage.removeItem('fil');
			}		
			if (sessionStorage.getItem('typeotd') != null) {
				sessionStorage.removeItem('typeotd');
			}		
			if (sessionStorage.getItem('typelink') != null) {
				sessionStorage.removeItem('typelink');
			}		
		}	
	}	
});

function logout() {
	$.ajax({
	  type: 'post',
	  url: '//auth.iood.ru/user/logout',
	  headers: {'X-Requested-With': 'XMLHttpRequest'},
	  xhrFields: {withCredentials: true},
	  crossDomain: true
	}).done(function(resp) {
	 					$('#logout').attr('href', '/login').text('Вход');
		location.reload();										
	});	
 }

