

/*const numeroWhatsApp = "573143582372";
document.getElementById('form').addEventListener('submit', function(e) {
    e.preventDefault();
    const nombre = document.getElementById('name').value;
    const telefono = document.getElementById('phone').value;
    const correo = document.getElementById('email').value;
    const mensaje = document.getElementById('mensaje').value;

    const texto = `Hola, soy ${nombre}.\nMi número es: ${telefono}\nMi correo es: ${correo}\nMensaje: ${mensaje}`;
    const url = `https://wa.me/${numeroWhatsApp}?text=${encodeURIComponent(texto)}`;
    window.open(url, '_blank');
});
*/

window.addEventListener('scroll', function () {
  var header = document.querySelector('.header',);
  header.classList.toggle('abajo', window.scrollY > 0);
});

window.addEventListener('scroll', function () {
  var admin_header = document.querySelector('.admin_header',);
  admin_header.classList.toggle('abajo', window.scrollY > 0);
});

document.getElementById("btnMenu2").addEventListener("click",
  function () {

    let elemento = document.getElementById("navbar2");
    if (elemento.classList.contains("navbar2")) {
      elemento.classList.remove("navbar2");
      elemento.classList.add("no_navbar2");
    } else {
      elemento.classList.remove("no_navbar2");
      elemento.classList.add("navbar2");
    }

  });
  
document.addEventListener('click', function (e) {
  const menu = document.getElementById('navbar2');
  const btn  = document.getElementById('btnMenu2');
  if (!menu || !btn) return;

  const abierto       = menu.classList.contains('navbar2');
  const clickEnMenu   = menu.contains(e.target);
  const clickEnBoton  = btn.contains(e.target);  

  if (abierto && !clickEnMenu && !clickEnBoton) {
    menu.classList.remove('navbar2');
    menu.classList.add('no_navbar2');
  }
});

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    const menu = document.getElementById('navbar2');
    if (menu && menu.classList.contains('navbar2')) {
      menu.classList.remove('navbar2');
      menu.classList.add('no_navbar2');
    }
  }
});