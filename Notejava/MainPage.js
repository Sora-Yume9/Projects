var currentRowIndex = 1;
var count = 1;
document.getElementById("enterButton").onclick = function myenter() {
    var table = document.getElementById("table");
    var row = table.insertRow(1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var text = document.getElementById("textBox1");
    var text2 = document.getElementById("textBox2");
    var text3 = document.getElementById("textBox3");
    var text4 = document.getElementById("textBox4");
    cell1.innerHTML = text === null || text === void 0 ? void 0 : text.value;
    cell2.innerHTML = text2 === null || text2 === void 0 ? void 0 : text2.value;
    cell3.innerHTML = text3 === null || text3 === void 0 ? void 0 : text3.value;
    cell4.innerHTML = text4 === null || text4 === void 0 ? void 0 : text4.value;
    count ++;
};
document.getElementById("removeButton").onclick = function mydeleteRow() {
    var table = document.getElementById("table");
 
    if (count > 1){
    table.deleteRow(1);
    }
    count--;
    if (count < 1) {
        count = 1 
    }
};
document.getElementById("Last").onclick = function mydeleteRow() {
    if (count > 1) {
    var table = document.getElementById("table");
   count--;
        table.deleteRow(count); 
    }
    if (count < 1) {
        count = 1 
    }
};
function updateTime() {
    var currenttime = new Date;
    var hours = currenttime.getHours();
    var minutes = currenttime.getMinutes();
    var newhours
   switch(hours){

    case 13:
        hours = 1
        break 
        case 14:
        hours = 2
        break
        case 13:
        hours = 1
        break 
        case 14:
        hours = 2
        break 
        case 15:
        hours = 3
        break 
        case 16:
        hours = 4
        break 
        case 17:
        hours = 5
        break 
        case 18:
        hours = 6
        break 
        case 19:
        hours = 7
        break 
        case 20:
        hours = 8
        break 
        case 21:
        hours = 9
        break 
        case 22:
        hours = 10
        break 
        case 23:
        hours = 11
        break 
        case 0:
        hours = 12
        break 
    }
    var t;
    var f = "0";
    if (hours > 12) {
        t = "PM";
    }
    else {
        t = "AM";
    }
    if (minutes < 10) 
    {
        var timeString = hours + ":" + f + minutes + t;

    }
    else
    {
        var timeString = hours + ":" + minutes + t;

    }
   
    var label = document.getElementById("currentTime");
    label.textContent = timeString;
    setInterval(updateTime, 10000);
}
updateTime();
function currentdate() {
    var currenttime = new Date;
    var day = currenttime.getUTCDate();
    var year = currenttime.getUTCFullYear();
    var month = currenttime.getMonth();
    month++;
    var date = year + ":" + month + ":" + day;
    var label = document.getElementById("currentDate");
    label.textContent = date;
}
currentdate();
setInterval(currentdate, 60000);
document.getElementById("calculateButton").onclick = function () {
    window.location.assign("Calculate");
};
document.getElementById('Save').onclick = function () {
    const table = document.getElementById('table');
    const tableContent = table.outerHTML;

    // Convert the table content to a JSON object
    const data = { tableContent: tableContent };
    const jsonContent = JSON.stringify(data);

    const blob = new Blob([jsonContent], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'table.json'; // Change the file extension to .json
    a.style.display = 'none';

    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};

document.getElementById('Load').onclick = function () {
    const input = document.createElement('input');
    input.type = 'file';

    input.addEventListener('change', function () {
        const file = input.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            const jsonData = e.target.result;
            const data = JSON.parse(jsonData);
            const table = document.getElementById('table');
            table.innerHTML = data.tableContent;
        };

        reader.readAsText(file);
    });

    input.click();
};
function loadPage(pageUrl) {
    var contentContainer = document.getElementById('content');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', pageUrl, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            contentContainer.innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}
document.getElementById('clearButton').onclick = function() {
    localStorage.clear();
    location.reload();
};

document.getElementById("GPT").onclick = function() {
    window.location.href = "https://chat.openai.com/";
};


function saveTableData() {
    const table = document.getElementById('table');
    const tableData = [];

    // Collect header data
    const headerRow = table.rows[0];
    const headerData = [];
    for (const headerCell of headerRow.cells) {
        headerData.push(headerCell.innerText);
    }
    tableData.push(headerData);

    // Collect row data
    for (let i = 1; i < table.rows.length; i++) {
        const rowDataInRow = [];
        const row = table.rows[i];
        for (let j = 0; j < row.cells.length; j++) {
            rowDataInRow.push(row.cells[j].innerText);
        }
        tableData.push(rowDataInRow);
    }

    // Clear existing data in local storage
    localStorage.removeItem('tableData');

    // Save the new data
    localStorage.setItem('tableData', JSON.stringify(tableData));

    // Update the count variable
    count = table.rows.length;
}



function loadTableDataFromLocalStorage() {
    const tableData = localStorage.getItem('tableData');

    if (tableData) {
        const parsedData = JSON.parse(tableData);
        const table = document.getElementById('table');
        table.innerHTML = ''; // Clear the table

        // Create table rows and cells based on the loaded data
        for (const rowData of parsedData) {
            const row = table.insertRow();
            for (const cellData of rowData) {
                const cell = row.insertCell();
                cell.innerText = cellData;
            }
        }
    }
}

window.addEventListener('load', loadTableDataFromLocalStorage);

// Save the table data every second
setInterval(saveTableData, 1000);
