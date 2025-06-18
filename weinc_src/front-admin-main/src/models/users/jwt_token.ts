declare module 'JwtToken' {
  export interface Token {
    id: number; // 회원번호
    name: string; // 회원명
    scope: object; // 회원의 권한
    exp: number; // 토근 만료 시각
  }
}
