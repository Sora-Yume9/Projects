const robot = require("robotjs");
const keypress = require("keypress");

// Button coordinates
const buttonCoordinates = {
  '0': { x: 630, y: 605 },
  '1': { x: 630, y: 550 },
  '2': { x: 684, y: 552 },
  '3': { x: 730, y: 550 },
  '4': { x: 630, y: 500 },
  '5': { x: 680, y: 500 },
  '6': { x: 740, y: 500 },
  '7': { x: 630, y: 440 },
  '8': { x: 680, y: 440 },
  '9': { x: 740, y: 440 },
};

function printButtonCombinations() {
  const buttons = Array.from({ length: 10 }, (_, i) => i.toString());

  // Listen for 'y' key press to terminate the program
  keypress(process.stdin);
  process.stdin.on('keypress', function(ch, key) {
    if (key && key.name === 'y') {
      process.exit(); // Terminate the program when 'y' is pressed
    }
  });

  let combinationsCount = 0;

  for (let r = 1; r <= buttons.length; r++) {
    const combinationsR = getCombinations(buttons, r);
    for (const combination of combinationsR) {
      const charArray = combination.split('');

      const combinationCoordinates = charArray.map(button => buttonCoordinates[button]);
      console.log(`Combination: ${charArray.join(' ')} - Coordinates: ${JSON.stringify(combinationCoordinates)}`);

      for (let idx = 0; idx < combinationCoordinates.length; idx++) {
        const coordinatesSet = combinationCoordinates[idx];
        console.log(`Set ${idx + 1}: ${JSON.stringify(coordinatesSet)}`);
        robot.moveMouse(coordinatesSet.x, coordinatesSet.y);
        robot.mouseClick();
      }
      robot.moveMouse(680, 400);
      robot.mouseClick();

      combinationsCount++;

      if (combinationsCount == 400) {
        console.log("Program stopped after processing 500 combinations.");
        process.exit();  // Terminate the program after processing 500 combinations
      }
    }
  }
}

function getCombinations(arr, r) {
  const combinations = [];

  function generateCombination(current, start) {
    if (current.length === r) {
      combinations.push(current.join(''));
      return;
    }

    for (let i = start; i < arr.length; i++) {
      generateCombination([...current, arr[i]], i);
    }
  }

  generateCombination([], 0);
  return combinations;
}

if (require.main === module) {
  printButtonCombinations();
}
