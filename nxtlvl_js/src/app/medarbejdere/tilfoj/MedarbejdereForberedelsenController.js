(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('MedarbejdereForberedelsenController', MedarbejdereForberedelsenController);

  /** @ngInject */
  function MedarbejdereForberedelsenController(MedarbejdereService, $stateParams, ForberedelsenService, $localStorage) {
    var vm = this;
//    vm.users = MedarbejdereService.getUsers();
    vm.cellState = "name";
    vm.showText = true;
    vm.duties = ForberedelsenService.getDuties();
    vm.settings = {
      question: ""
    }



    console.log('$stateParams-> ',$stateParams, $localStorage);

    ForberedelsenService.getActiveDevPlan().then(
        function (result) {
          console.log("getActiveDevPlan->",result);
          //debugger
          return vm.activedevPlan = result.data;
        }
      ,function (error) {
          console.log('getActiveDevPlan - error:',error);
      });

    ForberedelsenService.getAllDevPlan().then(
        function (result) {
          console.log("getAllDevPlan->",result);
          //debugger
          return vm.allDevPlan = result.data;
        }
      ,function (error) {
          console.log('getAllDevPlan - error:',error);
      });

    ForberedelsenService.getDevPlanCreate().then(
        function (result) {
          console.log("getDevPlanCreate->",result);
          //debugger
          return vm.getDevPlanCreate = result.data;
        }
      ,function (error) {
          console.log('getDevPlanCreate - error:',error);
      });

    ForberedelsenService.getAllCompetence().then(
      function (result) {
        console.log("getAllCompetence->",result);
        //debugger
        return vm.getDevPlanCreate = result.data;
      }
    ,function (error) {
        console.log('getAllCompetence - error:',error);
    });

    ForberedelsenService.getAllEmployees().then(
      function (result) {
        console.log("getAllEmployees->",result);
        //debugger
        return vm.getDevPlanCreate = result.data;
      }
    ,function (error) {
        console.log('getAllEmployees - error:',error);
    });





    vm.checkActive = function(e, i) {
    	e.preventDefault();
      //  MedarbejdereService.checkComm(i.id);
        e.target.src = e.target.src +"?"+ window.Math.random();//"../images/check-animated-8.gif";
    }

    vm.checkComm = function (e, i) {
    	e.preventDefault();
   // 	MedarbejdereService.checkComm(i.id);
    }

    vm.clickedOrTouched = function () {
      vm.showText = false;
    };

    vm.activeInfo = function (e) {
       if (angular.element(e.target).closest('.accordion-item').hasClass('active')) {
          angular.element(e.target).closest('.accordion-item').removeClass("active")
       } else {
         angular.element(e.target).closest('.accordion-item').addClass('active')
       }
    // akardion
    // if ( angular.element(e.target).parent().parent().hasClass('active') ) { angular.element(e.target).parent().parent().removeClass("active") } 
    //   else {
    //     angular.element(e.target).parent().parent().parent().find('.accordion-item').removeClass("active");
    //     angular.element(e.target).parent().parent().hasClass('active') ? angular.element(e.target).parent().parent().removeClass("active") :  angular.element(e.target).parent().parent().addClass('active');
    //   }  
    }

    vm.clickAddQuestion = function (e) {
      angular.element(e.target).closest('.add_row').find('.ng-hide').toggleClass('ng-show ng-hide');
    }

    vm.btnCancel = function (e) {
      e.preventDefault();
      angular.element(e.target).closest('.add_row').find('.ng-show').toggleClass('ng-hide ng-show');
    }

    vm.btnOk = function (e) {
      e.preventDefault();
      angular.element(e.target).closest('.add_row').find('.ng-show').toggleClass('ng-hide ng-show');
    }

    vm.activeRow = function(e) {
      angular.element(e.target).closest('.input-row').addClass("active-row");
    }
    
    vm.noActiveRow = function (e) {
      if (angular.element(e)[0].target.value.length < 1) {
        angular.element(e.target).closest('.input-row').removeClass("active-row");
      }
    }

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

  }

})();