var Adventures = {};
Adventures.SERVER_PATH = window.location.href.slice(0,-1);
//currentAdventure is used for the adventure we're currently on (id). This should be determined at the beginning of the program
Adventures.questionId = 0; //todo keep track from db
//currentStep is used for the step we're currently on (id). This should be determined at every crossroad, depending on what the user chose
Adventures.currentStep = 0;//todo keep track from db

Adventures.username = "";//todo keep track from db

Adventures.coins = 10;
Adventures.life = 100;
Adventures.optionId;
Adventures.nextQuestionId;
Adventures.options;
Adventures.picture;


Adventures.gameOver= false; //defining the game to false because we don't know already what's going on.


//TODO: remove for production
Adventures.debugMode = true;
Adventures.DEFAULT_IMG = "./images/choice.jpg";

Adventures.lifeAndCoinsUpdate=function(coin,life){ // will update the life and coins . Need to linked it with the database
Adventures.coins=Adventures.coins-coin;
Adventures.life=Adventures.life-life;
};


//Handle Ajax Error, animation error and speech support
Adventures.bindErrorHandlers = function () {
    //Handle ajax error, if the server is not found or experienced an error
    $(document).ajaxError(function (event, jqxhr, settings, thrownError) {
        Adventures.handleServerError(thrownError);
    });

    //Making sure that we don't receive an animation that does not exist
    $("#situation-image").error(function () {
        Adventures.debugPrint("Failed to load img: " + $("#situation-image").attr("src"));
        Adventures.setImage(Adventures.DEFAULT_IMG);
    });
};


//The core function of the app, sends the user's choice and then parses the results to the server and handling the response
Adventures.chooseOption = function(){
    Adventures.currentStep = $(this).val();
    $.ajax("/story",{
        type: "POST",
        data: {"username": Adventures.username,
            "questionId": Adventures.questionId,
            "nextquestion": Adventures.nextQuestionId,
            "coins":Adventures.coins,
            "life":Adventures.life,
            "options":Adventures.options,
            "picture":Adventures.picture,
            "next": Adventures.currentStep}, //what does currentStep do?

        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log(data);
            $(".greeting-text").hide();

            Adventures.write(data);

        }
    });
};

Adventures.write = function (message) {
    //Writing new choices and image to screen
    $(".situation-text")
        .text(message["question_text"])
        .show();
    for(var i=0;i<message["options"].length;i++){
        var opt = $("#option_" + (i+1));
        opt.text(message["options"][i]['option_text']);
        opt.attr('data-option-id', message['optionId'][i]['option_id']);
        opt.prop("value", message["options"][i]['option_id']);
    }
    Adventures.setImage(message["picture"]);
};



Adventures.start = function(){
    $(document).ready(function () {
        $(".game-option").click(Adventures.optionId);
        $("#nameField").keyup(Adventures.checkName);
        $(".adventure-button").click(Adventures.initAdventure);
        $(".adventure").hide();
        $(".welcome-screen").show();
        $("#coins").text(Adventures.coins);
        $('#life').text(Adventures.life);

    });
};

//Setting the relevant image according to the server response
Adventures.setImage = function (img){
    $("#situation-image").attr("src", "./images/" + img);
};

Adventures.checkName = function(){
    if($(this).val() !== undefined && $(this).val() !== null && $(this).val() !== ""){
        $(".adventure-button").prop("disabled", false);
    }
    else{
        $(".adventure-button").prop("disabled", true);
    }
};


Adventures.initAdventure = function(){

    $.ajax("/start",{
        type: "POST",
        data: {"username": $("#nameField").val(),
            "question_id": $(this).val(),
        },
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log(data);
            Adventures.write(data);
            Adventures.questionId=data.questionId;
            Adventures.username=data.username;
            Adventures.options = data.options;
            Adventures.optionId = data.optionId;
             $(".adventure").show();
            $(".welcome-screen").hide();
        }
    });
};

Adventures.handleServerError = function (errorThrown) {
    Adventures.debugPrint("Server Error: " + errorThrown);
    var actualError = "";
    if (Adventures.debugMode) {
        actualError = " ( " + errorThrown + " ) ";
    }
    Adventures.write("Sorry, there seems to be an error on the server. Let's talk later. " + actualError);

};

Adventures.debugPrint = function (msg) {
    if (Adventures.debugMode) {
        console.log("Adventures DEBUG: " + msg)
    }
};

Adventures.restart=function(){ // when the user loose or win
    if (Adventures.gameOver) {
        alert("gameOver")
        location.reload();
    }
};

Adventures.start();

