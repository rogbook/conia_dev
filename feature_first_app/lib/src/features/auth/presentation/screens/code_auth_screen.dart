import 'package:flutter/material.dart';
import '../../services/auth_service.dart';

class CodeAuthScreen extends StatefulWidget {
  final String email;
  const CodeAuthScreen({Key? key, required this.email}) : super(key: key);

  @override
  State<CodeAuthScreen> createState() => _CodeAuthScreenState();
}

class _CodeAuthScreenState extends State<CodeAuthScreen> {
  final TextEditingController _codeController = TextEditingController();
  final AuthService _authService = AuthService();
  bool _isLoading = false;

  void _onVerify() async {
    setState(() => _isLoading = true);
    final code = _codeController.text.trim();
    final isValid = await _authService.verifyCode(widget.email, code);
    setState(() => _isLoading = false);
    if (isValid) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('인증 성공!')));
      // 온보딩 등 다음 단계로 이동 구현 가능
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('인증 코드가 올바르지 않습니다.')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('인증 코드 입력')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _codeController,
              decoration: const InputDecoration(
                labelText: '인증 코드',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.number,
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _onVerify,
                child:
                    _isLoading
                        ? const CircularProgressIndicator(color: Colors.white)
                        : const Text('인증하기'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
