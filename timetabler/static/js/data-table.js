(function($) {
  'use strict';
  $(function() {
    $('#order-listing').DataTable({
      "aLengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
      "iDisplayLength": 10
    });

    $('#order-listing-1').DataTable({
      "aLengthMenu": [[5, 10, 20, -1], [5, 10, 20, "All"]],
      "iDisplayLength": 5
    });
  });
})(jQuery);
