var Adventures = {};
Adventures.SERVER_PATH = window.location.href.slice(0,-1);
//currentAdventure is used for the adventure we're currently on (id). This should be determined at the beginning of the program
Adventures.questionId = 0; //todo keep track from db
//currentStep is used for the step we're currently on (id). This should be determined at every crossroad, depending on what the user chose
Adventures.currentStep = 0;//todo keep track from db
<<<<<<< HEAD
Adventures.username = "";//todo keep track from db
=======
Adventures.username = 0;//todo keep track from db
>>>>>>> 29018ae504f23ea2f716e2b199bbb901b01693f4
Adventures.coins = 10;
Adventures.life = 100;
Adventures.optionId;
Adventures.nextQuestionId;
Adventures.options;


Adventures.gameOver= false; //defining the game to false because we don't know already what's going on.
//Adventures.questions=0;


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
            "options":Adventures.options}

        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log(data);
            $(".greeting-text").hide();
            Adventures.write(data);
            Adventures.coins=data.coins;
            console.log(Adventures.coins);
            Adventures.life=data.life; // we would need to create it in the database
            console.log(Adventures.life);
            $("#coins").text(Adventures.coins); // we would need to create it in the database
            $('#life').text(Adventures.life);
            Adventures.gameOver=data.gameOver; // we would need to create it in the database
            console.log(Adventures.gameOver);
            Adventures.restart();
        }
    });
};

Adventures.write = function (message) {
if (Adventures.life <= 0){
        Adventures.GameResult()
        return
    }
else if (Adventures.coins<=0){
        Adventures.GameResult()
        return
}
    //Writing new choices and image to screen
    $(".situation-text").text(message["text"]).show();
    for(var i=0;i<message['options'].length;i++){
        var opt = $("#option_" + (i+1));
        opt.text(message['options'][i]['option_text']);
        opt.prop("value", message['options'][i]['id']);
    }
    Adventures.setImage(message["image"]);
    Adventures.updateUserGameOver();
};

Adventures.updateUserGameOver() = function(){
    $("#life").prop("value", Adventures.life)
    $("#coins").text(Adventures.coins)
};

Adventures.GameResult= function(){
    $(".situation-text").text("You died because of your bad decisions!")
    Adventures.updateUserGameOver();
}



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
Adventures.setImage = function (img_name) {
    $("#situation-image").attr("src", "./images/" + img_name);
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
        data: {"username":
            $("#nameField").val(),
            "user_id": $(this).val()
        },
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log(data);
            Adventures.write(data);
            Adventures.questionId=data.questionId;
            Adventures.username=data.username;
             $(".questionId").show();
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

