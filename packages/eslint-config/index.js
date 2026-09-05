// AI Coding
/**
 * @file index.js
 * @description Flat config ESLint dung chung cho ca workspace. Rule kien truc
 * va rule tang DB nam o `rules/` de moi file giu duoc do dai doc duoc.
 */

import js from '@eslint/js';
import globals from 'globals';
import tseslint from 'typescript-eslint';

import { architectureBoundaries } from './rules/architecture-boundaries.js';
import { databaseGuardrails } from './rules/database-guardrails.js';

export const ignores = {
  ignores: ['**/dist/**', '**/node_modules/**', '**/coverage/**', 'scripts/**', 'mvp0/**'],
};

export const baseTypeScript = {
  files: ['**/*.ts'],
  languageOptions: {
    ecmaVersion: 2023,
    sourceType: 'module',
    globals: { ...globals.node },
  },
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/consistent-type-imports': 'error',
    eqeqeq: ['error', 'always'],
    'no-console': 'error',
  },
};

export default [
  ignores,
  js.configs.recommended,
  ...tseslint.configs.recommended,
  baseTypeScript,
  ...architectureBoundaries,
  ...databaseGuardrails,
];
