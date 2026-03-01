(function () {
    var version = 0;
    var KEY = 'glissade-current';

    function poll() {
        fetch('/~version')
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (version && data.v !== version) {
                    sessionStorage.setItem(KEY, currentSlide);
                    location.reload();
                }
                version = data.v;
            })
            .catch(function () { });
        setTimeout(poll, 500);
    }

    poll();

    window.addEventListener('DOMContentLoaded', function () {
        var saved = sessionStorage.getItem(KEY);
        if (saved !== null) {
            sessionStorage.removeItem(KEY);
            var idx = parseInt(saved, 10);
            if (!isNaN(idx) && typeof showSlide === 'function') showSlide(idx);
        }
    });
})();
