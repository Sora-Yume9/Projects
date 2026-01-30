var currentRowIndex = 1;



document.getElementById("enterButton")!.onclick = function myenter() {
 
    
    var table = document.getElementById("table") as HTMLTableElement;
    
    var row = table!.insertRow(1) ;
  
  
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var text = document.getElementById("textBox1") as HTMLInputElement;
  var text2 = document.getElementById("textBox2") as HTMLInputElement;
  var text3 = document.getElementById("textBox3") as HTMLInputElement;
  var text4 = document.getElementById("textBox4") as HTMLInputElement;
    
    cell1.innerHTML = text?.value;
    cell2.innerHTML = text2?.value;
    cell3.innerHTML = text3?.value;
    cell4.innerHTML = text4?.value;
  }

  document.getElementById("removeButton")!.onclick = function mydeleteRow() {
    var table = document.getElementById("table") as HTMLTableElement;
    table.deleteRow(1);

  }

  function updateTime() {
    var currenttime = new Date
    var hours = currenttime.getHours();
    var minutes = currenttime.getMinutes();
    let newhours = hours - 12
   var t
   if ( hours > 12 )
   { 
    t = "PM" 
   }
   else{
     t = "AM"}
    if (minutes < 10) {
      "0" + minutes
    }
    var timeString = newhours + ":" + minutes + t;
    var label = document.getElementById("currentTime");
    label!.textContent = timeString;
    
    setInterval(updateTime, 10000);
  }

  
updateTime(); 






function currentdate() {
const currenttime = new Date
var day:any = currenttime.getUTCDate();
var year:any = currenttime.getUTCFullYear();
var month:any = currenttime.getMonth();
var date = year + ":" + month + ":" + day  
var label = document.getElementById("currentDate");
label!.textContent = date
}
currentdate();

setInterval(currentdate,60000);
document.getElementById("calculateButton")!.onclick = function() {
  window.location.assign("Calculate.html");


}
