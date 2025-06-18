export const arrayToStringWithComma = (array: any[], propertyName: string, standard = ',') => array.reduce((prev, cur) => prev + cur[propertyName] + standard, '').slice(0, -standard.length);

export default {
  arrayToStringWithComma,
};
