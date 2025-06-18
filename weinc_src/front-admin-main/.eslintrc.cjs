/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  'extends': [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    parser: '@typescript-eslint/parser',
  },rules:{
    'vue/script-setup-no-uses-vars': 'off',
    'vue/multi-word-component-names': 0,
    "no-duplicate-imports": "off",
    "no-undef": "off",
    '@typescript-eslint/ban-ts-comment': 'off',
    "@typescript-eslint/no-duplicate-imports": "warn",
    'prettier/prettier': [
      'error',
      {
        singleQuote: true,
        backtick: true,
        semi: true,
        useTabs: false,
        bracketSpacing: true,
        bracketSameLine: true,
        tabWidth: 2,
        trailingComma: 'all',
        arrowParens: 'avoid',
        endOfLine: 'auto',
        overrides: [
          {
            files: '*.css',
            options: {
              singleQuote: false,
              useTabs: true,
              tabWidth: 4,
            },
          },
          {
            files: '*.json',
            options: {
              printWidth: 180,
              tabWidth: 4,
              semi: false,
              singleQuote: false,
              bracketSpacing: true,
              trailingComma: 'all',
            },
          },
        ],
      },
    ],

  }
}
