import pygame,sys,os
import pygame.freetype
class MusicLoader():
    def __init__(self):
        self.music_list = {}
        self.music_list["bg"] = pygame.mixer.music
        self.music_list["bg"].load(os.path.join("resources","cheetah_man.ogg"))
        
    def return_music_list(self):
        return self.music_list

class Player(pygame.sprite.Sprite):
    def __init__(self,image_path,root):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.effect = pygame.mixer.Sound(os.path.join("resources","jump.ogg"))
        
        div_w = 2
        div_h = 4
        self.rect = self.image.get_rect()
        self.rect.width = self.image.get_width()/div_w
        self.rect.height = self.image.get_height()/div_h
        
        self.root = root
        
        self.area = {}
        self.area["idle_R"]=(0,0,self.rect.width,self.rect.height)
        self.area["jump_R"]=(self.rect.width,0,self.rect.width*2,self.rect.height)
        self.area["idle_L"]=(0,self.rect.height*2,self.rect.width,self.rect.height)
        self.area["jump_L"]=(self.rect.width,self.rect.height*2,self.rect.width*2,self.rect.height)
        self.direction = "idle_R"
        self.oldx = 0
        self.oldy = 0
        
        self.x = 0
        self.y = 250-self.rect.height
        self.vx = 3
        self.vy = 5
        #self.y = pygame.mouse.get_pos()[1] - self.rect.height/2
        self.jump_state = False
        self.frame_count = 0
        self.dir="R"
        
    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            if self.x < self.root.get_width()-self.rect.width:
                self.x = self.x + self.vx
        elif pressed[pygame.K_LEFT]:
            if self.x > 0:
                self.x = self.x - self.vx
        
        if self.jump_state == False:
            if pressed[pygame.K_SPACE]:
                self.jump_state=True
                self.effect.play(0)
        elif self.jump_state == True:
            if self.frame_count < 10:
                self.y = self.y - self.vy
                self.frame_count+=1
            else:
                if self.frame_count < 20:
                    self.y = self.y + self.vy
                    self.frame_count += 1
                else:
                    self.frame_count = 0
                    self.jump_state = False
        if self.x - self.oldx > 0:
            self.dir ="R"
        elif self.x - self.oldx < 0:
            self.dir ="L"
        
        if self.jump_state == True:
            self.direction = "jump_"+self.dir
        else:
            self.direction = "idle_"+self.dir

        self.root.blit(self.image,dest = (self.x,self.y),area = self.area[self.direction]) #display player image on root surface
        self.oldx = self.x
        self.oldy = self.y

        
class Ground(pygame.sprite.Sprite):
    def __init__(self,image_path,root):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert()
        div_num = 1
        self.rect = self.image.get_rect()
        self.rect.width = self.image.get_width()/div_num
        self.rect.height = self.image.get_height()/div_num
        
        self.root = root
        
        self.oldy = 0
        
    def update(self):
        self.root.blit(self.image,dest = (0,self.root.get_height()-self.rect.height))

class CharWindow(pygame.sprite.Sprite):
    def __init__(self,image_path,root,player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.root = root
        self.score = 0
        self.player = player
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.realpath("fonts"))
        print(base_path)
        self.font1 = pygame.font.Font(os.path.join(base_path,"fonts/misaki_gothic.ttf"),25)
        self.char_name = self.font1.render("TIGER",False,(255,255,255))
        self.score_sur = self.font1.render("SCORE:"+str(self.score),False,(255,255,255))
        self.stage_name = self.font1.render("STAGE:1-1",False,(255,255,255))
        
    def update(self):
        self.root.blit(self.score_sur,dest = (20,10))
        self.root.blit(self.stage_name,dest = (self.root.get_width()-120,10))
        self.root.blit(self.image,dest = (20,self.root.get_width()-120))
        self.root.blit(self.char_name,dest = (40,self.root.get_width()-30))
        if self.player.jump_state == True:
            self.score_add()
        
    def score_add(self):
        self.score += 10
        self.score_sur = self.font1.render("SCORE:"+str(self.score),False,(255,255,255))
        
class Game:
    def __init__(self):
        pygame.init()

        root = pygame.display.set_mode((400,400))
        pygame.display.set_caption("TigerMan")
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.realpath("resources"))
        pygame.display.set_icon(pygame.image.load(os.path.join(base_path,"resources/tiger_icon.png")))
        running = True
    
        music_list = MusicLoader().return_music_list()
        player = Player(os.path.join("resources","cheetah_man.png"),root)
        ground = Ground(os.path.join("resources","ground.png"),root)
        charwindow = CharWindow(os.path.join("resources","tiger_window.png"),root,player)
    
        group_player = pygame.sprite.Group()
        group_player.add(ground)
        group_player.add(player)
    
        music_list["bg"].play(-1)
        clock = pygame.time.Clock()
        fps = 60
        while running:
            clock.tick(fps)
            root.fill((50,150,200)) # fill root as gray color
            group_player.update()
            charwindow.update()
            pygame.display.update()
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    music_list["bg"].stop()
                    pygame.quit()
                    sys.exit()
        pygame.event.clear()
    
if __name__ == "__main__":
    Game()