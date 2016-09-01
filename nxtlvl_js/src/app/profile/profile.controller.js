(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('ProfileController', ProfileController);

  /** @ngInject */
  function ProfileController(UserService, currentUserService, $localStorage, URL_SERV, toastr) {
    var vm = this;
//employee_id      :            1
            // user_id 
    vm.id = $localStorage.users.employee_id;

    vm.activeProfile = false;
    currentUserService.getCurrentUser(vm.id).then(
                function (result) {
                  console.log("profile",result);
                  if (result.data.photo == "") {
                    vm.srcFile = "images/empty-img.jpg"
                  } else {
                    vm.srcFile = URL_SERV + result.data.photo;
                  }
                  vm.is_manager = result.data.is_manager == true ? "Leader" : "User";
                  return vm.user = result.data;
                }
              ,function (error) {
                  console.log('error:',error);
              });
    vm.activeRole = true;
    var oldProfile;

    vm.photoInfo;  /* {name: "profile-photo-02.jpg",
                       size: 3466, 
                       type: "image/jpeg"}*/

    vm.profileSubmit = function () {
      vm.activeProfile = false;
      var editprofile = {
        company         :        vm.user.company.id,
        email           :        vm.user.email,
        is_manager      :        vm.user.is_manager == "Leader" ? true : false,
        manager         :        vm.user.manager.id,
        notes           :        vm.user.notes,
        phone           :        vm.user.phone,
        potenciale      :        vm.user.potenciale,
        roles           :        [],//vm.user.is_manager,
        status_questions:        vm.user.status_questions,
        title           :        vm.user.title,
        first_name      :        vm.user.user.split(' ')[0], 
        last_name       :        vm.user.user.split(' ').splice(1).join(' '),
        language_code   :        "en",
        photo           :        " ", 
        development_plan_type:   null,
        user            :        vm.user.id
      }
      //vm.user.user.split(' ')[0]
      //vm.user.user.split(' ').splice(1).join(' ')
      currentUserService.postEditProfile(editprofile, vm.id)
       .then(
          function (result) {
            console.log('profileEdit',result);
            toastr.success(result.statusText);
            
          },
          function (error) {
            console.log("profileEditerror",error); 
            toastr.error('Error');
        });

      vm.photoUser = {
        "photo": vm.srcFile.split(",")[1],
        "extension": "jpeg"
      }

      if (vm.photoUser.photo) {
      currentUserService.postPhoto(vm.id, vm.photoUser).then(
        function (result) {
          console.log("photo",result);
        }
      ,function (error) {
          console.log('error:',error);
      })
      };
    };

    vm.clickActiveProfile = function () {
      //debugger
      var inputs = [].slice.call(document.getElementsByTagName('input'));
      var textarea = [].slice.call(document.getElementsByTagName('textarea'));



      inputs.map(function (input) {
       checkArea(input);
      });

      textarea.map(function (textarea) {
        checkArea(textarea);
      });

      !document.getElementsByClassName('input-error').length ? angular.element(document.getElementsByTagName('form')[0]).removeClass('form-error') : angular.element(document.getElementsByTagName('form')[0]).addClass('form-error');

      vm.activeProfile = true;
      var tempUser = Object.assign(vm.user, {is_manager: vm.user.is_manager == true ? "Leader" : "User"})
      oldProfile = JSON.parse(JSON.stringify(tempUser));
    };

    vm.canselChang = function () {
      vm.activeProfile = false;
      vm.user = JSON.parse(JSON.stringify(oldProfile));
      currentUserService.overwriteUser(oldProfile);
    };

    vm.validation = function (e) {
      checkArea(e.currentTarget);
      !document.getElementsByClassName('input-error').length ? angular.element(document.getElementsByTagName('form')[0]).removeClass('form-error') : angular.element(document.getElementsByTagName('form')[0]).addClass('form-error');
    };

    function checkArea(input) {
      
      var re = /\S+@\S+\.\S+/;
      var ph = /\(?([0-9]{3})\)?([ .-]?)([0-9]{3})([ .-]?)([0-9]{2})([ .-]?)([0-9]{2})/;
      angular.element(input).hasClass('ng-empty')? angular.element(input).closest('.input-row').addClass('input-error') : angular.element(input).closest('.input-row').removeClass('input-error');
      if (input.id == 'email')
        !re.test(input.value) ? angular.element(input).closest('.input-row').addClass('input-error') : angular.element(input).closest('.input-row').removeClass('input-error');
      if (input.id == 'phone')
        !ph.test(input.value) ? angular.element(input).closest('.input-row').addClass('input-error') : angular.element(input).closest('.input-row').removeClass('input-error');

    }
  }

})();
