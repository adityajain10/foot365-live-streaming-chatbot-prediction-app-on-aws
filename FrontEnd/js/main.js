//Amazon service interaction JS

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?#&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    return vars;
}

var id_token = getUrlVars()["id_token"];

AWS.config.region = 'us-east-1';
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-1:8cd56551-c975-4618-82cc-43fef1e3a98e',
    Logins: {
        'cognito-idp.us-east-1.amazonaws.com/us-east-1_Ap83aBRuO': id_token
    }
});

var apigClient;
AWS.config.credentials.refresh(function () {
    var accessKeyId = AWS.config.credentials.accessKeyId;
    var secretAccessKey = AWS.config.credentials.secretAccessKey;
    var sessionToken = AWS.config.credentials.sessionToken;
    AWS.config.region = 'us-east-1';
    apigClient = apigClientFactory.newClient({
        accessKey: AWS.config.credentials.accessKeyId,
        secretKey: AWS.config.credentials.secretAccessKey,
        sessionToken: AWS.config.credentials.sessionToken, // this field was missing
        region: 'us-east-1'
    });
});

var messages = [], //array that hold the record of each string in chat
    lastUserMessage = "", //keeps track of the most recent input string from the user
    botMessage = "", //var keeps track of what the chatbot is going to say
    botName = 'Chatbot', //name of the chatbot
    talking = true; //when false the speach function doesn't work

function chatbotResponse() {

    // User's own message for display
    lastUserMessage = userMessage();

    return new Promise(function (resolve, reject) {
        talking = true;
        let params = {};
        let additionalParams = {
            headers: {
                "x-api-key": 'mFZDVAbsK63sAZoTnEHrx2jChIR0cezo3sOIWvMk'
            }
        };
        var body = {
            "message": lastUserMessage
        };
        apigClient.recommendPost(params, body, additionalParams)
            .then(function (result) {

                reply = result.data;

                $("<li class='replies'><p>" + reply + "</p></li>").appendTo($('.messages ul'));
                $('.message-input input').val(null);
                $('.contact.active .preview').html('<span>You: </span>' + reply);
                $(".messages").animate({scrollTop: $(document).height()}, "fast");

                resolve(result.data.body);
                botMessage = result.data.body;
            }).catch(function (result) {
            // Add error callback code here.
            console.log(result);
            botMessage = "Couldn't connect";
            reject(result);
        });
    })
}


//Js for the chat application


$(".messages").animate({scrollTop: $(document).height()}, "fast");


$(".expand-button").click(function () {
    $("#profile").toggleClass("expanded");
    $("#contacts").toggleClass("expanded");
});

$("#status-options ul li").click(function () {
    $("#status-online").removeClass("active");
    $("#status-away").removeClass("active");
    $("#status-busy").removeClass("active");
    $("#status-offline").removeClass("active");
    $(this).addClass("active");


    $("#status-options").removeClass("active");
});

function userMessage() {

    message = $(".message-input input").val();
    if ($.trim(message) == '') {
        return false;
    }

    $('<li class="sent"><p>' + message + '</p></li>').appendTo($('.messages ul'));
    $('.message-input input').val(null);
    $('.contact.active .preview').html('<span>You: </span>' + message);
    $(".messages").animate({scrollTop: $(document).height()}, "fast");

    return message;
}

$('.submit').click(function () {
    // newMessage();
    chatbotResponse();
});

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        // newMessage();
        chatbotResponse();
        return false;
    }
});
