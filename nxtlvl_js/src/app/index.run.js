(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .run(runBlock);

  /** @ngInject */
  function runBlock($rootScope, $cookies, $document, $window, UserService, KeyCode, permissionService, currentUserService, $localStorage) {
    var user = UserService.getUser();
    

    $rootScope.$on("$stateChangeStart", permissionService.init);
//debugger
    currentUserService.saveUser($localStorage.users);


    if ($cookies.get('userType'))
      user.role = $cookies.get('userType');

    $document.bind('keyup', onKeyUp);

/*  angular.element($window).bind("mousewheel DOMMouseScroll", mousewheel);
    angular.element($window).bind("scroll", scroll);
    angular.element($document).on("touchend", ".btn-scroll-to", touchend);*/

    function touchend() {
      this.style.backgroundColor = '#0a4160';
    }

    function onKeyUp(e) {
      if ((angular.element('.preparation-holder').length) && (e.keyCode == KeyCode.keyEnter))
        angular.element('.btn-holder a').click();
/*      if ((angular.element('.preparation-section').length) && ((e.keyCode == KeyCode.keyUp) || (e.keyCode == KeyCode.keyDown))) {
        var active = +angular.element('.active').attr('id').match(/\d+/)[0];
        if (e.keyCode == KeyCode.keyUp) {
          if (active > 1)
            CatchScroll(--active)
        } else {
          if (active < angular.element('.preparation-item').length)
            CatchScroll(++active);
        }
      }*/
    }

    var timeCatch = null;
    var scrollCatch = null;
    var scrollTopStart = 0;
    var custome_scroll = true;

    function scroll(e) {
      if ('ontouchstart' in window || navigator.maxTouchPoints)
        if (document.activeElement.tagName == 'INPUT') {
          e.preventDefault();
          return;
        }
        document.activeElement.blur();
        clearTimeout(scrollCatch);
        scrollCatch = setTimeout(function () {
          custome_scroll ? mousewheel() : custome_scroll = true;
        }, 100);
    }


    function mousewheel(e) {
      if(window.outerWidth <= 1024) return;
      if ($('.preparation-item').length) {
        if ('ontouchstart' in window || navigator.maxTouchPoints)
          if (document.activeElement.tagName == 'INPUT') {
            e.preventDefault();
            return;
          }
        document.activeElement.blur();
        clearTimeout(timeCatch);
        timeCatch = setTimeout(function () { scrollMath(); }, 200);
      }
    }

    function scrollMath() {
      var mediana = window.pageYOffset + window.innerHeight / 2;
      var blocks = $('.preparation-item');
      var active = angular.element('.active').attr('id').match(/\d+/)[0];
      var new_active = 0;

      if (navigator.maxTouchPoints) {
        if (Math.abs(scrollTopStart) <= window.pageYOffset) {
          //down
          if (active == blocks.length)
            return;
          for (var i = active; i < blocks.length; i++) {
            var block = blocks[i];
            if (block.offsetTop <= window.pageYOffset + window.innerHeight * 0.3) {
              new_active = i;
              break;
            }
          }
        } else {
          //up
          if (active == 1)
            return;
          for (var i = 0; i < active; i++) {
            var block = blocks[i];
            if (block.offsetTop + block.clientHeight + 100 >= window.pageYOffset + window.innerHeight * 0.3) {
              new_active = i;
              break;
            }
          }
        }
      } else {
        if (Math.abs(scrollTopStart) <= window.pageYOffset) {
          //down
          if (active == blocks.length)
            return;
          for (var i = active; i < blocks.length; i++) {
            var block = blocks[i];
            if (block.offsetTop >= mediana - block.clientHeight / 2 && block.offsetTop <= mediana) {
              new_active = i;
              break;
            }
            if (block.offsetTop <= mediana + window.innerHeight * 0.15 && block.offsetTop >= mediana) {
              new_active = i;
              break;
            }
          }
        } else {
          //up
          if (active == 1)
            return;
          for (var i = 0; i < active; i++) {
            var block = blocks[i];
            if (block.offsetTop + block.clientHeight + 100 >= mediana + block.clientHeight / 2) {
              new_active = i;
              break;
            }
            if (block.offsetTop + block.clientHeight + 100 >= mediana - window.innerHeight * 0.15 && block.offsetTop + block.clientHeight + 100 >= window.pageYOffset) {
              new_active = i;
              break;
            }
          }
        }
      }

      if (!new_active)
        for (var i = 0; i < blocks.length; i++) {
          if (blocks[i].offsetTop < mediana && blocks[i].offsetTop + blocks[i].clientHeight + 100 > mediana) {
            new_active = i;
            break;
          }
        }

      scrollTopStart = window.pageYOffset;
      custome_scroll = true;
      if (active != ++new_active) CatchScroll(new_active);
    }

    function CatchScroll(new_active) {
      angular.element('.active').removeClass('active');
      angular.element('#scroll-' + new_active).addClass('active');
      var elem = angular.element('.active')[0];

      var offset = elem.offsetTop;
      if (offset > 0)
        offset = offset - (window.innerHeight - angular.element('#footer')[0].offsetHeight - elem.offsetHeight) / 2;
      if (offset > elem.offsetTop)
        offset = elem.offsetTop;
      $('html,body').animate({scrollTop: offset}, 275);
      if (new_active < $('.preparation-item').length)
        scrollTopStart = offset;
      custome_scroll = false;
    }
  }

})();
