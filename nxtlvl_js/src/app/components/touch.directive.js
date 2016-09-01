(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('onTouch', OnTouch);

  /** @ngInject */
  function OnTouch() {
    var directive = {
      restrict: 'A',
      link: linkFunc
    };

    return directive;

    /** @ngInject */
    function linkFunc(scope, elm, attrs) {
      var ontouchFn = scope.$eval(attrs.onTouch);


      elm.bind('touchstart', function (evt) {
        scope.$apply(function () {
          ontouchFn.call(scope, evt.which);
        });
      });

      elm.bind('touchend', function (evt) {
        scope.$apply(function () {
          scope.forberedelsenCtrl.showText = true;
          scope.forberedelsenCtrl.checkInfoChange();
          scope.MedarbejdereForberedelsenCtrl.showText = true;
          scope.MedarbejdereForberedelsenCtrl.checkInfoChange();

        });
      });

      elm.bind('mouseup', function (evt) {
        scope.$apply(function () {
                   console.log('mouseup',scope);
          if (scope.forberedelsenCtrl !== undefined) {
            scope.forberedelsenCtrl.showText = true;
            scope.forberedelsenCtrl.checkInfoChange();
          }

          if (scope.MedarbejdereForberedelsenCtrl !== undefined) {
            scope.MedarbejdereForberedelsenCtrl.showText = true;
            scope.MedarbejdereForberedelsenCtrl.checkInfoChange();
          }

        });
      });

      elm.bind('mousedown', function (evt) {
        scope.$apply(function () {
          ontouchFn.call(scope, evt.which);
        });
      });
    }

  };

})();
