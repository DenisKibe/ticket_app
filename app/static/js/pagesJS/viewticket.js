$(document).ready(function(){
  //check if session is availabe
  if (sessionStorage.getItem('session') === null || sessionStorage.getItem('session')=="undefined") {
		window.location = "/";
	}
  document.cookie= "session="+sessionStorage.getItem('session');

  Sijax.request('getTick',[sessionStorage.getItem('BtnId')]);

  Sijax.request('getCom',[sessionStorage.getItem('BtnId')]);

  //for the breadcrumb
  $('#breadC').append('<li class="breadcrumb-item"><a href="viewticket.html" class="black-text">ViewTicket</a></li>');
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

  //for the options
  if(JSON.parse(sessionStorage.getItem('U')).data.role=='Admin'){
    $('#opt2').html('UNSOLVED').attr('value','UNSOLVED');
    $('#opt3').html('CLOSED').attr('value','CLOSED');
  }else{
    $('#opt2').html('SOLVED').attr('value','SOLVED');
    $('#opt3').html('UNSOLVED').attr('value','UNSOLVED');
  }

  //for the edit statusbtn
  $('#Estatus').click(function(){
    $('#changeSat').toggleClass('disabled');
  });

  //on change start to change status
  $('#changeSat').on('change',function(){
    let newS=$('#changeSat').val();
    Sijax.request('changeStatus',[sessionStorage.getItem('BtnId'),newS]);
    $('#changeSat').addClass('disabled');
    if(JSON.parse(sessionStorage.getItem('U')).data.role=='Technician'){
      Sijax.request('clearNew',[sessionStorage.getItem('BtnId')]);
    }
  });
  //make the register link visible is user is admin
  if(JSON.parse(sessionStorage.getItem('U')).data.role == 'Admin'){
    $('#regli').removeClass('invisible');
  }
  $('#usernameS').html(JSON.parse(sessionStorage.getItem('U')).data.username)
  $('#userRole').html(JSON.parse(sessionStorage.getItem('U')).data.role)

  //add event to checkbox
  jQuery(document).delegate("#listTechM .chb","change",function(){
    $(".chb").prop('checked', false);
    $(this).prop('checked', true);

    let useId = $(this).val();
    let id=$(this).attr('id');
    let name = $("[for='"+id+"']").text();

    Sijax.request('assigning',[useId,sessionStorage.getItem('BtnId')]);
    $('#assignedD').val(name);
    $('#opt1').html('ASSIGNED');
    $('#listTechM').modal('hide');
  });

  //for view image
  $('#viewPic').click(function(){
      let imgurl= $('#imgUrl').html();
      if(imgurl == ''){
        $('#imgCont').empty();
        $('#imgCont').append('<p>No Image to show!</p>')
        $('#imageView').modal('show');
      }else{
        $('#imgCont').empty();
        $('#imgCont').append('<img src="'+window.location.origin+'/static'+imgurl+'" class=""/>');
        $('#imageView').modal('show');
      }
  });

  //assign button
  $('#assignTech').click(function(){
    if(JSON.parse(sessionStorage.getItem('U')).data.role != 'Admin'){
      toastr.warning('You do not have permission to assign');
    }else{
      $.ajax({
    			url:window.location.origin+"/api/getlisttech",

    			method:'Get',
    			dataType:'json',
    			headers:{
    				'Content-Type':'application/json',
            'Authorization':'Bearer '+sessionStorage.getItem('session')
    			},
          data:false,
          statusCode:{
            401:function(){
              toastr.error("Unauthorized! Please Login again");
              sessionStorage.clear();
              setTimeout(function () {
                window.location="/";
              }, 3000);
            }
          },
    			success:function(ResponseBody){
            let resp = JSON.parse(JSON.stringify(ResponseBody));
            console.log(resp)
            let y=0;
            $('#Mcontent').empty();
            for ( var key in resp){
              if(resp.hasOwnProperty(key)){
                y++;
                  $('#Mcontent').append('<div class="form-check"><input type="checkbox" class="form-check-input chb" id="'+y+'" value="'+resp[key].user_id+'"><label class="form-check-label" for="'+y+'">'+resp[key].username+'</label></div>');
                }
              }

              $('#listTechM').modal('show');
          },
    			error:function(error){
    				console.log(JSON.stringify(error));
          }

    });
  }
});


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
