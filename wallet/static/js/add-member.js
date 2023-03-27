const addMemberBtn = document.querySelector('.add-member');
const memberInput = document.querySelector('.member-input')
const memberList = document.querySelector('.member-list')

function addMemberToList() {
    username = memberInput.value.trim()
    if (username != '') {
        if (username[0] != '@') {
            memberList.value += '@'
        }

        memberList.value += username + '\n'
    }
    memberInput.value = ''
}

addMemberBtn.addEventListener('click', addMemberToList)

