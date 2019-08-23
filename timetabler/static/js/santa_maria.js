function lkjhgfghjshwhDasTSanta(){

  var kjhgfghjiehnsj_9jhwyy3_4161bbahshsvj_l = new Date();
  var ms = kjhgfghjiehnsj_9jhwyy3_4161bbahshsvj_l.getDate();
  var ms1 = kjhgfghjiehnsj_9jhwyy3_4161bbahshsvj_l.getMonth();
  var ms2 = kjhgfghjiehnsj_9jhwyy3_4161bbahshsvj_l.getFullYear();

  var santa_maria = ms2 +'-'+(ms1+1)+'-' +ms;
  return santa_maria;

}

// AUTHME

  setInterval(function(){

    var page = (window.location.pathname).split("/").pop();
    if (page != 'autherror.php') {
      var kshslhdVajsjmi = lkjhgfghjshwhDasTSanta();
      $.ajax({
             type: "POST",
             url: "includes/authDate.php",
             data: {currentUserDate: kshslhdVajsjmi},
             dataType: "text",
             cache: false,
             success: function(response){
               if (response != true) {
                 window.location = "autherror.php";
               }
             }});
    }

  }, 1000);
// AUTHME
