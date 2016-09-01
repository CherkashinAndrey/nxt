(function() {
  'use strict';

  angular
    .module('nxtlvl', ['ngCookies', 'restangular', 'ui.router', 'toastr']);

})();

(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('VelkommenController', VelkommenController);

  /** @ngInject */
  function VelkommenController() {
    //var vm = this;
  }

})();

(function () {
  'use strict';

  angular.module('nxtlvl').service('UserService', UserService);

  /** @ngInject */
  function UserService() {
    var user = {
      name: 'Jane Hahn',
      title: 'Partner/cand.comm. & BA scient.pol.',
      email: 'jane@nxtlvl.dk',
      mobile: '(+45) 12 34 56 78',
      company: 'NXT LVL',
      role: 'Leder',
      ownLeader: 'Navn Navnesen',
      type: 'Classic V1'
    };

    var service = {
      getUser: getUser,
      chooseRole: chooseRole
    };

    return service;

    function getUser() {
      return user;
    }

    function chooseRole(type) {
      user.role = type;
    }
  }

})();

(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .service('MedarbejdereService', MedarbejdereService);

  /** @ngInject */
  function MedarbejdereService() {
    var medarbejdere = [
      {
        model: true,
        name: 'Navn Navnsesen (Niv 1.)',
        type: 'Classic',
        guide: {
          link: 'udfyld',
          img: 'udfyld',
          complete: false,
          text: 'Ikke afsluttet'
        },
        leaders: {
          link: 'PDF',
          img: 'pdf',
          complete: false,
          text: 'Ikke afsluttet'
        },
        options: {
          text: 'Fjern',
          options: 'delete'
        },
        insert: {
          text: 'udfyld',
          complete: false
        },
        medarbejdere: [
          {
            model: false,
            name: 'Navn Navnsesen (Niv 2.)',
            type: 'Classic',
            guide: {
              link: '',
              img: 'eye',
              complete: true,
              text: 'Ikke afsluttet'
            },
            leaders: {
              complete: true,
              text: 'Ikke afsluttet'
            },
            options: {
              text: 'Fjern',
              options: 'delete'
            },
            insert: {
              text: 'udfyld',
              complete: true
            },
            medarbejdere: [
              {
                model: false,
                name: 'Navn Navnsesen (Niv 3.)',
                type: 'Classic',
                guide: {
                  link: 'PDF',
                  img: 'pdf',
                  complete: true,
                  text: 'Ikke afsluttet'
                },
                leaders: {
                  complete: false,
                  text: 'Ikke afsluttet'
                },
                options: {
                  text: 'Fjern',
                  options: 'delete'
                },
                insert: {
                  text: 'udfyld',
                  complete: true
                },
                medarbejdere: [

                ]
              }
            ]
          },
          {
            model: false,
            name: 'Navn Navnsesen (Niv 2.)',
            type: 'Classic',
            guide: {
              link: 'udfyld',
              img: 'udfyld',
              complete: false,
              text: 'Ikke afsluttet'
            },
            leaders: {
              link: 'PDF',
              img: 'pdf',
              complete: false,
              text: 'Ikke afsluttet'
            },
            options: {
              text: 'Fjern',
              options: 'delete'
            },
            insert: {
              text: 'udfyld',
              complete: false
            },
            medarbejdere: []
          }
        ]
      },
      {
        model: true,
        name: 'Navn Navnsesen (Niv 1.)',
        type: 'Classic',
        guide: {
          link: 'udfyld',
          img: 'udfyld',
          complete: true,
          text: 'Ikke afsluttet'
        },
        leaders: {
          complete: false,
          text: 'Ikke afsluttet'
        },
        options: {
          text: 'Fjern',
          options: 'delete'
        },
        insert: {
          text: 'udfyld',
          complete: false
        },
        medarbejdere: [
          {
            model: false,
            name: 'Navn Navnsesen (Niv 2.)',
            type: 'Classic',
            guide: {
              link: 'udfyld',
              img: 'udfyld',
              complete: true,
              text: 'Ikke afsluttet'
            },
            leaders: {
              complete: true,
              text: 'Ikke afsluttet'
            },
            options: {
              text: 'Fjern',
              options: 'delete'
            },
            insert: {
              text: 'udfyld',
              complete: false
            },
            medarbejdere: []
          }
        ]
      }
    ];

    var service = {
      getMedarbejdere: getMedarbejdere
    };

    return service;

    function getMedarbejdere() {
      return medarbejdere;
    }
  }

})();

(function () {
  'use strict';

  angular.module('nxtlvl').service('InfoService', InfoService);

  /** @ngInject */
  function InfoService() {
    var infos = [
      {
        title: 'Forbedre mine styrker som leder (indsatsområde titel)',
        info: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
        date: '24. februar 2016',
        comments: []
      },
      {
        title: 'Indføre bedre arbejds-rutiner i min dagligdag',
        info: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
        date: '23. februar 2016',
        comments: [
          {
            author: 'Navn Navnsen',
            text: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
            time: '11.22',
            date: '24.02.2016'
          },
          {
            author: 'Jane Hahn',
            text: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
            time: '11.22',
            date: '24.02.2016'
          },
          {
            author: 'Navn Navnsen',
            text: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
            time: '11.22',
            date: '24.02.2016'
          }
        ]
      },
      {
        title: 'Give bedre og mere feedback, både positivt og konstruktiv',
        info: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
        date: '22. februar 2016',
        comments: []
      }
    ];

    var service = {
      addComm: addComm,
      getInfo: getInfo,
      submitInfo: submitInfo
    };

    return service;

    function addComm(index, author, text) {
      return infos[index].comments.push({author: author, text: text, time: '11.22', date: '24.02.2016'});
    }

    function getInfo() {
      return infos;
    }

    function submitInfo(title, info) {
      return infos.push({title: title, info: info, date: '22. februar 2016', comments: []});
    }
  }

})();

(function () {
  'use strict';

  angular.module('nxtlvl').service('ForberedelsenService', ForberedelsenService);

  /** @ngInject */
  function ForberedelsenService() {
    var duties = [
      {
        name: 'Lorem ipsum dolor sit amet',
        level: 'Kendt',
        complexity: 'Middel'
      },
      {
        name: 'consectetuer adipiscing elit',
        level: 'Kendt',
        complexity: 'Let'

      },
      {
        name: 'Aenean commodo ligula eget dolor.',
        level: 'Nyt',
        complexity: 'Middel'

      },
      {
        name: 'Aenean massa.',
        level: 'Nyt',
        complexity: 'Let'

      },
      {
        name: 'Cum sociis natoque penatibus et magnis dis parturient montes,',
        level: 'Kendt',
        complexity: 'Svær'

      },
      {
        name: 'nascetur ridiculus mus.',
        level: 'Ukendt',
        complexity: 'Let'

      },
      {
        name: 'Donee quam felis,',
        level: 'Nyt',
        complexity: 'Middel'

      },
      {
        name: 'ultricies nec, pellentesque eu,',
        level: 'Kendt',
        complexity: 'Svær'
      }
    ];
    var autocomplits = ['Lorem', 'Lorem ipsum', 'Lorem ipsum dolor', 'Lorem ipsum dolor sit'];
    var date = ['24. februar 2016', '12. april 2015', '2. april 2015'];

    var service = {
      addDutie: addDutie,
      getDuties: getDuties,
      getDate: getDate,
      getAutocomplit: getAutocomplit,
      selectComplaxity: selectComplaxity,
      changeLevel: changeLevel,
      complexityChange: complexityChange,
      levelChange: levelChange,
      removeDutie: removeDutie
    };

    return service;

    function addDutie(newDutie) {
      duties.push({name: newDutie, level: '', complexity: ''});
    }

    function getDuties() {
      return duties;
    }

    function getDate() {
      return date;
    }

    function getAutocomplit() {
      return autocomplits;
    }

    function selectComplaxity(i, complaxity) {
      duties[i].complexity = complaxity;
    }

    function changeLevel(i, level) {
      duties[i].level = level;
    }

    function complexityChange(index, value) {
      duties[index].complexity = value;
    }

    function levelChange(index, value) {
      duties[index].level = value;
    }

    function removeDutie(index) {
      duties.splice(index, 1);
    }
  }

})();

(function () {
  'use strict';

  ProfileController.$inject = ["UserService"];
  angular
    .module('nxtlvl')
    .controller('ProfileController', ProfileController);

  /** @ngInject */
  function ProfileController(UserService) {
    var vm = this;

    vm.activeProfile = false;
    vm.user =  UserService.getUser();

    vm.profileSubmit = function () {
      vm.activeProfile = false;
      //UserService.changeProfile();
    }
  }

})();

(function () {
  'use strict';

  MedarbejdereController.$inject = ["MedarbejdereService"];
  angular
    .module('nxtlvl')
    .controller('MedarbejdereController', MedarbejdereController);

  /** @ngInject */
  function MedarbejdereController(MedarbejdereService) {
    var vm = this;

    vm.activeNavn = {};

    vm.chooseMedar = function (mas) {
      vm.activeNavn = vm.activeNavn != mas ? mas : {};
    };

    vm.medarbejdere = MedarbejdereService.getMedarbejdere();
  }

})();

