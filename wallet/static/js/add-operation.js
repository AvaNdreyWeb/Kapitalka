const addOperationBtns = document.querySelectorAll('.add-btn');
const modalForm = document.querySelector('.modal-form');
const operationDate = document.querySelector('.operation-date');
const currencyBtnModal = document.querySelector('.currency-btn-modal');
const currencyBtnMain = document.querySelector('.currency-btn-main');
const modal = document.querySelector('.modal-card');
const background = document.querySelector('.modal-dark-bg');

function showModal() {
    modal.classList.add('block');
    background.classList.add('block');
}

function hideModal() {
    modal.classList.remove('block');
    background.classList.remove('block');
}

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}

for (let i = 0; i < 2; i++) {
    addOperationBtns[i].addEventListener('click', () => {
        showModal()
        operationDate.value = formatDate(new Date());
        currencyBtnModal.innerHTML = currencyBtnMain.innerHTML;
    })
}

background.addEventListener('click', hideModal)
modalForm.addEventListener('submit', hideModal)
