$(document).ready(function(){
  //check if session is availabe
  if (sessionStorage.getItem('session') === null || sessionStorage.getItem('session')=="undefined") {
		window.location = "/";
	}
  document.cookie= "session="+sessionStorage.getItem('session');
  //set the drop down to the clicked button
  $('#titleT').val(sessionStorage.getItem('status'));

  //for the breadcrumb
  $('#breadC').append('<li class="breadcrumb-item"><a href="dash.html" class="black-text">Dash</a></li>');

  //for the search btn
  $('#searchbtn').on('click',function(){

    let field=$('#fieldS').val();
    let vall=$('#vall').val();

    if(vall.length <=2){
      toastr.info('search characters must be more than 2 for optimum result.');
      return false;
    }
    else{
      $.ajax({
        url:window.location.origin+"/api/search",
        method:'POST',
        dataType:'json',
        headers:{
          'Content-Type':'application/json',
          'Authorization':'Bearer '+sessionStorage.getItem('session')
        },
        data:JSON.stringify({'field':field,'vall':vall,'role':JSON.parse(sessionStorage.getItem('U')).data.role}),
        statusCode:{
          401:function(){
            toastr.error("Unauthorized! Please Login again");
            sessionStorage.clear();
            setTimeout(function () {
              window.location="/";
            }, 3000);
          }
        },
        success:function(Resp){
          console.log(JSON.parse(JSON.stringify(Resp)));
          $('#content').empty();
          let r= JSON.parse(JSON.stringify(Resp));
          let z=0;
          for ( var key in r){
            if(r.hasOwnProperty(key)){
              z++;
              var colorP,colorS

              if (r[key].priority == "HIGH"){
                colorP='badge-success';
              }
              else if(r[key].priority == "MEDIUM"){
                colorP='badge-info';
              }
              else{
                colorP = 'badge-light';
              }

              if (r[key].status == 'NEW'){
                colorS="badge-primary";
              }
              else if(r[key].status == 'CLOSED'){
                colorS="badge-danger";
              }
              else if (r[key].status == 'ASSIGNED'){
                colorS="badge-warning";
              }
              else if(r[key].status == 'SOLVED'){
                colorS="badge-secondary";
              }
              else{
                colorS="badge-default";
              }
              $('#content').append('<tr><td scope="row">'+z+'</td><td>'+r[key].ticketId+'</td><td>'+r[key].username+'</td><td style="white-space:nowrap; text-overflow:ellipsis; overflow:hidden; max-width:4px;">'+r[key].subject+'</td><td>'+r[key].category+'</td><td><span class="badge badge-pill '+colorP+'">'+r[key].priority+'</span></td><td><span class="badge badge-pill '+colorS+'">'+r[key].status+'</span></td><td>'+r[key].created+'</td><td>'+r[key].updated+'</td><td><a href="viewticket.html" id="'+r[key].ticketId+'"class="btn btn-outline-info btn-rounded btn-sm px-2" style="font-size:10px;">&#9998</a></td></tr>');
            }
          }

        },
        error:function(Err){
          console.log(JSON.stringify(Err));
          toastr.error('An Error occured. Please try again later');
        }
      });
    }
  })

  //listen to any changes of the dropdrop and get contents
  $('#titleT').change(function(){

    if($("#titleT").val() == "Search"){
      $('#searchForm').removeClass('invisible');
      $('#content').empty();
    }else{
      sessionStorage.status=$("#titleT").val();

      $.ajax({
        url:window.location.origin+"/api/getdata",
        method:'POST',
        dataType:'json',
        headers:{
          'Content-Type':'application/json',
          'Authorization':'Bearer '+sessionStorage.getItem('session')
        },
        data:JSON.stringify({'role':JSON.parse(sessionStorage.getItem('U')).data.role,'status':$("#titleT").val()}),
        statusCode:{
          401:function(){
            toastr.error("Unauthorized! Please Login again");
            sessionStorage.clear();
            setTimeout(function () {
              window.location="/";
            }, 3000);
          }
        },
        success:function(Resp){
          console.log(JSON.parse(JSON.stringify(Resp)));
          let r= JSON.parse(JSON.stringify(Resp));
          $('#content').html('');
          let z=0;
          for ( var key in r){
            if(r.hasOwnProperty(key)){
              z++;
              var colorP,colorS

              if (r[key].priority == "HIGH"){
                colorP='badge-success';
              }
              else if(r[key].priority == "MEDIUM"){
                colorP='badge-info';
              }
              else{
                colorP = 'badge-light';
              }

              if (r[key].status == 'NEW'){
                colorS="badge-primary";
              }
              else if(r[key].status == 'CLOSED'){
                colorS="badge-danger";
              }
              else if (r[key].status == 'ASSIGNED'){
                colorS="badge-warning";
              }
              else if(r[key].status == 'SOLVED'){
                colorS="badge-secondary";
              }
              else{
                colorS="badge-default";
              }
              $('#content').append('<tr><td scope="row">'+z+'</td><td>'+r[key].ticketId+'</td><td>'+r[key].username+'</td><td style="white-space:nowrap; text-overflow:ellipsis; overflow:hidden; max-width:4px;">'+r[key].subject+'</td><td>'+r[key].category+'</td><td><span class="badge badge-pill '+colorP+'">'+r[key].priority+'</span></td><td><span class="badge badge-pill '+colorS+'">'+r[key].status+'</span></td><td>'+r[key].created+'</td><td>'+r[key].updated+'</td><td><a href="viewticket.html" id="'+r[key].ticketId+'"class="btn btn-outline-info btn-rounded btn-sm px-2" style="font-size:10px;">&#9998</a></td></tr>');
            }
          }

        },
        error:function(Err){
          console.log(JSON.stringify(Err));
          toastr.error('An Error occured. Please try again later');
        }
      });
    }
  });

  //make the register link visible is user is admin
  if(JSON.parse(sessionStorage.getItem('U')).data.role == 'Admin'){
    $('#regli').removeClass('invisible');
  }
  $('#usernameS').html(JSON.parse(sessionStorage.getItem('U')).data.username)
  $('#userRole').html(JSON.parse(sessionStorage.getItem('U')).data.role)

  //on enter start to get content
  $.ajax({
    url:window.location.origin+"/api/getdata",
    method:'POST',
    dataType:'json',
    headers:{
      'Content-Type':'application/json',
      'Authorization':'Bearer '+sessionStorage.getItem('session')
    },
    data:JSON.stringify({'role':JSON.parse(sessionStorage.getItem('U')).data.role,'status':sessionStorage.getItem('status')}),
    statusCode:{
      401:function(){
        toastr.error("Unauthorized! Please Login again");
        sessionStorage.clear();
        setTimeout(function () {
          window.location="/";
        }, 3000);
      }
    },
    success:function(Resp){
      console.log(JSON.parse(JSON.stringify(Resp)));
      let r= JSON.parse(JSON.stringify(Resp));
      let z=0;
      for ( var key in r){
        if(r.hasOwnProperty(key)){
          z++;
          var colorP,colorS

          if (r[key].priority == "HIGH"){
            colorP='badge-success';
          }
          else if(r[key].priority == "MEDIUM"){
            colorP='badge-info';
          }
          else{
            colorP = 'badge-light';
          }

          if (r[key].status == 'NEW'){
            colorS="badge-primary";
          }
          else if(r[key].status == 'CLOSED'){
            colorS="badge-danger";
          }
          else if (r[key].status == 'ASSIGNED'){
            colorS="badge-warning";
          }
          else if(r[key].status == 'SOLVED'){
            colorS="badge-secondary";
          }
          else{
            colorS="badge-default";
          }
          $('#content').append('<tr><td scope="row">'+z+'</td><td>'+r[key].ticketId+'</td><td>'+r[key].username+'</td><td style="white-space:nowrap; text-overflow:ellipsis; overflow:hidden; max-width:4px;">'+r[key].subject+'</td><td>'+r[key].category+'</td><td><span class="badge badge-pill '+colorP+'">'+r[key].priority+'</span></td><td><span class="badge badge-pill '+colorS+'">'+r[key].status+'</span></td><td>'+r[key].created+'</td><td>'+r[key].updated+'</td><td><a href="viewticket.html" id="'+r[key].ticketId+'"class="btn btn-outline-info btn-rounded btn-sm px-2" style="font-size:10px;">&#9998</a></td></tr>');
        }
      }

    },
    error:function(Err){
      console.log(JSON.stringify(Err));
      toastr.error('An Error occured. Please try again later');
    }
  });

  //for filter on keyup start to search
  $('#filterT').on('keyup', function(){
      var value = $(this).val().toLowerCase();
      $("#content tr").filter(function(){
        $(this).toggle($(this).text().toLowerCase().indexOf(value)> -1)
      });

  });


  jQuery(document).delegate("#content a[href='viewticket.html']","click",function(event){
			//event.preventDefault();

			let BtnId=$(this).attr('id');

      sessionStorage.BtnId=BtnId;

    });



})
