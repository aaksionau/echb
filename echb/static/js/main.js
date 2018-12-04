$(document).ready(function() {
  $(".js-menu__mobile").on("click", function() {
    $(".menu").toggleClass("menu--mobile");
    $(".menu__links").toggleClass("menu__links--mobile");
    $(".menu__item").toggleClass("menu__item--mobile");
    $(".menu__icon").toggleClass("fa-times");
    $(".menu__icon").toggleClass("menu__mobile-link--close");
    return false;
  });

  $(".js-dropdown__icon").on("click", function() {
    $(".dropdown__list").toggleClass("dropdown__list--active");
    $(".dropdown__icon").toggleClass("dropdown__icon--up");
    return false;
  });
});
function AddSubscriber() {
  $("#subscriberForm")
    .get(0)
    .submit();
}
