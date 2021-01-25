$(document).ready(function() {

  $('#userId').val(JSON.parse(sessionStorage.getItem('U')).data.user_id);

  //make the register link visible is user is admin
  if(JSON.parse(sessionStorage.getItem('U')).data.role == 'Admin'){
    $('#regli').removeClass('invisible');
  }
  $('#usernameS').html(JSON.parse(sessionStorage.getItem('U')).data.username)
  $('#userRole').html(JSON.parse(sessionStorage.getItem('U')).data.role)

  //for the breadcrumb
  $('#breadC').append('<li class="breadcrumb-item"><a href="{{url_for("createticket")}}" class="black-text">CreateTicket</a></li>');

  //click createbtn
  $('#createbtn').click(function(){
    $('#createbtn').addClass('disabled');
    $('#createbtn').html('<i class="fa fa-spinner fa-spin fa-1x fa-fw"></i>');
  });
});
