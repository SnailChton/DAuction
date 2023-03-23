const logo_p1 = document.querySelector('.header__logo__part__one')
const logo_p2 = document.querySelector('.header__logo__part__two')
const intro_sup = document.querySelector('.intro__suptittle')
const nav__links = document.querySelectorAll('.nav__link')

let R = 28
let G = 176
let B = 28

// RED
function RED() {
  if (R == 28) {
    let redTimer = setInterval(function() {
      if (R < 176) {
        R += 2
        logo_p1.style.color = `rgb(${R},${G},${B})`
        logo_p2.style.borderBottom = `3px solid rgb(${R},${G},${B})`
        intro_sup.style.color = `rgb(${R},${G},${B})`
        nav__links.forEach((nav__link) => {
          nav__link.style.setProperty('--hover-nav-link-color', `rgb(${R},${G},${B})`)
          nav__link.style.setProperty('--hover-nav-link-border-bottom', `2px solid rgb(${R},${G},${B})`)
        })
      } else {
        clearInterval(redTimer)
        BLUE()
      }
    }, 500)
  } else {
    let redTimer = setInterval(function() {
      if (R > 28) {
        R -= 2
        logo_p1.style.color = `rgb(${R},${G},${B})`
        logo_p2.style.borderBottom = `3px solid rgb(${R},${G},${B})`
        intro_sup.style.color = `rgb(${R},${G},${B})`
        nav__links.forEach((nav__link) => {
          nav__link.style.setProperty('--hover-nav-link-color', `rgb(${R},${G},${B})`)
          nav__link.style.setProperty('--hover-nav-link-border-bottom', `2px solid rgb(${R},${G},${B})`)
        })
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
    let greenTimer = setInterval(function() {
      if (G < 176) {
        G += 2
        logo_p1.style.color = `rgb(${R},${G},${B})`
        logo_p2.style.borderBottom = `3px solid rgb(${R},${G},${B})`
        intro_sup.style.color = `rgb(${R},${G},${B})`
        nav__links.forEach((nav__link) => {
          nav__link.style.setProperty('--hover-nav-link-color', `rgb(${R},${G},${B})`)
          nav__link.style.setProperty('--hover-nav-link-border-bottom', `2px solid rgb(${R},${G},${B})`)
        })
      } else {
        clearInterval(greenTimer)
        RED()
      }
    }, 500)
  } else {
    let greenTimer = setInterval(function() {
      if (G > 28) {
        G -= 2
        logo_p1.style.color = `rgb(${R},${G},${B})`
        logo_p2.style.borderBottom = `3px solid rgb(${R},${G},${B})`
        intro_sup.style.color = `rgb(${R},${G},${B})`
        nav__links.forEach((nav__link) => {
          nav__link.style.setProperty('--hover-nav-link-color', `rgb(${R},${G},${B})`)
          nav__link.style.setProperty('--hover-nav-link-border-bottom', `2px solid rgb(${R},${G},${B})`)
        })
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
    let blueTimer = setInterval(function() {
      if (B < 176) {
        B += 2
        logo_p1.style.color = `rgb(${R},${G},${B})`
        logo_p2.style.borderBottom = `3px solid rgb(${R},${G},${B})`
        intro_sup.style.color = `rgb(${R},${G},${B})`
        nav__links.forEach((nav__link) => {
          nav__link.style.setProperty('--hover-nav-link-color', `rgb(${R},${G},${B})`)
          nav__link.style.setProperty('--hover-nav-link-border-bottom', `2px solid rgb(${R},${G},${B})`)
        })
      } else {
        clearInterval(blueTimer)
        GREEN()
      }
    }, 500)
  } else {
    let blueTimer = setInterval(function() {
      if (B > 28) {
        B -= 2
        logo_p1.style.color = `rgb(${R},${G},${B})`
        logo_p2.style.borderBottom = `3px solid rgb(${R},${G},${B})`
        intro_sup.style.color = `rgb(${R},${G},${B})`
        nav__links.forEach((nav__link) => {
          nav__link.style.setProperty('--hover-nav-link-color', `rgb(${R},${G},${B})`)
          nav__link.style.setProperty('--hover-nav-link-border-bottom', `2px solid rgb(${R},${G},${B})`)
        })
      } else {
        clearInterval(blueTimer)
        GREEN()
      }
    }, 500)
  }
}

BLUE()