

function changesel() {
	if (window.sessionStorage) {
	  	sessionStorage.setItem('fil', document.getElementById("fil").value);
	  	sessionStorage.setItem('typeotd', document.getElementById("typeotd").value);
	  	sessionStorage.removeItem('idotdclick');
	}	
}	
	
function getphones(idotd) {
	$('#tableph').remove();
	
	//поиск всех ссылок по классу linksotd		
	var i, links = document.querySelectorAll('.linksotd');
	for(i = 0; i < links.length; i++) {
   	links[i].classList.remove('bg-primary');
   	links[i].classList.remove('text-light');
		if (links[i].id != idotd) {
			$('i', links[i]).removeClass('icon-arrow-down');
			$('i', links[i]).addClass('icon-arrow-right');
		}
  	}
  	
		$('i', document.getElementById(idotd)).toggleClass("icon-arrow-right icon-arrow-down");
	
		//запрос на получение телефонных номеров из БД		
		$.ajax({
		type: 'get',
		url: '/phoneslist?idotd='+idotd+'',
		crossDomain: true
		}).done(function(resp) {
			var ph = JSON.parse(resp);	
			if ($('i', document.getElementById(idotd))[0].className == 'icon icon-arrow-down') {		
				if (window.sessionStorage) {
				  	sessionStorage.setItem('idotdclick', idotd);
				}	
				if (ph[0] == undefined) {
					addTable(new Map(), idotd);
				} else {
	 				addTable(ph, idotd);
				}	
			} else {
				if (window.sessionStorage) {
		  			sessionStorage.removeItem('idotdclick');
				}
			}	
		});
}			

function selotd() {
	$("#tableph > tbody").empty();
	if (window.sessionStorage) {
		if (sessionStorage.getItem('fil') != null) {	  	
	  		document.getElementById("fil").value = sessionStorage.getItem('fil');
	  	}
		if (sessionStorage.getItem('typeotd') != null) {	  	
	  		document.getElementById("typeotd").value = sessionStorage.getItem('typeotd');
	  	}
	}
	var selfil = document.getElementById("fil");
	var valfil = selfil.value;
	var seltype = document.getElementById("typeotd");
	if (seltype.value == "") {
		var types = 'hosp,dhosp,amb,reanim,oper,serv,nonmed';
	}
	else {
		var types = seltype.value;	
	}
	$.ajax({
	type: 'get',
	url: '//struc.iood.ru/api/branch/'+valfil+'/deps?types='+types+'',
	crossDomain: true
	}).done(function(resp) {
			if ($('#otd').length > 0) {
				var objSel = document.getElementById("otd");
				//var selpust = (objSel.options[0].value == '') ? true : false;
				var oldotd = objSel.options[0].value;
				$('#otd').empty();						
			}
			var employees = resp;
			employees.sort(function(obj1, obj2) {
			  if (obj1.name < obj2.name) return -1;
			  if (obj1.name > obj2.name) return 1;
			  return 0;
			});			
			//предварительная очистка столбцов отделений
			$("#otdeleniya1").empty();
			$("#otdeleniya2").empty();
			$("#otdeleniya3").empty();
			//подсчет количества строк в столбце
			var allstr = resp.length;
			var strcount = Math.floor(allstr/3);
			if (allstr > strcount*3) {
				strcount++;
			}
			var i = 0;							
			for(el in employees) {
				if ($('#otd').length == 0) {
				i++;
				if (i <= strcount*1) {
					var colotd = '#otdeleniya1';		
				} else if (i <= strcount*2) {
					var colotd = '#otdeleniya2';	
				} else {
					var colotd = '#otdeleniya3';
				}
				$(colotd).append('<a href="#" id='+employees[el]['id']+' onclick=getphones("'+employees[el]['id']+'") class="linksotd text-dark text-bold"><i class="icon icon-arrow-right"></i>'+employees[el]['name']+'</a>');					
				//$('<a>', { href: '#', text: employees[el]['name'], id: employees[el]['id'], onclick: 'getphones("'+employees[el]['id']+'")', class: 'linksotd' }).appendTo(colotd);
				$(colotd).append('<br>');
				//$('<br>').appendTo(colotd);
				} else {
					objSel.append(new Option(employees[el]['name'], employees[el]['id']));
				}
			}
			if ($('#otd').length != 0) {
				if (objSel.options.length == 0) {
					objSel.append(new Option('', ''));
				} else if (oldotd != '') {
					objSel.value = oldotd;						
				}	
			}
			if (window.sessionStorage && document.URL.indexOf('phonesnew') != -1) {
				var myidotd = sessionStorage.getItem('idotdclick');
				if (myidotd != null) {
					getphones(myidotd);	
				}
			}

		});	
}

