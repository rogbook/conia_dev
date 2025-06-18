import axios from 'axios';
import { showLogConsole } from '@/utils/common-utils';

const APIURL = 'https://dapi.kakao.com/v2/local/search/address.json?query=';
const RESTAPIKEY = import.meta.env.VITE_KAKAO_RESTAPI_KEY;

export const map = {
  getCoordinate: async (roadAddress: string) => {
    const headers = {
      Authorization: `KakaoAK ${RESTAPIKEY}`,
    };

    try {
      const res = await axios.get(APIURL + roadAddress, { headers: headers });
      return res.data.documents[0];
    } catch (err) {
      showLogConsole(err, 'err');
    }
  },
};
