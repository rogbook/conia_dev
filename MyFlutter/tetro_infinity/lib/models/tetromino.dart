import 'package:flutter/material.dart';
import 'dart:math';

enum TetrominoType { I, O, T, S, Z, J, L }

class Tetromino {
  final TetrominoType type;
  final List<List<bool>> shape;
  final Color color;
  int rotation = 0;

  Tetromino({required this.type, required this.shape, required this.color});

  // 블록 회전
  void rotate() {
    final int n = shape.length;
    List<List<bool>> rotated = List.generate(
      n,
      (_) => List.generate(n, (_) => false),
    );

    for (int i = 0; i < n; i++) {
      for (int j = 0; j < n; j++) {
        rotated[j][n - 1 - i] = shape[i][j];
      }
    }

    shape.clear();
    shape.addAll(rotated);
    rotation = (rotation + 1) % 4;
  }

  // I 블록 생성
  static Tetromino createI() {
    return Tetromino(
      type: TetrominoType.I,
      shape: [
        [false, false, false, false],
        [true, true, true, true],
        [false, false, false, false],
        [false, false, false, false],
      ],
      color: Colors.cyan,
    );
  }

  // O 블록 생성
  static Tetromino createO() {
    return Tetromino(
      type: TetrominoType.O,
      shape: [
        [true, true],
        [true, true],
      ],
      color: Colors.yellow,
    );
  }

  // T 블록 생성
  static Tetromino createT() {
    return Tetromino(
      type: TetrominoType.T,
      shape: [
        [false, true, false],
        [true, true, true],
        [false, false, false],
      ],
      color: Colors.purple,
    );
  }

  // S 블록 생성
  static Tetromino createS() {
    return Tetromino(
      type: TetrominoType.S,
      shape: [
        [false, true, true],
        [true, true, false],
        [false, false, false],
      ],
      color: Colors.green,
    );
  }

  // Z 블록 생성
  static Tetromino createZ() {
    return Tetromino(
      type: TetrominoType.Z,
      shape: [
        [true, true, false],
        [false, true, true],
        [false, false, false],
      ],
      color: Colors.red,
    );
  }

  // J 블록 생성
  static Tetromino createJ() {
    return Tetromino(
      type: TetrominoType.J,
      shape: [
        [true, false, false],
        [true, true, true],
        [false, false, false],
      ],
      color: Colors.blue,
    );
  }

  // L 블록 생성
  static Tetromino createL() {
    return Tetromino(
      type: TetrominoType.L,
      shape: [
        [false, false, true],
        [true, true, true],
        [false, false, false],
      ],
      color: Colors.orange,
    );
  }

  // 랜덤 블록 생성
  static Tetromino createRandom() {
    final random = Random();
    final types = [
      createI,
      createO,
      createT,
      createS,
      createZ,
      createJ,
      createL,
    ];
    return types[random.nextInt(types.length)]();
  }
}
