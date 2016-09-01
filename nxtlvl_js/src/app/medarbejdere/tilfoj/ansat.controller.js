(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('MedarbejdereAnsatController', MedarbejdereAnsatController);

  /** @ngInject */
  function MedarbejdereAnsatController(MedarbejdereService, $localStorage, currentUserService, URL_SERV) {
    var vm = this;
    vm.manager = [];
    vm.pageState = "list1";
    vm.fileName = "No file selected";
    vm.invalidForm = false;
    vm.loadState = 0;   // 0 -choosen file, 1 - file loding ; 2 file loaded; 3 - error;
    vm.dropDownCheck = false;
    var idUser = $localStorage.users.employee_id;
    vm.idCompany;
    vm.file;

    MedarbejdereService.getManagers().then(
                function (result) {
                  console.log("managers->", result);
                  if (!Array.isArray(result.data.employee_managers)) {
                      debugger
                      vm.managers = [result.data.employee_managers];
                  }
                  if (Array.isArray(result.data.employee_managers)) {
                      vm.managers = result.data.employee_managers;
                  }

                }
              ,function (error) {
               //debugger
                  // var managerId = Object.assign($localStorage.usersManager, {id: $localStorage.users.employee_id });
                  // vm.managers = [$localStorage.usersManager];
                  console.log('error:',error);
              });

    currentUserService.getCurrentUser(idUser).then(
            function (result) {
              return vm.idCompany = result.data.company.id;
            }
          ,function (error) {
              console.log('error:',error);
          });



   

    vm.emailPattern = '\\w+.?\\w+@[a-zA-Z_]+?\\.[a-zA-Z]{2,6}';
    vm.userList = {
      id: window.Math.random() + window.Math.random(),
      lastName: "",
      manager:'',
      name: '',
      title: '',
      email: '',
      mobile: '',
      company: '',
      role: '',
      ownLeader: '',
      type: '',
      firstDate: '',
      middleDate: '',
      lastDate: '',
      statusAnsat: 'offline',
      statusIndsats: 'offline',
      statusLeder: 'offline',
      potencial: '',
      note: '',
      isManager: '',
      checkComm: false,
    };

    vm.userList1 = {
      first_name: "",
      last_name:'',
      title: '',
      email: '',
      is_manager: '',
      manager:'',
      language_code: 'en',

      status_questions: "STATUS_SHOW",
      roles: [],
      notes: "2016-08-12T11:53:21.666Z",
      date_start: "2016-08-12T11:53:21.666Z",
      date_finish: "2016-08-12T11:53:21.666Z",
      date_of_birth: null,
      username: window.Math.random()+window.Math.random() + "",
      user: "1",
      company: "1",
      potenciale: "YES",
      phone: ""
    };

    vm.activeManager = "";
    vm.is_manager = ""
    // vm.managers = [{ name: "1"},
    //               { name: "Ivan"},
    //               { name: "Tatyana"}];

    // vm.roles = [{role : "Manager"},
    //             {role : "User"}];
    vm.roles = ["Leader","User"];

    vm.changePageState = function(state) {
        vm.pageState = state;
        // angular.element(e.target).parent().parent().parent().find('.delHover').find('.delHover').css({'background' : '#0a4160'});
    }

    vm.activeRow = function(e) {
      angular.element(e.target).closest('.input-row').addClass("active-row");
    }

    vm.userFormAdd = function () {
      console.log('userFormAdd');
    }

    // vm.btnOk = function (e) {
    //   e.preventDefault();
    //   console.log('vm.activeManager->',vm.activeManager);
    //   if ((vm.userList.lastName.length > 1) ) {
    //     MedarbejdereService.addUser(vm.userList);
    //   }
    // }

    vm.submit = function (valid, e) {
      e.preventDefault();
      if ( valid ) {
        vm.invalidForm = true;
        return;
      }

      vm.invalidForm = false;
      console.log('addUser', vm.userList);
      //MedarbejdereService.addUser(vm.userList);
      var dom =  angular.element(e.target).find('.error');
      MedarbejdereService.postAddUser(vm.userList1, dom);
    }

    vm.isInvalid = function(element) {
      return element.$invalid && element.$dirty || element.$invalid && vm.invalidForm
    }

    vm.btnOkCancel = function (e) {
      e.preventDefault();
    }

    vm.selectItem = function (e, manager) {
      angular.element(e.target).closest('.input-row').addClass("active-row");
    //  debugger
      vm.userList1.manager = manager.id;
     // vm.dropDownCheck = false;
      vm.activeManager = manager.last_name+ " " + manager.first_name
      angular.element(e.target).closest('.select-task-select').find('.ng-show').toggleClass('ng-hide ng-show');
    }

    vm.selectRole = function (e, isManager) {
      angular.element(e.target).closest('.input-row').addClass("active-row");
      vm.is_manager = isManager;
      vm.userList1.is_manager = true ? isManager == "Leader" : false ;
      angular.element(e.target).closest('.select-task-select').find('.ng-show').toggleClass('ng-hide ng-show');
    }

    vm.dropDown = function (e) {
      if (angular.element(e.target).closest('.select-task-select').find('.select-options').hasClass('ng-show')) {
        angular.element(e.target).closest('.select-task-select').find('.select-options').toggleClass('ng-show ng-hide')
      } else {
        angular.element(e.target).closest('.select-task-select').find('.select-options').toggleClass('ng-hide ng-show')
      }

      //vm.dropDownCheck = !vm.dropDownCheck;
     // angular.element(e.target).closest('.select-task-select').find('.ng-hide').toggleClass('ng-show ng-hide');
    }

    vm.noActiveRow = function (e) {
      if (angular.element(e)[0].target.value.length < 1) {
        angular.element(e.target).closest('.input-row').removeClass("active-row");
      }
    }

    vm.btnFileOk =function (e, form) {
      e.preventDefault();
    // angular.element(e.target).css({'background' : '#0a4160'})
     // #0a4160
     //debugger
      var file = {
        "employee_file": vm.file.split(',')[1]
      }
     
      // angular.element(e.target).parent().parent().find('.field-box').addClass('loading');

      // angular.element(e.target).hasClass('ng-empty') ? angular.element(e.target).closest('.preparation-box').addClass("input-error") : angular.element(e.target).closest('.preparation-box').removeClass("input-error");
      MedarbejdereService.addUsersFile(file , vm.idCompany, angular.element(e.target).parent().parent().find('.field-box'));


    }

    vm.btnFileDel = function (e, form) {
    // debugger
      angular.element(e.target).parent().parent().removeClass('loaded');
      form.file.$viewValue = "";
      vm.fileName = "No file selected";
    // angular.element(e.target).parent().parent().removeClass('loaded');
    // debugger;
    }

  }

})();