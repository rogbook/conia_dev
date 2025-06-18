export enum DETECTED_M_TYPE {
  Android = 'AOS',
  IOS = 'IOS',
  Mobile = 'M',
  Pc = 'P',
}

export default (): DETECTED_M_TYPE => {
  const ua = navigator.userAgent;
  if (/android/i.test(ua)) {
    return DETECTED_M_TYPE.Android;
  } else if (/iPad|iPhone|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) {
    return DETECTED_M_TYPE.IOS;
  } else if (/webOS|BlackBerry|Windows Phone/.test(ua)) {
    return DETECTED_M_TYPE.Mobile;
  }
  return DETECTED_M_TYPE.Pc;
};
