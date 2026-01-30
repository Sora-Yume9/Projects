
const mainText = document.getElementById('MainText') as HTMLInputElement;
const buttons = document.querySelectorAll('.button');


function handleButtonClick(event: Event) {
  const button = event.target as HTMLButtonElement;
  const value = button.value;

  
  mainText.value += value;
}


buttons.forEach((button) => {
  button.addEventListener('click', handleButtonClick);
});
document.getElementById("Clear")!.onclick = function (){
  
mainText.value = "";
}
document.getElementById("Calc")!.onclick = function () {
    const inputValue = mainText.value;
    
  
    const intValue = parseInt(inputValue, 10);
    if (!isNaN(intValue)) {
        const result = eval(inputValue);

        mainText.value = result.toString();
    } else {
        
        mainText.value = "Error"
    }
}