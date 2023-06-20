import sys
import random
import pygame as pg


WIDTH, HEIGHT = 900, 600
win_size = [WIDTH, HEIGHT]


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_load_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_ang_dict = dict()
    kk_ang_key_lis = [[-5, 5], [-5, 0], [-5, -5], [0, -5], [5, -5], [5, 0], [5, 5], [0, 5]]
    for i in range(4):
        kk_ang_dict[tuple(kk_ang_key_lis[i])] = pg.transform.rotozoom(kk_load_img, -i*45+45, 1)
    for i in range(4):
        kk_ang_dict[tuple(kk_ang_key_lis[i+4])] = pg.transform.rotozoom(
            pg.transform.flip(kk_load_img, False, True), -(i+4)*45+45, 1)
        
    kk_img = kk_ang_dict[(-5, 0)]
    kk_rec = kk_img.get_rect()
    kk_move_key = dict(zip(
        [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT], 
        [[0, -5], [0, 5], [-5, 0], [5, 0]]
    ))
    kk_move = [0, 0]
    bom_sur = pg.Surface((20,20))
    bom_sur.set_colorkey((0, 0, 0))
    pg.draw.circle(bom_sur, (255, 0, 0), (10, 10), 10)
    bom_rect = bom_sur.get_rect()
    bom_rect.center = [random.randint(10,i-10) for i in win_size]
    bom_moveIp = [5, 5]
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            # DELETE Key で終了 ---------------
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DELETE:
                    return
            # --------------------------------
            if event.type == pg.KEYDOWN:
                if event.key in kk_move_key:
                    for i in range(2):
                        kk_move[i] += kk_move_key[event.key][i]
            
            if event.type ==pg.KEYUP:
                if event.key in kk_move_key:
                    for i in range(2):
                        kk_move[i] -= kk_move_key[event.key][i]
        if kk_rec.colliderect(bom_rect):
            print("game over")
            return

        kk_move_lim = [0, 0]
        for i in range(len(win_size)):
            if not check_win(kk_rec[i], win_size[i], kk_rec[i+2], kk_move[i]):
                kk_move_lim[i] = kk_move[i]
            if check_win(bom_rect[i], win_size[i], bom_rect[i+2], 0):
                bom_moveIp[i] *= -1

        screen.blit(bg_img, [0, 0])

        if tuple(kk_move_lim) in kk_ang_dict:
            kk_img = kk_ang_dict[tuple(kk_move_lim)]

        print(tuple(kk_move_lim))
        kk_rec.move_ip(kk_move_lim)
        screen.blit(kk_img, kk_rec)
        
        bom_rect.move_ip(bom_moveIp)
        screen.blit(bom_sur, bom_rect)

        pg.display.update()
        tmr += 1
        clock.tick(50)

def check_win(rec, win_size, sur_size, sur_move):
    if rec+sur_move < 0 or rec+sur_move > win_size-sur_size:
        return True
            


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()