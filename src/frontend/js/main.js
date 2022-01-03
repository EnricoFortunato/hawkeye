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
const id_token = accessParams.get("id_token"); 
const access_token = accessParams.get("access_token"); 
console.log("id-token");
console.log(id_token);
console.log("access-token");
console.log(access_token);

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
        console.log(data);
        identity_id = data.IdentityId

        AWS.config.region = 'eu-west-1';
        AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            IdentityPoolId: 'eu-west-1:3db9b3fe-0e0b-4176-8217-7a06808dffb6',
            Logins: {
                'cognito-idp.eu-west-1.amazonaws.com/eu-west-1_1wzfZ5LC1': id_token
            }
        });

        AWS.config.credentials.get(function(err) {
            if (err) return console.error(err);
            else console.log(AWS.config.credentials);
                                                                                                                                                                                                            
            const s3 = new AWS.S3({
                apiVersion: '2006-03-01',
                params: {Bucket: 'hawkeye-data-storage'}
            });

            // s3.listObjects({Delimiter: '/'}, function(err, data) {
            //     if (err) console.log(err, err.stack); // an error occurred
            //     else {
            //         console.log(data);

            //     }
            // });

            s3.getObject({Key: 'frontend/refresh-image/refresh_image.jpg'}, function(err, data) {
                if (err) console.log(err, err.stack); // an error occurred
                else {
                    console.log(data);
                    snap_img.firstElementChild.src = "data:image/png;base64," + encode(data.Body);
                }
            });

        });
    }

});

function encode(data)
{
    var str = data.reduce(function(a,b){ return a+String.fromCharCode(b) },'');
    return btoa(str).replace(/.{76}(?=.)/g,'$&\n');
}

const snap_btn = document.querySelector('#snap-button');
const snap_img = document.querySelector('#snap-img');

//snap_img.firstElementChild.src = "https://hawkeye-data-storage.s3.eu-west-1.amazonaws.com/pi/snap/2021_12_23_20_35_41.jpg"

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

