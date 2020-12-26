$(document).ready(function(){
  if (sessionStorage.getItem('session') === null || sessionStorage.getItem('session')=="undefined") {
		window.location = "/";
	}

  document.cookie= "session="+sessionStorage.getItem('session');

  $.ajax({
			url:window.location.origin+"/auth/status",

			method:'Get',
			dataType:'json',
			headers:{
				'Content-Type':'application/json',
        'Authorization':'Bearer '+sessionStorage.getItem('session')
			},
      data:false,
			success:function(ResponseBody){

				let r =JSON.parse(JSON.stringify(ResponseBody));
				console.log(JSON.stringify(ResponseBody));
        sessionStorage.U=JSON.stringify(ResponseBody);
        if(r.data.role == 'Admin'){
          $('#regli').removeClass('invisible');
        }

        Sijax.request('getCounts',[r.data.user_id,r.data.role]);
			},
			error:function(error){
				console.log(JSON.stringify(error));
        toastr.error(JSON.parse(JSON.stringify(error)).responseJSON.error);
        sessionStorage.removeItem('session');
        sessionStorage.removeItem('userId');
        setTimeout(function () {
          window.location="/";
        }, 5000);
			}
    });

    $('#totalTL').click(function(){
      sessionStorage.status="Total";
    });
    $('#newTL').click(function(){
      sessionStorage.status="NEW";
    });
    $('#openTL').click(function(){
      sessionStorage.status="OPEN";
    });
    $('#closedTL').click(function(){
      sessionStorage.status="CLOSED";
    });
    $('#solvedTL').click(function(){
      sessionStorage.status="SOLVED";
    });
    $('#unsolvedTL').click(function(){
      sessionStorage.status="UNSOLVED";
    });
    $('#assignedTL').click(function(){
      sessionStorage.status="ASSIGNED";
    });

});
