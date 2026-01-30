const { app, globalShortcut, ipcMain } = require('electron');
const { execSync,spawn } = require('child_process');
const teseract = require("tesseract.js")
const fs = require('fs');
const pathModule = require('path');
const sharp = require('sharp');


app.whenReady().then(()  => {
const isRegistered = globalShortcut.register('1',async () => {
    var basePath = "../../../Pictures/Screenshots/"

    const files = fs.readdirSync(basePath);

    const pngFile = files.find(file => pathModule.extname(file) === '.png');
    if(pngFile) {
     const mainpath = pathModule.join(basePath, pngFile);
     const roi = { left: 19, top: 160, width: 1100 - 19, height: 741 - 160 };
     const croppedBuffer = await sharp(mainpath)
     .extract({ left: roi.left, top: roi.top, width: roi.width, height: roi.height })
     .toBuffer();
     const result = await teseract.recognize(croppedBuffer); 
     var text = result.data.text.trim();
     text = text.replace(/[.!?\n"]/g, ' ');
     text = text.replace(/1/g, 'i');
     text = text.replace(/\$/g, 's');
     text = text.replace(/0/g, 'o');
     text = text.replace(/"/g, ' ');
     text = text.replace(/[^a-zA-Z]/g, ' ');

     console.log(text)
     const command = `echo "${text}" | festival --tts`;

     const output = execSync(command).toString();
     fs.unlinkSync(mainpath);

    }
  })
    
})

   



