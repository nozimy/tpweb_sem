

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function senPost(url, data, error) {
    $.post(
        url,
        data,
        function(response) {
            if (!response.status) {
                var data = response.message;
                Object.keys(data).forEach(function (key) {
                    error.html(key + ': ' + data[key].toString());
                });
            } else {
                $(location).attr('href', response.message);
            }
      }
    ).fail(function(jqXHR, textStatus, err) {
          alert('text status ' + textStatus + ', err ' + err)
    });
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    }
});


jQuery(document).ready(function() {

  $('#logIn').on('submit', function (event) {

      event.preventDefault();
      var email = $('#email').val(),
          password = $('#password').val(),
          next = $(this).find('input[name=\'next\']').eq(0).val(),
          error = $('.errorLogin').eq(0);

      if (next === '') next = '/';

      senPost('/login/' ,
             { 'email': email, 'password': password, 'next': next },
                  error);
  });

  $('#signUp').on('submit', function (event) {

      event.preventDefault();
      var username = $('#username').val(),
          email = $('#email').val(),
          password1 = $('#password1').val(),
          password2 = $('#password2').val(),
          error = $('.errorSignup').eq(0);

      if (password1 !== password2) {
          error.html('Passwords doesn\'t match');
      } else {
          senPost('/signup/' ,
                 { 'username': username, 'email': email, 'password1': password1, 'password2': password2 },
                      error);
      }
  });

  $('#askForm').on('submit', function (event) {

      event.preventDefault();
      var title = $('#title').val(),
          text = $('#description').val(),
          tags = $('#tags').val(),
          error = $('.errorSignup').eq(0);

      senPost('/ask/' ,
             { 'title': title, 'text': text, 'tags': tags },
                  error);
  });

  $('#addAnswer').on('submit', function (event) {

      event.preventDefault();
      var text = $('#answer'),
          action = $(this).attr("action"),
          error = $('.errorAnswer').eq(0);

      $.post(
          action,
          {'text': text.val()},
          function(response) {
              if (!response.status) {
                  var data = response.message;
                  Object.keys(data).forEach(function (key) {
                        error.html(key + ': ' + data[key].toString());
                  });
              } else {
                  location.reload();
              }
          }
      ).fail(function(jqXHR, textStatus, err) {
          alert('text status ' + textStatus + ', err ' + err)
      });
  });

});