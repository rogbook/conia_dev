import apis from '@/apis';
import { AxiosError } from 'axios';
import { showAlert } from './common-utils';

// ✅ 여기부터가 API 요청 가이드 샘플을 가져온 것
export default class UploadAdapter {
  url?: string;
  loader?: any;
  constructor(loader: any, url?: string) {
    // The file loader instance to use during the upload.
    this.loader = loader;
    if (url) {
      this.url = url;
    }
  }

  // Starts the upload process.
  upload() {
    const data = new FormData();
    const allowed_extensions = ['png', 'jpg', 'jpeg', 'ico', 'svg', 'gif'];

    return this.loader.file.then(
      //@ts-ignore
      file =>
        new Promise((resolve, reject) => {
          const fileExtension = file.name.split('.').pop();
          const isAllow = allowed_extensions.includes(fileExtension);

          if (!isAllow) {
            reject();
            showAlert('이미지 형식의 파일만 업로드 할 수 있습니다.', 'warning');
            return;
          }

          if (file.size > 20 * 1024 * 1024) {
            reject();
            showAlert('업로드 할 수 있는 이미지의 크기는 20MB 이하입니다.', 'warning');
            return;
          }

          data.append('file', file);

          if (this.url) {
            apis.common
              .uploadImage(this.url, data)
              .then(result => {
                if (result instanceof AxiosError) {
                  reject(result.message);
                } else {
                  resolve({ default: result.uri });
                }
              })
              .catch(err => {
                reject();
                showAlert('이미지 업로드에 실패했습니다', 'warning');
              });
          } else {
            apis.product
              .uploadForExplanInfo(data)
              .then(result => {
                if (result instanceof AxiosError) {
                  reject(result.message);
                } else {
                  resolve({ default: result.uri });
                }
              })
              .catch(err => {
                reject();
                showAlert('이미지 업로드에 실패했습니다', 'warning');
              });
          }
        }),
    );
  }
}
