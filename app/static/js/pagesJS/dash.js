function getData(cb_func) {
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
    success:cb_func,
    error:function(Err){
      console.log(JSON.stringify(Err));
      toastr.error('An Error occured. Please try again later');
    }
  });
}
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
      getData(function( data ) {
        console.log(JSON.parse(JSON.stringify(data)));

        data = JSON.parse(JSON.stringify(data));
        $('#ticketTable').DataTable().destroy();

    	$('#ticketTable').DataTable( {
        data:data,
        columns:[
          {
            data:"numCount"
          },
          {
            data:"ticketId"
          },
          {

            data:"username"
          },
          {

            data:"subject"
          },
          {

            data:"category"
          },
          {

            data:"priority"
          },
          {

            data:"status"
          },
          {
            data:"created"
          },
          {
            data:"updated"
          }
        ],
        "pagingType": "full"
    	});
      $('.dataTables_length').addClass('bs-select');
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

      getData(function( data ) {
        console.log(JSON.parse(JSON.stringify(data)));

        data = JSON.parse(JSON.stringify(data));
        $('#ticketTable').DataTable().destroy();

      	$('#ticketTable').DataTable( {
          data:data,
          columns:[
            {
              data:"numCount"
            },
            {
              data:"ticketId"
            },
            {
              data:"username"
            },
            {
              data:"subject"
            },
            {
              data:"category"
            },
            {
              data:"priority"
            },
            {
              data:"status"
            },
            {
              data:"created"
            },
            {
              data:"updated"
            }
          ],
          "pagingType": "full"
      	});
        $('.dataTables_length').addClass('bs-select');
      });
    }
  });

  //make the register link visible is user is admin
  if(JSON.parse(sessionStorage.getItem('U')).data.role == 'Admin'){
    $('#regli').removeClass('invisible');
  }
  $('#usernameS').html(JSON.parse(sessionStorage.getItem('U')).data.username)
  $('#userRole').html(JSON.parse(sessionStorage.getItem('U')).data.role)




  //for filter on keyup start to search
  $('#filterT').on('keyup', function(){
      var value = $(this).val().toLowerCase();
      $("#content tr").filter(function(){
        $(this).toggle($(this).text().toLowerCase().indexOf(value)> -1)
      });

  });


    //on enter start to get content
  getData(function( data ) {
    console.log(JSON.parse(JSON.stringify(data)));

    data = JSON.parse(JSON.stringify(data));

	$('#ticketTable').DataTable( {
    data:data,
    columns:[
      {
        data:"numCount"
      },
      {
        data:"ticketId"
      },
      {
        data:"username"
      },
      {
        data:"subject"
      },
      {
        data:"category"
      },
      {
        data:"priority"
      },
      {
        data:"status"
      },
      {
        data:"created"
      },
      {
        data:"updated"
      }
    ],
    "pagingType": "full",
    select:{
      style:'single'
    }

	});
  $('.dataTables_length').addClass('bs-select');
  });

  $('#ticketTable tbody').on("click","tr",function(){

    sessionStorage.BtnId = $(this).find('td:nth-child(2)').html();

    window.location = "/viewticket.html";
  })


})
