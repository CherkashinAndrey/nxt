(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('ForberedelsenStartController', ForberedelsenStartController);

  /** @ngInject */
  function ForberedelsenStartController(ForberedelsenService) {
    var vm = this;

    vm.autocomplits = ForberedelsenService.getAutocomplit();
    vm.duties = ForberedelsenService.getDuties();
    vm.box1 = ForberedelsenService.reciveBox1();
    vm.box2 = ForberedelsenService.reciveBox2();

    vm.showText = true;

    vm.removeDutie = function (index) {
      ForberedelsenService.removeDutie(index);
      vm.checkInfoChange();
    };

    vm.complexityChange = function (index, event) {
      var radio = event.currentTarget.getAttribute('value');
      ForberedelsenService.changeComplexity(index, radio);
      vm.checkInfoChange();
    };

    vm.levelChange = function (index, event) {
      var radio = event.currentTarget.getAttribute('value');
      ForberedelsenService.levelChange(index, radio);
      vm.checkInfoChange();
    };

    vm.textChange = function (e) {
      angular.element(e.target).hasClass('ng-empty') ? angular.element(e.target).closest('.preparation-box').addClass("input-error") : angular.element(e.target).closest('.preparation-box').removeClass("input-error");
      e.stopImmediatePropagation();
      vm.checkInfoChange();
    };

/*    vm.btnUp = function () {
      var e = $.Event('keyup');
      e.keyCode = KeyCode.keyUp;
      $document.trigger(e);
    };

    vm.btnDown = function () {
      var e = $.Event('keyup');
      e.keyCode = KeyCode.keyDown;
      $document.trigger(e);
    };*/

    vm.clickedOrTouched = function () {
      vm.showText = false;
    };

    vm.checkInfoChange = function () {
      vm.progress = 0;

      var middle = 100 / document.getElementsByClassName('validate').length;

      if (vm.duties.duties.length) {
        vm.progress = vm.progress + middle;
        var type = vm.duties.duties;
        vm.progress = vm.progress + middle;
        for (var i = 0; i < type.length; i++) {
          if (!type[i].level) {
            vm.progress =  vm.progress - middle;
            break;
          }
        }
        vm.progress =  vm.progress + middle;
        for (var i = 0; i < type.length; i++) {
          if (!type[i].complexity) {
            vm.progress =  vm.progress - middle;
            break;
          }
        }
      }

      /* For all textareas must be set their id */
      var textareas = [].slice.call(document.getElementsByTagName('textarea'));
      textareas.map(function (textarea) {
        var number = textarea.id;
        if (vm.duties[number]) vm.progress =  vm.progress + middle;
      });

      if ('range_1' in vm.duties) vm.progress = vm.progress + middle;
      if ('range_2' in vm.duties) vm.progress = vm.progress + middle;
      if ('range_3' in vm.duties) vm.progress = vm.progress + middle;
      if ('range_4' in vm.duties && 'range_5' in vm.duties && 'range_6' in vm.duties) vm.progress = vm.progress + middle;

      vm.progress = Math.round(vm.progress);

    };

    vm.checkInfoChange();
  }

})();
