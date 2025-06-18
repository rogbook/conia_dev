declare module 'StoreShopListModule' {
  export interface StoreShopList {
    total: number;
    datas: Shop[];
  }

  export interface Shop {
    id: number;
    name: string;
    description: string;
    address: string;
    work_time: string;
    holiday: string;
    image: string;
    lat: string;
    lng: string;
    tel: string;
    member: {
      id: number;
      name: string;
      email: string;
    };
  }
}
