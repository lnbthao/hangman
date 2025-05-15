import pygame
import math
import random
import time

pygame.init()

# setup display
WIDTH = 800
HEIGHT = 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# icon
icon = pygame.image.load("assets\icon.png")
pygame.display.set_icon(icon)

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SILVER = (192, 192, 192)
MIDBLUE = (25, 25, 112)
GAY11 = (28, 28, 28)
WHITESMOKE = (245, 245, 245)

# image
bgr = pygame.image.load(r"assets\bg.jpg")
bgr_ctp = pygame.image.load(r"assets\ctp_bg.jpg")
bg_end = pygame.image.load(r"assets\bg_end.jpg")
bg_gameplay = pygame.image.load(r"assets\bg_gameplay.jpg")
coin_img = pygame.image.load(r"assets\dollar.png")

images = []
for i in range(7):
    image = pygame.image.load("assets\hangman" + str(i)+".png")
    images.append(image)


# fonts
FONT_10 = pygame.font.SysFont('comicsans', 10)
FONT_15 = pygame.font.SysFont('comicsans', 15)
FONT_20 = pygame.font.SysFont('comicsans', 20)
FONT_30 = pygame.font.SysFont('comicsans', 30)
FONT_40 = pygame.font.SysFont('comicsans', 40)
FONT_50 = pygame.font.SysFont('comicsans', 50)
FONT_60 = pygame.font.SysFont('comicsans', 60)

# setup game loop
FPS = 60
clock = pygame.time.Clock()

# score
score = 0
high_score = 0
high_score_animal = 0
high_score_fruit = 0
high_score_vehicle = 0

# coin
coin_numbers = 3

# setup word
list_word = [("HANDSOME","LETHUAN"), ("FILM","TITANIC"),("SINGER","MRTHUAN"),("COLOR","PINK"),("FRUIT","ORANGE"),("ANIMAL","CAT"),("FOOD","HAMBURGER")]
list_word_animal = [("ANIMAL","CAT"),("ANIMAL","DOG"),("ANIMAL","LION"),("ANIMAL","ELEPHANT"),("ANIMAL","PENGUIN"),("ANIMAL","MONKEY"),("ANIMAL","KANGAROO"),("ANIMAL","DOLPHIN"),("ANIMAL","TIGER"),("ANIMAL","BEAR")]
list_word_fruit = [("FRUIT", "ORANGE"), ("FRUIT", "BANANA"), ("FRUIT", "APPLE"), ("FRUIT", "GRAPE"), ("FRUIT", "KIWI"), ("FRUIT", "LEMON"), ("FRUIT", "MANGO"), ("FRUIT", "PEACH"), ("FRUIT", "PEAR"), ("FRUIT", "PINEAPPLE")]
list_word_vehicle = [("VEHICLE", "CAR"), ("VEHICLE", "MOTORCYCLE"), ("VEHICLE", "BICYCLE"), ("VEHICLE", "BOAT"), ("VEHICLE", "AIRPLANE"), ("VEHICLE", "TRAIN"), ("VEHICLE", "TRUCK"), ("VEHICLE", "BUS")]

# timer
pygame.time.set_timer(pygame.USEREVENT ,20000)
pygame.time.set_timer(pygame.USEREVENT +1 ,1000)
pygame.time.set_timer(pygame.USEREVENT +2 ,3000)

#Sound
click_sound = pygame.mixer.Sound('sound\click.wav')
end_sound = pygame.mixer.Sound('sound/end.wav')
win_sound = pygame.mixer.Sound('sound/win.wav')
soundtrack = pygame.mixer.Sound('sound/nen.wav')

class Hangman:
    def __init__(self):
        self.status = 0     

    def draw(self):
        win.blit(images[self.status], (70, 100))

