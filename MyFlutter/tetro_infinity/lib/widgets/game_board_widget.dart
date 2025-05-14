import 'package:flutter/material.dart';
import '../models/game_board.dart';

class GameBoardWidget extends StatelessWidget {
  final GameBoard gameBoard;
  final double cellSize;

  const GameBoardWidget({
    Key? key,
    required this.gameBoard,
    this.cellSize = 25.0,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: const Color(0xFF333333),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: List.generate(
          gameBoard.height,
          (y) => Row(
            mainAxisSize: MainAxisSize.min,
            children: List.generate(gameBoard.width, (x) {
              // 현재 움직이는 블록의 위치인지 확인
              bool isCurrentPiece = false;
              if (gameBoard.currentPiece != null) {
                int pieceX = x - gameBoard.currentX;
                int pieceY = y - gameBoard.currentY;
                if (pieceX >= 0 &&
                    pieceX < gameBoard.currentPiece!.shape[0].length &&
                    pieceY >= 0 &&
                    pieceY < gameBoard.currentPiece!.shape.length &&
                    gameBoard.currentPiece!.shape[pieceY][pieceX]) {
                  isCurrentPiece = true;
                }
              }

              return Container(
                width: cellSize,
                height: cellSize,
                decoration: BoxDecoration(
                  border: Border.all(
                    color: Colors.black.withOpacity(0.1),
                    width: 1,
                  ),
                  color:
                      isCurrentPiece
                          ? gameBoard.currentPiece!.color
                          : gameBoard.getCell(x, y)?.color ??
                              Colors.transparent,
                ),
              );
            }),
          ),
        ),
      ),
    );
  }
}
