var currentt = null;
currentt = {};

function lowCase(str) {
	var splitStr = str.toLowerCase().split('.');
	for (var i = 0; i < splitStr.length; i++) {
		// You do not need to check if i is larger than splitStr length, as your for does that for you
		// Assign it back to the array
		splitStr[i] = splitStr[i].substring(0).toLowerCase();     
	}
	// Directly return the joined string
	return splitStr.join('.'); 
 }

$.ajax({
	url : 'php/getUser.php', // your php file
	type : 'GET', // type of the HTTP request
	//async: true,
	cache: false,
	success : function(data){
		var obj = data.split('\\');
		var userName = obj[1];
		processUser(userName);			
	}
}); 

function processUser(data){
	currentt["user"] = data;
	$.ajax({
		url : 'php/mrvUsers.php', // your php file
		type : 'GET', // type of the HTTP request
		cache: false,
		success : function(data){
			var obj = jQuery.parseJSON(data);
			for (i=0; i<obj.length; i++){
				if(lowCase(currentt["user"]) == lowCase(obj[i].UserName)){
					currentt["userFound"] = "YES";
				}
			}
			if(currentt["userFound"] == "YES"){
				$.ajax({
					url : 'php/piDaily.php', // your php file
					type : 'GET', // type of the HTTP request
					cache: false,
					success : function(data){
						var obj = jQuery.parseJSON(data);
						processPiDaily(obj);
						$.ajax({
							url : 'php/flareData.php', // your php file
							type : 'GET', // type of the HTTP request
							cache: false,
							success : function(data){
								var obj = jQuery.parseJSON(data);
								processFlareData(obj);
								$.ajax({
									url : 'php/plantMonthly.php', // your php file
									type : 'GET', // type of the HTTP request
									cache: false,
									success : function(data){
										var obj = jQuery.parseJSON(data);
										processPlantMonthly(obj);
										$.ajax({
											url : 'php/getPILive.php', // your php file
											type : 'GET', // type of the HTTP request
											cache: false,
											success : function(data){
												var obj = jQuery.parseJSON(data);
												processLiveData(obj);
										/*$.ajax({
											url : 'mrv_data/getPILive.json', // your php file
											type : 'GET', // type of the HTTP request
											cache: false,
											success : function(data){
												//var data = jQuery.parseJSON(data);
												processLiveData(data);*/
												$.ajax({
													url : 'php/officeData.php', // your php file
													type : 'GET', // type of the HTTP request
													cache: false,
													success : function(data){
														var obj = jQuery.parseJSON(data);
														processOffData(obj);
														$.ajax({
															url : 'php/getOfficesData.php', // your php file
															type : 'GET', // type of the HTTP request
															cache: false,
															success : function(data){
																var obj = jQuery.parseJSON(data);
																processOfficesData(obj);
																$.ajax({
																	url : 'php/logisticsData.php', // your php file
																	type : 'GET', // type of the HTTP request
																	cache: false,
																	success : function(data){
																		var obj = jQuery.parseJSON(data);
																		processLogisticsData(obj);
																		$.ajax({
																			url : 'php/upstreamData.php', // your php file
																			type : 'GET', // type of the HTTP request
																			cache: false,
																			success : function(data){
																				var obj = jQuery.parseJSON(data);
																				processUpstreamData(obj);
																				$.ajax({
																					url : 'php/projData.php', // your php file
																					type : 'GET', // type of the HTTP request
																					cache: false,
																					success : function(data){
																						var obj = jQuery.parseJSON(data);
																						processprojData(obj);
																						$.ajax({
																							url : 'php/projectData.php', // your php file
																							type : 'GET', // type of the HTTP request
																							cache: false,
																							success : function(data){
																								var obj = jQuery.parseJSON(data);
																								processprojectData(obj);
																								$.ajax({
																									url : 'php/shipData.php', // your php file
																									type : 'GET', // type of the HTTP request
																									cache: false,
																									success : function(data){
																										var obj = jQuery.parseJSON(data);
																										processShipData(obj);
																										$.ajax({
																											url : 'php/summaryData.php', // your php file
																											type : 'GET', // type of the HTTP request
																											cache: false,
																											success : function(data){
																												var obj = jQuery.parseJSON(data);
																												processSummaryData(obj);
																												$.ajax({
																													url : 'mrv_data/cargoes.json', // your php file
																													type : 'GET', // type of the HTTP request
																													dataType : 'json',
																													async: true,
																													cache: false,
																													success : function(data){
																														processCargoes(data);
																													}
																												});
																												postVisit();
																												/*console.log(window.screen.width)
																												if(window.screen.width > 300){
																													//document.getElementById("summary").style.height = window.screen.height - 150 + 'px';
																													//document.getElementById("summary").style.width = window.screen.width - 20 + 'px';
																													document.getElementById("homepage").style.height = window.screen.height - 150 + 'px';
																													document.getElementById("homepage").style.width = window.screen.width - 20 + 'px';
																												}*/
																											}
																										});
																									}
																								});
																							}
																						});
																					}
																				});
																			}
																		});
																	}
																});
															}
														});
													}
												});
											}
										});
									}
								});
							}
						});
					}
				});
			}
			else{
				document.getElementById('homepage').style.display='none';
				document.getElementById('error').style.display='block';
				document.getElementById('loading').style.display='none';
			}
		}
	});
}


