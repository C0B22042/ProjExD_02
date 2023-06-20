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
    kk_ang_key_lis = [[0, 5], [-5, 5], [-5, 0], [-5, -5], [0, -5], [5, -5], [5, 0], [5, 5]]
    for i in range(4):
        kk_ang_dict[tuple(kk_ang_key_lis[i])] = pg.transform.rotozoom(kk_load_img, -i*45+90, 1)
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

    kk_gameover_img = pg.transform.rotozoom(pg.image.load("ex02/fig/8.png"), 0, 2.0)
    
    bom_surs = list()
    for i in range(1, 11):
        bom = pg.Surface((20*i,20*i))
        bom.set_colorkey((0, 0, 0))
        pg.draw.circle(bom, (255, 0, 0), (10*i, 10*i), 10*i)
        bom_surs.append(bom)
    bom_rect = bom_surs[0].get_rect()
    bom_rect.center = [random.randint(10,i-10) for i in win_size]
    bom_moveIp = [5, 5]
    bom_moveIp2 = [0, 0]

    clock = pg.time.Clock()
    tmr = 0
    tmr2 = 1
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

        b_i = min(tmr//500, 9)
        bom_rect[2:] = bom_surs[b_i].get_rect()[2:]

        if kk_rec.colliderect(bom_rect) and tmr2>0:
            tmr2 = -50

        kk_move_lim = [0, 0]
        for i in range(len(win_size)):
            if not check_win(kk_rec[i], win_size[i], kk_rec[i+2], kk_move[i]):
                kk_move_lim[i] = kk_move[i]

            bom_s = bom_surs[b_i].get_rect()
            if check_win(bom_rect[i], win_size[i], bom_s[i+2], 0):
                bom_moveIp[i] *= -1

        screen.blit(bg_img, [0, 0])

        if tuple(kk_move_lim) in kk_ang_dict:
            kk_img = kk_ang_dict[tuple(kk_move_lim)]

        if tmr2 > 0:
            screen.blit(kk_img, kk_rec)
            kk_rec.move_ip(kk_move_lim)
        else:
            screen.blit(kk_gameover_img, kk_rec)

        #for i in range(2):
        #    bom_moveIp[i] = bom_rect[i]-kk_rec[i]

        for i in range(2):
            bom_moveIp2[i] = bom_moveIp[i] * (b_i+1)
        bom_rect.move_ip(bom_moveIp2)
        screen.blit(bom_surs[b_i], bom_rect)

        pg.display.update()

        if tmr2 == 0:
            return

        tmr2 += 1
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