(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('IndsatsenController', IndsatsenController);

  /** @ngInject */
  function IndsatsenController(ForberedelsenService, InfoService, UserService) {
    var vm = this;

    vm.user = UserService.getUser();
    vm.editForm = false;
    
    vm.duties = ForberedelsenService.getDuties();
    vm.date = ForberedelsenService.getDate();
    vm.box1 = ForberedelsenService.reciveBox1();
    vm.box2 = ForberedelsenService.reciveBox2();
    vm.infos = InfoService.getInfo();

    vm.description = '';
    vm.title = '';

    var oldDuties;
    
    vm.removeDutie = function (index) {
      ForberedelsenService.removeDutie(index);
    };

    vm.submitData = function (e) {
      e.preventDefault();
    };

    vm.startEditForm = function () {
      vm.editForm = !vm.editForm;
      oldDuties = JSON.parse(JSON.stringify(vm.duties.duties));
    };

    vm.canselDuties = function () {
      vm.editForm = !vm.editForm;
      ForberedelsenService.overwriteDuties(oldDuties);
    };

    vm.slideDown = function (e) {
      var parent = angular.element(e.currentTarget).parents('.open-close');
      var slide = parent.find('.slide');
      if (parent.hasClass('opened')) {
        slide.slideDown();
      } else {
        slide.slideUp();
      }
    };

    vm.dropDown = function (e) {
      if (angular.element(e.target).closest('.select-task-select').find('.select-options').hasClass('ng-show')) {
        angular.element(e.target).closest('.select-task-select').find('.select-options').toggleClass('ng-show ng-hide')
      } else {
        angular.element(e.target).closest('.select-task-select').find('.select-options').toggleClass('ng-hide ng-show')
      }
      //angular.element(e.target).closest('.select-task-select').find('.ng-hide').toggleClass('ng-show ng-hide');
    }

    vm.submitInfo = function () {
      InfoService.submitInfo(vm.title, vm.description);
      vm.description = '';
      vm.title = '';
    };

    vm.addComm = function (e, index, newComm) {
      if (e.keyCode == '13') {
        InfoService.addComm(index, vm.user.name, newComm);
        e.currentTarget.value = '';
      }
    };

    vm.selectLevel = function (index, name, e) {
      ForberedelsenService.changeLevel(index, name);
      angular.element(e.target).closest('.select-task-select').find('.ng-show').toggleClass('ng-hide ng-show');
    };

    vm.selectComplaxity = function (index, name, e) {
      ForberedelsenService.selectComplaxity(index, name);
      angular.element(e.target).closest('.select-task-select').find('.ng-show').toggleClass('ng-hide ng-show');
    };

    vm.checkComm = function (e, i) {
      e.preventDefault();
      InfoService.checkComm(i);
    }

    vm.checkActive = function(e, i) {
      e.preventDefault();
        InfoService.checkComm(i);
        e.target.src = e.target.src +"?"+ window.Math.random();//"../images/check-animated-8.gif";
    }

  }

})();
