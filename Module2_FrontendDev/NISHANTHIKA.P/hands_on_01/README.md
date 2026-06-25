# Hands-On 1 — HTML5 Semantic Structure & CSS3 Foundations

**Program:** Digital Nurture 5.0 — Python Full Stack Engineer Track  
**Module:** Module 2 — Frontend Development  
---

## Topics Covered
- HTML5 Semantic Elements
- CSS3 Selectors & Specificity
- CSS Box Model
- Typography & Spacing
- Basic Page Layout

---

## Files
```
handson_01/
├── index.html      
├── styles.css      
└── README.md      
```

---

## Task Breakdown

### Task 1 — Build the Page Skeleton with Semantic HTML5
| Step | What was done |
|------|--------------|
| 1 | Created `index.html` with HTML5 doctype, `<html lang="en">`, charset UTF-8, viewport meta, and descriptive `<title>` |
| 2 | Added semantic sections: `<header>`, `<main>` (with `#hero` and `#courses`), and `<footer>` |
| 3 | Added `<nav>` inside `<header>` with an unordered list: Home, Courses, Profile, Grades |
| 4 | Added `<h1>`, description `<p>`, and `<button>Explore Courses</button>` inside the hero section |
| 5 | Added 3 `<article>` elements inside the courses section — each with `<h3>`, `<p>`, and `<span>` for credits |
| 6 | Validated at https://validator.w3.org/ — zero errors |

**Why `<article>` over `<div>`?**  
`<article>` represents self-contained content that could stand independently (like a course card). `<div>` has no semantic meaning.

---

### Task 2 — Apply CSS3 Fundamentals
| Step | What was done |
|------|--------------|
| 7 | Linked `styles.css` via `<link>` inside `<head>` |
| 8 | Applied CSS reset: `margin: 0`, `padding: 0`, `box-sizing: border-box` on `*` |
| 9 | Styled `<body>` with system font stack (`Arial, Helvetica, sans-serif`), background colour `#f0f4f8`, text colour `#1a202c` |
| 10 | Styled `<header>` with `display: flex`, `justify-content: space-between`, padding, and dark background `#1e3a5f` |
| 11 | Styled nav links: removed `list-style`, displayed inline with `display: flex` + `gap`, removed `text-decoration` |
| 12 | Styled hero with `text-align: center`, generous padding, button with `:hover` pseudo-class |
| 13 | Added `.course-card` class with `padding`, `border`, `border-radius: 8px`, and `box-shadow` |


---



## Expected Output
- A page with a visible dark-blue header and nav links
- A blue hero section with a centred heading, paragraph, and hover-effect button
- Three bordered course cards with a subtle box-shadow
- A dark footer

---