function selotdPhoneForm() {
	var selfil = document.getElementById("fil");
	var valfil = selfil.value;
	var seltype = document.getElementById("typeotd");
		if (seltype.value == "") {
			var types = 'hosp,dhosp,amb,reanim,oper,serv,nonmed';
		}
		else {
			var types = seltype.value;	
		}
		$.ajax({
		type: 'get',
		url: '//struc.iood.ru/api/branch/'+valfil+'/deps?types='+types+'',
		crossDomain: true
		}).done(function(resp) {
			var objSel = document.getElementById("otd");
			$('#otd').empty();						
			var employees = resp;
			employees.sort(function(obj1, obj2) {
			  if (obj1.name < obj2.name) return -1;
			  if (obj1.name > obj2.name) return 1;
			  return 0;
			});			
				for(el in employees) {
						objSel.append(new Option(employees[el]['name'], employees[el]['id']));
				}
				if (objSel.options.length == 0) {
					objSel.append(new Option('', ''));
				} else {
					objSel.value = objSel.options[0].value;						
					//$('#otd > option[value="'+oldotd+'"]').attr("selected", "");
				}			
		});	
}


function addTable(ph, idotd) {
	let elem = document.getElementById(idotd);
	let table = document.createElement('table');
	table.className = 'table';
	table.id = 'tableph';
	elem.after(table);
	$('#tableph').append(`<thead class="text-center">
									<tr>
										<th>абонент</th>
										<th>внешний</th>
										<th>внутренний</th>
									</tr>
								</thead>
								<tbody></tbody>`);
	for(el in ph) {
		
		if (ph[el]['email'] != '') {
			var butmail = `<td class="special pop text-center">
		 							<div class="popover popover-bottom">
		 								<button type="button" class="btn btn-link"><i class="icon icon-mail"></i></button>
		 								<div class="popover-container">
 											<div class="card">
 												<div class="card-body">
													${ph[el]['email']} 																	
 												</div>
 											</div>		    														
 										</div>	
		 							</div>	
		 						</td>`;
		} else {
			var butmail = '';	
		}

		if (ph[el]['comment'] != '') {
			var butcomm = `<td class="special pop text-center">
		 							<div class="popover popover-bottom">
		 								<button type="button" class="btn btn-link"><i class="icon icon-bookmark"></i></button>
		 								<div class="popover-container">
 											<div class="card">
 												<div class="card-body">
													${ph[el]['comment']} 																	
 												</div>
 											</div>		    														
 										</div>	
		 							</div>	
		 						</td>`;
		} else {
			var butcomm = '';	
		}
				
		$('#tableph > tbody').append(`<tr id=${ph[el]['id']} onclick=clicktr("${ph[el]['id']}")>
													<td class="special">${ph[el]['nameabon']}</td>
							 						<td class="special sm text-center">${ph[el]['numberout']}</td>
							 						<td class="special sm text-center">${ph[el]['numberin']}</td>
							 						${butmail}
							 						${butcomm}
												</tr>`);		
		if (ph[el]['isactive']) {
			if (ph[el]['isgeneral']) {	
				$('#'+ph[el]['id']).addClass('text-bold');			
			}
		} else {
			$('#'+ph[el]['id']).addClass('text-error');
		}		
	}
}

