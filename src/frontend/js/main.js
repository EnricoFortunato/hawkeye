// Token validity
const loc = window.location.href.split('#')[0].replace("127.0.0.1","localhost")
const params = window.location.href.split('#')[1]
let accessParams
let id_token;
let access_token;

const cognito_auth_uri = `https://hawkeye.auth.eu-west-1.amazoncognito.com/login?client_id=${_config.cognito.clientId}&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=`
const relocation_uri = cognito_auth_uri + encodeURIComponent(loc)

if (typeof(params)==='undefined') {
    window.location.replace(relocation_uri)
}
else {
    accessParams = new URLSearchParams(params);
    id_token = accessParams.get("id_token"); 
    access_token = accessParams.get("access_token");

    is_token_valid = true
    if (!is_token_valid){
        window.location.replace(relocation_uri)
    }
}

// Authentication
let s3;
const key = 'frontend/refresh-image/refresh_image.jpg';

const cognitoidentity = new AWS.CognitoIdentity({apiVersion: '2014-06-30',region:'eu-west-1'});

const cognito_params = {
    IdentityPoolId: 'eu-west-1:3db9b3fe-0e0b-4176-8217-7a06808dffb6', /* required */
    AccountId: '081972465094',
    Logins: {
      'cognito-idp.eu-west-1.amazonaws.com/eu-west-1_1wzfZ5LC1': id_token,
    }
  };

cognitoidentity.getId(cognito_params, (err, data) => {
    if (err) console.log(err, err.stack); // an error occurred
    else {
        identity_id = data.IdentityId

        AWS.config.region = 'eu-west-1';
        AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            IdentityPoolId: 'eu-west-1:3db9b3fe-0e0b-4176-8217-7a06808dffb6',
            Logins: {
                'cognito-idp.eu-west-1.amazonaws.com/eu-west-1_1wzfZ5LC1': id_token
            }
        });

        //first image refresh
        s3 = new AWS.S3({
            apiVersion: '2006-03-01',
            params: {Bucket: 'hawkeye-data-storage'}
        });
        
        refresh_image(s3)
        .then((res)=> console.log(res))
    }
});

function refresh_image(s3) {
    return new Promise((res,rej) => {
        s3.getObject({Key: key}, (err, data) => {
            if (err) {
                console.log(err, err.stack); // an error occurred
                rej(`Error: ${err}`)
            }
            else {
                snap_img.firstElementChild.src = "data:image/png;base64," + encode(data.Body);
                res(`Image updated`)
            }
        });
    })
}

function encode(data) {
    var str = data.reduce(function(a,b){ return a+String.fromCharCode(b) },'');
    return btoa(str).replace(/.{76}(?=.)/g,'$&\n');
}

const snap_btn = document.querySelector('#snap-button');
const snap_img = document.querySelector('#snap-img');
let header = new Headers();
let snap_request = new Request('https://icpjhcglc3.execute-api.eu-west-1.amazonaws.com/prod/snap')

header.append('Authorization',access_token)
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

    // Send post request
    fetch(snap_request,snap_init)
    .then((res)=> {
        console.log(res);
        return res.json()})
    .then((data)=> console.log("Snap request completed"))
    .catch((err)=> console.log(err))
    .then( () => {
        setTimeout(()=>{
            // reactivate button
            snap_btn.disabled = false
            snap_btn.textContent = 'Refresh'
            refresh_image(s3)
        },1000)
    })
}

setInterval(() => {
    refresh_image(s3);
}, 1000);