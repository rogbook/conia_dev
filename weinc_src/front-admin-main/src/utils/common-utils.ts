import Swal from 'sweetalert2';
import type { SweetAlertIcon } from 'sweetalert2';
import { computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { AxiosError } from 'axios';
import router from '@/router';
import { useModalStore } from '@/stores/modal';

export const showAlert = (contents: string, icon: SweetAlertIcon = 'success', callback?: () => void) => {
  Swal.fire({ html: contents.replace('\n', '<br/>'), icon: icon, allowEnterKey: false, allowEscapeKey: false, allowOutsideClick: false }).then(() => {
    if (callback) {
      callback();
    }
  });
};

export const showConfirm = (contents: string, callback: () => void, cancel?: () => void) => {
  Swal.fire({
    html: contents.replace('\n', '<br/>'),
    showConfirmButton: true,
    confirmButtonText: '확인',
    showCancelButton: true,
    cancelButtonText: '취소',
    icon: 'question',
    allowEnterKey: false,
    allowEscapeKey: false,
    allowOutsideClick: false,
  }).then(result => {
    if (result.value) {
      callback();
    } else {
      if (cancel) {
        cancel();
      }
    }
  });
};

export const showConfirmInput = (contents: string, ph: string, callback: (res: string) => void, cancel?: () => void) => {
  Swal.fire({
    html: contents.replace('\n', '<br/>'),
    showConfirmButton: true,
    confirmButtonText: '확인',
    showCancelButton: true,
    cancelButtonText: '취소',
    icon: 'question',
    input: 'text',
    inputPlaceholder: ph,
    allowEnterKey: false,
    allowEscapeKey: false,
    allowOutsideClick: false,
  }).then(result => {
    if (result.value) {
      callback(result.value);
    } else {
      if (cancel) {
        cancel();
      }
    }
  });
};

export const convertProductLog = (value: string) => {
  interface attr {
    [key: string]: string;
  }
  const obj: attr = {
    member_id: '정산대상자',
    name: '상품명',
    type: '타입',
    status: '상태',
    view_yn: '노출여부',
    code: '상품코드',
    summary: '간략설명',
    keyword: '검색어',
    contents: '내용',
    tax: '과세여부',
    min_purchase_limit: '최소 구매 수량',
    max_purchase_limit: '최대 구매 수량',
    adult: '성인인증',
    ipcc_yn: '개인통관번호 여부',
    cancel_yn: '청약철회',
    confirm: '관리자 승인 여부',
    video: '동영상 링크',
    memo: '메모',
    common_info_id: '공통정보 id',
    shipping_info_id: '배송그룹 id',
    inven_use: '간편 재고 사용 여부',
    coupon_yn: '쿠폰 사용 여부',
    option_use: '옵션 사용 여부',
    barcode: '배송그룹 id',
    user_limit: '1인당 구매횟수 제한',
    use_end_period: '비실물 상품 사용 기한 (일)',
    use_end_date: '비실물 상품 사용 기한 (지정 일시)',
    sale_start_date: '판매 가능 시간 시작',
    sale_end_date: '판매 가능 시간 종료',
    sale_start_time: '판매 가능 일(시각) 시작',
    sale_end_time: '판매 가능 일(시각) 종료',
    tel: '전화번호',
    address: '주소',
    address_detail: '주소 상세',
    subtitle: '부제목',
    view_inventory: '재고 노출여부',
    view_end_time: '판매 종료시간 노출여부',
    option_id: '옵션 id',
    supply_price: '공급가',
    origin_price: '정상가',
    selling_price: '판매가',
    weight: '무게',
    pg_provider: '결제수단 제한',
    use_place: '이용가능 매장',
    user_limit_reset: '1인당 구매횟수 제한 초기화 주기',
    count: '재고',
    safe_count: '안전재고',
    use_acc_qty: '누적수량 재고사용 여부',
    day_able_count: '일처리가능수량',
    default_yn: '옵션 사용 여부',
    option_title: '옵션 제목',
    option_1: '옵션값',
    option_code_1: '옵션코드',
    resale: '사입여부',
  };
  if (!obj[value]) return value;
  return obj[value];
};

export const convertStoreLog = (value: string) => {
  interface attr {
    [key: string]: string;
  }

  const obj: attr = {
    title: '제목',
    contents: '내용',
    link: '링크',
    status: '설정',
    logo_pc: 'pc로고',
    logo_mobile: '모바일로고',
    favicon: '파비콘',
    type: '공개설정',
    able_target_use: '회원검증 방식설정',
    dupl_store: '공통몰 사용설정',
    info: '정보',
    name: '테마명',
    description: '테마내용',
    top_visible: '상단메뉴 노출',
    layout: '레이아웃',
    use_layout: '레이아웃 사용여부',
    sort: '순서',
    view_start_date: '시작일',
    view_end_date: '종료일',
    menu_visible: '메뉴 노출여부',
    view_type: '노출타입',
    view_end_content: '기간지난 콘텐츠 노출여부',
    pin: '상위고정',
    duplicate: '하위상점 표시여부',
    image: '이미지',
    img: '이미지',
    start_date: '시작일',
    end_date: '종료일',
    confirm: '승인여부',
    exclude_menu: '마이메뉴 설정',
    verify_code: '회원검증 고정코드',
    group: '상점 그룹 지정',
    prd_pg_opt_use: '상품별 결제수단 옵션 사용여부',
    meal_opt_use: '식권 결제 옵션 사용 여부',
    meal_opt_limit_use: '식권 결제 사용시간 제한 사용 여부',
    meal_opt_limit_time: '식권 결제 사용시간 제한 시간 정보',
    meal_opt_cancel_use: '식권 결제 일괄 취소 기능 사용 여부',
    keyword: '검색어',
  };
  if (!obj[value]) return value;
  return obj[value];
};

export const convertOrderStatus = (status: string, isLog: boolean = false): string => {
  switch (status) {
    case 'PW':
      return '입금대기';
    case 'PU':
      return '부분사용';
    case 'PD':
      return '결제완료';
    case 'CD':
      return '결제취소';
    case 'DW':
      return '상품준비중';
    case 'DN':
      return '배송중';
    case 'DC':
      return '배송완료';
    case 'DD':
      return '출고지연';
    case 'CP':
      return '구매확정';
    case 'AR':
      return '관리자환불';
    case 'RTR':
      return '반품요청';
    case 'RTN':
      return '반품진행중';
    case 'RTC':
      return '반품완료';
    case 'EXR':
      return '교환요청';
    case 'EXN':
      return '교환진행중';
    case 'EXC':
      return '교환완료';
    case 'EXP':
      return '유효기간만료';
    case 'RFR':
      return '반품요청';
    case 'RFN':
      return '반품진행중';
    case 'RFC':
      return '반품완료';
    default:
      if (isLog === true) return status;
      return '-';
  }
};

export const convertPartner = (value: string = '') => {
  switch (value) {
    case 'admin':
      return '관리자';
    case 'customer':
      return '일반회원';
    case 'partner':
      return '파트너 전체';
    case 'partner_CO':
      return 'CO';
    case 'partner_MC':
      return 'MC';
    case 'partner_MC-V':
      return 'MC-V';
    case 'partner_PA':
      return 'PA';
    case 'partner_PA-S':
      return 'PA-S';
    default:
      return '-';
  }
};

export const dateTimeFormatConverter = (date: string | Date): string => {
  const d = new Date(date);

  const year = d.getFullYear();
  const month = d.getMonth() + 1 > 9 ? (d.getMonth() + 1).toString() : '0' + (d.getMonth() + 1);
  const day = d.getDate() > 9 ? d.getDate().toString() : '0' + d.getDate().toString();
  const hour = d.getHours() > 9 ? d.getHours().toString() : '0' + d.getHours().toString();
  const min = d.getMinutes() > 9 ? d.getMinutes().toString() : '0' + d.getMinutes().toString();

  return year + '. ' + month + '. ' + day + ' ' + hour + ':' + min;

  // d.setTime(d.getTime());
  // return d.toLocaleString('ko-KR', { hour12: false, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
};
/** 로그인 한 사용자의 클래스 */
export const getUserClassStr = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

export const apiResponseCheck = (res: any, callback?: () => void, errorCallBack?: (err?: number) => void, detail: boolean = false) => {
  if (res instanceof AxiosError) {
    const error = res.response?.data;
    if (error?.msg) {
      let msg = error.msg;
      // M12 상세 에러 문구 추가
      if (error?.detail?.includes('M12') || detail) {
        msg = msg.concat(`<br/>(${error.detail})`);
      }
      showAlert(`<span class="text-danger">${msg}</span>\n관리자에게 문의해주세요.`, 'warning', () => {
        if (errorCallBack) {
          errorCallBack(res.response?.status);
        } else {
          if (res.response?.status === 403) {
            if (window.history.length > 1) {
              router.back();
            } else {
              router.replace('/');
            }
          }
        }
      });
    } else {
      if (res.code === 'ECONNABORTED' || res.response?.status === 408) {
        showAlert(`응답 대기 시간이 만료되었습니다.`, 'error', () => {
          window.location.reload();
        });
      } else {
        showAlert(`오류가 발생하였습니다.\n관리자에게 문의해주세요. ${res?.response?.status ? `[${res.response.status}]` : ''}`, 'error');
      }
    }
  } else {
    if (callback) {
      callback();
    }
  }
};

export const checkPermission = (permission_code: string): boolean => {
  if (useUserStore().user.admin === 'Y') {
    return true;
  }
  const scopes: any = useUserStore().user.scopes;
  return scopes ? Object.keys(scopes).includes(permission_code) : false;
};

export const showLogConsole = (data: any, type: string = 'log') => {
  if (import.meta.env.VITE_CONSOLE_LOG === 'true') {
    switch (type) {
      case 'info':
        console.info(data);
        break;
      case 'warn':
      case 'warning':
        console.warn(data);
        break;
      case 'err':
      case 'error':
        console.error(data);
        break;
      default:
        console.log(data);
    }
  }
};

export const showModal = (modalId: string) => {
  //@ts-ignore
  window.$(`#${modalId}`).modal('show');
  if (!useModalStore().getModalIdArr.includes(modalId)) useModalStore().addModalId(modalId);
};
export const hideModal = (modalId: string) => {
  //@ts-ignore
  window.$(`#${modalId}`).modal('hide');
};

export const convertPgType = (kind: string = ''): string => {
  switch (kind) {
    case 'card':
      return '신용카드';
    case 'vbank':
      return '가상계좌';
    case 'bank':
      return '실시간이체';
    case 'point':
      return '포인트';
    default:
      return kind;
  }
};

export const isAdmin = computed(() => {
  return useUserStore().user.admin === 'Y';
});
