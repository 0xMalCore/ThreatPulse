document.addEventListener("DOMContentLoaded", function () {

    // ================= LOGIN MODAL =================
    const loginBtn = document.getElementById("loginNav");
    const loginBox = document.getElementById("loginBox");

    if (loginBtn && loginBox) {

        loginBtn.addEventListener("click", function (e) {
            e.preventDefault();
            loginBox.classList.toggle("show-modal");
        });

        document.addEventListener("click", function (e) {
            if (!loginBox.contains(e.target) && e.target !== loginBtn) {
                loginBox.classList.remove("show-modal");
            }
        });
    }

    // ================= GLOBAL SMOOTH SCROLL =================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            const targetId = this.getAttribute("href");

            // Ignore empty #
            if (targetId.length > 1) {

                e.preventDefault();

                const target = document.querySelector(targetId);

                if (target) {
                    target.scrollIntoView({
                        behavior: "smooth"
                    });

                    // Adjust for fixed navbar height
                    setTimeout(() => {
                        window.scrollBy(0, -70);
                    }, 400);
                }
            }
        });
    });

});