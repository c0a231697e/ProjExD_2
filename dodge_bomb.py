import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650


DELTA = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, 5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRect爆弾Rect
    戻り値：真理値タプル(横、縦)/画面内/True,画面外/False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間とともに爆弾が拡大，加速する
    戻り値:tuple 爆弾画像リストと加速度リスト
    """
    # 加速度のリストを作成
    bb_accs = [a for a in range(1, 11)]  # 1から10の加速度リスト
    # サイズが異なる爆弾Surfaceのリストを作成
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))  # 爆弾の円形Surface
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 円描画
        bb_img.set_colorkey((0, 0, 0))  # 黒を透過させる
        bb_imgs.append(bb_img)  # リストに追加
    return bb_imgs, bb_accs


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に半透明の黒い画面にする
    画面上に(Gane Over)と表示する
    泣いているこうかとんの画像を貼り付ける
    引数:screen(pg.Surface)ゲームウィンドウのSurfaceオブジェクト
    """
    _bg = pg .Surface((WIDTH, HEIGHT))
    pg.draw.rect(_bg, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    _bg.set_alpha(200)  # 半透明の黒
    screen.blit(_bg, [0, 0])
    # 文字の設定
    font = pg.font.Font(None, 80)  # フォントとサイズ
    text = font.render("Game Over", True, (255, 255, 255))  # しろの文字
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    # 画像の設定
    crying_kk_img = pg.image.load("fig/8.png")  # 泣いているこうかとん画像の読み込み
    crying_kk_img = pg.transform.rotozoom(crying_kk_img, 0, 1)  # サイズ調整
    kk_rect1 = crying_kk_img.get_rect(center=(screen.get_width() // 3, screen.get_height() // 2))
    screen.blit(crying_kk_img, kk_rect1)
    # 右側に画像を描画
    kk_rect_right = crying_kk_img.get_rect(center=(screen.get_width() * 2 // 3, screen.get_height() // 2))
    screen.blit(crying_kk_img, kk_rect_right)
    # 画面更新と5秒間の待機
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 黒を透過させる
    bb_rct = bb_img.get_rect()  # 爆弾rectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    clock = pg.time.Clock()
    bb_imgs, bb_accs = init_bb_imgs()  # リストを取得
    vx, vy = +5, +5  # 爆弾速度ベクトル
    tmr = 0
    while True:
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            print("ゲームオーバー")
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, vy)  # 爆弾が動く
        # こうかとんが画面外なら元の場所に戻す
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出てる
            vx *= -1
        if not tate:
            vy *= -1  # 縦にはみ出てる
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