window.setInterval(function(){
	$.ajax({
		url : 'php/piDaily.php', // your php file
		type : 'GET', // type of the HTTP request
		cache: false,
		success : function(data){
			var obj = jQuery.parseJSON(data);
			processPiDaily(obj);
			$.ajax({
				url : 'php/flareData.php', // your php file
				type : 'GET', // type of the HTTP request
				cache: false,
				success : function(data){
					var obj = jQuery.parseJSON(data);
					processFlareData(obj);
					$.ajax({
						url : 'php/plantMonthly.php', // your php file
						type : 'GET', // type of the HTTP request
						cache: false,
						success : function(data){
							var obj = jQuery.parseJSON(data);
							processPlantMonthly(obj);
							$.ajax({
								url : 'php/getPILive.php', // your php file
								type : 'GET', // type of the HTTP request
								cache: false,
								success : function(data){
									var obj = jQuery.parseJSON(data);
									processLiveData(obj);
							/*$.ajax({
								url : 'mrv_data/getPILive.json', // your php file
								type : 'GET', // type of the HTTP request
								cache: false,
								success : function(data){
									//var data = jQuery.parseJSON(data);
									processLiveData(data);*/
									$.ajax({
										url : 'php/officeData.php', // your php file
										type : 'GET', // type of the HTTP request
										cache: false,
										success : function(data){
											var obj = jQuery.parseJSON(data);
											processOffData(obj);
											$.ajax({
												url : 'php/getOfficesData.php', // your php file
												type : 'GET', // type of the HTTP request
												cache: false,
												success : function(data){
													var obj = jQuery.parseJSON(data);
													processOfficesData(obj);
													$.ajax({
														url : 'php/logisticsData.php', // your php file
														type : 'GET', // type of the HTTP request
														cache: false,
														success : function(data){
															var obj = jQuery.parseJSON(data);
															processLogisticsData(obj);
															$.ajax({
																url : 'php/upstreamData.php', // your php file
																type : 'GET', // type of the HTTP request
																cache: false,
																success : function(data){
																	var obj = jQuery.parseJSON(data);
																	processUpstreamData(obj);
																	$.ajax({
																		url : 'php/projData.php', // your php file
																		type : 'GET', // type of the HTTP request
																		cache: false,
																		success : function(data){
																			var obj = jQuery.parseJSON(data);
																			processprojData(obj);
																			$.ajax({
																				url : 'php/projectData.php', // your php file
																				type : 'GET', // type of the HTTP request
																				cache: false,
																				success : function(data){
																					var obj = jQuery.parseJSON(data);
																					processprojectData(obj);
																					$.ajax({
																						url : 'php/shipData.php', // your php file
																						type : 'GET', // type of the HTTP request
																						cache: false,
																						success : function(data){
																							var obj = jQuery.parseJSON(data);
																							processShipData(obj);
																							$.ajax({
																								url : 'php/summaryData.php', // your php file
																								type : 'GET', // type of the HTTP request
																								cache: false,
																								success : function(data){
																									var obj = jQuery.parseJSON(data);
																									processSummaryData(obj);
																									$.ajax({
																										url : 'cargoes.json', // your php file
																										type : 'GET', // type of the HTTP request
																										dataType : 'json',
																										async: true,
																										cache: false,
																										success : function(data){
																											processCargoes(data);
																										}
																									});
																								}
																							});
																						}
																					});
																				}
																			});
																		}
																	});
																}
															});
														}
													});
												}
											});
										}
									});
								}
							});
						}
					});
				}
			});
		}
	});
}, 5 * 60 * 1000);