(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('placeHolder', placeHolder);


  /** ngInject */
  function placeHolder($timeout) {
    var directive = {
      restrict: 'A',
      link: linkFunc
    };

    return directive;

    function linkFunc(scope, element, attrs) {
      var placeholder = '';

      element.on('focus', function (e) {
        placeholder = attrs.placeholder;
        element[0].placeholder = '';
        //$timeout(function(){autocompliteShow = !!angular.element('#search').val();}, 100);
      });

      element.on('blur', function (e) {
        element[0].placeholder = placeholder;
      });

    }
  }
})();
