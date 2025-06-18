import { fileURLToPath, URL } from 'node:url';

import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };
  return {
    plugins: [vue({ reactivityTransform: true })],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    base: '',
    build: {
      sourcemap: true,
      polyfillDynamicImport: false,
      // rollupOptions: {
      //   output: {
      //     entryFileNames: 'assets/js/[name]-[hash].js',
      //     chunkFileNames: 'assets/js/[name]-[hash].js',
      //     assetFileNames: assetInfo => {
      //       // @ts-ignore
      //       let extType = assetInfo.name.split('.').at(1);
      //       // @ts-ignore
      //       if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
      //         extType = 'img';
      //       }
      //       return `assets/${extType}/[name]-[hash][extname]`;
      //     },
      //   },
      // },
    },
    server: {
      hmr: {
        overlay: process.env.VITE_RUN_MODE !== 'PROD',
      },
      proxy: {
        '/naver-issue-token': {
          target: 'https://nid.naver.com/oauth2.0/token',
          changeOrigin: true,
          rewrite: path => path.replace(/^\/naver-issue-token/, ''),
        },
        '/naver-get-token': {
          target: 'https://openapi.naver.com/v1/nid/me',
          changeOrigin: true,
          rewrite: path => path.replace(/^\/naver-get-token/, ''),
        },
        '/payco-issue-token': {
          target: 'https://id.payco.com/oauth2.0/token',
          changeOrigin: true,
          rewrite: path => path.replace(/^\/payco-issue-token/, ''),
        },
        '/payco-get-token': {
          target: 'https://apis-payco.krp.toastoven.net/payco/friends/find_member_v2.json',
          changeOrigin: true,
          rewrite: path => path.replace(/^\/payco-get-token/, ''),
        },
      },
    },
  };
});
