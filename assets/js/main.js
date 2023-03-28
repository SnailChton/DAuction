let R = 28
let G = 176
let B = 28

// RED
function RED() {
  if (R == 28) {
    let redTimer = setInterval(function () {
      if (R < 176) {
        R += 2
        document.documentElement.style.cssText = `--theme-color: rgb(${R},${G},${B})`;
      } else {
        clearInterval(redTimer)
        BLUE()
      }
    }, 500)
  } else {
    let redTimer = setInterval(function () {
      if (R > 28) {
        R -= 2
        document.documentElement.style.cssText = `--theme-color: rgb(${R},${G},${B})`;
      } else {
        clearInterval(redTimer)
        BLUE()
      }
    }, 500)
  }
}

//GREEN
function GREEN() {
  if (G == 28) {
    let greenTimer = setInterval(function () {
      if (G < 176) {
        G += 2
        document.documentElement.style.cssText = `--theme-color: rgb(${R},${G},${B})`;
      } else {
        clearInterval(greenTimer)
        RED()
      }
    }, 500)
  } else {
    let greenTimer = setInterval(function () {
      if (G > 28) {
        G -= 2
        document.documentElement.style.cssText = `--theme-color: rgb(${R},${G},${B})`;
      } else {
        clearInterval(greenTimer)
        RED()
      }
    }, 500)
  }
}

//BLUE
function BLUE() {
  if (B == 28) {
    let blueTimer = setInterval(function () {
      if (B < 176) {
        B += 2
        document.documentElement.style.cssText = `--theme-color: rgb(${R},${G},${B})`;
      } else {
        clearInterval(blueTimer)
        GREEN()
      }
    }, 500)
  } else {
    let blueTimer = setInterval(function () {
      if (B > 28) {
        B -= 2
        document.documentElement.style.cssText = `--theme-color: rgb(${R},${G},${B})`;
      } else {
        clearInterval(blueTimer)
        GREEN()
      }
    }, 500)
  }
}

BLUE()

