(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('MedarbejdereController', MedarbejdereController);

  /** @ngInject */
  function MedarbejdereController($scope, MedarbejdereService, translateService, $localStorage, URL_SERV) {
    var vm = this;

    vm.activeNavn = {};
    vm.newArrayUsers = [];
    vm.pageState = "list1";
    vm.cellState = "name";
    var oldcellState = "";
    vm.revers = true;
    var params ={};
    vm.undefinedUser = false;
    vm.translate = translateService.getTextTranslate();
    vm.groupeUser = [];
    vm.onePerson = [];
    vm.breadcrumbs = [];
    vm.showGroup = true;
    vm.focusSearchMark = true;
    vm.search = "";

  //  console.log('1111111111',vm.translate);

    vm.chooseMedar = function (mas) {
      vm.activeNavn = vm.activeNavn != mas ? mas : {};
    };

    vm.URL_SERV = URL_SERV;
//    vm.users = MedarbejdereService.getUsers();


    vm.id = $localStorage.users.employee_id;

   // debugger
    MedarbejdereService.getUsersGet(vm.id).then(
                function (result) {
                  console.log("JSON_Employee->",result);
                  //debugger
                  result.data.employees.map(function(el,i){
                    vm.newArrayUsers.push(Object.assign( {}, el, {showInfo:false, photo: el.photo ? el.photo + "?" + window.Math.random() : ""} ));
                  })
                  console.log('vm.undefinedUser',vm.undefinedUser);

                  if (vm.newArrayUsers.length <= 0) {
                    vm.undefinedUser = true;
                  }

                  console.log('vm.undefinedUser',vm.undefinedUser);
                  return vm.usersGet = result.data;
                }
                ,function (error) {
                    console.log('error:',error);
                });

  //  vm.medarbejdere = MedarbejdereService.getMedarbejdere();

    // vm.users.map(function(el,i){
    //   vm.newArrayUsers.push(Object.assign( {}, el, {showInfo:false} ));
    // })
    console.log("vm.undefinedUser",vm.undefinedUser);

    vm.openInfo = function(e, user) {
      //user.showInfo = true;
      e.preventDefault();
      MedarbejdereService.checkComm(user.id);
      e.target.src = e.target.src +"?"+ window.Math.random();
      $state.go('home.tilfotForberedelsen', { user: user } );
    }

    vm.return = function (user) {
      console.log('user!!!',user);
    }

    vm.dropDownUser = function (e, user) {
      console.log('e, user', e, user);
      $scope.$emit('breadcrumbsClick', e , user);

     // debugger
      //angular.element(e.target).closest('.parent_item').addClass('parent_active')   
      vm.onePerson = [user];
      vm.breadcrumbs.push(user);

    //  vm.groupeUser = MedarbejdereService.getNextGroupUser(user);
      MedarbejdereService.getUsersGet(user.id).then(
                function (result) {
                 // debugger
                  console.log("groupeUser->",result);
                  //debugger
                  // result.data.employees.map(function(el,i){
                  //   vm.newArrayUsers.push(Object.assign( {}, el, {showInfo:false} ));
                  // })

                  return vm.groupeUser = result.data.employees;
                }
              ,function (error) {
                  console.log('error:',error);
              });

      vm.showGroup = false;
      vm.search = "";

    }

    vm.closeInfo = function(user) {
      user.showInfo = false;
    }

    vm.focusSearch = function() {
      vm.focusSearchMark = false;
    }

    vm.noActiveSearch = function() {
      vm.focusSearchMark = true;
    }

    vm.changePageState = function(state) {
      vm.pageState = state;
    }

    vm.sendUserEdit = function(user) {
      console.log('dsfsdfsdfsdf',user);
     // $state.go('home.editProfile', { user: user });
    }

    vm.changeCellState = function(e, state) {
      if (vm.cellState == state){
        vm.revers = !vm.revers;
        oldcellState = state;
      }

      if (oldcellState != state) {
        vm.revers = true;
      }

      vm.cellState = state;

      angular.element(e.currentTarget).parent().find('.arrow').css({ transform : 'rotate(224deg)' , top: '-2px' })
      angular.element(e.currentTarget).children().children('.arrow').css({ transform : 'rotate(404deg)' , top: '2px' })

      if (vm.revers) {
        angular.element(e.currentTarget).parent().find('.arrow').css({ transform : 'rotate(224deg)' , top: '-2px' })
        angular.element(e.currentTarget).children().children('.arrow').css({ transform : 'rotate(224deg)' , top: '-1px' })
      }

    }

  }

})();
