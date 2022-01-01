const loc = window.location.href.split('#')[0].replace("127.0.0.1","localhost")
const params = window.location.href.split('#')[1]

console.log(loc);
console.log(params);


if (typeof(params)==='undefined') {
    const cognito_auth_uri = `https://hawkeye.auth.eu-west-1.amazoncognito.com/login?client_id=${_config.cognito.clientId}&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=`
    const relocation_uri = cognito_auth_uri + encodeURIComponent(loc)
    console.log(relocation_uri)
    window.location.replace(relocation_uri)
}


const accessParams = new URLSearchParams(params);

console.log("id-token");
console.log(accessParams.get("id_token"));
console.log("access-token");
console.log(accessParams.get("access_token"));

const snap_btn = document.querySelector('#snap-button');
const snap_img = document.querySelector('#snap-img');

snap_img.firstElementChild.src = "https://hawkeye-data-storage.s3.eu-west-1.amazonaws.com/pi/snap/2021_12_23_20_35_41.jpg"

let header = new Headers();
let snap_request = new Request('https://icpjhcglc3.execute-api.eu-west-1.amazonaws.com/prod/snap')

header.append('Authorization',accessParams.get("access_token"))
const snap_init = {
    method: 'POST',
    headers: header,
    cache: 'default'
}
snap_btn.addEventListener('click', onClick);

function onClick(e) {
    e.preventDefault();  
    snap_btn.disabled = true
    snap_btn.textContent = 'refreshing...'
    console.log(snap_btn);

    // Send post request
    fetch(snap_request,snap_init)
    .then((res)=> {
        console.log(res);
        return res.json()})
    .then((data)=> console.log(data))
    .catch((err)=> console.log(err))
    .then( () => {
        // reactivate button
        snap_btn.disabled = false
        snap_btn.textContent = 'Refresh'
    })

}

