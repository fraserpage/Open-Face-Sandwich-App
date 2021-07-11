document.addEventListener('DOMContentLoaded', () => {

    const mobileMenuBtn = document.getElementById('mobileMenuBtn'); 
    const mainMenu = document.getElementById('mainMenu');
    mobileMenuBtn.addEventListener('click', () => {
          if(mainMenu.classList.contains('showMenu')) {
            mainMenu.classList.remove('showMenu');
            mobileMenuButton.innerHTML = '&#9776; MENU';
        } else {
            mainMenu.classList.add('showMenu');
            mobileMenuButton.innerHTML = '&#9776; CLOSE';
        }
    })
  })


