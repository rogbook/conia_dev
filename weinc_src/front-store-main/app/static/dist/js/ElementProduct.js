import { onMounted , ref, computed, watch } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.prod.js';

export const ElementProduct = {
	props: ['store_code','store_type','exclude_menu','current_datetime','current_time','prod','user'],
	setup(props) {
		const store_code = ref(props.store_code);
		const store_type = ref(props.store_type);
		const exclude_menu = ref(props.exclude_menu);
		const current_datetime = ref(props.current_datetime);
		const current_time = ref(props.current_time);
		const prod = ref(props.prod);
		const user = ref(props.user);
		const pInfo = ref({});
		const pStatus = ref();

		const daysVal = ref(0);
		const hoursVal = ref(0);
		const minutesVal= ref(0);
		const secondsVal = ref(0);
		const timer = ref(null);

		watch(pInfo, () => {
			if(checkTimer.value == true){
				countdown(); 
			}
		});

		const checkTimer = computed(() => {
			if(pInfo.value.view_end_time == 'Y' && (pInfo.value.sale_end_date && (pInfo.value.sale_end_date.replace('T', ' ') > current_datetime.value))){
				return true
			}else{
				return false
			}
		});
		const checkEndDate = computed(() => {
			if( pInfo.value.sale_start_date && (pInfo.value.sale_start_date.replace('T', ' ') > current_datetime.value) ){
				return 'A'
			}else if((pInfo.value.sale_start_time && (pInfo.value.sale_start_time > current_time.value)) || (pInfo.value.sale_start_time && pInfo.value.sale_end_time && (pInfo.value.sale_end_time < current_time.value))){
				return 'B'
			}else if(pInfo.value.sale_end_time && (pInfo.value.sale_end_time > current_time.value)){
				return 'C'
			}else{
				return 'D'
			}
		});

		onMounted( async () => {
			if(prod.value.id){
				getProduct();
			}
		});

		const countdown = () => {
			let endDate = '';
			
			switch (checkEndDate.value) {
				case 'A':
					endDate = new Date(pInfo.value.sale_start_date).getTime();
					break;
				case 'B':
					endDate = new Date(add_date_str(pInfo.value.sale_start_time)).getTime();
					break;
				case 'C':
					endDate = new Date(add_date_str(pInfo.value.sale_end_time)).getTime();
					break;
				case 'D':
					endDate = new Date(pInfo.value.sale_end_date).getTime();
					break;
			}
	
			if (isNaN(endDate)) return;
			if(timer.value) clearInterval(timer.value);
			timer.value = setInterval(calculate, 1000);

			function calculate() {
				let startDate = new Date().getTime();
				let timeRemaining = parseInt((endDate - startDate) / 1000);
				if (timeRemaining >= 0) {
					const days = parseInt(timeRemaining / 86400);
					timeRemaining = timeRemaining % 86400;
					const hours = parseInt(timeRemaining / 3600);
					timeRemaining = timeRemaining % 3600;
					const minutes = parseInt(timeRemaining / 60);
					timeRemaining = timeRemaining % 60;
					const seconds = parseInt(timeRemaining);
	

					daysVal.value = parseInt(days, 10);
					hoursVal.value = hours < 10 ? '0' + hours : hours;
					minutesVal.value = minutes < 10 ? '0' + minutes : minutes;
					secondsVal.value = seconds < 10 ? '0' + seconds : seconds;
				} else {
					// 타이머가 끝난 경우 동작
					clearInterval(timer.value);
					// 종료 후에 수행할 작업을 여기에 추가
				}
			}
		};

		const getProduct = () => {
			axios.get(`/api/product?store_code=${store_code.value}&product_id=${prod.value.id}`)
      .then((res)=>{	
				pInfo.value = res.data;
				getProdStatus();
      }).catch((err)=>{
        console.log(err);
      });
		};
		const getProdStatus = () => {
			if(pInfo.value.sale_start_date && (pInfo.value.sale_start_date.replace('T', ' ') > current_datetime.value)) pStatus.value = 'PT';
			if(pInfo.value.sale_end_date && (pInfo.value.sale_end_date.replace('T', ' ') < current_datetime.value)) pStatus.value = 'PT';
			if(pInfo.value.sale_start_time && (pInfo.value.sale_start_time > current_time.value)) pStatus.value = 'PT';
			if(pInfo.value.sale_end_time && (pInfo.value.sale_end_time < current_time.value)) pStatus.value = 'PT';
			if(pInfo.value.use_end_date && (pInfo.value.use_end_date.replace('T', ' ') < current_datetime.value)) pStatus.value = 'PT';
		};
		const add_date_str = (time) => {
			if (time) {
        const now = new Date(current_datetime.value);
        const currentTime = now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds();
        const [hours, minutes, seconds] = time.split(':').map(Number);
        const inputTime = hours * 3600 + minutes * 60 + (seconds || 0);

        const formatDate = date => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        
        if (currentTime > inputTime) {
          const tomorrow = new Date(now);
          tomorrow.setDate(now.getDate() + 1);
          return `${formatDate(tomorrow)} ${time}`;
        } else {
          return `${formatDate(now)} ${time}`;
        }
      } else {
        return time;
      }
		}

		return {
			store_code,
			store_type,
			exclude_menu,
			current_datetime,
			current_time,
			prod,
			user,
			pInfo,
			pStatus,
			timer,
			daysVal,
			hoursVal,
			minutesVal,
			secondsVal,
			checkTimer,
			checkEndDate
		}
	},
	template: 
		`
			<div v-if="Object.keys(pInfo).length" class="card product-card h-100 border-0 overflow-hidden">
				<a :href="'/' + store_code + '/product/' + prod.id" class="d-block h-100 text-dark" >
					<div class="position-relative">
						<img v-if="prod.thumbnail" class="w-100 rounded-3" :src="prod.thumbnail" alt=""/>
						<img v-else class="w-100 rounded-3"  :src="pInfo.photos.length ? pInfo.photos[0].uri : ''" alt=""/>

						<div v-if="pInfo.is_sold_out || pInfo.status === 'S'" class="img-disable">
							<span class="fw-bold fs-3">품절</span>
						</div>
						<div v-else-if="pInfo.status === 'P'" class="img-disable">
							<span class="fw-bold fs-3">판매 중지</span>
						</div>
						<div v-else-if="pStatus === 'PT'" class="img-disable">
							<span class="fw-bold fs-3">판매 준비중</span>
						</div>
					</div>

					<div class="item-card-body">
						<div class="item-name-wrap">
							<div v-if="pInfo.brands.length" class="item-shop-name">{{ pInfo.brands[0].name }}</div>
							<div class="item-title ellipsis-2">{{ pInfo.name }}</div>
						</div>

						<div v-if="user || store_type == 'O'" class="item-price-wrap">
							<span v-if="pInfo.product_default.origin_price > pInfo.product_default.selling_price" class="item-discount-per">
								{{ Math.round((pInfo.product_default.origin_price - pInfo.product_default.selling_price)/pInfo.product_default.origin_price * 100) }}%
							</span>

							<div class="item-selling-price">
								{{ pInfo.product_default.selling_price.toLocaleString() }}원
							</div>
							<del v-if="pInfo.product_default.origin_price > pInfo.product_default.selling_price" class="item-discount-price">
								{{ pInfo.product_default.origin_price.toLocaleString() }}원
							</del>
						</div>
						<div v-if="pInfo.subtitle" class="item-subtitle ellipsis-2">{{ pInfo.subtitle }}</div>

						<div v-if="pInfo.badges.length" class="item-badge-wrap">
							<span v-for="(badge, i) in pInfo.badges" :key="i" class="badge badge-shadow" :style="{ backgroundColor: badge.color }">
								{{ badge.name }}
							</span>
						</div>

						<div v-if="checkTimer">
							<div v-if="checkEndDate === 'A'" class="countdown mt-1 text-info fs-xs">
								<div class="d-flex align-items-center gap-1 me-1"><i class="ci-time"></i>판매 시작까지</div>
								<div class="countdown-days m-0 d-flex align-items-baseline">
									<span class="countdown-value">{{daysVal}}</span>
									<span>일&nbsp;</span>
								</div>
								<div class="countdown-hours m-0 d-flex align-items-center">
									<span class="countdown-value">{{hoursVal}}</span>
									<span>:</span>
								</div>
								<div class="countdown-minutes m-0 d-flex align-items-center">
									<span class="countdown-value">{{minutesVal}}</span>
									<span>:</span>
								</div>
								<div class="countdown-seconds m-0 d-flex align-items-center">
									<span class="countdown-value">{{secondsVal}}</span>
								</div>
							</div>
							<div v-else-if="checkEndDate === 'B'" class="countdown mt-1 text-info fs-xs">
								<div class="d-flex align-items-center gap-1 me-1"><i class="ci-time"></i>판매 시작까지</div>
								<div class="countdown-hours m-0 d-flex align-items-center">
									<span class="countdown-value">{{hoursVal}}</span>
									<span>:</span>
								</div>
								<div class="countdown-minutes m-0 d-flex align-items-center">
									<span class="countdown-value">{{minutesVal}}</span>
									<span>:</span>
								</div>
								<div class="countdown-seconds m-0 d-flex align-items-center">
									<span class="countdown-value">{{secondsVal}}</span>
								</div>
							</div>
							<div v-else-if="checkEndDate === 'C'" class="countdown mt-1 text-info fs-xs">
								<div class="d-flex align-items-center gap-1 me-1"><i class="ci-time"></i>판매 종료까지</div>
								<div class="countdown-hours m-0 d-flex align-items-center">
									<span class="countdown-value">{{hoursVal}}</span>
									<span>:</span>
								</div>
								<div class="countdown-minutes m-0 d-flex align-items-center">
									<span class="countdown-value">{{minutesVal}}</span>
									<span>:</span>
								</div>
								<div class="countdown-seconds m-0 d-flex align-items-center">
									<span class="countdown-value">{{secondsVal}}</span>
								</div>
							</div>
							<div v-else class="countdown mt-1 text-info fs-xs">
								<div class="d-flex align-items-center gap-1 me-1"><i class="ci-time"></i>판매 종료까지</div>
								<div class="countdown-days m-0 d-flex align-items-baseline">
									<span class="countdown-value">{{daysVal}}</span>
									<span>일&nbsp;</span>
								</div>
								<div class="countdown-hours m-0 d-flex align-items-center">
									<span class="countdown-value">{{hoursVal}}</span>
									<span>:</span>
								</div>
								<div class="countdown-minutes m-0 d-flex align-items-center">
									<span class="countdown-value">{{minutesVal}}</span>
									<span>:</span>
								</div>
								<div class="countdown-seconds m-0 d-flex align-items-center">
									<span class="countdown-value">{{secondsVal}}</span>
								</div>
							</div>
						</div>

						<div v-if="pInfo.view_inventory == 'Y'" class="mt-1 fs-xs lineH-10 text-danger">
							남은 수량 
							<span v-if="pInfo.inven_cnt && pInfo.inven_cnt > 0">{{ pInfo.inven_cnt }}</span>	
							<span v-else>0</span>개
						</div>
					</div>	
				</a>
			</div>
	`,
}

export default ElementProduct;
