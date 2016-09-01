(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('search', search);

  /** @ngInject */
  function search() {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/search.directive.html',
      link: linkFunc,
      replace: true,
      controller: searchController,
      controllerAs: 'vm'
    };

    return directive;

    /** @ngInject */
    function searchController($scope, ForberedelsenService, KeyCode) {
      var vm = this;

      vm.autocompliteShow = false;
      vm.autocomplits = ForberedelsenService.getAutocomplit();

      vm.autocompleteBlur = function () {
        vm.autocompliteShow = false;
      };

      vm.findDutie = function (e, newDutie) {
        e.keyCode == KeyCode.keyUp || e.keyCode == KeyCode.keyDown || e.keyCode == KeyCode.keyEnter ? switchAutocomplite(e) : vm.autocompliteShow = !!newDutie;
      };

      vm.addDutie = function (newDutie) {
        ForberedelsenService.addDutie(newDutie);
        vm.autocompliteShow = false;
        angular.element('#search').focus();
        angular.element('#search')[0].value = '';
        if ('forberedelsenCtrl' in $scope)
          $scope.forberedelsenCtrl.checkInfoChange();
      };

      vm.tabChoosen = function (e) {
        e.stopImmediatePropagation();
        switchAutocomplite(e);
      };

      vm.canselAnchor = function (e) {
        switch (e.keyCode) {
          case KeyCode.keyUp:
          case KeyCode.keyDown:
          case KeyCode.keyEnter:
            e.preventDefault();
        }
      };

      function switchAutocomplite(e) {
        if (!angular.element('#search').val()) return;

        e.stopImmediatePropagation();
        var list = $('.autocomplete-list li');
        var focus = document.activeElement;
        var index = list.index(focus);

        switch (e.keyCode) {
          case KeyCode.keyUp:
            var next = index - 1;
            switch (next) {
              case -2:
                angular.element(list[list.length - 1]).focus();
                break;
              case -1:
                angular.element('#search').focus();
                break;
              default:
                angular.element(list[next]).focus();
                break;
            }
            break;

          case KeyCode.keyDown:
            var next = index + 1;
            switch (next) {
              case list.length :
                angular.element('#search').focus();
                break;
              default:
                angular.element(list[next]).focus();
                break;
            }
            break;

          case KeyCode.keyEnter:
            if (focus.tagName == 'LI') vm.addDutie(angular.element(focus)[0].innerText);
            break;
        }
      }

    }

    function linkFunc(scope, element, attrs) {
      attrs.$observe('show', function () {
        scope.vm.autocompleteBlur();
      });
    }
  }
})();
