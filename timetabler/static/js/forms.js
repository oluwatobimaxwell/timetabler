function back_to_login(){
  $('#password_reset').css('display','none'); $('#login_content').css('display','');
}

$('#reset_submit_me__btn').on('click', function(){

    var email_reset_ = $('#password_reset_email').val();
    $('#password_reset').css('display', 'none');
    $('#password_reset_loading').css('display', '');


          $.ajax({
                 type: "POST",
                 url: "includes/p_reset_lock.php",
                 data: {email_reset: email_reset_, jhbgvfdfghj: 'oibnkssgshsbpoelolsejhe'},
                 dataType: "text",
                 cache: false,
                 success: function(response){
                      // alert(response);
                  if (response == true) {

                    swal(
                      'Email Found!',
                      'A password reset link has been sent to your email address, please check your mail to complete password reset!',
                      'success'
                    )

                  }else if (response == false) {
                    swal(
                      'Error!',
                      'The email address entered does not exist!',
                      'error'
                    );
                  }else {
                    swal(
                      'Error!',
                      'Connection failed, please try again later!',
                      'error'
                    );
                  }


                 }
           }).then(function () {
             $('#password_reset').css('display', '');
             $('#password_reset_loading').css('display', 'none');
          })
});

$('#reset_submit_me__btn_new').on('click', function(){
  var client_server_code = $('#client_servelet_emplathstu').html();
  var new_password = $('#password_reset_new').val();
  var new_password_confirm = $('#password_reset_new_confirm').val();
  var comfirmcode = $('#client_servelet_resetcode').html();


    // var old = $('#change-password-private').val();
    var new_p = $('#password_reset_new').val();
    var new_p_conf = $('#password_reset_new_confirm').val();

    if(new_p != '' && new_p_conf != ''){
          if (new_p == new_p_conf) {
            if (password_check(new_p) == true) {
              // old = hex_sha512(old);
              new_p = hex_sha512(new_p);
              new_p_conf = hex_sha512(new_p_conf);
              $.ajax({
                     type: "POST",
                     url: "includes/p_reset_lock.php",
                     data: {pirvate_new_p: new_p, private_new_p_conf: new_p_conf, account_owner_for_use: client_server_code, code_reset: comfirmcode},
                     dataType: "text",
                     cache: false,
                     success: function(response){

                      if (response == true) {
                        swal(
                          'Successful',
                          'Password successfully set!',
                          'success'
                        ).then(function(){
                          window.location.href = 'index.php';
                        })
                      }else {
                        swal(
                          'Error',
                          'Unable to set your password, please try again.',
                          'error'
                        )
                      }
                     }
                   }
                 )
            }else {
              swal(
                'Password Not Allowed!',
                'Passwords must contain at least one number, one lowercase and one uppercase letter and must be at least 8 characters.  Please try again',
                'warning'
              )
            }

          }else {
            swal(
              'Error!',
              'New Password and Confirmation password <br> must be the same. Please try again!',
              'error'
            )
          }

  }else {
      swal(
        'Error',
        'All fields are required, please try again.',
        'error'
      )
    }

})
function formhash(submit) {

    var email = $('#email').val();
    var password = $('#password').val();

    if (email != '' && password != '') {
      // Finally submit the form.
      $('#login_content').css('display', 'none');
      $('#index_login_account').css('display', '');
      //
      // var login_content = $('#login_content').html();
      // $('#login_content').html('<div style="width: 50%; margin: auto"><img src="images/login_loading.gif" style="width: 100%; margin-top: 50%" /></div> <p style="text-align: center">Login in...</p>');

      var p = hex_sha512(password);

      $.ajax({
             type: "POST",
             url: "includes/process_login.php",
             data: {email, p},
             dataType: "json",
             cache: false,
             success: function(response){
            //   alert(response);

               if (response[0] == true) {
                 if (response[1] == 3) {
                //   window.location = 'manager/';
                   window.location.href = 'manager/';
                 }else {
                   window.location.href = 'admin_manager/';
                 }
               }else {
                 swal(
                   'Error!',
                   'Unable to log you in, please try again!',
                   'error'
                 )
               }

             }
       }).then(function () {

         $('#login_content').css('display', '');
         $('#index_login_account').css('display', 'none');

       })
    }else {
      swal(
        'Error!',
        'All fields are required, please check and try again!',
        'error'
      )
    }
}


function regformhash(form, email, password, conf) {
     // Check each field has a value
    if (
          matricno.value == ''     ||
          password.value == ''  ||
          conf.value == '') {

        alert('You must provide all the requested details. Please try again');
        return false;
    }



    // Check that the password is sufficiently long (min 6 chars)
    // The check is duplicated below, but this is included to give more
    // specific guidance to the user
    if (password.value.length < 6) {
        alert('Passwords must be at least 6 characters long.  Please try again');
        form.password.focus();
        return false;
    }


    // Check password and confirmation are the same
    if (password.value != conf.value) {
        alert('Your password and confirmation do not match. Please try again');
        form.password.focus();
        return false;
    }

    // Create a new element input, this will be our hashed password field.
    var p = document.createElement("input");

    // Add the new element to our form.
    form.appendChild(p);
    p.name = "p";
    p.type = "hidden";
    p.value = hex_sha512(password.value);

    // Make sure the plaintext password doesn't get sent.

    conf.value = "";

    // Finally submit the form.
    form.submit();
    return true;
}

function passwordformhash(form, oldpassword, newpassword, confirmnewp) {
     // Check each field has a value
    if (
          oldpassword.value == ''     ||
          newpassword.value == ''  ||
          confirmnewp.value == '') {

        alert('You must provide all the requested details. Please try again');
        return false;
    }



    // Check that the password is sufficiently long (min 6 chars)
    // The check is duplicated below, but this is included to give more
    // specific guidance to the user
    if (newpassword.value.length < 6) {
        alert('Passwords must be at least 6 characters long.  Please try again');
        form.password.focus();
        return false;
    }


    // Check password and confirmation are the same
    if (newpassword.value != confirmnewp.value) {
        alert('Your password and confirmation do not match. Please try again');
        form.password.focus();
        return false;
    }

    // Check password and confirmation are the same
    if (newpassword.value == oldpassword.value) {
        alert('Old and new password are the same. Use different password');
        form.password.focus();
        return false;
    }

    // Create a new element input, this will be our hashed password field.
    var oldp = document.createElement("input");
    var newp = document.createElement("input");


    // Add the new element to our form.
    form.appendChild(oldp);
    form.appendChild(newp);


    oldp.name = "oldp";
    newp.name = "newp";

    oldp.type = "hidden";
    newp.type = "hidden";


    oldp.value = hex_sha512(oldpassword.value);
    newp.value = hex_sha512(newpassword.value);


    // Make sure the plaintext password doesn't get sent.
    newpassword.value = "";
    confirmnewp.value = "";
    oldpassword.value = "";

    // Finally submit the form.
    form.submit();
    return true;
}

function password_check(password){
    re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/;

  if ((password.length < 8) || (!re.test(password)) ){
    return false;
  }else {
      return true;
  }
}
