import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:async';
import '../models/game_board.dart';
import '../models/tetromino.dart';
import '../widgets/game_board_widget.dart';
import '../widgets/next_piece_widget.dart';

class GameScreen extends StatefulWidget {
  const GameScreen({Key? key}) : super(key: key);

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  late GameBoard gameBoard;
  late FocusNode _focusNode;
  Timer? _gameTimer;
  static const int _normalSpeed = 1000; // 일반 하강 속도 (1초)
  static const int _fastSpeed = 100; // 빠른 하강 속도 (0.1초)
  bool _isFastFalling = false;
  bool _isGameOver = false;
  late Tetromino _nextPiece;

  @override
  void initState() {
    super.initState();
    _initializeGame();
  }

  void _initializeGame() {
    gameBoard = GameBoard();
    _focusNode = FocusNode();
    _isGameOver = false;
    _isFastFalling = false;
    _nextPiece = Tetromino.createRandom();
    _spawnNewPiece();
    _startGameTimer();
  }

  @override
  void dispose() {
    _gameTimer?.cancel();
    _focusNode.dispose();
    super.dispose();
  }

  void _startGameTimer() {
    _gameTimer?.cancel();
    _gameTimer = Timer.periodic(
      Duration(milliseconds: _isFastFalling ? _fastSpeed : _normalSpeed),
      (timer) {
        if (_isGameOver) {
          timer.cancel();
          return;
        }
        setState(() {
          if (!gameBoard.moveDown()) {
            // 블록이 더 이상 내려갈 수 없으면 새로운 블록 생성
            _spawnNewPiece();
          }
        });
      },
    );
  }

  void _spawnNewPiece() {
    // 현재 다음 블록을 게임 보드에 생성
    if (!gameBoard.spawnPiece(_nextPiece)) {
      _gameOver();
      return;
    }
    // 새로운 다음 블록 생성
    _nextPiece = Tetromino.createRandom();
  }

  void _gameOver() {
    setState(() {
      _isGameOver = true;
    });
  }

  void _restartGame() {
    setState(() {
      _initializeGame();
    });
  }

  void _handleKeyPress(RawKeyEvent event) {
    if (_isGameOver) {
      if (event is RawKeyDownEvent &&
          event.logicalKey == LogicalKeyboardKey.space) {
        _restartGame();
      }
      return;
    }

    if (event is RawKeyDownEvent) {
      setState(() {
        switch (event.logicalKey) {
          case LogicalKeyboardKey.arrowLeft:
            gameBoard.moveLeft();
            break;
          case LogicalKeyboardKey.arrowRight:
            gameBoard.moveRight();
            break;
          case LogicalKeyboardKey.arrowUp:
            gameBoard.rotate();
            break;
          case LogicalKeyboardKey.arrowDown:
            _isFastFalling = true;
            _startGameTimer();
            break;
        }
      });
    } else if (event is RawKeyUpEvent) {
      if (event.logicalKey == LogicalKeyboardKey.arrowDown) {
        setState(() {
          _isFastFalling = false;
          _startGameTimer();
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1A1A1A),
      body: SafeArea(
        child: Center(
          child: RawKeyboardListener(
            focusNode: _focusNode,
            onKey: _handleKeyPress,
            child: SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text(
                      'TETR∞',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 48,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 2,
                        shadows: [
                          Shadow(
                            color: Colors.black26,
                            offset: Offset(0, 2),
                            blurRadius: 4,
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        GameBoardWidget(
                          gameBoard: gameBoard,
                          cellSize: 25.0, // 셀 크기 축소
                        ),
                        const SizedBox(width: 16),
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: const Color(0xFF333333),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'SCORE',
                                style: TextStyle(
                                  color: Colors.white70,
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  letterSpacing: 1,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                '${gameBoard.score}',
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 32,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 16),
                              NextPieceWidget(
                                nextPiece: _nextPiece,
                                cellSize: 12.0, // 셀 크기 축소
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),
                    if (_isGameOver)
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.red.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: Colors.red.withOpacity(0.3),
                            width: 2,
                          ),
                        ),
                        child: Column(
                          children: [
                            const Text(
                              'GAME OVER',
                              style: TextStyle(
                                color: Colors.red,
                                fontSize: 32,
                                fontWeight: FontWeight.bold,
                                letterSpacing: 1,
                              ),
                            ),
                            const SizedBox(height: 8),
                            const Text(
                              'Press SPACE to restart',
                              style: TextStyle(
                                color: Colors.white70,
                                fontSize: 16,
                                letterSpacing: 0.5,
                              ),
                            ),
                          ],
                        ),
                      )
                    else
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.05),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Text(
                          '← → : Move\n↑ : Rotate\n↓ : Fast Fall',
                          style: TextStyle(
                            color: Colors.white70,
                            fontSize: 16,
                            height: 1.5,
                            letterSpacing: 0.5,
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
