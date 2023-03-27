const newDebtCard = document.querySelector('.new-debt-card');
const modalForm = document.querySelector('.modal-form')
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

newDebtCard.addEventListener('click', showModal)
background.addEventListener('click', hideModal)
modalForm.addEventListener('submit', hideModal)


const currency = "$₽֏";
const currencyBtn = document.querySelector('.currency-btn');

currencyBtn.addEventListener('click', () => {
    const i = currency.indexOf(currencyBtn.innerHTML)
    const next = (i + 1) % currency.length
    currencyBtn.innerHTML = currency[next]
})