(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController() {
    //var vm = this;
  }
})();

(function () {
  'use strict';

  IndsatsenController.$inject = ["ForberedelsenService", "InfoService", "UserService"];
  angular
    .module('nxtlvl')
    .controller('IndsatsenController', IndsatsenController);

  /** @ngInject */
  function IndsatsenController(ForberedelsenService, InfoService, UserService) {
    var vm = this;

    vm.user = UserService.getUser();

    vm.editForm = false;

    vm.duties = ForberedelsenService.getDuties();

    vm.autocomplits = ForberedelsenService.getAutocomplit();

    vm.date = ForberedelsenService.getDate();

    vm.autocompliteShow = false;

    vm.findDutie = function (newDutie) {
      vm.autocompliteShow = !!newDutie;
    };

    vm.addDutie = function (newDutie) {
      ForberedelsenService.addDutie(newDutie);
      vm.autocompliteShow = false;
    };

    vm.removeDutie = function (index) {
      ForberedelsenService.removeDutie(index);
    };

    vm.submitData = function (e) {
      e.preventDefault();
      //console.log('Form submit');
    }

    vm.infos = InfoService.getInfo();

    vm.slideDown = function (e) {
      var parent = angular.element(e.currentTarget).parents('.open-close');
      var slide = parent.find('.slide');
      if (parent.hasClass('opened')) {
        slide.slideDown();
      } else {
        slide.slideUp();
      }
    };

    vm.description = '';
    vm.title = '';

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

    vm.selectLevel = function (index, name) {
      ForberedelsenService.changeLevel(index, name);
    };

    vm.selectComplaxity = function (index, name) {
      ForberedelsenService.selectComplaxity(index, name);
    };
  }

})();

(function () {
  'use strict';

  ChooseUserController.$inject = ["$cookies", "UserService"];
  angular
    .module('nxtlvl')
    .controller('ChooseUserController', ChooseUserController);

  /** @ngInject */
  function ChooseUserController($cookies, UserService) {
    var vm = this;

    vm.ChooseUser = function (type) {
      $cookies.put('userType', type);
      UserService.chooseRole(type);
    };
  }

})();

(function () {
  'use strict';

  ForberedelsenStartController.$inject = ["$document", "ForberedelsenService"];
  angular
    .module('nxtlvl')
    .controller('ForberedelsenStartController', ForberedelsenStartController);

  /** @ngInject */
  function ForberedelsenStartController($document, ForberedelsenService) {
    var vm = this;

    vm.firstRange = '0';
    vm.secondRange = '0';

    vm.firstRangeChange = function () {
      //console.log(vm.firstRange);
    };

    vm.secondRangeChange = function () {
      //console.log(vm.secondRange);
    };

    vm.autocomplits = ForberedelsenService.getAutocomplit();

    vm.autocompliteShow = false;

    vm.duties = ForberedelsenService.getDuties();

    vm.addDutie = function (newDutie) {
      ForberedelsenService.addDutie(newDutie);
      vm.autocompliteShow = false;
    };

    vm.findDutie = function (newDutie) {
      vm.autocompliteShow = !!newDutie;
    };

    vm.removeDutie = function (index) {
      ForberedelsenService.removeDutie(index);
    };

    vm.complexityChange = function (index, event) {
      var radio = event.currentTarget.getAttribute('value');
      ForberedelsenService.complexityChange(index, radio);
    };

    vm.levelChange = function (index, event) {
      var radio = event.currentTarget.getAttribute('value');
      ForberedelsenService.levelChange(index, radio);
    };

    vm.btnUp = function() {
      var e = $.Event('keyup');
      e.keyCode = 38;
      $document.trigger(e);
    };

    vm.btnDown = function() {
      var e = $.Event('keyup');
      e.keyCode = 40;
      $document.trigger(e);
    };
  }

})();

(function () {
  'use strict';

  ForberedelsenController.$inject = ["$document"];
  angular
    .module('nxtlvl')
    .controller('ForberedelsenController', ForberedelsenController);

  /** @ngInject */
  function ForberedelsenController($document) {
    var vm = this;
  }
})();

(function() {
  'use strict';

  select.$inject = ["$window"];
  angular
    .module('nxtlvl')
    .directive('select', select);

  /** @ngInject */
  function select ($window) {
    var directive = {
      link: linkFun
    };

    return directive;

    function linkFun() {
      angular.element($window).bind('click', outsideClick);

      function outsideClick(e) {
        if (angular.element('.select-task-select').length) {
          var task = e.target;
          var show = false;

          if (angular.element(task).hasClass('center') || angular.element(task).hasClass('select-opener')) {
            var select = angular.element(task).parent().siblings('.select-options');
            if (angular.element(select[0]).hasClass('ng-show'))
              show = true;
          }

          var select_options = angular.element('.select-options');
          angular.element(select_options).each(function(){
            angular.element(this).removeClass('ng-show').addClass('ng-hide');
          });

          if (angular.element(task).hasClass('center') || angular.element(task).hasClass('select-opener')) {
            var select = angular.element(task).parent().siblings('.select-options');
            angular.element(select[0]).toggleClass('ng-hide ng-show');
            if (show) angular.element(select[0]).toggleClass('ng-hide ng-show');
          }
        }
      }
    }
  }
})();

(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('input', input);

  /** @ngInject */
  function input() {
    var directive = {
      restrict: 'E',
      require: '?ngModel',
      link: linkFunc
    };

    return directive;

    function linkFunc(scope, element, attrs, ngModel) {
      if ('type' in attrs && attrs.type.toLowerCase() === 'range') {
        ngModel.$parsers.push(parseFloat);
      }
    }
  }
})();

(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('headerNav', headerNav);

  /** @ngInject */
  function headerNav() {
    headerNavController.$inject = ["UserService"];
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/navigation.directive.html',
      replace:true,
      controller: headerNavController,
      controllerAs: 'vm',
      bindToController: true
    };

    return directive;

    /** @ngInject */
    function headerNavController(UserService) {
      var vm = this;
      vm.type = UserService.getUser().role;
    }
  }

})();

(function () {
  'use strict';

  angular.module('nxtlvl').directive('asideNav', asideNav);

  /** @ngInject */
  function asideNav() {
    asideNavController.$inject = ["UserService"];
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/aside-navigation.directive.html',
      replace:true,
      controller: asideNavController,
      controllerAs: 'vm'
    };

    return directive;

    /** @ngInject */
    function asideNavController(UserService) {
      var vm = this;
      vm.type = UserService.getUser().role;
    }
  }

})();

(function () {
  'use strict';

  runBlock.$inject = ["$cookies", "$document", "$window", "UserService"];
  angular
    .module('nxtlvl')
    .run(runBlock);

  /** @ngInject */
  function runBlock($cookies, $document, $window, UserService) {
    var user = UserService.getUser();
    if ($cookies.get('userType'))
      user.role = $cookies.get('userType');

    $document.bind('keyup', onKeyUp);

    angular.element($window).bind("mousewheel DOMMouseScroll", scroll);
/*    angular.element('.btn-scroll-to.down').bind("click", CatchScroll);
    angular.element('.btn-scroll-to.up').bind("click", CatchScroll);*/
  }

  function onKeyUp(e) {
    if ((angular.element('.preparation-holder').length)  && (e.keyCode == 13))
      angular.element('.btn-holder a').click();
    if ((angular.element('.preparation-section').length)  && ((e.keyCode == 38) || (e.keyCode == 40))) {
      e.keyCode == 38 ? CatchScroll(1) : CatchScroll(-1);
    }
  }



  var timeCatch = null;
  var scrollEvent = 0;

  function scroll(e) {
    if ($('.preparation-item').length) {
      e.preventDefault();

      clearTimeout(timeCatch);
      scrollEvent++;
      timeCatch = setTimeout(function () {
        var delta = e.originalEvent.wheelDelta || -e.originalEvent.detail;
        CatchScroll(delta); }, 200);
    }
  }

  function CatchScroll(delta) {
    var active = angular.element('.active').attr('id').match(/\d/)[0];
    var blocks = angular.element('.preparation-item');
    var elem = null;

    if (delta < 0) {
      //down
      if (active == blocks.length) {
        elem = angular.element('.active')[0];
      } else {
        angular.element('.active').removeClass('active');

        active = +active + ((~~(scrollEvent/10)) + 1);
        if (active > 7) active = 7;

        angular.element('#scroll-'+active).addClass('active');
        elem = angular.element('.active')[0];
      }
    } else {
      //up
      if (active == 1) {
        elem = document.getElementById('wrapper');
      } else {
        angular.element('.active').removeClass('active');

        active = +active - ((~~(scrollEvent/10)) + 1);
        if (active < 1)  {
          active = 1;
          angular.element('#scroll-'+active).addClass('active');
          elem = document.getElementById('wrapper');
        } else {
          angular.element('#scroll-'+active).addClass('active');
          elem = angular.element('.active')[0];
        }
      }
    }
    var offset = elem.offsetTop;
    if (offset > 0)
      offset = offset - (window.innerHeight - angular.element('#footer')[0].offsetHeight - elem.offsetHeight)/2;
    angular.element('html,body').animate({
      scrollTop: offset
    }, 100);

    scrollEvent = 0;
  }



})();

