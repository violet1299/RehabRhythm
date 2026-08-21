import pygame
from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets
from UI.badges import KeyBadges

class PauseScene:
    def __init__(self):
        self.widgets=RehabWidgets(); self.badges=KeyBadges(self.widgets)

    def panel(self,screen,rect,color,radius=36):
        t=self.widgets.theme; s=pygame.Surface((rect.w,rect.h),pygame.SRCALPHA)
        pygame.draw.rect(s,(*t.card,248),(0,0,rect.w,rect.h),border_radius=radius)
        pygame.draw.rect(s,color,(0,0,rect.w,rect.h),4,border_radius=radius)
        pygame.draw.rect(s,(*color,95),(9,9,rect.w-18,rect.h-18),2,border_radius=radius-8)
        screen.blit(s,rect.topleft)

    def draw(self,screen):
        t=self.widgets.theme
        overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); overlay.fill((0,0,0,205)); screen.blit(overlay,(0,0))
        p=pygame.Rect(155,150,WIDTH-310,400); self.panel(screen,p,t.primary,38)
        tf=self.widgets.fonts.get(50,bold=True); sf=self.widgets.fonts.get(29,bold=True)
        af=self.widgets.fonts.get(38,bold=True); bf=self.widgets.fonts.get(25,bold=True)
        title=tf.render("Training Paused",True,t.text); sub=sf.render("Take a short rest whenever you need.",True,t.subtext)
        screen.blit(title,title.get_rect(center=(p.centerx,p.y+62))); screen.blit(sub,sub.get_rect(center=(p.centerx,p.y+115)))
        cx=p.centerx; cy=p.y+215; points=[(cx-30,cy-48),(cx-30,cy+48),(cx+55,cy)]
        pygame.draw.polygon(screen,t.success,points,width=8)
        r=af.render("Resume Training",True,t.success); screen.blit(r,r.get_rect(center=(p.centerx,p.y+305)))
        b=bf.render("Your current training progress is temporarily preserved.",True,t.subtext)
        screen.blit(b,b.get_rect(center=(p.centerx,p.y+350)))
        self.badges.draw_footer(screen,[("SPACE","Resume"),("ESC","Main Menu")])
