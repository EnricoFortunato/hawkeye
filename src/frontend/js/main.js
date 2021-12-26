const snap_btn = document.querySelector('#snap-button');
const snap_img = document.querySelector('#snap-img');
const images = [
    "https://galeriemagazine.com/wp-content/uploads/2019/01/Dining_3-1920x1200.jpg",
    "https://img.gtsstatic.net/reno/imagereader.aspx?imageurl=https%3A%2F%2Fsir.azureedge.net%2F1253i215%2F1v9t6ecteh5c4aa1fnbvzpwby5i215&option=N&h=472&permitphotoenlargement=false"
]
let counter = 0

snap_btn.addEventListener('click', onClick);

snap_img.firstElementChild.src = images[counter]

function onClick(e) {
    e.preventDefault();
    counter = (counter + 1) %2
    snap_img.firstElementChild.src = images[counter]
}

// setTimeout(() => msg.remove(), 3000)

