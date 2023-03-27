const newGroupCard = document.querySelector('.new-group-card');
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

newGroupCard.addEventListener('click', showModal)
background.addEventListener('click', hideModal)
modalForm.addEventListener('submit', hideModal)
