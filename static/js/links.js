function ch_type() {
	if (window.sessionStorage) {
		sessionStorage.setItem('typelink', document.getElementById('typelink').value);
	}	
}
function get_links() {
	if ($('#list').length > 0) {
		$('#list').empty();	
		if (window.sessionStorage) {
			if (sessionStorage.getItem('typelink') != null) {
				document.getElementById('typelink').value = sessionStorage.getItem('typelink');	
			}
		}
		var valtype = document.getElementById('typelink').value;
		
		//запрос на получение значений по отбору БД		
		$.ajax({
		type: 'get',
		url: '/admin/get_links?typelink='+valtype+'',
		crossDomain: true
		}).done(function(resp) {
			var query = resp;	
			for (el in query) {
				$('#list').append(`<tr>
										  	<td>${query[el]['linkname']}</td>
							 				<td>${query[el]['fullname']}</td>
							 				<td>${query[el]['typelink']}</td>
											<td class='text-center'>
												<button type='submit' class='btn btn-link' name='changesub' value=${query[el]['id']}>
													<i class='icon icon-edit'></i>
												</button>					
											</td>						
											<td class='text-center'>
												<button type='submit' class='btn btn-link' name='delsub' value=${query[el]['id']}>
													<i class='icon icon-delete'></i>
												</button>					
											</td>						
										  </tr>`);		
			}			
		});
	}		
}
 
