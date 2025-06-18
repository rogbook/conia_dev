CERT_SMS: str = "인증번호 {code}"

BULK_ADD_CUSTOMER_MAIL_BODY = """
<!DOCTYPE html>
<html lang='ko'>
<head>
  <meta http-equiv='Content-Type' content='text/html charset=UTF-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Welcome to Weinc</title>
</head>
<style>
  @font-face {{
      font-family: 'Pretendard';
      src: url('https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/font/Pretendard-Regular.woff2') format('woff2');
      src: url('https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/font/Pretendard-Regular.woff') format('woff');
      font-weight: 400;
      font-style: normal;
  }}

  *{{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    letter-spacing: -0.32px;
    line-height: normal;
  }}
  body{{
    font-family: 'Pretendard', 'AppleSDGothicNeo', sans-serif;
  }}
  h3{{font-size: 20px;}}
</style>
<body>
  <div><img src='https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/img/topBanner.png' alt='topBanner' style='width: 100%;'></div>
  <div style='width: 90%; margin: auto; padding-bottom:60px;'>  
    <div style='padding: 30px 0; border-bottom:1px solid #000; text-align: center;'><img src='https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/img/BI.png' alt='weinc' style='width:90px;'></div>
    <div style='margin-top: 60px;'>
      <h3>반가워요, {name}님!</h3>
      <div style='margin-top:10px; line-height: 24px;'>윙크(weinc)와 함께 회사 주변 매장에서 <span style='color: #ff5f00;'>매일 10~15% 할인 혜택</span>을 누려보세요.</div>
    </div>
    <div style='margin-top: 30px;'>
      <h3>🎉 몰 오픈 기념! 윌컴 선물로 만나는 첫 혜택의 순간!</h3>
      <div style='margin-top: 10px; line-height: 24px;'>
        <span style='color: #ff5f00;'>100원 딜부터 다양한 할인 상품</span>이 준비되어 있어요.<br>
        지금 바로 <span style='color: #ff5f00;'>윙크</span>에서 확인하고 혜택을 빠르게 경험하세요!
      </div>
    </div>
    <div style='margin-top: 50px;'>
      <a 
        target='_blank'
        href='https://applink.coniaworld.com/'
        style='display: block; width:100%; max-width: 360px; margin: auto; padding: 20px 0; background: #000; color: #fff; text-align: center; text-decoration: none; font-size: 24px;'
        >
        🧡 앱 설치하고 첫 혜택 받기
      </a>
    </div>
    <div style='margin-top: 20px; font-size: 14px; color: #a0a0a0; text-align: center;'>* Google Play 또는 App Store에서 ‘윙크몰’을 검색하세요.</div>
    <div style='margin-top: 50px;'>
      <h3 style='margin-bottom: 14px;'>🔐 로그인 정보</h3>
      <div style='margin-bottom: 14px;'>아이디 : {email}</div>
      <div style='margin-bottom: 14px;'>비밀번호 : {password}</div>
      <div style='margin-top: 20px; font-size: 14px; color: #a0a0a0;'>
        * 계정 보안을 위해 로그인 후 꼭 비밀번호를 변경해주세요.<br>
        [마이메뉴] - [개인정보 수정] - [비밀번호 변경]
      </div>
    </div>
    <div style='margin-top: 30px;'>윙크를 자주 이용할수록 더 큰 혜택과 <span style='color: #FF5F00;'>특별한 이벤트</span>가 기다리고 있으니, 앞으로 자주 만나요!</div>
    <div style='margin: 60px 0;'>
      <a
        target='_blank'
        href='https://drive.google.com/file/d/1lMSuBZP4xipGuw_XdNT_LW864Rooa8_q/view?usp=drive_link'
        style='display: block; width:100%; max-width: 360px; margin: auto; padding: 20px 0; background: #FF5F00; color: #fff; text-align: center; text-decoration: none; font-size: 24px;'
        >
        <span>📖 윙크 100% 활용하기</span>
      </a>
    </div>
    <div style='font-size: 14px; color: #a0a0a0;'>본 메일은 발신전용이며 회신이 불가능합니다. 문의사항은 로그인 후 고객센터를 이용해 주세요.</div>
  </div>
</body>
</html>
"""


