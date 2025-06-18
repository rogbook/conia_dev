declare module 'ShopInfoModule' {
  export interface Shop {
    id: number;
    name: string;
    subtitle?: string;
    description: string;
    address: string;
    address_detail: string;
    work_time: string;
    holiday: string;
    image: string;
    lat: string;
    lng: string;
    tel: string;
    badges: Badge[];
  }

  export interface Badge {
    id: number;
    name: string;
    color: string;
    img: string;
    shape: string;
  }
}
