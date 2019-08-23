
$('#loginsubmit').on('click', function(){
  event.preventDefault()

  var username = $('#loginform input:eq(1)').val()
  var password = $('#loginform input:eq(2)').val()

  if (username != '' && password != '') {
    $.ajax({
               type: "POST",
               url: "/process/",
               headers: { "X-CSRFToken": $('#loginform input:eq(0)').val() },
               data: {username: username, password:password},
               dataType: "json",
               cache: true,
               success: function(response){
                  if (response.status == true) {
                    window.location.href = response.message;
                  }else {
                    $('#message').html(response.message)
                  }
               }})
  }else {
    $('#message').html('<div class="alert alert-danger" role="alert" style="font-size: 12px; border: none;background: #ea2c54a3;">'
                        +'Both username and password are required!</div>')
  }

})

function loadModal(contenturl){
    $('#modalLoader .modal-dialog').load(contenturl)
}


function submitfaculty(facid){
      var id = $('#facultyform input:eq(1)').val()
      var name = $('#facultyform input:eq(2)').val()
      var officer = $('#facultyform select:eq(0)').val()
      var image = '';
      if (id != '' && name != '') {
        dataSend = {'facid': id, 'facname': name, 'facofficer': officer, 'facimage': image}
        $.ajax({
                   type: "POST",
                   url: "/home/processor/",
                   headers: { "X-CSRFToken": $('#facultyform input:eq(0)').val()},
                   data: dataSend,
                   dataType: "text",
                   cache: true,
                   beforeSend: function(){
                     $('.modal-footer button:eq(1)').html('<i class="fa fa-spin fa-spinner"></i>')
                   },
                   success: function(response){
                     $('.modal-footer button:eq(1)').html('Add Faculty')
                     $('#modalmessage').html(response)
                   }
                 })
      }else {
        $('#modalmessage').html('<div class="alert alert-danger" role="alert" style="font-size: 12px; border: none;background: #ea2c54a3;">'
                            +'Faculty ID and Name are required to continue!</div>')
      }
}



// REFRESH WHOLE PAGE
function loadpage(placement, url){
    $(placement).load(url)
}


function popalertQuesty(
  alert_title, alert_message, alert_type,
  button_text,request_type,request_url,
  request_data,
  success_message_board,
){
  swal({
  title: alert_title,
  html: alert_message,
  type: alert_type,
  showCancelButton: true,
  confirmButtonColor: '#002388',
  cancelButtonColor: '#ea2c54',
  confirmButtonText: button_text
}).then(function () {
  $.ajax({
         type: request_type,
         url: request_url,
         data: request_data,
         dataType: "text",
         cache: true,
         beforeSend: function(){
           $(success_message_board).html('<div class="col-12 alert alert-warning" role="alert">'
                        +'<strong><i class="fa fa-spin fa-spinner"></i></strong> Processing ...</div>')
         },
         success: function(response){
           $(success_message_board).html(response)
         }
       })})
}

$('.deleteDpt').on('click',function(){
  var tr = $(this).closest('tr')
  var name = tr.find('.name').text()
  var url = ($(this).val())
  var application = ($(this).attr('name'))
  var message = 'Are you sure you want to delete the '+application+' <br><strong>'+name+'</strong>? '
  popalertQuesty('Delete '+application+'?', message,'warning',
    'Continue', 'GET', url, '', '.page-message',
  )
})


$('.deleteFac').on('click',function(){
  var div = $(this).closest('div');
  var name = div.find('.faculty_name').text();
  var url = ($(this).val())
  var application = ($(this).attr('name'))
  var message = 'Are you sure you want to delete the '+application+' <br><strong>'+name+'</strong>? '
  popalertQuesty('Delete '+application+'?', message,'warning',
    'Continue', 'GET', url, '', '.page-message',
  )
})

//
$('input[type=checkbox]').on('change', function(){
    var cover  = $(this).attr('name')
    if($(this). prop("checked") == true){
      $('.'+cover).css('display', 'none')
    }else {
      $('.'+cover).css('display', '')
    }
})



$('#savesettings').submit(function(event){
    event.preventDefault()
    var form_data = new FormData(this);
    var url = $(this).attr('action')
        $.ajax({
                 type         : "POST",
                 url          : url,
                 data         : form_data,
                 dataType     : "text",
                 contentType  : false,
                 processData  : false,
                 beforeSend: function(){
                   $('.page-message').html('<div class="col-12 alert alert-warning" role="alert">'
                                +'<strong><i class="fa fa-spin fa-spinner"></i></strong> Saving constraints ...</div>')
                 },
                 success: function(response){
                    $('.page-message').html(response)
                 }})
})


function checkadmtype(value){
  $('#id_currentsemestername').prop("selectedIndex", 0)
  $('#id_currentsemestertype').prop("selectedIndex", 0)
  if (value == 'True') {
    $('.semester').css('display','none')
    $('.semester_').css('display','inline-block')
  }else {
    $('.semester_').css('display','none')
    $('.semester').css('display','inline-block')
  }
}




var elem = document.getElementById('modalLoader_inner');

/* View in fullscreen */
function openFullscreen() {
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.mozRequestFullScreen) { /* Firefox */
    elem.mozRequestFullScreen();
  } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE/Edge */
    elem.msRequestFullscreen();
  }
}

/* Close fullscreen */
function closeFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.mozCancelFullScreen) { /* Firefox */
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) { /* IE/Edge */
    document.msExitFullscreen();
  }
}