(function() {
  'use strict';

  routerConfig.$inject = ["$stateProvider", "$urlRouterProvider"];
  angular
    .module('nxtlvl')
    .config(routerConfig);

  /** @ngInject */
  function routerConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('/', {
        url: '/',
        templateUrl: 'app/choose/choose-user.html',
        controller: 'ChooseUserController',
        controllerAs: 'chooseCtrl'
      })
      .state('home', {
        url: '/home',
        templateUrl: 'app/main/main.html',
        controller: 'MainController',
        controllerAs: 'mainCtrl'
      })
      .state('home.velkommen', {
        url: '/velkommen',
        templateUrl: 'app/velkommen/velkommen.html'
      })
      .state('home.forberedelsen', {
        url: '/forberedelsen',
        templateUrl: 'app/forberedelsen/forberedelsen.html',
        controller: 'ForberedelsenController',
        controllerAs: 'forberedelsenFirstCtrl'
      })
      .state('home.forberedelsen-start', {
        url: '/forberedelsen-start',
        templateUrl: 'app/forberedelsen/forberedelsen.start.html',
        controller: 'ForberedelsenStartController',
        controllerAs: 'forberedelsenCtrl'
      })
      .state('home.samtalen', {
        url: '/samtalen',
        templateUrl: 'app/samtalen/samtalen.html'
      })
      .state('home.indsatsen', {
        url: '/indsatsen',
        templateUrl: 'app/indsatsen/indsatsen.html',
        controller: 'IndsatsenController',
        controllerAs: 'indsatsenCtrl'
      })
      .state('home.medarbejdere', {
        url: '/medarbejdere',
        templateUrl: 'app/medarbejdere/medarbejdere.html',
        controller: 'MedarbejdereController',
        controllerAs: 'medarbejdereCtrl'
      })
      .state('home.profile', {
        url: '/profile',
        templateUrl: 'app/profile/profile.html',
        controller: 'ProfileController',
        controllerAs: 'profileCtrl'
      });

    $urlRouterProvider.otherwise('/');
  }

})();

(function() {
  'use strict';

  config.$inject = ["$logProvider", "toastrConfig"];
  angular
    .module('nxtlvl')
    .config(config);

  /** @ngInject */
  function config($logProvider, toastrConfig) {
    // Enable log
    $logProvider.debugEnabled(true);

    // Set options third-party lib
    toastrConfig.allowHtml = true;
    toastrConfig.timeOut = 3000;
    toastrConfig.positionClass = 'toast-top-right';
    toastrConfig.preventDuplicates = true;
    toastrConfig.progressBar = true;
  }

})();

