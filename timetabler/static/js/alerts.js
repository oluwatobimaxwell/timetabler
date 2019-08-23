/*
(function($) {
  showSwal = function(type){
        'use strict';
        if(type === 'basic'){
        	swal({
            text: 'Any fool can use a computer',
            confirmButtonColor: '#002388'
          })

    	}else if(type === 'title-and-text'){
        	swal({
            title: 'The Internet?',
            text: 'That thing is still around?',
            type: 'question',
            confirmButtonColor: '#002388'
          })

    	}else if(type === 'success-message'){
        	swal({
            title: 'Good job!',
            text: 'You clicked the button!',
            type: 'success',
            confirmButtonColor: '#002388'
          })

    	}else if(type === 'auto-close'){
            swal({
              title: 'Auto close alert!',
              text: 'I will close in 2 seconds.',
              timer: 2000,
              confirmButtonColor: '#002388'
            }).then(
            function () {},
              // handling the promise rejection
            function (dismiss) {
              if (dismiss === 'timer') {
                console.log('I was closed by the timer')
              }
            }
          )
    	}else if(type === 'warning-message-and-cancel'){
            swal({
              title: 'Are you sure?',
              text: "You won't be able to revert this!",
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#002388',
              cancelButtonColor: '#ea2c54',
              confirmButtonText: 'Yes, delete it!'
            }).then(function () {
            swal(
              'Deleted!',
              'Your file has been deleted.',
              'success'
            )
          })

    	}else if(type === 'custom-html'){
        	swal({
            title: '<i>HTML</i> <u>example</u>',
            type: 'info',
            html:
              'You can use <b>bold text</b>, ' +
              '<a href="//github.com">links</a> ' +
              'and other HTML tags',
            showCloseButton: true,
            showCancelButton: true,
            confirmButtonColor: '#002388',
            cancelButtonColor: '#ea2c54',
            confirmButtonText:
              '<i class="mdi mdi-thumb-up-outline"></i> Great!',
            cancelButtonText:
              '<i class="mdi mdi-thumb-down-outline"></i>'
          })
    	}
        }

})(jQuery);
*/
