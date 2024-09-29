/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {cupcake: {
        "color-scheme": "light",
        "primary": "#65c3c8",
        "secondary": "#EBEBEB",  //home blocks bg color
        "accent": "#eeaf3a",
        "neutral": "#291334",
        "base-100": "#faf7f5",
        "base-200": "#efeae6",
        "base-300": "#e7e2df",
        "base-content": "#161616", //home blocks text color
        "--rounded-btn": "1.9rem",
        "--tab-border": "2px",
        "--tab-radius": "0.7rem",
      }},
      {dark: {
          "color-scheme": "dark",
          "primary": "oklch(65.69% 0.196 275.75)",
          "secondary": "#050617",
          "accent": "oklch(74.51% 0.167 183.61)",
          "neutral": "#2a323c",
          "neutral-content": "#A6ADBB",
          "base-100": "#1d232a",
          "base-200": "#191e24",
          "base-300": "#15191e",
          "base-content": "#ffffff",
      }},
    ], 
    // false: only light + dark | true: all themes | array: specific themes like this ["light", "dark", "cupcake"]
    darkTheme: "dark", // name of one of the included themes for dark mode
    styled: true, // include daisyUI colors and design decisions for all components
    utils: true, // adds responsive and modifier utility classes
  },
}