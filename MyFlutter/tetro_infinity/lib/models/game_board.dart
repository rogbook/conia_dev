import 'package:flutter/material.dart';
import 'tetromino.dart';

class GameBoard {
  static const int rows = 20;
  static const int columns = 10;
  final List<List<Tetromino?>> board;
  Tetromino? currentPiece;
  int currentX = 0;
  int currentY = 0;
  int score = 0;

  GameBoard()
    : board = List.generate(rows, (_) => List.generate(columns, (_) => null));

  int get height => rows;
  int get width => columns;

  Tetromino? getCell(int x, int y) {
    if (x < 0 || x >= columns || y < 0 || y >= rows) {
      return null;
    }
    return board[y][x];
  }

  // 새로운 블록 생성
  bool spawnPiece(Tetromino piece) {
    currentPiece = piece;
    currentX = (columns - piece.shape[0].length) ~/ 2;
    currentY = 0;

    // 충돌 체크
    if (_checkCollision()) {
      return false;
    }

    return true;
  }

  // 충돌 체크
  bool _checkCollision() {
    if (currentPiece == null) return true;

    for (int y = 0; y < currentPiece!.shape.length; y++) {
      for (int x = 0; x < currentPiece!.shape[y].length; x++) {
        if (currentPiece!.shape[y][x]) {
          int boardX = currentX + x;
          int boardY = currentY + y;

          if (boardX < 0 ||
              boardX >= columns ||
              boardY < 0 ||
              boardY >= rows ||
              board[boardY][boardX] != null) {
            return true;
          }
        }
      }
    }
    return false;
  }

  // 블록 이동
  bool moveLeft() {
    if (currentPiece == null) return false;
    currentX--;
    if (_checkCollision()) {
      currentX++;
      return false;
    }
    return true;
  }

  bool moveRight() {
    if (currentPiece == null) return false;
    currentX++;
    if (_checkCollision()) {
      currentX--;
      return false;
    }
    return true;
  }

  bool moveDown() {
    if (currentPiece == null) return false;
    currentY++;
    if (_checkCollision()) {
      currentY--;
      _lockPiece();
      return false;
    }
    return true;
  }

  // 블록 회전
  void rotate() {
    if (currentPiece == null) return;
    currentPiece!.rotate();
    if (_checkCollision()) {
      // 회전이 불가능한 경우 원래대로 되돌림
      for (int i = 0; i < 3; i++) {
        currentPiece!.rotate();
      }
    }
  }

  // 블록 고정
  void _lockPiece() {
    if (currentPiece == null) return;

    for (int y = 0; y < currentPiece!.shape.length; y++) {
      for (int x = 0; x < currentPiece!.shape[y].length; x++) {
        if (currentPiece!.shape[y][x]) {
          int boardX = currentX + x;
          int boardY = currentY + y;
          if (boardY >= 0 && boardY < rows && boardX >= 0 && boardX < columns) {
            board[boardY][boardX] = currentPiece;
          }
        }
      }
    }

    _checkAndClearLines();
    currentPiece = null;
  }

  // 라인 제거 및 점수 계산
  void _checkAndClearLines() {
    for (int y = rows - 1; y >= 0; y--) {
      bool isLineFull = true;
      for (int x = 0; x < columns; x++) {
        if (board[y][x] == null) {
          isLineFull = false;
          break;
        }
      }

      if (isLineFull) {
        // 라인 제거
        for (int y2 = y; y2 > 0; y2--) {
          for (int x = 0; x < columns; x++) {
            board[y2][x] = board[y2 - 1][x];
          }
        }
        // 맨 위 라인 비우기
        for (int x = 0; x < columns; x++) {
          board[0][x] = null;
        }
        // 점수 추가
        score += 100;
        // 같은 라인을 다시 체크
        y++;
      }
    }
  }

  // 현재 보드 상태 반환
  List<List<Color?>> getBoardState() {
    List<List<Color?>> displayBoard = List.generate(
      rows,
      (y) => List.generate(columns, (x) => board[y][x]?.color),
    );

    if (currentPiece != null) {
      for (int y = 0; y < currentPiece!.shape.length; y++) {
        for (int x = 0; x < currentPiece!.shape[y].length; x++) {
          if (currentPiece!.shape[y][x]) {
            int boardX = currentX + x;
            int boardY = currentY + y;
            if (boardY >= 0 &&
                boardY < rows &&
                boardX >= 0 &&
                boardX < columns) {
              displayBoard[boardY][boardX] = currentPiece!.color;
            }
          }
        }
      }
    }

    return displayBoard;
  }
}
