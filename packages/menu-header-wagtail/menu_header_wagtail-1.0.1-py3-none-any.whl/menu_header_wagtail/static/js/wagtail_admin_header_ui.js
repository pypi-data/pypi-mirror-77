/**
 * dynamic field - JavaScript
 *
 * @link    https://joseflorez.co
 * @license For open source use: MIT
 * @author  Jose Florez https://joseflorez.co
 * @version 1.0.0
 *
 * See usage examples at https://joseflorez.co/
 */

// Initialize all event handlers on page load
document.addEventListener('DOMContentLoaded', function () {
    // Initialize select fields choice handler
    const choiceSelect = document.querySelector("select[name='logo_type']");
    if (choiceSelect) {
        addEventFile(choiceSelect);
        showHiddenSelect(choiceSelect);
    }
});

/**
 * Add event of field handler
 * @param target: field
 */
function addEventFile(target) {
    target.addEventListener('change', function (event) {
        showHiddenSelect(event.target);
    })
}

/**
 * Search field with pre j__ and show or hidden agree value of field element select
 * @param target: field element
 */
function showHiddenSelect(target) {
    let value = target.value;
    let img_l = document.querySelector('.object.model_choice_field .object-layout input[name="image_logo"]');
    let text_l = document.querySelector('.object.char_field input[name="text_logo"]');
    debugger;
    if(value === "text") {
        img_l.parentNode.parentNode.parentNode.parentNode.parentNode.classList.add('hidden');
        text_l.parentNode.parentNode.parentNode.parentNode.parentNode.classList.remove('hidden');
    } else {
        img_l.parentNode.parentNode.parentNode.parentNode.parentNode.classList.remove('hidden');
        text_l.parentNode.parentNode.parentNode.parentNode.parentNode.classList.add('hidden');
    }
}