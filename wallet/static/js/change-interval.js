const intervals = ["всё время", "за месяц", "сегодня"];
const intervalBtns = document.querySelectorAll('.interval-btn');

function updateIntervals(el, i) {
    const next = (i+1)%intervals.length
    el.dataset.index = next.toString()
    el.innerHTML = intervals[next]
}

for (let i = 0; i < 2; i++) {
    const intervalBtn = intervalBtns[i]
    intervalBtn.addEventListener('click', () => {
        const index = parseInt(intervalBtn.dataset.index)
        updateIntervals(intervalBtns[0], index)
        updateIntervals(intervalBtns[1], index)
    })
}
