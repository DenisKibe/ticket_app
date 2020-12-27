$(document).ready(function(){
  //check if session is availabe
  if (sessionStorage.getItem('session') === null || sessionStorage.getItem('session')=="undefined") {
		window.location = "/";
	}
  document.cookie= "session="+sessionStorage.getItem('session');

  Sijax.request('getTick',[sessionStorage.getItem('BtnId')]);

  Sijax.request('getCom',[sessionStorage.getItem('BtnId')]);

  $('#sendcom').click(function(){
    comment=$('#comVal').val();

    if(comment.length < 1){
      toastr.warning('please write a comment');
      $('#comVal').focus();
    }else{
      Sijax.request('commenting',[sessionStorage.getItem('BtnId'),JSON.parse(sessionStorage.getItem('U')).data.user_id,comment]);
      Sijax.request('changeStatus',[sessionStorage.getItem('BtnId'),"OPEN"]);
      
  }
  });

  //make the register link visible is user is admin
  if(JSON.parse(sessionStorage.getItem('U')).data.role == 'Admin'){
    $('#regli').removeClass('invisible');
  }

  // $.ajax({
  //     url:window.location.origin+"/api/getticket",
  //
  //     method:'POST',
  //     dataType:'json',
  //     headers:{
  //       'Content-Type':'application/json',
  //     },
  //     data:JSON.stringify({'ticketId':tickId}),
  //     success:function(ResponseBody){
  //
  //       console.log(JSON.stringify(ResponseBody));
  //       let dataD=JSON.parse(JSON.stringify(ResponseBody));
  //
  //       $('#usrNameD').html(dataD.username);
  //       $('#assignedD').html(dataD.Assigned);
  //       $('#statusD').html(dataD.status);
  //       $('#priorityD').html(dataD.priority);
  //       $('#createdD').html(dataD.created);
  //       $('#updatedD').html(dataD.updated);
  //       $('#categoryD').html(dataD.category);
  //       $('#subjectD').html(dataD.subject);
  //       $('#noteD').html(dataD.comment);
  //     },
  //     error:function(error){
  //       console.log(JSON.stringify(error));
  //
  //     }
  //   });



})
