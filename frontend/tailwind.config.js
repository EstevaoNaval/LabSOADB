/** @type {import('tailwindcss').Config} */
import daisyui from "daisyui"
export default {
  content: [ 
    '@srcDir/components/**/*.{vue,js,ts}',
    '@srcDir/layouts/**/*.vue',
    `@srcDir/pages/**/*.vue`,
    `@srcDir/composables/**/*.{js,ts}`,
    `@srcDir/plugins/**/*.{js,ts}`,
    `@srcDir/utils/**/*.{js,ts}`,
    `@srcDir/App.{js,ts,vue}`,
    `@srcDir/app.{js,ts,vue}`,
    `@srcDir/Error.{js,ts,vue}`,
    `@srcDir/error.{js,ts,vue}`,
    `@srcDir/app.config.{js,ts}`,
    `@srcDir/content/**/*.md`
  ],
  theme: {
    extend: {},
  },
  plugins: [
    daisyui
  ],
  daisyui: {
    themes: ["night","winter"]
  },
  darkMode: 'media'
}

