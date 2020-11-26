$(document).ready(function(){
  //function to check password length
  function lengthValidator(pass){
        if (pass.length >= 8) {
          return true;
        } else {
            $('#errorMSG').html("password must be greater than 8 characters!");
            $('#ErrorM').modal('show');
          return false;
        }
      };


    $('#login').click(function(e){
      e.preventDefault();
      var username=$('#username').val();
      var password=$('#PwordL').val();

      var lengthValid = lengthValidator(password);

      if (lengthValid) {

          $('#labelforpassword').attr('data-success','right');
          $('#login').addClass('disabled');
          $('#login').html('<i class="fa fa-spinner fa-spin fa-1x fa-fw"></i>');

          $.ajax({
              url: "http://127.0.0.1:5000/auth/login",

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
                          sessionStorage.type = userResponse.token_type;

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
                              window.location = "http://127.0.0.1:5000/dashboard";
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



toastr.options = {
  "closeButton": true,
  "debug": true,
  "newestOnTop": true,
  "progressBar": true,
  "positionClass": "md-toast-top-right",
  "preventDuplicates": true,
  "onclick": null,
  "showDuration": 300,
  "hideDuration": 3000,
  "timeOut": 5000,
  "extendedTimeOut": 1000,
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

});
