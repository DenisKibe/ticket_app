$(document).ready(function() {
  $('.mdb-select').materialSelect();

  $('#userId').val(JSON.parse(sessionStorage.getItem('U')).data.user_id);

  //make the register link visible is user is admin
  if(JSON.parse(sessionStorage.getItem('U')).data.role == 'Admin'){
    $('#regli').removeClass('invisible');
  }

  //for the breadcrumb
  $('#breadC').append('<li class="breadcrumb-item"><a href="{{url_for("createticket")}}" class="black-text">CreateTicket</a></li>');
});
