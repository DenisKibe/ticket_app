$(document).ready(function(){
  if (sessionStorage.getItem('session') === null || sessionStorage.getItem('session')=="undefined") {
		window.location = "/";
	}
  $.ajax({
			url:"http://127.0.0.1:5000/auth/status",

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

});
