(function($) {
  'use strict';
  $(function() {
		$('#show').avgrund({
			height: 500,
			holderClass: 'custom',
			showClose: true,
			showCloseText: 'close',
			onBlurContainer: '.container-scroller',
			template: '<div class="alert alert-warning" role="alert"><p style="text-align:justify; color: #000">Dear Supervisor, please make sure you confirm that this manager\'s account is complete and accurate. Confirm all submitted cash, expenses, trading balances etc.'+
      '<br><strong>NOTE:</strong> You will be held responsible for any loss on this account if you didn\'t report any fault, shortage or fraudulent acts immediately.</p></div>' +
			'<div>' +
      '<form><input id="exampleInputPassword1" placeholder="Password" type="password" style="width: 100%; font-size:12px; margin-bottom: 10px; height:40px;">'+
      '<button id="mysjsjxllls" class="btn btn-github btn-block"><i class="mdi mdi-thumb-up"></i> Accept Record</button>' +
			'</form></div>'
		});
	})
})(jQuery);
