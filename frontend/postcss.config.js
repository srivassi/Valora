import tailwindcss from '@tailwindcss/postcss';
import autoprefixer from 'autoprefixer'; // Make sure 'autoprefixer' is also imported

export default {
  plugins: [ // <-- Change this from an object `{}` to an array `[]`
    tailwindcss(), // <-- Call tailwindcss as a function
    autoprefixer(), // <-- Call autoprefixer as a function
  ],
};