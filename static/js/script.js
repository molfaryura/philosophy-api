/**
 * Changes the background color of the button to a random color when clicked.
 */
const colorButton = document.getElementById("colorButton");

colorButton.addEventListener("click", () => {
  const randomColor = generateRandomColor();
  colorButton.style.backgroundColor = randomColor;
});

/**
 * Generates a random color code in hexadecimal format.
 * @returns {string} The randomly generated color code.
 */
function generateRandomColor() {
  const letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
