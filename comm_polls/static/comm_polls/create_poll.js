document.addEventListener('DOMContentLoaded', () => {
    const addChoiceBtn = document.getElementById('add-choice-form');
    const formList = document.getElementById('choice-form-list');
    const formTemplate = document.getElementById('choice-form-template');
    const totalFormsInput = document.querySelector('input[name$="TOTAL_FORMS"]');
    const mainForm = document.querySelector('form');

    if (!addChoiceBtn) return; // Exit if not on the create poll page

    const updateRemoveButtons = () => {
        const forms = formList.querySelectorAll('.choice-form');
        const minForms = parseInt(document.querySelector('input[name$="MIN_NUM_FORMS"]').value) || 2;
        const canRemove = forms.length > minForms;
        forms.forEach(form => {
            const removeBtn = form.querySelector('.remove-choice-form');
            if (removeBtn) removeBtn.style.display = canRemove ? '' : 'none';
        });
    };

    const reindexForms = () => {
        const forms = formList.querySelectorAll('.choice-form');
        const formsetPrefix = totalFormsInput.name.split('-')[0];
        forms.forEach((form, index) => {
            const prefixRegex = new RegExp(`${formsetPrefix}-\\d+-`, 'g');
            const replacement = `${formsetPrefix}-${index}-`;
            form.querySelectorAll('input, select, textarea, label').forEach(el => {
                if (el.name) el.name = el.name.replace(prefixRegex, replacement);
                if (el.id) el.id = el.id.replace(prefixRegex, replacement);
                if (el.htmlFor) el.htmlFor = el.htmlFor.replace(prefixRegex, replacement);
            });
        });
    };

    addChoiceBtn.addEventListener('click', () => {
        const formNum = formList.querySelectorAll('.choice-form').length;
        const newFormHtml = formTemplate.innerHTML.replace(/__prefix__/g, formNum);
        const newFormDiv = document.createElement('div');
        newFormDiv.innerHTML = newFormHtml;
        formList.appendChild(newFormDiv.firstElementChild);
        totalFormsInput.value = formNum + 1;
        updateRemoveButtons();
    });

    formList.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-choice-form')) {
            e.target.closest('.choice-form').remove();
            totalFormsInput.value = formList.querySelectorAll('.choice-form').length;
            reindexForms();
            updateRemoveButtons();
        }
    });

    // Initial setup
    updateRemoveButtons();
});