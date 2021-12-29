const poolData = {
	UserPoolId: _config.cognito.userPoolId, // Your user pool id here
	ClientId: _config.cognito.clientId, // Your client id here
};
const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

let username;
let password;

function onSubmit(evt,data){

    const authenticationData = {
        Username: document.getElementsByName("username")[0].value,
        Password: document.getElementsByName("password")[0].value,
    };

    const  authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(
        authenticationData
    );

    const userData = {
        Username: document.getElementsByName("username")[0].value,
        Pool: userPool,
    };

    const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);



    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function(result) {

            const accessToken = result.getAccessToken().getJwtToken();
            console.log(accessToken);
            sessionStorage.setItem("accessToken",accessToken)
            window.location.replace('./index.html')
    
            // //POTENTIAL: Region needs to be set if not already set previously elsewhere.
            // AWS.config.region = _config.cognito.region;
    
            // AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            //     IdentityPoolId: '...', // your identity pool id here
            //     Logins: {
            //         // Change the key below according to the specific region your user pool is in.
            //         'cognito-idp.eu-west-1.amazonaws.com/eu-west-1_1wzfZ5LC1': result
            //             .getIdToken()
            //             .getJwtToken(),
            //     },
            // });
    
            // //refreshes credentials using AWS.CognitoIdentity.getCredentialsForIdentity()
            // AWS.config.credentials.refresh(error => {
            //     if (error) {
            //         console.error(error);
            //     } else {
            //         // Instantiate aws sdk service objects now that the credentials have been updated.
            //         // example: var s3 = new AWS.S3();
            //         console.log('Successfully logged!');
            //     }
            // });
        },
    
        onFailure: function(err) {
            alert(err.message || JSON.stringify(err));
        },
    });
}
