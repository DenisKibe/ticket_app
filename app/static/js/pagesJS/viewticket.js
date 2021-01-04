$(document).ready(function(){
  //check if session is availabe
  if (sessionStorage.getItem('session') === null || sessionStorage.getItem('session')=="undefined") {
		window.location = "/";
	}
  document.cookie= "session="+sessionStorage.getItem('session');

  Sijax.request('getTick',[sessionStorage.getItem('BtnId')]);

  Sijax.request('getCom',[sessionStorage.getItem('BtnId')]);

  //for the comment
  $('#sendcom').click(function(){
    let comment=$('#comVal').val();

    if(comment.length < 1){
      toastr.warning('please write a comment');
      $('#comVal').focus();
    }else{
      $('#comVal').val('');
      Sijax.request('commenting',[sessionStorage.getItem('BtnId'),JSON.parse(sessionStorage.getItem('U')).data.user_id,comment]);
  }
  });

  // popovers Initialization
  $(function () {
    $('[data-toggle="popover"]').popover()
  })
  //for the change status
  $('#Cstatus').popover({
    html: true,
    placement: 'right',
    content: function () { return (JSON.parse(sessionStorage.getItem('U')).data.role=='Admin')?'<ol><li>CLOSED</li><hr><li>UNSOLVED</li></ol>':'<ul><li>SOLVED</li><li>UNSOLVED</li></ul>'; }
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
