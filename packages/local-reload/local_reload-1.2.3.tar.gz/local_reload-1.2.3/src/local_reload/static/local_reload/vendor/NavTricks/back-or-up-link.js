/*
    back-or-up-link
    similar to back-or-up-button, but acts as "contextual breadcrumb" instead of a back button
    Users can include as many <a back-or-up-link></a> elements as they want in the page.
*/
addEventListener('load', function() {
    var placeholders = document.querySelectorAll('[back-or-up-link]');
    if (placeholders.length == 0) return

    function generate_links(href, title) {
        for (var i = 0; i < placeholders.length; i++) {
            placeholders[i].href = href;
            placeholders[i].innerText = title + ' >';
        }        
    }

    if (NavTricks.previousPageIsInternal()) {
        generate_links(NavTricks.previousPage.url, NavTricks.previousPage.title);
    }
    else NavTricks.withParentPage(function(page) {
        generate_links(page.path, page.title);
    });
});