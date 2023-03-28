const currency = "$₽֏";
const currencyBtnMobile = document.querySelector('.currency-btn-mobile');
const currencyHidden = document.querySelector('.hidden-cur-code');

const curs = ["USD", "RUB", "AMD"]

function updateCurrency(el, i) {
    const next = (i+1)%currency.length
    el.dataset.index = next.toString()
    el.innerHTML = currency[next]
}

function updateAllCurrency() {
    const index = parseInt(currencyBtnMain.dataset.index)
    updateCurrency(currencyBtnMain, index)
    updateCurrency(currencyBtnMobile, index)
    updateCurrency(currencyBtnModal, index)
    currencyHidden.value = curs[(index+1)%currency.length]
}

currencyBtnMain.addEventListener('click', updateAllCurrency)
currencyBtnMobile.addEventListener('click', updateAllCurrency)
currencyBtnModal.addEventListener('click', () => {
    const index = parseInt(currencyBtnModal.dataset.index)
    updateCurrency(currencyBtnModal, index)
    currencyHidden.value = curs[(index+1)%currency.length]
})
