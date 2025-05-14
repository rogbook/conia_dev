import 'package:flutter/material.dart';
import '../models/tetromino.dart';

class NextPieceWidget extends StatelessWidget {
  final Tetromino nextPiece;
  final double cellSize;

  const NextPieceWidget({
    Key? key,
    required this.nextPiece,
    this.cellSize = 15.0,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // 모든 블록을 4x4 그리드에 맞추기
    final int gridSize = 4;
    List<List<bool>> displayShape = List.generate(
      gridSize,
      (_) => List.generate(gridSize, (_) => false),
    );

    // 블록을 중앙에 배치
    int offsetX = (gridSize - nextPiece.shape[0].length) ~/ 2;
    int offsetY = (gridSize - nextPiece.shape.length) ~/ 2;

    for (int y = 0; y < nextPiece.shape.length; y++) {
      for (int x = 0; x < nextPiece.shape[y].length; x++) {
        if (y + offsetY < gridSize && x + offsetX < gridSize) {
          displayShape[y + offsetY][x + offsetX] = nextPiece.shape[y][x];
        }
      }
    }

    return Container(
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: const Color(0xFF2A2A2A),
        borderRadius: BorderRadius.circular(8),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text(
            'NEXT',
            style: TextStyle(
              color: Colors.white70,
              fontSize: 14,
              fontWeight: FontWeight.bold,
              letterSpacing: 1,
            ),
          ),
          const SizedBox(height: 4),
          Container(
            padding: const EdgeInsets.all(4),
            decoration: BoxDecoration(
              color: Colors.black.withOpacity(0.3),
              borderRadius: BorderRadius.circular(4),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: List.generate(
                gridSize,
                (y) => Row(
                  mainAxisSize: MainAxisSize.min,
                  children: List.generate(
                    gridSize,
                    (x) => Container(
                      width: cellSize,
                      height: cellSize,
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: Colors.black.withOpacity(0.1),
                          width: 0.5,
                        ),
                        color:
                            displayShape[y][x]
                                ? nextPiece.color
                                : Colors.transparent,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
