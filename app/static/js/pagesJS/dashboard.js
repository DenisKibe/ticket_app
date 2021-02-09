$(document).ready(function(){
  if (sessionStorage.getItem('session') === null || sessionStorage.getItem('session')=="undefined") {
		window.location = "/";
	}

  document.cookie= "session="+sessionStorage.getItem('session');

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

				let r =JSON.parse(JSON.stringify(ResponseBody));
				console.log(JSON.stringify(ResponseBody));
        sessionStorage.U=JSON.stringify(ResponseBody);
        if(r.data.role == 'Admin'){
          $('#regli').removeClass('invisible');
        }
        $('#usernameS').html(r.data.username)
        $('#userRole').html(r.data.role)

        Sijax.request('getCounts',[r.data.user_id,r.data.role]);
			},
			error:function(error){
				console.log(JSON.stringify(error));
        toastr.error(JSON.parse(JSON.stringify(error)).responseJSON.error);
        sessionStorage.clear();
        setTimeout(function () {
          window.location="/";
        }, 5000);
			}
    });

    $('#totalTL').click(function(){
      sessionStorage.status="Total";
    });
    $('#newTL').click(function(){
      sessionStorage.status="NEW";
    });
    $('#openTL').click(function(){
      sessionStorage.status="OPEN";
    });
    $('#closedTL').click(function(){
      sessionStorage.status="CLOSED";
    });
    $('#solvedTL').click(function(){
      sessionStorage.status="SOLVED";
    });
    $('#unsolvedTL').click(function(){
      sessionStorage.status="UNSOLVED";
    });
    $('#assignedTL').click(function(){
      sessionStorage.status="ASSIGNED";
    });


    //bar
    function test(contentdata){
      var ctxB = document.getElementById("barChart").getContext('2d');
      var myBarChart = new Chart(ctxB, {
        type: 'bar',
        data: {
          labels: ["New", "Assigned", "solved", "Unsolved", "Closed"],
          datasets: [{
            label: 'tickets',
            data: contentdata ,
            backgroundColor: [

              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 99, 132, 0.2)'
            ],
            borderColor: [

              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(255,99,132,1)'
            ],
            borderWidth: 1
          }]
        },
        optionss: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true
              }
            }]
          }
        }
      });

      $('#newT').on('change',function(event){
        alert(event.type);
      });
    }



    $.ajax({
  			url:window.location.origin+"/api/stats",

  			method:'Get',
  			dataType:'json',
        headers:{
  				'Content-Type':'application/json',
          'Authorization':'Bearer '+sessionStorage.getItem('session')
  			},
        data:false,
  			success:function(ResponseBody){

  				let r =JSON.parse(JSON.stringify(ResponseBody));
  				console.log(JSON.stringify(ResponseBody));
          test([r.newT,r.assignedT,r.solvedT,r.unsolvedT, r.closedT]);
  			},
  			error:function(error){
  				console.log(JSON.stringify(error));
          toastr.error('error');
  			}
      });

      $('#getStatDate').on('change', function(){
        let dateVal=$('#getStatDate').val();
        var start="", end="";
        if (dateVal == "Today"){
          let today= new Date();
          start = today.toISOString().slice(0,10);
          end = today.toISOString().slice(0,10);
        }
        else if ( dateVal == "Yesterday"){
          let today = new Date();
          today.setDate(today.getDate() - 1);
          start = today.toISOString().slice(0,10);
          end = today.toISOString().slice(0,10);
        }
        else if (dateVal == "7days"){
          let today = new Date();
          today.setDate(today.getDate() - 7);
          start = today.toISOString().slice(0,10);
          end = new Date().toISOString().slice(0,10);
        }
        else if (dateVal == "30days"){
          let today = new Date();
          end = today.toISOString().slice(0,10);
          today.setDate(today.getDate()- 30);
          start = today.toISOString().slice(0,10);
        }
        else if (dateVal == "week"){
          let today = new Date();
          today.setDate(today.getDate() - today.getDay());
          end = today.toISOString().slice(0,10);
          today.setDate(today.getDate() - 6);
          start = today.toISOString().slice(0,10);
        }
        else if (dateVal == "month"){
          let today = new Date();
          today.setDate(today.getDate() - today.getDate());
          end  = today.toISOString().slice(0,10);
          today.setDate((today.getDate() - today.getDate())+1 );
          start = today.toISOString().slice(0,10);
        }

        $.ajax({
          url:window.location.origin+"/api/getdates",
          method:'post',
          dataType:'json',
          headers:{
    				'Content-Type':'application/json',
            'Authorization':'Bearer '+sessionStorage.getItem('session')
    			},
          data:JSON.stringify({'start':start,'end':end}),
          success:function(ResponseBody){
            let r =JSON.parse(JSON.stringify(ResponseBody));
            console.log(JSON.stringify(ResponseBody));
            test([r.newT,r.assignedT,r.solvedT,r.unsolvedT, r.closedT]);

          },
          error:function(err){
            console.log(JSON.stringify(err));
            toastr.error('error');
          }
        });
      })

});