class Letter:
    def __init__(self):
        self.radius = 20    # bán kính
        self.gap = 15       # khoảng cách
        self.letters = []   # mảng chứa các phím kí tự
        self.startx = round(
            (WIDTH - ((self.radius*2 + self.gap)*12 + (self.radius*2)))/2) # biên độ từ màn hình bên trái đến chạm rìa nút đầu tiên
        self.starty = 400   # tọa độ y của hàng đầu
        self.A = 65              # gia tri ki tu A

    def listletters(self):
        for i in range(26):
            # tọa độ x thuộc tâm của 26 kí tự
            x = self.startx + self.radius + \
                ((self.radius*2 + self.gap)*(i % 13))
                
            # tọa độ y thuộc tâm của 26 kí tự. Hết 13 kí tự thì xuống dòng
            y = self.starty + ((i//13)*(self.gap + self.radius*2))
            
            # thêm vào mảng vòng tròn kí tự
            self.letters.append([x, y, chr(self.A+i), True])

    def draw(self):
        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible:
                # vẽ hình tròn với tọa độ tâm (x,y) , bán kính = radius, và viền = 3px
                pygame.draw.circle(win, BLACK, (x, y), self.radius, 3)
                
                # vẽ kí tự lên màn hình
                text = FONT_30.render(ltr, 1, BLACK)
                win.blit(text, (x - text.get_width() /
                         2, y - text.get_height()/2))
    
    # xử lí khi click vào vòng tròn kí tự
    def press(self, m_x, m_y, word, let, hangman):
        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible:
                temp = math.sqrt((x - m_x)**2 + (y - m_y)**2) # tính khoảng cách từ điểm click chuột đến tâm của từng vòng tròn kí tự
                if temp < self.radius:
                    click_sound.play()
                    letter[3] = False
                    word.guessed.append(ltr)
                    if ltr not in let[1]:
                        hangman.status += 1


class Button:
    def __init__(self):
        # tạo các khối rect của các nút
        self.play_rect = 0              
        self.quit_rect = 0
        self.back_rect = 0
        self.backnext_rect = 0
        self.coin_rect = 0
        self.auto_play_rect = 0
        self.fruit_play_rect = 0
        self.vehicle_play_rect = 0
        self.animal_play_rect = 0

    def create_playbutton(self):
        self.play_rect = pygame.draw.rect(win, SILVER, (480, 110, 180, 60))
        pygame.draw.rect(win, BLACK, (480, 110, 180, 60), 2)
        text = FONT_50.render("PLAY", 1, BLACK)
        win.blit(text, (510, 100))

    def create_quitbutton(self):
        self.quit_rect = pygame.draw.rect(win, SILVER, (480, 210, 180, 60))
        pygame.draw.rect(win, BLACK, (480, 210, 180, 60), 2)
        text = FONT_50.render("QUIT", 1, BLACK)
        win.blit(text, (500, 200))
        
    def create_autoplaybutton(self):
        self.auto_play_rect = pygame.draw.rect(win, SILVER, (280, 120, 240, 60),2)
        text = FONT_50.render("AUTO", 1, WHITE)
        win.blit(text, ((WIDTH-text.get_width())/2, 110))
        
    def create_animalplaybutton(self):
        self.animal_play_rect = pygame.draw.rect(win, SILVER, (280, 210, 240, 60),2)
        text = FONT_50.render("ANIMAL", 1, WHITE)
        win.blit(text, ((WIDTH-text.get_width())/2, 200))
        
    def create_fruitplaybutton(self):
        self.fruit_play_rect = pygame.draw.rect(win, SILVER, (280, 300, 240, 60),2)
        text = FONT_50.render("FRUIT", 1, WHITE)
        win.blit(text, ((WIDTH-text.get_width())/2, 290))

    def create_vehicleplaybutton(self):
        self.vehicle_play_rect = pygame.draw.rect(win, SILVER, (280, 390, 240, 60),2)
        text = FONT_50.render("VEHICLE", 1, WHITE)
        win.blit(text, ((WIDTH-text.get_width())/2, 380))
    
    def create_backbutton(self):
        self.back_rect = pygame.draw.rect(win, SILVER, (0, 0, 80, 40))
        pygame.draw.rect(win, BLACK, (0, 0, 80, 40), 1)
        text = FONT_20.render('<-Back', 1, BLACK)
        win.blit(text, (10, 5))

    def create_backnextbutton(self, backnext):
        self.backnext_rect = pygame.draw.rect(win, SILVER, (360, 360, 80, 30))
        pygame.draw.rect(win, BLACK, (360, 360, 80, 30), 2)
        text = FONT_20.render(backnext, 1, MIDBLUE)
        win.blit(text, (WIDTH/2 - text.get_width() /
                 2, 380 - text.get_height()/2 - 6))
        
    def create_helpbutton(self):
        self.coin_rect = pygame.draw.circle(win, BLACK, (765, 60), 34, 2)
        text = FONT_15.render('Help',1, BLACK)
        win.blit(text,(750,40))
        win.blit(coin_img, (740,60))
        text = FONT_15.render('x1',1, BLACK)
        win.blit(text,(768,60))
    
    # xử lí khi nhấn nút vàng trợ giúp
    def press_button_helpCoin(self, Word, Letter, let):
        global coin_numbers
        # check vàng
        if (coin_numbers <= 0):
            print("Het tien")
        else:
            while True:
                # lấy 1 kí tự ngẫu nhiên trong từ khóa
                char = random.choice(let[1])
                # tạo mảng lưu index của các kí tự đó
                positions = [i for i, c in enumerate(let[1]) if c == char]
                # kiểm tra kí tự đó có thuộc với từ khóa còn ẩn hiện tại
                if char not in Word.display_word:
                    for pos in positions:
                        # đổi kí tự "_" thành kí tự char vào vào các vị trí pos
                        Word.display_word = Word.display_word[:pos] + char + Word.display_word[pos+1:]
                    # mảng kí tự đã nhấn thêm vào kí tự char
                    Word.guessed.append(char)
                    # tắt hiển thị vòng tròn kí tự char
                    for letter in Letter.letters:
                        x, y, ltr, visible = letter
                        if (ltr == char):
                            letter[3] = False
                    coin_numbers -= 1
                    break
    
    # check có click vào button tương ứng hay không        
    def press_button(self, pos, rect):
        return rect.collidepoint(pos)

class Word:
    def __init__(self,list_word):
        self.words = list_word      # tạo danh sách từ khóa theo chủ đề tương ứng
        self.guessed = []           # mảng danh sách các kí tự đã nhấn
        self.display_word = ""      # từ khóa còn ẩn hiện tại

    def draw_title(self, let):
        title = let[0]
        text = FONT_60.render(title, 1, BLACK)
        win.blit(text, (WIDTH/3 + (WIDTH/3 - 2*text.get_width()/3), 80))

    def draw_word(self, let):
        self.display_word = ""
        for letter in let[1]:   
            # check từ kí tự trong từ khóa có thuộc mảng kí tự đã nhấn không   
            # cập nhật từ khóa hiện tại và vẽ lên màn hình 
            if letter in self.guessed:                  
                self.display_word += letter + " "       
            else:
                self.display_word += "_ "
        text = FONT_40.render(self.display_word, 1, MIDBLUE)
        win.blit(text, (WIDTH/3 + (WIDTH/3 - 2*text.get_width()/3) ,250))

    def draw_header(self, score, topic, coin_numbers):
        # draw score text
        text = FONT_20.render(f"SCORE:{int(score)}", 1, WHITE)
        win.blit(text, (170, 10))

        # draw hight score text
        # check từng chế độ mà hiển thị từng loại điểm cao khác nhau
        if topic == "auto":
            high_score_temp = high_score
        elif topic == "animal":
            high_score_temp = high_score_animal
        elif topic == "fruit":
            high_score_temp = high_score_fruit
        elif topic == "vehicle":
            high_score_temp = high_score_vehicle
        text = FONT_20.render(f"HIGH SCORE:{int(high_score_temp)}", 1, WHITE)
        win.blit(text, (340, 10))
        
        # draw coin numbers
        win.blit(coin_img, (560,12))
        text = FONT_20.render(f"x{int(coin_numbers)}", 1, WHITE)
        win.blit(text, (590, 10))
        
    def cre(self):
        # làm bởi 2 hotgơ và 1 nam thần
        text = FONT_15.render("by QuynhThaoThuan ><",1,WHITE)
        win.blit(text,(630,475))


class GamePlay():
    def __init__(self):
        pass

    def update_score(self, score, high_score):
        if score > high_score:
            high_score = score
        return high_score

    def main_menu(self):
        global list_word
        global list_word_animal
        global list_word_vehicle
        global list_word_fruit
        button = Button()
        # load lại list từ khóa
        list_word = [("VEHICLE", "MOTORCYCLE"), ("FILM","TITANIC"),("FOOD","SANDWICH"),("COLOR","PINK"),("FRUIT","ORANGE"),("ANIMAL","CAT"),("FOOD","HAMBURGER")]
        list_word_animal = [("ANIMAL","CAT"),("ANIMAL","DOG"),("ANIMAL","LION"),("ANIMAL","ELEPHANT"),("ANIMAL","PENGUIN"),("ANIMAL","MONKEY"),("ANIMAL","KANGAROO"),("ANIMAL","DOLPHIN"),("ANIMAL","TIGER"),("ANIMAL","BEAR")]
        list_word_fruit = [("FRUIT", "ORANGE"), ("FRUIT", "BANANA"), ("FRUIT", "APPLE"), ("FRUIT", "GRAPE"), ("FRUIT", "KIWI"), ("FRUIT", "LEMON"), ("FRUIT", "MANGO"), ("FRUIT", "PEACH"), ("FRUIT", "PEAR"), ("FRUIT", "PINEAPPLE")]
        list_word_vehicle = [("VEHICLE", "CAR"), ("VEHICLE", "MOTORCYCLE"), ("VEHICLE", "BICYCLE"), ("VEHICLE", "BOAT"), ("VEHICLE", "AIRPLANE"), ("VEHICLE", "TRAIN"), ("VEHICLE", "TRUCK"), ("VEHICLE", "BUS")]
        word = Word(list_word)
        global score
        score = 0       # reset điểm số
        soundtrack.play()
        while True:
            win.blit(bgr, (0, 0))
            # khởi tọa 2 button play quit
            button.create_playbutton()
            button.create_quitbutton()
            word.cre()
            text = FONT_60.render('The Hangman', 1, WHITE)
            win.blit(text, (360, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.USEREVENT:
                    soundtrack.play()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()        # lây tọa độ khi click chuột pos = (x, y)
                    if button.press_button(pos, button.play_rect):      # check xem có click vào button hay không
                        click_sound.play()
                        self.choose_to_play_menu()
                    if button.press_button(pos, button.quit_rect):
                        click_sound.play()
                        pygame.quit()
            pygame.display.update()
            
    def choose_to_play_menu(self):
        button = Button()
        while True:
            win.blit(bgr_ctp, (0, 0))
            text = FONT_60.render('Choose Game Mode', 1, WHITESMOKE)
            win.blit(text, ((WIDTH - text.get_width())/2, 0))
            
            # khởi tạo 4 button trong chế độ chơi
            button.create_autoplaybutton()
            button.create_animalplaybutton()
            button.create_fruitplaybutton()
            button.create_vehicleplaybutton()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button.press_button(pos, button.auto_play_rect):     #tương tự
                        soundtrack.stop()
                        click_sound.play()
                        self.game_play("auto")
                    if button.press_button(pos, button.animal_play_rect):
                        soundtrack.stop()
                        click_sound.play()
                        self.game_play("animal")
                    if button.press_button(pos, button.vehicle_play_rect):
                        soundtrack.stop()
                        click_sound.play()
                        self.game_play("vehicle")
                    if button.press_button(pos, button.fruit_play_rect):
                        soundtrack.stop()
                        click_sound.play()
                        self.game_play("fruit")
            pygame.display.update()
             
    def game_play(self, topic):
        hangman = Hangman()
        letter_obj = Letter()
        button = Button()
        
        # khởi tạo list từ khóa theo từng chủ đề
        if topic == "auto":
            word = Word(list_word)
        elif topic == "fruit":
            word = Word(list_word_fruit)
        elif topic == "vehicle":
            word = Word(list_word_vehicle)
        elif topic == "animal":
            word = Word(list_word_animal)
        
        letter_obj.listletters()
        # chọn ngẫu nhiên 1 từ khóa trong list
        let = random.choice(word.words)
        
        # đặt biến toàn cục vì có thể các giá trị thay đổi trong hàm này
        global score
        global high_score
        global high_score_animal
        global high_score_fruit
        global high_score_vehicle
        global coin_numbers
        
        soundtrack.play()

        while True:
            clock.tick(FPS)
            
            # khởi tạo các đối tượng cần thiết cho trò chơi 
            win.blit(bg_gameplay,(0,0))
            letter_obj.draw()
            hangman.draw()
            word.draw_title(let)
            word.draw_header(score, topic, coin_numbers)
            word.draw_word(let)
            word.cre()
            button.create_backbutton()
            button.create_helpbutton()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.USEREVENT:
                    soundtrack.play()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    m_x, m_y = pygame.mouse.get_pos()
                    letter_obj.press(m_x, m_y, word, let, hangman)      # check khi click vào vòng tròn kí tự
                    if button.press_button(pos, button.back_rect):
                        click_sound.play()
                        soundtrack.stop()
                        self.main_menu()
                    if button.press_button(pos, button.coin_rect):
                        click_sound.play()
                        button.press_button_helpCoin(word, letter_obj, let)

            won = True
            for letter in let[1]:
                if letter not in word.guessed:      # check các kí tự của từ khóa có nằm trong mảng các phím đã nhấn hay không
                    won = False
                    break
            if won:
                score += 1
                
                # kiểm tra chủ đề, và xóa đi từ khóa đã vừa hiển thị (tránh trùng lặp) , và cập nhật điểm cao
                if topic == "auto":
                    del list_word[list_word.index(let)]
                    high_score = self.update_score(score, high_score)
                elif topic == "fruit":
                    del list_word_fruit[list_word_fruit.index(let)]
                    high_score_fruit = self.update_score(score, high_score_fruit)
                elif topic == "vehicle":
                    del list_word_vehicle[list_word_vehicle.index(let)]
                    high_score_vehicle = self.update_score(score, high_score_vehicle)
                elif topic == "animal":
                    del list_word_animal[list_word_animal.index(let)]
                    high_score_animal = self.update_score(score, high_score_animal)
                    
                word.draw_word(let)
                pygame.display.update()
                win_sound.play()
                soundtrack.stop()
                time.sleep(1)
                coin_numbers +=1
                self.display_end(let, score, topic, "WIN")      # chuyển màn hình sang màn hình display
            if hangman.status == 6:
                hangman.draw()
                word.draw_word(let)
                pygame.display.update()
                end_sound.play()
                soundtrack.stop()
                time.sleep(1)
                self.display_end(let, score, topic, "LOSE")
                
            pygame.display.update()

    def display_end(self, let, score, topic, game_over):
        height = 450
        width = 350
        xfr = (WIDTH - width) / 2
        yfr = (HEIGHT - height) / 2
        word = Word(list_word)
        button = Button()
        
        if topic == "auto":
            high_score_temp = high_score
        elif topic == "animal":
            high_score_temp = high_score_animal
        elif topic == "fruit":
            high_score_temp = high_score_fruit
        elif topic == "vehicle":
            high_score_temp = high_score_vehicle
        
        
        while True:
            win.blit(bg_gameplay,(0,0))
            # frame
            win.blit(bg_end,(xfr,yfr))
            # border
            pygame.draw.rect(win, BLACK, pygame.Rect(
                xfr, yfr, width, height), 2)
            # game_over ?
            text = FONT_50.render(game_over, 1, BLACK)
            win.blit(text, (WIDTH/2 - text.get_width()/2, yfr + 15))
            # word
            text = FONT_20.render(let[1], 1, BLUE)
            win.blit(text, (WIDTH/2 - text.get_width()/2, yfr + 100))
            # score
            text = FONT_20.render(f"SCORE: {int(score)}", 1, BLACK)
            win.blit(text, (WIDTH/2 - text.get_width()/2, yfr + 220))
            # high score
            text = FONT_15.render(f"HIGH SCORE: {int(high_score_temp)}", 1, BLACK)
            win.blit(text, (WIDTH/2 - text.get_width()/2, yfr + 255))
            
            win.blit(coin_img, (375, yfr + 300))
            text = FONT_20.render(f" +1", 1, BLACK)
            win.blit(text, (WIDTH/2 - text.get_width()/2+15, yfr + 297))
            # back next
            if game_over == "WIN":
                button.create_backnextbutton("Next")
            if game_over == "LOSE":
                button.create_backnextbutton("Back")

            pos = pygame.mouse.get_pos()
            word.cre()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.press_button(pos, button.backnext_rect):
                        if game_over == "WIN":
                            click_sound.play()
                            self.game_play(topic)
                        if game_over == "LOSE":
                            click_sound.play()
                            soundtrack.stop()
                            self.main_menu()
            pygame.display.update()


game = GamePlay()
game.main_menu()