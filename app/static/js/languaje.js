
var idiomaActual = "{{ session['language'] }}";

document.addEventListener('DOMContentLoaded', function() {
    var languageSelector = document.getElementById('language-selector');
    if (languageSelector) {
        languageSelector.addEventListener('change', function() {
            this.form.submit();
        });
    }
});