PASSWD_RESET = """
<!DOCTYPE html>
<html lang='ko'>
<head>
  <meta http-equiv='Content-Type' content='text/html charset=UTF-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Welcome to Weinc</title>
</head>
<style>
  @font-face {{
      font-family: 'Pretendard';
      src: url('https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/font/Pretendard-Regular.woff2') format('woff2');
      src: url('https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/font/Pretendard-Regular.woff') format('woff');
      font-weight: 400;
      font-style: normal;
  }}

  *{{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    letter-spacing: -0.32px;
    line-height: normal;
  }}
  body{{
    font-family: 'Pretendard', 'AppleSDGothicNeo', sans-serif;
  }}
  h3{{font-size: 20px;}}
</style>
<body>
  <div><img src='https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/img/topBanner.png' alt='topBanner' style='width: 100%;'></div>
  <div style='width: 90%; margin: auto; padding-bottom:60px;'>  
    <div style='padding: 30px 0; border-bottom:1px solid #000; text-align: center;'><img src='https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/img/BI.png' alt='weinc' style='width:90px;'></div>
    <div style='margin-top: 60px;'>
      <h3>안녕하세요, {name}님!</h3>
      <div style='margin-top:10px; line-height: 24px;'>
        먼저 [윙크]에 가입해 주셔서 진심으로 감사드립니다. 지난번 비밀번호 설정 중 불편함이 있으셨다면 정말 죄송합니다.<br>
        시스템 개선 과정에서 약간의 오류가 있었고, 이를 해결하여 고객님의 비밀번호를 안전하게 업데이트했습니다.<br><br>
        지금부터 <span style='color: #ff5f00;'>윙크</span>에 로그인하시어 모든 혜택을 마음껏 누려보세요! 다시 즐겁게 서비스를 이용하실 수 있도록 최선을 다하겠습니다.
      </div>
    </div>
    <div style='margin-top: 50px;'>
      <h3 style='margin-bottom: 14px;'>🔐 로그인 정보</h3>
      <div style='margin-bottom: 14px;'>아이디 : {email}</div>
      <div style='margin-bottom: 14px;'>비밀번호 : 1234</div>
    </div>
    <div style='margin-top: 30px;'>
      혹시 비밀번호나 다른 사항에 대해 궁금한 점이 있으시면 언제든지 편하게 문의해 주세요. <span style='color: #FF5F00;'>윙크</span>는 고객님의 만족을 위해 늘 준비되어 있습니다!
    </div>
    <div style='margin-top: 60px;'>
      <a 
        target='_blank'
        href='https://applink.coniaworld.com/'
        style='display: block; width:100%; max-width: 360px; margin: auto; padding: 20px 0; background: #000; color: #fff; text-align: center; text-decoration: none; font-size: 24px;'
        >
        윙크 혜택 받기 🧡
      </a>
    </div>
    <div style='margin: 30px 0;'>
      <a
        target='_blank'
        href='http://pf.kakao.com/_JxnZxkxj'
        style='display: block; width:100%; max-width: 360px; margin: auto; padding: 20px 0; background: #FF5F00; color: #fff; text-align: center; text-decoration: none; font-size: 24px;'
        >
        카카오톡 문의하기 💬
      </a>
    </div>
    <div>감사합니다.<br><br>윙크 드림</div>
    <div style='margin-top:60px; font-size: 14px; color: #a0a0a0;'>본 메일은 앱에 로그인 이력은 있으나 구매 내역이 없는 고객님께 발송되었습니다. 다만, 발송 시점에 따라 본 메일을 받으신 고객님께서도 변경된 비밀번호로 로그인해 주세요.</div>
  </div>
</body>
</html>
"""


PASSWORD_RESET_CUSTOMER = """
<!DOCTYPE html>
<html lang='ko'>
<head>
  <meta http-equiv='Content-Type' content='text/html charset=UTF-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Welcome to Weinc</title>
</head>
<style>
  @font-face {{
      font-family: 'Pretendard';
      src: url('https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/font/Pretendard-Regular.woff2') format('woff2');
      src: url('https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/font/Pretendard-Regular.woff') format('woff');
      font-weight: 400;
      font-style: normal;
  }}

  *{{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    letter-spacing: -0.32px;
    line-height: normal;
  }}
  body{{
    font-family: 'Pretendard', 'AppleSDGothicNeo', sans-serif;
  }}
  h3{{font-size: 20px;}}
</style>
<body>
  <div><img src='https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/img/passwd_reset_top_banner.png' alt='topBanner' style='width: 100%;'></div>
  <div style='width: 90%; margin: auto; padding-bottom:60px;'>  
    <div style='padding: 30px 0; border-bottom:1px solid #000; text-align: center;'><img src='https://conia-public.s3.ap-northeast-2.amazonaws.com/email-form/img/BI.png' alt='weinc' style='width:90px;'></div>
    <div style='margin-top: 60px;'>
      <h3>안녕하세요, 윙크입니다.</h3>
      <div style='margin-top:10px; line-height: 24px;'>
        회원님의 원활한 로그인을 위해 임시 비밀번호를 발급해 드렸습니다. 아래 정보를 확인하시고, 로그인 후 비밀번호를 변경해 주세요.
      </div>
    </div>
    <div style='margin-top: 50px;'>
      <h3 style='margin-bottom: 14px;'>🔐 로그인 정보</h3>
      <div style='margin-bottom: 14px;'>아이디(이메일) : {email}</div>
      <div style='margin-bottom: 14px;'>임시 비밀번호 : {password}</div>
      <div style='margin-top: 20px; font-size: 14px; color: #a0a0a0;'>
        * 계정 보안을 위해 로그인 후 꼭 비밀번호를 변경해주세요.<br>
        [마이메뉴] - [개인정보 수정] - [비밀번호 변경]
      </div>      
    </div>
    <div style="margin-top:60px;">문의사항이 있으시면 언제든 고객센터로 연락해 주세요.<br>오늘도 윙크와 함께 즐거운 하루 보내세요!</div>
    <div style='margin-top: 60px; text-align: center;'>
      <a
        target='_blank'
        href='http://pf.kakao.com/_JxnZxkxj'
        style='display: inline-block; width:100%; max-width: 360px; margin: 6px; padding: 20px 0; background: #000; color: #fff; text-align: center; text-decoration: none; font-size: 24px;'
        >
        카카오톡 문의하기 💬
      </a>
      <a
        target='_blank'
        href='https://drive.google.com/file/d/1lMSuBZP4xipGuw_XdNT_LW864Rooa8_q/view'
        style='display: inline-block; width:100%; max-width: 360px; margin: 6px; padding: 20px 0; background: #FF5F00; color: #fff; text-align: center; text-decoration: none; font-size: 24px;'
        >
        <span>윙크 사용 가이드 📖</span>
      </a>      
    </div>
  </div>
</body>
</html>
"""