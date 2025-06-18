import {createApp, nextTick} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.prod.js'
import ElementProduct from "./ElementProduct.js";
import ElementProductList from "./ElementProductList.js";


const app = createApp({
  components: {
    'element-product': ElementProduct,
    'element-product-list': ElementProductList
  },
  mounted() {
    // 모든 컴포넌트가 마운트된 후 추가 작업
    nextTick(() => {
      this.addSwiper();
      this.passwordVisibilityToggle();
      this.productGallery();
    });
  },
  methods: {
    addSwiper() {
      new Swiper(".swiper_number", {
        autoHeight: "false",
        autoplay: {
          delay: 3500,
          disableOnInteraction: false,
        },
        loop: "true",
        effect: "fade",
        pagination: {
          el: ".swiper-pagination",
          type: "fraction",
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        }
      });
    },
    passwordVisibilityToggle() {
      let elements = document.querySelectorAll('.password-toggle');

      elements.forEach(function (element) {
        let passInput = element.querySelector('.form-control');
        let passToggle = element.querySelector('.password-toggle-btn');

        passToggle.addEventListener('click', function (e) {
          if (e.target.type !== 'checkbox') return;

          passInput.type = e.target.checked ? 'text' : 'password';
        }, false);
      });
    },
    productGallery() {
      const galleries = document.querySelectorAll('.product-gallery');

      galleries.forEach(gallery => {
        const thumbnails = gallery.querySelectorAll('.product-gallery-thumblist-item:not(.video-item)');
        const previews = gallery.querySelectorAll('.product-gallery-preview-item');
        const videos = gallery.querySelectorAll('.product-gallery-thumblist-item.video-item');

        thumbnails.forEach((thumbnail, index) => {
          thumbnail.addEventListener('click', e => {
            e.preventDefault();
            previews.forEach(preview => preview.classList.remove('active'));
            thumbnails.forEach(thumb => thumb.classList.remove('active'));

            thumbnail.classList.add('active');
            const target = gallery.querySelector(thumbnail.getAttribute('href'));
            if (target) {
              target.classList.add('active');
            }
          });
        });

        videos.forEach(video => {
          lightGallery(video, {
            selector: 'this',
            download: false,
            videojs: true,
            youtubePlayerParams: {
              modestbranding: 1,
              showinfo: 0,
              rel: 0,
              controls: 0
            },
            vimeoPlayerParams: {
              byline: 0,
              portrait: 0,
              color: 'fe696a'
            }
          });
        });
      });
    }
  },
});
app.mount('#app');