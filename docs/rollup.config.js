// rollup.config.js
import { terser } from 'rollup-plugin-terser'
import json from '@rollup/plugin-json'
import css from 'rollup-plugin-css-only'

export default {
  input: 'script.js',
  output: {
    file: 'script.min.js',
    format: 'es',
    plugins: [
      terser({
        mangle: true
      })
    ]
  },
  plugins: [
    json(),
    css({
      output: 'style.min.css'
    })
  ]
}
