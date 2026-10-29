(function () {
    if (!window.frappe || !frappe.boot) {
        return;
    }

    // Keep Documentation visible for the Super Admin Role Profile.
    if (frappe.boot.anyadha_role_profile === "Super Admin") {
        return;
    }

    function removeDocumentationLinks() {
        document
            .querySelectorAll(".dropdown-menu a, .dropdown-menu button")
            .forEach(function (item) {
                if (
                    (item.textContent || "").trim() ===
                    __("Documentation")
                ) {
                    var container = item.closest("li") || item;
                    container.remove();
                }
            });
    }

    // Remove existing links and links added when menus open later.
    var observer = new MutationObserver(function () {
        removeDocumentationLinks();
    });

    function start() {
        removeDocumentationLinks();

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    if (document.body) {
        start();
    } else {
        document.addEventListener("DOMContentLoaded", start, {
            once: true
        });
    }
})();
