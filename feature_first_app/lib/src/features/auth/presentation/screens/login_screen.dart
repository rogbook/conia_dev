import 'package:flutter/material.dart';
import '../../services/auth_service.dart';
import 'code_auth_screen.dart';
import 'package:url_launcher/url_launcher.dart'
    show canLaunch, launch, LaunchMode, launchUrl;
import 'package:uni_links/uni_links.dart' show uriLinkStream;
import 'dart:async';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _emailController = TextEditingController();
  final AuthService _authService = AuthService();
  bool _isLoading = false;
  String? _authType;
  String? _companyName;
  String? _idpUrl;
  StreamSubscription<Uri?>? _sub;

  @override
  void dispose() {
    _sub?.cancel();
    _emailController.dispose();
    super.dispose();
  }

  void _listenDeepLink() {
    _sub = uriLinkStream.listen((Uri? uri) {
      if (uri != null && uri.scheme == 'myapp' && uri.host == 'auth') {
        final token = uri.queryParameters['token'];
        if (token != null) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text('SSO 인증 성공! 토큰: $token')));
          // 실제 온보딩/로그인 처리 구현 가능
        }
      }
    }, onError: (err) {});
  }

  void _onContinue() async {
    setState(() => _isLoading = true);
    final email = _emailController.text.trim();
    final authType = await _authService.checkAuthType(email);
    setState(() => _authType = authType);
    if (authType == 'CODE') {
      setState(() => _isLoading = false);
      Navigator.of(
        context,
      ).push(MaterialPageRoute(builder: (_) => CodeAuthScreen(email: email)));
    } else if (authType == 'SSO') {
      final ssoInfo = await _authService.getSsoInfo(email);
      setState(() {
        _companyName = ssoInfo['companyName'];
        _idpUrl = ssoInfo['idpUrl'];
        _isLoading = false;
      });
      _listenDeepLink();
    } else {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('인증 방식: $authType')));
    }
  }

  void _onSsoLogin() async {
    if (_idpUrl != null && await canLaunch(_idpUrl!)) {
      await launch(_idpUrl!, forceSafariVC: false, forceWebView: false);
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('SSO URL을 열 수 없습니다.')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('로그인')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child:
            _authType == 'SSO'
                ? Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      '${_companyName ?? ''} 계정으로 로그인',
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _onSsoLogin,
                        child:
                            _isLoading
                                ? const CircularProgressIndicator(
                                  color: Colors.white,
                                )
                                : Text('${_companyName ?? ''} 계정으로 로그인'),
                      ),
                    ),
                  ],
                )
                : Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    TextField(
                      controller: _emailController,
                      decoration: const InputDecoration(
                        labelText: '기업 이메일 주소',
                        border: OutlineInputBorder(),
                      ),
                      keyboardType: TextInputType.emailAddress,
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _onContinue,
                        child:
                            _isLoading
                                ? const CircularProgressIndicator(
                                  color: Colors.white,
                                )
                                : const Text('계속하기'),
                      ),
                    ),
                  ],
                ),
      ),
    );
  }
}

// 임시 mock HRD 함수 (실제 서비스 연결 전)
// Future<String> mockCheckAuthType(String email) async {
//   await Future.delayed(const Duration(seconds: 1));
//   if (email.endsWith('@sso.com')) {
//     return 'SSO';
//   } else if (email.endsWith('@code.com')) {
//     return 'CODE';
//   } else {
//     return 'UNKNOWN';
//   }
// }
