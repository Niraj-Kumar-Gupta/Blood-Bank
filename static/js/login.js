function goContactPage()
{
    document.getElementById("personalPage").style.display="none";
    document.getElementById("accountPage").style.display="none";
    document.getElementById("contactPage").style.display="block";
}
function goAccountPage()
{
    document.getElementById("contactPage").style.display="none";
    document.getElementById("accountPage").style.display="block";
}
function goMedicalPage()
{
    document.getElementById("accountPage").style.display="none";
    document.getElementById("medicalPage").style.display="block";
}
function backLastPage(){
    document.getElementById("medicalPage").style.display="none";
    document.getElementById("accountPage").style.display="block";
    document.getElementById("contactPage").style.display="none";

}
function backFirstPage()
{
    document.getElementById("personalPage").style.display="block";
    document.getElementById("contactPage").style.display="none";
}
///
(function ($) {
    "use strict";
    /*==================================================================
    [ Validate after type ]*/
    $('.validate-input .input100').each(function(){
        $(this).on('blur', function(){
            if(validate(this) == false){
                showValidate(this);
            }
            else {
                $(this).parent().addClass('true-validate');
            }
        })    
    })
  
  
    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
           $(this).parent().removeClass('true-validate');
        });
    });

     function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');

        $(thisAlert).append('<span class="btn-hide-validate">&#xf135;</span>')
        $('.btn-hide-validate').each(function(){
            $(this).on('click',function(){
               hideValidate(this);
            });
        });
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
        $(thisAlert).find('.btn-hide-validate').remove();
    }
    

})(jQuery);



//// register page ////////////////

             const emailInput=document.querySelector('#email');
             const resultElement = document.getElementById('result');
             const nextButton = document.querySelector('#nxt');
             const nextButton1 = document.querySelector('#nxt1');
             const userInput=document.querySelector('#username');
             const userElement = document.getElementById('user-result');

            
             emailInput.addEventListener('input',()=>{

                const email = emailInput.value;
                // ---- fetch syntx ---
                // fetch( 'req', {res}.then(response => response.json()).then(data => {...}) )

                fetch('/check-email', {
                    method: 'POST',
                    body: new URLSearchParams({ email }),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if(data.exists) {
                        resultElement.textContent = 'Email already exists.';
                        resultElement.style.color = 'red';
                        nextButton.onclick = null;
                    } else {
                        resultElement.textContent = 'Good to go.';
                        resultElement.style.color = 'green';
                        nextButton.onclick = goAccountPage;
                       
                    }
                });
             });

             userInput.addEventListener('input',()=>{

                const username = userInput.value;

                fetch('/check-username',{
                    method:'POST',
                    body: new URLSearchParams({ username }),
                    headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                         }
                }).then(response => response.json()).then(data=>{
                    if(data.exists)
                    {
                        userElement.textContent = 'username already exists.';
                        userElement.style.color = 'red';
                        nextButton1.onclick = null;
                        
                    }
                    else{
                        userElement.textContent = 'Nice username.';
                        userElement.style.color = 'green';
                        nextButton1.onclick = goMedicalPage;
                        
                    }
                })
               
      

             });


               // Selecting the confirm password field
                const confirmPassField = document.querySelector('#confirm-pass');
                const PassField = document.querySelector('#pass');

                // Adding an event listener for the 'input' event
                confirmPassField.addEventListener('input', function() {
                    const pass1 = document.querySelector('#pass').value;
                    const pass2 = document.querySelector('#confirm-pass').value;
                    const passElement = document.getElementById('pass-result');
                    
                    if (pass1 !== pass2) {
                        passElement.textContent = 'Password and Confirm Password are not the same.';
                        passElement.style.color = 'red';
                        nextButton1.onclick = null;
                    } else {
                        passElement.textContent = 'Passwords match.';
                        passElement.style.color = 'green';
                        nextButton1.onclick = goMedicalPage;
                    }
                });

                PassField.addEventListener('input', function() {
                    const pass1 = document.querySelector('#pass').value;
                    const pass2 = document.querySelector('#confirm-pass').value;
                    const passElement = document.getElementById('pass-result');
                    
                    if (pass1 !== pass2) {
                        passElement.textContent = 'Password and Confirm Password are not the same.';
                        passElement.style.color = 'red';
                        nextButton1.onclick = null;
                    } else {
                        passElement.textContent = 'Passwords match.';
                        passElement.style.color = 'green';
                        nextButton1.onclick = goMedicalPage;
                    }
                });
 
             

