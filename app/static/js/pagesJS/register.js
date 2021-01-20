$(document).ready(function(){

$('#Rusername').blur(function(){
  username=$('#Rusername').val();
  if(username==""){

  }else{
    Sijax.request('validates',[username]);
  }
});

$('#CSpass').keyup(function(){
  if($('#CSpass').val() != $('#Spass').val()){
    $('#LCSpass').attr('data-error','Not Equal');
    $('#CSpass').removeClass('validate').addClass('invalid').removeClass('valid');
  }else{
    $('#LCSpass').attr('data-success','right');
    $('#CSpass').removeClass('validate').addClass('valid').removeClass('invalid');
  }

  if($('#CSpass').hasClass('valid') && $('#Rusername').hasClass('valid')){
    $('#Rbtn').removeClass('disabled');
  }
});

$('#Rbtn').click(function(){
  let username= $('#Rusername').val();
  let role= $('#Rrole').val();
  let password= $('#Spass').val();
  let email = $('#Remail').val();

  $.ajax({
    url:window.location.origin+"/auth/register",

    method:'Post',
    dataType:'json',
    headers:{
      'Content-Type':'application/json',
      'Authorization':'Bearer '+sessionStorage.getItem('session')
    },
    data:JSON.stringify({ 'username': username, 'password': password,'role':role,'email':email }),
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
      console.log(JSON.stringify(ResponseBody));
      toastr.success('Registered successifuly');
    },
    error:function(error){
      console.log(JSON.stringify(error));
      toastr.error('Failed');
    }
  });
});

$('#usernameS').html(JSON.parse(sessionStorage.getItem('U')).data.username)
$('#userRole').html(JSON.parse(sessionStorage.getItem('U')).data.role)
});
