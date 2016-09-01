(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .filter('unique', Unique);

  /** @ngInject */
  function Unique(ForberedelsenService) {
    return function (a) {
      var duties = ForberedelsenService.getDuties();
      var filter = a.filter(function (item) {
        var present = false;
        duties.duties.forEach(function (dutie) {
          if (item == dutie.name)
            present = true;
        });
        return !present;
      });
      return filter;
    }
  }
})();
