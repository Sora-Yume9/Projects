var mainText = document.getElementById('MainText');
var buttons = document.querySelectorAll('.button');
function handleButtonClick(event) {
    var button = event.target;
    var value = button.value;
    mainText.value += value;
}
buttons.forEach(function (button) {
    button.addEventListener('click', handleButtonClick);
});
document.getElementById("Clear").onclick = function () {
    mainText.value = "";
};
document.getElementById("Calc").onclick = function () {
    var inputValue = mainText.value;
    var intValue = parseInt(inputValue, 10);
    if (!isNaN(intValue)) {
        var result = eval(inputValue);
        mainText.value = result.toString();
    }
    else {
        mainText.value = "Error";
        
    }
};
