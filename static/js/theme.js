/* MultiShop — Light / Dark tema keçidi
   Seçim localStorage-da "theme" açarı altında saxlanılır. */
(function () {
    var STORAGE_KEY = 'theme';
    var DARK_CLASS = 'dark-theme';

    function isDark() {
        return document.documentElement.classList.contains(DARK_CLASS);
    }

    function updateIcons(dark) {
        var icons = document.querySelectorAll('#themeToggle i, .btn-theme-toggle i');
        icons.forEach(function (icon) {
            icon.className = dark ? 'fas fa-sun text-warning' : 'fas fa-moon';
        });
    }

    window.toggleTheme = function () {
        var makeDark = !isDark();
        document.documentElement.classList.toggle(DARK_CLASS, makeDark);
        try {
            localStorage.setItem(STORAGE_KEY, makeDark ? 'dark' : 'light');
        } catch (e) {
            /* localStorage əlçatan deyilsə səssiz davam et */
        }
        updateIcons(makeDark);
    };

    function init() {
        var savedTheme = null;
        try {
            savedTheme = localStorage.getItem(STORAGE_KEY);
        } catch (e) { }

        var shouldBeDark = savedTheme === 'dark';
        if (shouldBeDark) {
            document.documentElement.classList.add(DARK_CLASS);
        }
        updateIcons(isDark());

        var btn = document.getElementById('themeToggle');
        if (btn && !btn._themeBound) {
            btn._themeBound = true;
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                window.toggleTheme();
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
