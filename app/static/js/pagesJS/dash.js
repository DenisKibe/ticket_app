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

    if($("#titleT").val() == "Search"){
      $('#searchFrom').html('');
      $('#searchForm').html('<form class=""><div class="input-group"><select class="form-control" id="fieldS" name="fieldS"><option value="ID">ID</option><option value="subject">subject</option><option value="comment">comment</option><option value="category">category</option></select><input type="text" aria-label="vall" id="vall" class="form-control"><div class="input-group-append"><button class="btn btn-md btn-outline-default m-0 px-3 py-2 z-depth-0 waves-effect" type="button" id="searchbtn">search</button></div></div></form>');
      $('#content').html('');
    }else{
      sessionStorage.status=$("#titleT").val();

      $.ajax({
        url:window.location.origin+"/api/getdata",
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

              $('#content').append('<tr><td scope="row">'+z+'</td><td>'+r[key].ticketId+'</td><td>'+r[key].username+'</td><td style="white-space:nowrap; text-overflow:ellipsis; overflow:hidden; max-width:4px;">'+r[key].subject+'</td><td>'+r[key].category+'</td><td><span class="badge badge-pill badge-secondary">'+r[key].priority+'</span></td><td><span class="badge badge-pill badge-secondary">'+r[key].status+'</span></td><td>'+r[key].created+'</td><td>'+r[key].updated+'</td><td><a href="viewticket.html" id="'+r[key].ticketId+'"class="btn btn-outline-info btn-rounded btn-sm px-2">&#9998</a></td></tr>');
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

  //on enter start to get content
  $.ajax({
    url:window.location.origin+"/api/getdata",
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

          $('#content').append('<tr><td scope="row">'+z+'</td><td>'+r[key].ticketId+'</td><td>'+r[key].username+'</td><td style="white-space:nowrap; text-overflow:ellipsis; overflow:hidden; max-width:4px;">'+r[key].subject+'</td><td>'+r[key].category+'</td><td><span class="badge badge-pill badge-secondary">'+r[key].priority+'</span></td><td><span class="badge badge-pill badge-secondary">'+r[key].status+'</span></td><td>'+r[key].created+'</td><td>'+r[key].updated+'</td><td><a href="viewticket.html" id="'+r[key].ticketId+'"class="btn btn-outline-info btn-rounded btn-sm px-2">&#9998</a></td></tr>');
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

$('#searchbtn').click(function(){
  alert('clicked')
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
        'Content-Type':'application/json'
      },
      data:JSON.stringify({'field':field,'vall':vall}),
      success:function(Resp){
        console.log(JSON.parse(JSON.stringify(Resp)));
        let r= JSON.parse(JSON.stringify(Resp));
        let z=0;
        for ( var key in r){
          if(r.hasOwnProperty(key)){
            z++;

            $('#content').append('<tr><td scope="row">'+z+'</td><td>'+r[key].ticketId+'</td><td>'+r[key].username+'</td><td style="white-space:nowrap; text-overflow:ellipsis; overflow:hidden; max-width:4px;">'+r[key].subject+'</td><td>'+r[key].category+'</td><td><span class="badge badge-pill badge-secondary">'+r[key].priority+'</span></td><td><span class="badge badge-pill badge-secondary">'+r[key].status+'</span></td><td>'+r[key].created+'</td><td>'+r[key].updated+'</td><td><a href="viewticket.html" id="'+r[key].ticketId+'"class="btn btn-outline-info btn-rounded btn-sm px-2">&#9998</a></td></tr>');
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

})
