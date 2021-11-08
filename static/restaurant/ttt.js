function signInCallback(authResult) {
            if (authResult['code']) {
                // Hide the sign-in button now that the user is authorized
                $('#signinButton').attr('style', 'dislay: none');
                $.ajax({
                    type: 'POST',
                    url: '/gconnect?state={% csrf_token %}',
                    processData: false,
                    contentType: 'application/octet-stream; charset=utf-8',
                    data: authResult(result) {
                        if (result) {
                            $('#result').html('Login Successful!</br>' + result +
                            '<br>Redirecting...')
                            setTimeout(function() {
                                window.location.href = "{% url 'restaurant:index' %}";
                            }, 4000);
                        } else if (authResult['error']) {
                            console.log('There was an error: ' + authResult['error']);
                        } else {
                            $('#result').html('Failed to make a server side call.
                            Check your configuration and console.');
                        }
                    }
                }
            }
        }
