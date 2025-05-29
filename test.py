import sys
import pygame
from pygame.locals import *

# 棋盘参数
GRID_SIZE = 30       # 每格宽度（像素）
BOARD_LEN = 19       # 棋盘行列数
MARGIN = 40          # 棋盘边距
BOARD_SIZE = GRID_SIZE * (BOARD_LEN - 1)  # 实际网格线区域大小

def draw_board(screen):
    """绘制棋盘网格"""
    for i in range(BOARD_LEN):
        # 横线
        start_pos = (MARGIN, MARGIN + i * GRID_SIZE)
        end_pos = (MARGIN + BOARD_SIZE, MARGIN + i * GRID_SIZE)
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 1)

        # 竖线
        start_pos = (MARGIN + i * GRID_SIZE, MARGIN)
        end_pos = (MARGIN + i * GRID_SIZE, MARGIN + BOARD_SIZE)
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 1)

def main():
    """运行游戏主循环"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('五子棋')

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        screen.fill((255, 255, 255))  # 白色背景
        draw_board(screen)           # 绘制棋盘
        pygame.display.flip()        # 刷新屏幕

if __name__ == '__main__':
    main()
