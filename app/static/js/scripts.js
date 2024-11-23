document.addEventListener('DOMContentLoaded', function () {
    var passwordField = document.querySelector('[name="password"]');
    var confirmPasswordField = document.querySelector('[name="confirm_password"]');
    var capsLockIndicator = document.getElementById('capsLockIndicator');

    // Function to check Caps Lock state
    function checkCapsLock(event) {
        if (event.getModifierState && event.getModifierState("CapsLock")) {
            capsLockIndicator.style.display = "block";  // Show Caps Lock indicator
        } else {
            capsLockIndicator.style.display = "none";  // Hide Caps Lock indicator
        }
    }

    // Check Caps Lock on keydown event for password fields
    if (passwordField) {
        passwordField.addEventListener('keydown', checkCapsLock);
    }
    if (confirmPasswordField) {
        confirmPasswordField.addEventListener('keydown', checkCapsLock);
    }

    // Optional: Hide the indicator when user clicks outside the password fields
    passwordField.addEventListener('blur', function() {
        capsLockIndicator.style.display = "none";
    });

    confirmPasswordField.addEventListener('blur', function() {
        capsLockIndicator.style.display = "none";
    });
});
