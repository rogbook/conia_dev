function loadScript(src: string) {
  // eslint-disable-line no-param-reassign
  return new Promise(function (resolve, reject) {
    let shouldAppend = false;
    // @ts-ignore
    let el: HTMLScriptElement = document.querySelector('script[src="' + src + '"]');
    if (!el) {
      el = document.createElement('script');
      el.type = 'text/javascript';
      el.async = true;
      el.src = src;
      shouldAppend = true;
    } else if (el.hasAttribute('data-loaded')) {
      resolve(el);
      return;
    }

    el.addEventListener('error', reject);
    el.addEventListener('abort', reject);
    el.addEventListener('load', function loadScriptHandler() {
      //@ts-ignore
      el.setAttribute('data-loaded', true);
      resolve(el);
    });

    if (shouldAppend) document.head.appendChild(el);
  });
}

function unloadScript(src: string) {
  // eslint-disable-line no-param-reassign
  return new Promise(function (resolve, reject) {
    const el = document.querySelector('script[src="' + src + '"]');

    if (!el) {
      reject();
      return;
    }
    document.head.removeChild(el);
    //@ts-ignore
    resolve();
  });
}

export { unloadScript, loadScript };

const plugin = {
  //@ts-ignore
  install: function (app) {
    app.config.globalProperties.$loadScript = loadScript;
    app.config.globalProperties.$unloadScript = unloadScript;
  },
};

export default plugin;
