$(document).ready(function(){
  //check if session is availabe
  if (sessionStorage.getItem('session') === null || sessionStorage.getItem('session')=="undefined") {
		window.location = "/";
	}
  document.cookie= "session="+sessionStorage.getItem('session');
  //set the drop down to the clicked button
  $('#titleT').val(sessionStorage.getItem('status'));

  //listen to any changes of the dropdrop and get contents
  $('#titleT').change(function(){
    sessionStorage.status=$("#titleT").val();

    $.ajax({
      url:"http://35.189.71.15:8000/api/getdata",
      method:'POST',
      dataType:'json',
      headers:{
        'Content-Type':'application/json'
      },
      data:JSON.stringify({'role':JSON.parse(sessionStorage.getItem('U')).data.role,'status':$("#titleT").val(),'userId':JSON.parse(sessionStorage.getItem('U')).data.user_id}),
      success:function(Resp){
        console.log(JSON.parse(JSON.stringify(Resp)));
        let r= JSON.parse(JSON.stringify(Resp));
        $('#content').html('');
        let z=0;
        for ( var key in r){
          if(r.hasOwnProperty(key)){
            z++;

            $('#content').append('<tr><td scope="row">'+z+'</td><td>'+r[key].ticketId+'</td><td>'+r[key].username+'</td><td style="white-space:nowrap; text-overflow:ellipsis; overflow:hidden; max-width:4px;">'+r[key].subject+'</td><td>'+r[key].category+'</td><td><span class="badge badge-pill badge-secondary">'+r[key].priority+'</span></td><td><span class="badge badge-pill badge-secondary">'+r[key].status+'</span></td><td>'+r[key].created+'</td><td>'+r[key].updated+'</td><td><button type="button" id="'+r[key].ticketId+'"class="btn btn-outline-info btn-rounded btn-sm px-2"><i class="fas fa-pencil-alt mt-0"></i></button></td></tr>');
          }
        }

      },
      error:function(Err){
        console.log(JSON.stringify(Err));
        toastr.error('An Error occured. Please try again later');
      }
    });
  });

  //make the register link visible is user is admin
  if(JSON.parse(sessionStorage.getItem('U')).data.role == 'Admin'){
    $('#regli').removeClass('invisible');
  }

  //on enter start to get content
  $.ajax({
    url:"http://35.189.71.15:8000/api/getdata",
    method:'POST',
    dataType:'json',
    headers:{
      'Content-Type':'application/json'
    },
    data:JSON.stringify({'role':JSON.parse(sessionStorage.getItem('U')).data.role,'status':sessionStorage.getItem('status'),'userId':JSON.parse(sessionStorage.getItem('U')).data.user_id}),
    success:function(Resp){
      console.log(JSON.parse(JSON.stringify(Resp)));
      let r= JSON.parse(JSON.stringify(Resp));
      let z=0;
      for ( var key in r){
        if(r.hasOwnProperty(key)){
          z++;

          $('#content').append('<tr><td scope="row">'+z+'</td><td>'+r[key].ticketId+'</td><td>'+r[key].username+'</td><td style="white-space:nowrap; text-overflow:ellipsis; overflow:hidden; max-width:4px;">'+r[key].subject+'</td><td>'+r[key].category+'</td><td><span class="badge badge-pill badge-secondary">'+r[key].priority+'</span></td><td><span class="badge badge-pill badge-secondary">'+r[key].status+'</span></td><td>'+r[key].created+'</td><td>'+r[key].updated+'</td><td><button type="button" id="'+r[key].ticketId+'"class="btn btn-outline-info btn-rounded btn-sm px-2">&#9998</button></td></tr>');
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


  jQuery(document).delegate("#content button[type='button']","click",function(event){
			event.preventDefault();

			let BtnId=$(this).attr('id');

      newHref = "/viewticket/"+BtnId;

      window.location = newHref;
    });


})
