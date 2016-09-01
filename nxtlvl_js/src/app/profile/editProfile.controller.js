(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('EditProfileController', EditProfileController);

  /** @ngInject */
  function EditProfileController($stateParams, currentUserService, $localStorage, URL_SERV, MedarbejdereService) {
    var vm = this;
    // vm.phonePattern=/^[0-9]{6}$/
    vm.activeProfile = false;
    if ($stateParams.user) {
      $localStorage['editUser'] = $stateParams.user.id;
    }

    vm.potenciales = ["NO","YES"];
    vm.roles = ["Leader","User"];
    vm.is_manager = "";

    var id = $localStorage.editUser;
   // vm.user =  $stateParams.user;
    currentUserService.getCurrentUser(id).then(
                function (result) {
                  console.log("profile",result);

                  if (result.data.photo == "") {
                    vm.srcFile = "images/empty-img.jpg"
                  } else {
                    vm.srcFile = URL_SERV + result.data.photo + "?" + window.Math.random();
                  }
                  vm.is_manager = result.data.is_manager == true ? "Leader" : "User";
                  return vm.user = result.data;
                }
              ,function (error) {
                  console.log('error:',error);
              });
   // vm.currentUser = currentUserService.getCurrentUser();
   
    MedarbejdereService.getManagers().then(
                function (result) {
                  console.log("managers->", result);
                  return vm.managers = result.data.employee_managers;
                }
              ,function (error) {
                  vm.managers = [$localStorage.usersManager];
                  console.log('error:',error);
              });


    vm.currentUserRole =  $stateParams.currentUserRole; //admin
    vm.compareUser = false;
    var oldProfile;
   // vm.srcFile = "images/profile-photo-03.jpg" ;
    console.log('currentUserRole',vm.currentUserRole);


    vm.compareUsers = function () {

      if ( (currentUser.role == 'admin') && (currentUser.type == 'Classic A') ) {

      }
 
    	vm.compareUser = true
    }

    vm.profileSubmit = function () {
      vm.activeProfile = false;
      vm.editprofile = {
        company         :        vm.user.company.id,
        email           :        vm.user.email,
        is_manager      :        vm.user.is_manager == "Leader" ? true : false,
        manager         :        vm.user.manager.id,
        notes           :        vm.user.notes,
        phone           :        vm.user.phone,
        potenciale      :        vm.user.potenciale,
        roles           :        [],//vm.user.is_manager == "Leader" ? true : false,
        status_questions:        vm.user.status_questions,
        title           :        vm.user.title,
        first_name      :        vm.user.user.split(' ')[0], 
        last_name       :        vm.user.user.split(' ').splice(1).join(' '),
        language_code   :        "en",
        photo           :        "", 
        development_plan_type:   null,
        user            :        vm.user.id
      }

      //vm.user.user.split(' ')[0]
      //vm.user.user.split(' ').splice(1).join(' ')
      currentUserService.postEditProfile(vm.editprofile, id).then(
                function (result) {
                  //vm.user = result.data;
                  console.log(result);
                }
              ,function (error) {
                  console.log('error:',error);
              });

      vm.photoUser = {
        "photo": vm.srcFile.split(",")[1],
        "extension": "jpeg"
      }

      if (vm.photoUser.photo === undefined) {
        return;
      } else {
        currentUserService.postPhoto(id, vm.photoUser).then(
          function (result) {
            console.log("photo",result);
          }
        ,function (error) {
            console.log('error:',error);
        });
      }
    };

    vm.clickActiveProfile = function () {

      var inputs = [].slice.call(document.getElementsByTagName('input'));
      var textarea = [].slice.call(document.getElementsByTagName('textarea'));
      var div = [].slice.call(document.getElementsByTagName('div'));


      inputs.map(function (input) {
       checkArea(input);
      });


      textarea.map(function (textarea) {
        checkArea(textarea);
      });


      div.map(function (textarea) {
        checkArea(textarea);
      });

      !document.getElementsByClassName('input-error').length ? angular.element(document.getElementsByTagName('form')[0]).removeClass('form-error') : angular.element(document.getElementsByTagName('form')[0]).addClass('form-error');

      vm.activeProfile = true;

      var tempUser = Object.assign(vm.user, {is_manager: vm.user.is_manager == true ? "Leader" : "User"})
      oldProfile = JSON.parse(JSON.stringify(tempUser));

    };

    vm.dropDown = function (e) {
       if (angular.element(e.target).closest('.select-task-select').find('.select-options').hasClass('ng-show')) {
        angular.element(e.target).closest('.select-task-select').find('.select-options').toggleClass('ng-show ng-hide')
      } else {
        angular.element(e.target).closest('.select-task-select').find('.select-options').toggleClass('ng-hide ng-show')
      }
    }

    vm.selectRoles = function (e, role) {
      console.log("role",role);
      vm.user.is_manager = role;
    }

    vm.selectPotenciale = function (e, potenciale) {
      vm.user.potenciale = potenciale;
    }

    vm.canselChang = function () {
      vm.activeProfile = false;
      vm.user = JSON.parse(JSON.stringify(oldProfile));
      UserService.overwriteUser(oldProfile);
    };

    vm.validation = function (e) {

      checkArea(e.currentTarget, e);
      !document.getElementsByClassName('input-error').length ? angular.element(document.getElementsByTagName('form')[0]).removeClass('form-error') : angular.element(document.getElementsByTagName('form')[0]).addClass('form-error');
    };

    function checkArea(input, e) {
      
      var re = /\S+@\S+\.\S+/;
      var ph = /\(?([0-9]{3})\)?([ .-]?)([0-9]{3})([ .-]?)([0-9]{2})([ .-]?)([0-9]{2})/;
      // angular.element(input).hasClass('ng-empty')? angular.element(input).closest('.input-row').addClass('input-error') : angular.element(input).closest('.input-row').removeClass('input-error');
      if (input.id == 'email')
        !re.test(input.value) ? angular.element(input).closest('.input-row').addClass('input-error') : angular.element(input).closest('.input-row').removeClass('input-error');
      // if (input.id == 'phone')
      //   !ph.test(input.value) ? angular.element(input).closest('.input-row').addClass('input-error') : angular.element(input).closest('.input-row').removeClass('input-error');
      // if (input.value == "") return
      if (input.id == 'phone') {
        
      }

    }
  }

})();