angular.module("nxtlvl").run(["$templateCache", function($templateCache) {$templateCache.put("app/choose/choose-user.html","<div class=\"admin-user\">\r\n  <a href=\"#/home/velkommen\" ng-click=\"chooseCtrl.ChooseUser(\'Leder\')\" class=\"btn-admin-user\">Leder</a>\r\n  <a href=\"#/home/velkommen\" ng-click=\"chooseCtrl.ChooseUser(\'Muligheder\')\" class=\"btn-admin-user\">Muligheder</a>\r\n</div>\r\n");
$templateCache.put("app/components/aside-navigation.directive.html","<div id=\"aside-nav\" ng-class=\"{\'open-nav\': vm.asideNavOpen}\">\r\n  <a class=\"nav-opener aside-nav-toggle\" ng-click=\"vm.asideNavOpen = true\"><span></span></a>\r\n  <div class=\"add-nav-box\">\r\n    <a class=\"nav-close aside-nav-toggle\" ng-click=\"vm.asideNavOpen = false\"></a>\r\n    <ul class=\"add-nav\" ng-click=\"vm.asideNavOpen = false\">\r\n      <li><a class=\"welcome\" ui-sref=\".velkommen\">Velkommen</a></li>\r\n      <li><a class=\"preparations\" ui-sref=\".forberedelsen\">Forberedelsen</a></li>\r\n      <li><a class=\"efforts\" ui-sref=\".indsatsen\">Indsatsen</a></li>\r\n      <li><a class=\"conversation\" ui-sref=\".samtalen\">Samtalen</a></li>\r\n      <li><a class=\"profile\" ui-sref=\".profile\">Profil</a></li>\r\n      <li><a class=\"settings\" ui-sref=\".medarbejdere\" ng-if=\"vm.type == \'Leder\'\">Indstillinger / Admin</a></li>\r\n    </ul>\r\n    <div class=\"bottom-box\">\r\n      <address>\r\n        <span class=\"title\">NXT LVL <i>by</i> Enso</span><br>\r\n        <span>Ehlersvej 11<br>2900 Hellerup</span>\r\n        <dl class=\"contacts\">\r\n          <dt>T:</dt>\r\n          <dd>70207845</dd>\r\n          <dt>E:</dt>\r\n          <dd><a href=\"mailto:&#105;&#114;&#102;&#111;&#064;&#101;&#110;&#115;&#111;&#099;&#111;&#110;&#115;&#117;&#108;:&#046;&#099;&#107;\">&#105;&#114;&#102;&#111;&#064;&#101;&#110;&#115;&#111;&#099;&#111;&#110;&#115;&#117;&#108;:&#046;&#099;&#107;</a></dd>\r\n        </dl>\r\n        <ul class=\"social-network\">\r\n          <li><a class=\"facebook\"><i class=\"icon-facebook\"></i></a></li>\r\n          <li><a><i class=\"icon-linkedin\"></i></a></li>\r\n        </ul>\r\n      </address>\r\n    </div>\r\n  </div>\r\n</div>\r\n");
$templateCache.put("app/components/navigation.directive.html","<nav class=\"nav\">\r\n  <ul id=\"nav\">\r\n    <li>\r\n      <a ui-sref=\".forberedelsen\">\r\n							<span class=\"ico-holder\">\r\n								<img class=\"main-img\" src=\"images/ico-01.png\" height=\"47\" width=\"34\" alt=\"image description\">\r\n								<img class=\"hover-img\" src=\"images/ico-01-hover.png\" height=\"47\" width=\"34\" alt=\"image description\">\r\n							</span>\r\n        Forberedelsen\r\n      </a>\r\n    </li>\r\n    <li>\r\n      <a ui-sref=\".samtalen\">\r\n							<span class=\"ico-holder\">\r\n								<img class=\"main-img\" src=\"images/ico-02.png\" height=\"44\" width=\"50\" alt=\"image description\">\r\n								<img class=\"hover-img\" src=\"images/ico-02-hover.png\" alt=\"image description\" width=\"50\" height=\"44\">\r\n							</span>\r\n        Samtalen\r\n      </a>\r\n    </li>\r\n    <li>\r\n      <a ui-sref=\".indsatsen\">\r\n							<span class=\"ico-holder\">\r\n								<img class=\"main-img\" src=\"images/ico-03.png\" height=\"33\" width=\"50\" alt=\"image description\">\r\n								<img class=\"hover-img\" src=\"images/ico-03-hover.png\" alt=\"image description\" width=\"50\" height=\"33\">\r\n							</span>\r\n        Indsatsen\r\n      </a>\r\n    </li>\r\n    <li ng-if=\"vm.type == \'Leder\'\">\r\n      <a ui-sref=\".medarbejdere\">\r\n							<span class=\"ico-holder\">\r\n								<img class=\"main-img\" src=\"images/ico-04.png\" height=\"33\" width=\"45\" alt=\"image description\">\r\n								<img class=\"hover-img\" src=\"images/ico-04-hover.png\" alt=\"image description\" width=\"45\" height=\"33\">\r\n							</span>\r\n        Medarbejdere\r\n      </a>\r\n    </li>\r\n  </ul>\r\n</nav>\r\n");
$templateCache.put("app/forberedelsen/forberedelsen.html","<main id=\"main\" role=\"main\">\r\n  <div class=\"preparation-holder\">\r\n    <img src=\"images/ico-05.jpg\" alt=\"image description\" class=\"heading-img\" width=\"30\" height=\"40\">\r\n    <h1>Forberedelsen</h1>\r\n    <div class=\"preparation-box\">\r\n      <p>Din forberedelse og engagement har stor indflydelse på, hvor stor effekt din MUS vi have for dig. Derfor skal du forud for samtalen gøre følgende:</p>\r\n      <ul class=\"text-box\">\r\n              <li>Afsætte mindst 2 timer uforstyrret til at udfylde forberedelsesguiden</li>\r\n              <li>Læse og reflektere over opgavenoglen og notere dine arbejdsopgaver</li>\r\n              <li>Læse og reflektere over kompetencenøglen og notere i forhold til spørgsmålene</li>\r\n              <li>Udfylde forberedelsesguiden til aftalt tid</li>\r\n              <li>Medbringe den udfyldte forberedelsesguide til samtalen</li>\r\n            </ul>\r\n      <p>Denne forberedelsesguide er ikke en deadlineopgave. Du kan forvente, at det tager noget tid, hvorfor vi foreslår, at du begynder en uge før. Dette er en forberedelse, som du gerne må gå frem og tilbage til.</p>\r\n      <p>Jo større indsatsen er under forberedelsen, desto større bliver udbyttet i sidste ende. Hvis du har spørgsmål eller er i tvivl om noget i forbindelse med forberedelsesguiden, kan du kontakte din leder, som er ansvarlig for din MUS for at få afklaret eventuelle spørgsmål.</p>\r\n    </div>\r\n    <div class=\"btn-holder\">\r\n      <a href=\"#/home/forberedelsen-start\" class=\"btn\">Start Forberedelsen</a>\r\n      <span class=\"info\">Tryk Enter</span>\r\n    </div>\r\n  </div>\r\n</main>\r\n");
$templateCache.put("app/forberedelsen/forberedelsen.start.html","<main id=\"main\" role=\"main\">\r\n  <div class=\"container\">\r\n    <div class=\"preparation-section\">\r\n      <div class=\"preparation-item active\" id=\"scroll-1\">\r\n        <div class=\"heading\">\r\n          <h2>Tilføj dine arbejdsopgaver</h2>\r\n          <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donee quam felis, ultricies nec, pellentesque eu, pretium quis, sem lorem ipsum dolor.</p>\r\n        </div>\r\n        <form class=\"search-form\">\r\n          <div class=\"search-input-row\">\r\n            <input type=\"text\" name=\"search\" id=\"search\" autocomplete=\"off\" placeholder=\"SØG OG/ELLER TILFØJ ARBEJDSOPGAVE\" ng-keyup=\"forberedelsenCtrl.findDutie(findDutie)\" ng-focus=\"forberedelsenCtrl.findDutie(findDutie)\" ng-model=\"findDutie\">\r\n          </div>\r\n          <div class=\"autocomplete-box\" ng-show=\"forberedelsenCtrl.autocompliteShow\">\r\n            <ul class=\"autocomplete-list\">\r\n              <li ng-repeat=\"autocomplite in forberedelsenCtrl.autocomplits | filter: findDutie\" ng-click=\"forberedelsenCtrl.addDutie(autocomplite)\">\r\n                {{autocomplite}}\r\n              </li>\r\n            </ul>\r\n          </div>\r\n        </form>\r\n        <ul class=\"striped-list\">\r\n          <li ng-repeat=\"dutie in forberedelsenCtrl.duties\">\r\n            <a class=\"delete-btn\" ng-click=\"forberedelsenCtrl.removeDutie($index)\">fjern</a>\r\n            {{dutie.name}}\r\n          </li>\r\n        </ul>\r\n      </div>\r\n      <div class=\"preparation-item\" id=\"scroll-2\">\r\n        <div class=\"heading\">\r\n          <h2>Hvor kendt er opgaven for dig?</h2>\r\n          <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. <b>Kendt</b>, <b>Nyt</b> eller <b>Ukendt</b></p>\r\n        </div>\r\n        <ul class=\"striped-list info-table\">\r\n          <li class=\"title-row\">\r\n            <div class=\"box\">\r\n              Arbejdsopgaver\r\n            </div>\r\n            <div class=\"box\">\r\n              <div class=\"item\">Kendt</div>\r\n              <div class=\"item\">Nyt</div>\r\n              <div class=\"item\">Ukendt</div>\r\n            </div>\r\n          </li>\r\n          <li ng-repeat=\"level in forberedelsenCtrl.duties\">\r\n            <div class=\"box\">\r\n              <a class=\"delete-btn\">fjern</a>\r\n              {{level.name}}\r\n            </div>\r\n            <div class=\"box\">\r\n              <div class=\"item\">\r\n                <span class=\"item-title\">Kendt</span>\r\n                <input class=\"custom-input\" type=\"radio\" name=\"radio-row-01-{{$index}}\" id=\"radio-01-{{$index}}\" value=\"Kendt\" ng-model=\"level.level\" ng-click=\"forberedelsenCtrl.levelChange($index, $event)\">\r\n                <label for=\"radio-01-{{$index}}\" class=\"fake-radio\"></label>\r\n              </div>\r\n              <div class=\"item\">\r\n                <span class=\"item-title\">Nyt</span>\r\n                <input class=\"custom-input\" type=\"radio\" name=\"radio-row-01-{{$index}}\" id=\"radio-02-{{$index}}\" value=\"Nyt\" ng-model=\"level.level\" ng-click=\"forberedelsenCtrl.levelChange($index, $event)\">\r\n                <label for=\"radio-02-{{$index}}\" class=\"fake-radio\"></label>\r\n              </div>\r\n              <div class=\"item\">\r\n                <span class=\"item-title\">Ukendt</span>\r\n                <input class=\"custom-input\" type=\"radio\" name=\"radio-row-01-{{$index}}\" id=\"radio-03-{{$index}}\" value=\"Ukendt\" ng-model=\"level.level\" ng-click=\"forberedelsenCtrl.levelChange($index, $event)\">\r\n                <label for=\"radio-03-{{$index}}\" class=\"fake-radio\"></label>\r\n              </div>\r\n            </div>\r\n          </li>\r\n        </ul>\r\n      </div>\r\n      <div class=\"preparation-item\" id=\"scroll-3\">\r\n        <div class=\"heading\">\r\n          <h2>Hvor svært tror du det bliver for dig at opfylde opgaven?</h2>\r\n          <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. <b>Svær</b>, <b>Middel</b> eller <b>Let</b></p>\r\n        </div>\r\n        <ul class=\"striped-list info-table\">\r\n          <li class=\"title-row\">\r\n            <div class=\"box\">\r\n              Arbejdsopgaver\r\n            </div>\r\n            <div class=\"box\">\r\n              <div class=\"item\">Svær</div>\r\n              <div class=\"item\">Middel</div>\r\n              <div class=\"item\">Let</div>\r\n            </div>\r\n          </li>\r\n          <li ng-repeat=\"complexity in forberedelsenCtrl.duties\">\r\n            <div class=\"box\">\r\n              <a class=\"delete-btn\">fjern</a>\r\n              {{complexity.name}}\r\n            </div>\r\n            <div class=\"box\">\r\n              <div class=\"item\">\r\n                <span class=\"item-title\">Svær</span>\r\n                <input class=\"custom-input\" type=\"radio\" name=\"radio-row-04-{{$index}}\" id=\"radio-04-{{$index}}\" value=\"Svær\" ng-model=\"complexity.complexity\" ng-click=\"forberedelsenCtrl.complexityChange($index, $event)\">\r\n                <label for=\"radio-04-{{$index}}\" class=\"fake-radio\"></label>\r\n              </div>\r\n              <div class=\"item\">\r\n                <span class=\"item-title\">Middel</span>\r\n                <input class=\"custom-input\" type=\"radio\" name=\"radio-row-05-{{$index}}\" id=\"radio-05-{{$index}}\" value=\"Middel\" ng-model=\"complexity.complexity\" ng-click=\"forberedelsenCtrl.complexityChange($index, $event)\">\r\n                <label for=\"radio-05-{{$index}}\" class=\"fake-radio\"></label>\r\n              </div>\r\n              <div class=\"item\">\r\n                <span class=\"item-title\">Let</span>\r\n                <input class=\"custom-input\" type=\"radio\" name=\"radio-row-06-{{$index}}\" id=\"radio-06-{{$index}}\" value=\"Let\" ng-model=\"complexity.complexity\" ng-click=\"forberedelsenCtrl.complexityChange($index, $event)\">\r\n                <label for=\"radio-06-{{$index}}\" class=\"fake-radio\"></label>\r\n              </div>\r\n            </div>\r\n          </li>\r\n        </ul>\r\n      </div>\r\n      <div class=\"preparation-item\" id=\"scroll-4\">\r\n        <div class=\"heading\">\r\n          <h2>Opsummering?</h2>\r\n          <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.</p>\r\n        </div>\r\n        <div class=\"summary-block\">\r\n          <div class=\"summary-row\">\r\n            <div class=\"item\">\r\n              <span class=\"left-text\">Høj</span>\r\n              <span class=\"new-text\" ng-repeat=\"dutie in forberedelsenCtrl.duties | filter: {level: \'Kendt\', complexity: \'Svær\'} : true\">\r\n                {{dutie.name}}\r\n              </span>\r\n            </div>\r\n            <div class=\"item\">\r\n              <span class=\"new-text\" ng-repeat=\"dutie in forberedelsenCtrl.duties | filter: {level: \'Kendt\', complexity: \'Middel\'} : true\">\r\n                {{dutie.name}}\r\n              </span>\r\n            </div>\r\n            <div class=\"item\">\r\n              <span class=\"new-text\" ng-repeat=\"dutie in forberedelsenCtrl.duties | filter: {level: \'Kendt\', complexity: \'Let\'} : true\">\r\n                {{dutie.name}}\r\n              </span>\r\n            </div>\r\n          </div>\r\n          <div class=\"summary-row\">\r\n            <div class=\"item\">\r\n              <span class=\"left-text\">Middel</span>\r\n              <span class=\"new-text\" ng-repeat=\"dutie in forberedelsenCtrl.duties | filter: {level: \'Nyt\', complexity: \'Svær\'} : true\">\r\n                {{dutie.name}}\r\n              </span>\r\n            </div>\r\n            <div class=\"item\">\r\n              <span class=\"new-text\" ng-repeat=\"dutie in forberedelsenCtrl.duties | filter: {level: \'Nyt\', complexity: \'Middel\'} : true\">\r\n                {{dutie.name}}\r\n              </span>\r\n            </div>\r\n            <div class=\"item\">\r\n              <span class=\"new-text\" ng-repeat=\"dutie in forberedelsenCtrl.duties | filter: {level: \'Nyt\', complexity: \'Let\'} : true\">\r\n                {{dutie.name}}\r\n              </span>\r\n            </div>\r\n          </div>\r\n          <div class=\"summary-row\">\r\n            <div class=\"item\">\r\n              <span class=\"left-text\">Lav</span>\r\n              <span class=\"bottom-text\">Lav</span>\r\n              <span class=\"new-text\" ng-repeat=\"dutie in forberedelsenCtrl.duties | filter: {level: \'Ukendt\', complexity: \'Svær\'} : true\">\r\n                {{dutie.name}}\r\n              </span>\r\n            </div>\r\n            <div class=\"item\">\r\n              <span class=\"bottom-text\">Middel</span>\r\n              <span class=\"new-text\" ng-repeat=\"dutie in forberedelsenCtrl.duties | filter: {level: \'Ukendt\', complexity: \'Middel\'} : true\">\r\n                {{dutie.name}}\r\n              </span>\r\n            </div>\r\n            <div class=\"item\">\r\n              <span class=\"bottom-text\">Høj</span>\r\n              <span class=\"new-text\" ng-repeat=\"dutie in forberedelsenCtrl.duties | filter: {level: \'Ukendt\', complexity: \'Let\'} : true\">\r\n                {{dutie.name}}\r\n              </span>\r\n            </div>\r\n          </div>\r\n          <div class=\"left-info\">Sværhedsgrad</div>\r\n          <div class=\"bottom-info\">Nyhedsværdi</div>\r\n        </div>\r\n        <div class=\"summary-view\">\r\n          <ul class=\"summary-list\">\r\n            <li>\r\n              <div class=\"title-row\">Svær</div>\r\n              <div class=\"value-row\">\r\n                <span class=\"col-value\">\r\n                  A: <span class=\"num\">{{(forberedelsenCtrl.duties | filter: {level: \'Kendt\', complexity: \'Svær\'} : true).length}}</span>\r\n                </span>\r\n                <span class=\"col-value\">\r\n                  B: <span class=\"num\">{{(forberedelsenCtrl.duties | filter: {level: \'Nyt\', complexity: \'Svær\'} : true).length}}</span>\r\n                </span>\r\n                <span class=\"col-value\">\r\n                  C: <span class=\"num\">{{(forberedelsenCtrl.duties | filter: {level: \'Ukendt\', complexity: \'Svær\'} : true).length}}</span>\r\n                </span>\r\n              </div>\r\n            </li>\r\n            <li>\r\n              <div class=\"title-row\">Middel</div>\r\n               <div class=\"value-row\">\r\n                <span class=\"col-value\">\r\n                  A: <span class=\"num\">{{(forberedelsenCtrl.duties | filter: {level: \'Kendt\', complexity: \'Middel\'} : true).length}}</span>\r\n                </span>\r\n                <span class=\"col-value\">\r\n                  B: <span class=\"num\">{{(forberedelsenCtrl.duties | filter: {level: \'Nyt\', complexity: \'Middel\'} : true).length}}</span>\r\n                </span>\r\n                <span class=\"col-value\">\r\n                  C: <span class=\"num\">{{(forberedelsenCtrl.duties | filter: {level: \'Ukendt\', complexity: \'Middel\'} : true).length}}</span>\r\n                </span>\r\n              </div>\r\n            </li>\r\n            <li>\r\n              <div class=\"title-row\">Let</div>\r\n               <div class=\"value-row\">\r\n                <span class=\"col-value\">\r\n                  A: <span class=\"num\">{{(forberedelsenCtrl.duties | filter: {level: \'Kendt\', complexity: \'Let\'} : true).length}}</span>\r\n                </span>\r\n                <span class=\"col-value\">\r\n                  B: <span class=\"num\">{{(forberedelsenCtrl.duties | filter: {level: \'Nyt\', complexity: \'Let\'} : true).length}}</span>\r\n                </span>\r\n                <span class=\"col-value\">\r\n                  C: <span class=\"num\">{{(forberedelsenCtrl.duties | filter: {level: \'Ukendt\', complexity: \'Let\'} : true).length}}</span>\r\n                </span>\r\n              </div>\r\n            </li>\r\n          </ul>\r\n        </div>\r\n      </div>\r\n      <div class=\"preparation-item\" id=\"scroll-5\">\r\n        <div class=\"heading\">\r\n          <h2>Iken grad er du tilfreds med din nuværende sammensætning af arbejdsopgaver?</h2>\r\n          <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.</p>\r\n        </div>\r\n        <div class=\"slider-block\">\r\n          <span class=\"left-value\"><i class=\"smile\"></i></span>\r\n          <span class=\"right-value\"><i class=\"smile sad\"></i></span>\r\n          <div class=\"slider-row\">\r\n            <div class=\"range-slider\">\r\n                <input class=\"range-inner-slider\" min=\"0\" max=\"100\" type=\"range\" ng-model=\"forberedelsenCtrl.firstRange\" ng-change=\"forberedelsenCtrl.firstRangeChange()\">\r\n            </div>\r\n          </div>\r\n        </div>\r\n      </div>\r\n      <div class=\"preparation-item\" id=\"scroll-6\">\r\n        <h2>Begrund dit svar</h2>\r\n        <div class=\"marked-block\">\r\n          <textarea name=\"\" id=\"\" cols=\"30\" rows=\"10\" placeholder=\"Begrund dit svar her...\"></textarea>\r\n        </div>\r\n      </div>\r\n      <div class=\"preparation-item\" id=\"scroll-7\">\r\n        <div class=\"heading\">\r\n          <h2>Lorem ipsum dolor sit amett</h2>\r\n          <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.</p>\r\n        </div>\r\n        <div class=\"slider-block\">\r\n          <span class=\"left-value\"><span class=\"text\">Lorem ipsum <br> dolor sed</span></span>\r\n          <span class=\"right-value\"><span class=\"text\">Lorem ipsum <br> dolor sed</span></span>\r\n          <div class=\"slider-row\">\r\n            <div class=\"range-slider\">\r\n              <input class=\"range-inner-slider\" value=\"72\" min=\"0\" max=\"100\" type=\"range\" ng-model=\"forberedelsenCtrl.secondRange\" ng-change=\"forberedelsenCtrl.secondRangeChange()\">\r\n            </div>\r\n          </div>\r\n        </div>\r\n      </div>\r\n    </div>\r\n  </div>\r\n</main>\r\n<footer id=\"footer\">\r\n  <span class=\"progress-info\"><span class=\"progress\">36% </span>udført</span>\r\n  <div class=\"footer-right\">\r\n    <ul class=\"move-buttons\">\r\n      <li><a class=\"btn-scroll-to down\" ng-click=\"forberedelsenCtrl.btnDown()\"></a></li>\r\n      <li><a class=\"btn-scroll-to up\" ng-click=\"forberedelsenCtrl.btnUp()\"></a></li>\r\n    </ul>\r\n    <span class=\"powered\">Powered by <a>NXT LVL</a></span>\r\n  </div>\r\n</footer>\r\n");
$templateCache.put("app/indsatsen/indsatsen.html","<main id=\"main\" role=\"main\">\r\n  <div class=\"container\">\r\n    <section class=\"effort-section\">\r\n      <div class=\"profile-head\">\r\n        <img src=\"images/profile-photo-01.jpg\" height=\"100\" width=\"100\" alt=\"image description\" class=\"profile-img\">\r\n        <h2>{{indsatsenCtrl.user.name}} <a href=\"#/home/profile\" class=\"icon-settings\"></a></h2>\r\n        <span class=\"profile-info\">{{indsatsenCtrl.user.title}} <br>Virksomhedsrådgiver & certificeret coach</span>\r\n      </div>\r\n      <div class=\"effort-item\">\r\n        <div class=\"heading\">\r\n          <h2>Mine arbejdsopgaver</h2>\r\n          <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean massa. <b>Kendt</b>, <b>Nyt</b> eller <b>Ukendt</b> og <b>Svær</b>, <b>Middel</b> eller <b>Let</b></p>\r\n        </div>\r\n        <form class=\"task-form\" ng-submit=\"indsatsenCtrl.submitData($event)\">\r\n          <ul class=\"striped-list info-table tasks-table\" ng-class=\"{\'active-edit\': indsatsenCtrl.editForm}\">\r\n            <li class=\"title-row\">\r\n              <div class=\"box\">\r\n                Arbejdsopgaver\r\n              </div>\r\n              <div class=\"box\">\r\n                <div class=\"item\">Nyhedsværdi</div>\r\n                <div class=\"item\">Sværhedsgrad</div>\r\n                <div class=\"item delete-item\">Fjern</div>\r\n              </div>\r\n            </li>\r\n            <li ng-repeat=\"dutie in indsatsenCtrl.duties\">\r\n              <div class=\"box\">\r\n                {{dutie.name}}\r\n              </div>\r\n              <div class=\"box\">\r\n                <div class=\"item\">\r\n                  <span class=\"name\">Nyhedsværdi:</span>\r\n                  <div class=\"value\">\r\n                    <span class=\"task-text\">{{dutie.level}}</span>\r\n                    <span class=\"select-task-select\">\r\n                      <span style=\"width: 75px\" class=\"task-select select-area\">\r\n                        <span class=\"left\"></span>\r\n                        <span class=\"center\">\r\n                          {{dutie.level}}\r\n                        </span>\r\n                        <a class=\"select-opener\"></a>\r\n                      </span>\r\n                      <div class=\"select-options drop-task-select drop-box ng-hide\">\r\n                        <div class=\"drop-holder\">\r\n                          <div class=\"drop-list\">\r\n                            <ul style=\"font-weight: 500\">\r\n                              <li rel=\"0\" class=\"\"><a ng-click=\"indsatsenCtrl.selectLevel($index,\'Ukendt\')\"><span>Ukendt</span></a></li>\r\n                              <li rel=\"1\" class=\"\"><a ng-click=\"indsatsenCtrl.selectLevel($index,\'Kendt\')\"><span>Kendt</span></a></li>\r\n                              <li rel=\"2\" class=\"\"><a ng-click=\"indsatsenCtrl.selectLevel($index,\'Nyt\')\"><span>Nyt</span></a></li>\r\n                            </ul>\r\n                          </div>\r\n                        </div>\r\n                      </div>\r\n                    </span>\r\n                  </div>\r\n                </div>\r\n                <div class=\"item\">\r\n                  <span class=\"name\">Sværhedsgrad:</span>\r\n                  <span class=\"task-text\">{{dutie.complexity}}</span>\r\n                  <span class=\"select-task-select\">\r\n                    <span style=\"width: 75px\" class=\"task-select select-area\">\r\n                      <span class=\"left\"></span>\r\n                      <span class=\"center\">\r\n                        {{dutie.complexity}}\r\n                      </span>\r\n                      <a class=\"select-opener\"></a>\r\n                    </span>\r\n                      <div class=\"select-options drop-task-select drop-box ng-hide\">\r\n                        <div class=\"drop-holder\">\r\n                          <div class=\"drop-list\">\r\n                            <ul style=\"font-weight: 500\">\r\n                              <li rel=\"0\" class=\"\"><a ng-click=\"indsatsenCtrl.selectComplaxity($index,\'Svær\')\"><span>Svær</span></a></li>\r\n                              <li rel=\"1\" class=\"\"><a ng-click=\"indsatsenCtrl.selectComplaxity($index,\'Middel\')\"><span>Middel</span></a></li>\r\n                              <li rel=\"2\" class=\"\"><a ng-click=\"indsatsenCtrl.selectComplaxity($index,\'Let\')\"><span>Let</span></a></li>\r\n                            </ul>\r\n                          </div>\r\n                        </div>\r\n                      </div>\r\n                    </span>\r\n                </div>\r\n                <div class=\"item delete-item\"><a class=\"delete-btn\" ng-click=\"indsatsenCtrl.removeDutie($index)\"></a></div>\r\n              </div>\r\n            </li>\r\n            <li class=\"edit-row\">\r\n              <a class=\"btn-open-edit btn-toggle-edit\" ng-click=\"indsatsenCtrl.editForm = !indsatsenCtrl.editForm\">\r\n                Tilføj / Fjern arbejdsopgaver\r\n              </a>\r\n              <div class=\"task-input-row\">\r\n                <input type=\"text\" name=\"task\" id=\"task\" autocomplete=\"off\" ng-keyup=\"indsatsenCtrl.findDutie(findDutie)\" ng-focus=\"indsatsenCtrl.findDutie(findDutie)\" ng-model=\"findDutie\">\r\n                <button type=\"submit\" ng-click=\"indsatsenCtrl.editForm = !indsatsenCtrl.editForm; indsatsenCtrl.autocompliteShow = false\"></button>\r\n              </div>\r\n		          <div class=\"autocomplete-box\" ng-show=\"indsatsenCtrl.autocompliteShow\">\r\n			          <ul class=\"autocomplete-list\">\r\n                  <li ng-repeat=\"autocomplite in indsatsenCtrl.autocomplits | filter: findDutie\" ng-click=\"indsatsenCtrl.addDutie(autocomplite)\">\r\n                      {{autocomplite}}\r\n                  </li>\r\n			          </ul>\r\n		          </div>\r\n            </li>\r\n          </ul>\r\n        </form>\r\n      </div>\r\n      <div class=\"effort-item\">\r\n        <div class=\"heading\">\r\n          <h2>Mine indsatsområder</h2>\r\n          <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean massa Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</p>\r\n        </div>\r\n        <ul class=\"priority-list\" ng-class=\"{\'active-add\': addInfo}\">\r\n          <li class=\"open-close\" ng-repeat=\"info in indsatsenCtrl.infos\" ng-init=\"openComm = \'false\'\" ng-class=\"{opened: openComm}\">\r\n            <div class=\"priority-holder\">\r\n              <span class=\"title\">{{info.title}}</span>\r\n              <div class=\"bottom-row\">\r\n                <ul class=\"info-list\" ng-click=\"openComm = !openComm; indsatsenCtrl.slideDown($event);\">\r\n                  <li><span class=\"more-info\">mere info</span></li>\r\n                  <li>kommentar (<span class=\"comment-count\">{{info.comments.length}}</span>)</li>\r\n                </ul>\r\n                <span class=\"date\">{{info.date}}</span>\r\n              </div>\r\n              <div class=\"slide\">\r\n                <div class=\"comments-block\">\r\n                  <div class=\"content\">\r\n                    <p>{{info.info}}</p>\r\n                  </div>\r\n                  <div class=\"comments-box\">\r\n                    <ul class=\"comments-list\">\r\n                      <li ng-repeat=\"comm in info.comments\">\r\n                        <div class=\"text-box\">\r\n                          <a class=\"author\">{{comm.author}}</a>\r\n                          <p>{{comm.text}}</p>\r\n                        </div>\r\n                        <ul class=\"date-list\">\r\n                          <li>\r\n                            <span class=\"time-box\">{{comm.time}}</span>\r\n                          </li>\r\n                          <li> <span class=\"date-box\">{{comm.date}}</span></li>\r\n                        </ul>\r\n                      </li>\r\n                    </ul>\r\n                    <form class=\"comment-form\">\r\n                      <textarea name=\"comment\" id=\"\" cols=\"30\" rows=\"1\" placeholder=\"Skriv en kommentar\" ng-model=\"newComm\" ng-keyup=\"indsatsenCtrl.addComm($event, $index, newComm)\"></textarea>\r\n                      <div class=\"input-file-box\">\r\n                        <input type=\"file\" name=\"file\" id=\"file\" class=\"custom\" style=\"opacity: 0\">\r\n                      </div>\r\n                    </form>\r\n                  </div>\r\n                </div>\r\n              </div>\r\n            </div>\r\n          </li>\r\n          <li>\r\n            <a class=\"btn-add-action open-action\" ng-click=\"addInfo = !addInfo\">Tilføj indsatsområde</a>\r\n            <form class=\"add-action-form\" ng-submit=\"indsatsenCtrl.submitInfo()\">\r\n              <fieldset>\r\n                <div class=\"input-row\">\r\n                  <label>overskrift</label>\r\n                  <textarea name=\"heading\" id=\"title\" cols=\"30\" rows=\"1\" class=\"heading-text\" ng-model=\"indsatsenCtrl.title\"></textarea>\r\n                </div>\r\n                <div class=\"input-row\">\r\n                  <label for=\"description\"></label>\r\n                  <textarea name=\"description\" id=\"description\" cols=\"30\" rows=\"5\" placeholder=\"Indsatsområde beskrivelse\" ng-model=\"indsatsenCtrl.description\"></textarea>\r\n                </div>\r\n                <div class=\"submit-row\">\r\n                  <input type=\"submit\" value=\"Tilføj indsatsområde\" class=\"btn\">\r\n                  <a class=\"open-action close\" ng-click=\"addInfo = !addInfo\">Fortryd</a>\r\n                </div>\r\n              </fieldset>\r\n            </form>\r\n          </li>\r\n        </ul>\r\n      </div>\r\n      <div class=\"effort-item\">\r\n        <div class=\"heading\">\r\n          <h2>Forberedelser</h2>\r\n          <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean massa Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</p>\r\n        </div>\r\n        <ul class=\"preparation-list\">\r\n          <li ng-repeat=\"date in indsatsenCtrl.date\">\r\n            <div class=\"preparation-frame\">\r\n              <ul class=\"btn-list\">\r\n                <li><a>vis</a></li>\r\n                <li><a>ret</a></li>\r\n              </ul>\r\n              <span class=\"text-box\">{{date}}</span>\r\n            </div>\r\n          </li>\r\n        </ul>\r\n      </div>\r\n    </section>\r\n  </div>\r\n</main>\r\n");
$templateCache.put("app/main/main.html","<div id=\"wrapper\" scroll select>\r\n  <header id=\"header\">\r\n    <div class=\"logo\"><a ui-sref=\".velkommen\"><img src=\"images/logo.png\" height=\"41\" width=\"124\" alt=\"NXT LVL\"></a></div>\r\n    <aside-nav></aside-nav>\r\n    <header-nav></header-nav>\r\n  </header>\r\n  <div ui-view></div>\r\n</div>\r\n");
$templateCache.put("app/medarbejdere/medarbejdere.html","<main id=\"main\" role=\"main\" class=\"admin-page\">\r\n  <section class=\"admin-section\">\r\n    <div class=\"control-panel\" ng-class=\"{\'active-control\': openPanel}\">\r\n      <div class=\"control-holder\">\r\n        <ul class=\"controls\">\r\n          <li><a class=\"add\">Tilføj<br> bruger(e)</a></li>\r\n          <li><a class=\"assign\">Tilknyt<br> guide</a></li>\r\n          <li><a class=\"create\">Opret<br> ledermodel</a></li>\r\n        </ul>\r\n        <form class=\"panel-search-form\">\r\n          <label for=\"search\">Søg</label>\r\n          <input type=\"search\" name=\"search\" id=\"search\" placeholder=\"...\">\r\n        </form>\r\n      </div>\r\n      <a class=\"open-panel-btn\" ng-click=\"openPanel = !openPanel\"></a>\r\n    </div>\r\n    <ul class=\"person-description model\" ng-if=\"medarbejdereCtrl.activeNavn.name\">\r\n      <li>\r\n        <span class=\"col value-col\"><a class=\"person-name\">{{medarbejdereCtrl.activeNavn.name}}</a></span>\r\n        <span class=\"col marc-col\"></span>\r\n        <span class=\"col action-col\"></span>\r\n      </li>\r\n      <li>\r\n        <span class=\"col value-col\">Type</span>\r\n        <span class=\"col marc-col\"></span>\r\n        <span class=\"col action-col\">{{medarbejdereCtrl.activeNavn.type}}</span>\r\n      </li>\r\n      <li>\r\n        <span class=\"col value-col\">Medarbejders (guide)</span>\r\n        <span class=\"col marc-col\">\r\n          <span class=\"status-mark\" ng-class=\"{complete: medarbejdereCtrl.activeNavn.guide.complete}\"></span>\r\n        </span>\r\n        <span class=\"col action-col\">\r\n          <a ng-class=\"{\'fill\': medarbejdereCtrl.activeNavn.guide.img == \'udfyld\', \'pdf\': medarbejdereCtrl.activeNavn.guide.img == \'pdf\', \'eye\': medarbejdereCtrl.activeNavn.guide.img == \'eye\'}\"></a>\r\n        </span>\r\n      </li>\r\n      <li>\r\n        <span class=\"col value-col\">Leders (guide)</span>\r\n        <span class=\"col marc-col\">\r\n          <span class=\"status-mark\" ng-class=\"{complete: medarbejdereCtrl.activeNavn.leaders.complete}\"></span>\r\n        </span>\r\n        <span class=\"col action-col\">\r\n          <a ng-class=\"{\'fill\': medarbejdereCtrl.activeNavn.leaders.img == \'udfyld\', \'pdf\': medarbejdereCtrl.activeNavn.leaders.img == \'pdf\', \'eye\': medarbejdereCtrl.activeNavn.leaders.img == \'eye\'}\"></a>\r\n        </span>\r\n      </li>\r\n      <li>\r\n        <span class=\"col value-col\">Muligheder</span>\r\n        <span class=\"col marc-col\"></span>\r\n        <span class=\"col action-col\">\r\n          <a class=\"icon-garbage\"></a>\r\n        </span>\r\n      </li>\r\n      <li>\r\n        <span class=\"col value-col\">Indsatsnøgle</span>\r\n        <span class=\"col marc-col\">\r\n          <span class=\"status-mark\" ng-class=\"{complete: medarbejdereCtrl.activeNavn.insert.complete}\"></span>\r\n        </span>\r\n        <span class=\"col action-col\">\r\n          <a class=\"icon-page\"></a>\r\n        </span>\r\n      </li>\r\n    </ul>\r\n    <div class=\"control-table\">\r\n      <div class=\"row-table heading-row\">\r\n        <div class=\"col name\">Navn</div>\r\n        <div class=\"col type\">Type</div>\r\n        <div class=\"col employee\"><span class=\"hidden\">Medarbejders (guide)</span> <span class=\"show-mob\">Medarb.</span></div>\r\n        <div class=\"col leader\"><span class=\"hidden\">Leders</span> <span class=\"show-mob\">Leder</span></div>\r\n        <div class=\"col options\">Muligheder (Guide)</div>\r\n        <div class=\"col insert\"><span class=\"hidden\">Indsatsnøgle</span> <span class=\"show-mob\">Indsats</span></div>\r\n      </div>\r\n      <div class=\"row\" ng-repeat=\"medar in medarbejdereCtrl.medarbejdere\" ng-class=\"{\'open\': openNavn, \'has-child\': medar.medarbejdere.length}\">\r\n        <div class=\"row-table\" ng-class=\"{\'model\': medar.model}\">\r\n          <div class=\"col name\">\r\n            <a ng-click=\"openNavn = !openNavn; medarbejdereCtrl.chooseMedar(medar)\">{{medar.name}}</a>\r\n          </div>\r\n          <div class=\"col type\">{{medar.type}}</div>\r\n          <div class=\"col employee\">\r\n            <a ng-class=\"{\'fill\': medar.guide.img == \'udfyld\', \'pdf\': medar.guide.img == \'pdf\', \'eye\': medar.guide.img == \'eye\'}\">{{medar.guide.link}}</a>\r\n            <span class=\"text\">{{medar.guide.text}}</span>\r\n            <span class=\"status-mark\" ng-class=\"{complete: medar.guide.complete}\"></span>\r\n          </div>\r\n          <div class=\"col leader\">\r\n            <a ng-class=\"{\'pdf\':  medar.leaders.img == \'pdf\'}\">{{medar.leaders.link}}</a>\r\n            <span class=\"text\">{{medar.leaders.text}}</span>\r\n            <span class=\"status-mark\" ng-class=\"{complete: medar.leaders.complete}\"></span>\r\n          </div>\r\n          <div class=\"col options\">\r\n            <a class=\"delete\">Fjern</a>\r\n          </div>\r\n          <div class=\"col insert\">\r\n            <a class=\"fill\">udfyld</a>\r\n            <span class=\"status-mark\" ng-class=\"{complete: medar.insert.complete}\"></span>\r\n          </div>\r\n        </div>\r\n        <div class=\"row\" ng-repeat=\"medar_2 in medar.medarbejdere\" ng-class=\"{\'open\': openNavn_2, \'has-child\': medar_2.medarbejdere.length}\">\r\n          <div class=\"row-table\" ng-class=\"{\'model\': medar_2.model}\">\r\n            <div class=\"col name\">\r\n              <a ng-click=\"openNavn_2 = !openNavn_2; medarbejdereCtrl.chooseMedar(medar_2)\">{{medar_2.name}}</a>\r\n            </div>\r\n            <div class=\"col type\">{{medar_2.type}}</div>\r\n            <div class=\"col employee\">\r\n              <a ng-class=\"{\'fill\': medar_2.guide.img == \'udfyld\', \'pdf\': medar_2.guide.img == \'pdf\', \'eye\': medar_2.guide.img == \'eye\'}\">{{medar_2.guide.link}}</a>\r\n              <span class=\"text\">{{medar_2.guide.text}}</span>\r\n              <span class=\"status-mark\" ng-class=\"{complete: medar_2.guide.complete}\"></span>\r\n            </div>\r\n            <div class=\"col leader\">\r\n              <a ng-class=\"{\'pdf\':  medar_2.leaders.img == \'pdf\'}\">{{medar_2.leaders.link}}</a>\r\n              <span class=\"text\">{{medar_2.leaders.text}}</span>\r\n              <span class=\"status-mark\" ng-class=\"{complete: medar_2.leaders.complete}\"></span>\r\n            </div>\r\n            <div class=\"col options\">\r\n              <a class=\"delete\">Fjern</a>\r\n            </div>\r\n            <div class=\"col insert\">\r\n              <a class=\"fill\">udfyld</a>\r\n              <span class=\"status-mark\" ng-class=\"{complete: medar_2.insert.complete}\"></span>\r\n            </div>\r\n          </div>\r\n          <div class=\"row\" ng-repeat=\"medar_3 in medar_2.medarbejdere\" ng-class=\"{\'open\': openNavn_3, \'has-child\': medar_3.medarbejdere.length}\">\r\n            <div class=\"row-table\" ng-class=\"{\'model\': medar_3.model}\">\r\n              <div class=\"col name\">\r\n                <a ng-click=\"openNavn_3 = !openNavn_3; medarbejdereCtrl.chooseMedar(medar_3)\">{{medar_3.name}}</a>\r\n              </div>\r\n              <div class=\"col type\">{{medar_3.type}}</div>\r\n              <div class=\"col employee\">\r\n                <a ng-class=\"{\'fill\': medar_3.guide.img == \'udfyld\', \'pdf\': medar_3.guide.img == \'pdf\', \'eye\': medar_3.guide.img == \'eye\'}\">{{medar_3.guide.link}}</a>\r\n                <span class=\"text\">{{medar_3.guide.text}}</span>\r\n                <span class=\"status-mark\" ng-class=\"{complete: medar_3.guide.complete}\"></span>\r\n              </div>\r\n              <div class=\"col leader\">\r\n                <a ng-class=\"{\'pdf\':  medar_3.leaders.img == \'pdf\'}\">{{medar_3.leaders.link}}</a>\r\n                <span class=\"text\">{{medar_3.leaders.text}}</span>\r\n                <span class=\"status-mark\" ng-class=\"{complete: medar_3.leaders.complete}\"></span>\r\n              </div>\r\n              <div class=\"col options\">\r\n                <a class=\"delete\">Fjern</a>\r\n              </div>\r\n              <div class=\"col insert\">\r\n                <a class=\"fill\">udfyld</a>\r\n                <span class=\"status-mark\" ng-class=\"{complete: medar_3.insert.complete}\"></span>\r\n              </div>\r\n            </div>\r\n          </div>\r\n        </div>\r\n      </div>\r\n    </div>\r\n  </section>\r\n</main>\r\n");
$templateCache.put("app/samtalen/samtalen.html","<main id=\"main\" role=\"main\" class=\"bg-style\">\r\n  <div class=\"container\">\r\n    <section class=\"article-section\">\r\n      <div class=\"heading\">\r\n        <h1>Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts</h1>\r\n        <p>Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.</p>\r\n      </div>\r\n      <p>Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life <a>One day however a small line of blind</a> text by the name of Lorem Ipsum decided to leave for the far World of Grammar. The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen. </p>\r\n      <blockquote>\r\n        <q>“She packed her seven versalia, put her initial into the belt and made herself on the way. When she reached the first hills of the Italic Mountains”</q>\r\n      </blockquote>\r\n      <p>she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then she continued her way. <a>On her way she met a copy.</a></p>\r\n      <img src=\"images/photo-01.jpg\" height=\"419\" width=\"692\" alt=\"image description\">\r\n      <span class=\"title-text\">The copy warned the Little Blind Text</span>\r\n      <p>that where it came from it would have been rewritten a thousand times and everything that was left from its origin would be the word \"and\" and the Little Blind Text should turn around and return to its own, safe country. But nothing the copy said could convince her and so it didn’t take long until a few insidious Copy Writers ambushed her, made her drunk with Longe and Parole and dragged her into their agency, where they abused her for their.</p>\r\n    </section>\r\n  </div>\r\n</main>\r\n");
$templateCache.put("app/profile/profile.html","<main id=\"main\" role=\"main\">\r\n  <div class=\"container\">\r\n    <section class=\"profile-section\" ng-class=\"{\'active-profile\': profileCtrl.activeProfile}\">\r\n      <div class=\"profile-img-box\">\r\n        <img src=\"images/profile-photo-01.jpg\" height=\"100\" width=\"100\" alt=\"image description\" class=\"profile-img\">\r\n        <a class=\"profile-settings-btn\"><i class=\"icon-settings\"></i></a>\r\n      </div>\r\n      <div class=\"profile-box\">\r\n        <form ng-submit=\"profileCtrl.profileSubmit()\" class=\"profile-form\">\r\n          <ul class=\"profile-list\">\r\n            <li class=\"input-holder\">\r\n              <div class=\"input-row\">\r\n                <label for=\"name\">Navn</label>\r\n                <span class=\"input-text name\">{{profileCtrl.user.name}}</span>\r\n                <input type=\"text\" name=\"name\" id=\"name\" placeholder=\"{{profileCtrl.user.name}}\" ng-model=\"profileCtrl.user.name\">\r\n              </div>\r\n            </li>\r\n            <li class=\"input-holder\">\r\n              <div class=\"input-row\">\r\n                <label for=\"name\">Titel</label>\r\n                <span class=\"input-text title\">{{profileCtrl.user.title}}</span>\r\n                <input type=\"text\" name=\"title\" id=\"title\" placeholder=\"{{profileCtrl.user.title}}\" ng-model=\"profileCtrl.user.title\">\r\n              </div>\r\n            </li>\r\n            <li class=\"input-holder\">\r\n              <div class=\"input-row\">\r\n                <label for=\"name\">E-mail</label>\r\n                <span class=\"input-text email\">{{profileCtrl.user.email}}</span>\r\n                <input type=\"email\" name=\"email\" id=\"email\" placeholder=\"{{profileCtrl.user.email}}\" ng-model=\"profileCtrl.user.email\">\r\n              </div>\r\n            </li>\r\n            <li class=\"input-holder\">\r\n              <div class=\"input-row\">\r\n                <label for=\"name\">Mobil</label>\r\n                <span class=\"input-text phone\">{{profileCtrl.user.mobile}}</span>\r\n                <input type=\"text\" name=\"phone\" id=\"phone\" placeholder=\"{{profileCtrl.user.mobile}}\" ng-model=\"profileCtrl.user.mobile\">\r\n              </div>\r\n            </li>\r\n            <li>\r\n              <span class=\"label\">Virksomhed</span>\r\n              <span class=\"descript\">NXT LVL</span>\r\n            </li>\r\n            <li>\r\n              <span class=\"label\">Rolle</span>\r\n              <span class=\"descript\">Leder</span>\r\n            </li>\r\n            <li>\r\n              <span class=\"label\">Nærmeste leder</span>\r\n              <span class=\"descript\">Navn Navnesen</span>\r\n            </li>\r\n            <li>\r\n              <span class=\"label\">Type</span>\r\n              <span class=\"descript\">Classic V1</span>\r\n            </li>\r\n            <li class=\"edit-row\">\r\n              <a class=\"edit-profile toggle-profile-btn\" ng-click=\"profileCtrl.activeProfile = !profileCtrl.activeProfile\">Rediger Profil</a>\r\n              <div class=\"btn-row\">\r\n                <input type=\"submit\" value=\"OK\" class=\"btn\">\r\n                <a class=\"btn toggle-profile-btn\" ng-click=\"profileCtrl.activeProfile = !profileCtrl.activeProfile\">Fortryd</a>\r\n              </div>\r\n            </li>\r\n          </ul>\r\n        </form>\r\n      </div>\r\n    </section>\r\n  </div>\r\n</main>\r\n");
$templateCache.put("app/velkommen/velkommen.html","<main id=\"main\" role=\"main\" class=\"bg-style\">\r\n  <div class=\"main-holder\">\r\n    <h1>Hej Jane</h1>\r\n    <p>Velkommen til din kommende medarbejderudviklingssamtale (MUS). Som navnet antyder, er det en samtale, hvor målet er at udvikle dig som medarbejder. For at MUS kan skabe værdi for såvel dig som virksomheden, er det afgørende at forberede dig forud for samtalen.</p>\r\n    <p>Før samtalen er det vigtigt, at både du og din leder tænker og reflekterer over en række spørgsmål. Under samtalen er det vigtigt, at I begge bidrager til en god dialog.</p>\r\n    <p>Til sidst i samtalen skal I opsummere og nedskrive de udviklingsområder, som I er blevet enige om.</p>\r\n  </div>\r\n</main>\r\n<nav class=\"bottom-nav\">\r\n	<ul id=\"bottom-nav\">\r\n		<li>\r\n			<a href=\"#/home/forberedelsen\">\r\n				<span class=\"ico-holder\">\r\n					<img class=\"main-img\" src=\"images/ico-01-mobile.png\" height=\"40\" width=\"30\" alt=\"image description\">\r\n					<img src=\"images/ico-01-mobile-hover.png\" height=\"40\" width=\"30\" alt=\"image description\" class=\"hover-img\">\r\n				</span>\r\n				Forberedelsen\r\n			</a>\r\n		</li>\r\n		<li>\r\n			<a href=\"#/home/samtalen\">\r\n				<span class=\"ico-holder\">\r\n					<img class=\"main-img\" src=\"images/ico-02-mobile.png\" height=\"35\" width=\"40\" alt=\"image description\">\r\n					<img src=\"images/ico-02-mobile-hover.png\" alt=\"image description\" class=\"hover-img\" width=\"40\" height=\"35\">\r\n				</span>\r\n				Samtalen\r\n			</a>\r\n		</li>\r\n		<li>\r\n			<a href=\"#/home/indsatsen\">\r\n				<span class=\"ico-holder\">\r\n					<img class=\"main-img\" src=\"images/ico-03-mobile.png\" height=\"26\" width=\"40\" alt=\"image description\">\r\n					<img src=\"images/ico-03-mobile-hover.png\" alt=\"image description\" class=\"hover-img\" width=\"40\" height=\"26\">\r\n				</span>\r\n				Indsatsen\r\n			</a>\r\n		</li>\r\n	</ul>\r\n</nav>\r\n");}]);