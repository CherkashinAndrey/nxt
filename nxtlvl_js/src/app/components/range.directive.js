(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('input', input);

  /** @ngInject */
  function input() {
    var directive = {
      restrict: 'E',
      require: '?ngModel',
      link: linkFunc
    };

    return directive;

    function linkFunc(scope, element, attrs, ngModel) {
      if ('type' in attrs && attrs.type.toLowerCase() === 'range') {
        ngModel.$parsers.push(parseFloat);
      }
    }
  }
})();
