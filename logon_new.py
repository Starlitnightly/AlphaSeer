import sys
from PyQt6.QtWidgets import (QMainWindow, 
                             QPushButton, 
                             QApplication,
                             QLabel,
                             QProgressBar,
                             QScrollArea,
                             QWidget,
                             QVBoxLayout)

from PyQt6.QtGui import QPixmap,QTransform
from PyQt6.QtCore import Qt
import random
 
from genie import Genie
import gymnasium
from gymnasium import spaces
import numpy as np
import time

global_info=''


global_gaiya=Genie("盖亚","战斗",
                    {"hp":351,
                     "attack":371,
                     "defense":210,
                     "speed":309,
                     "special_attack":205,
                     "special_defense":192},
                     {"skill1":
                      {"name":"日月皆伤",
                       "type":"物理攻击",
                       "power":140,
                       "pp":5,"pp_max":5,
                       "effect":{"up_disappear":True}},
                      "skill2":
                      {"name":"石破天惊",
                       "type":"物理攻击",
                       "power":150,
                       "pp":5,"pp_max":5,
                       "effect":None},
                      "skill3":
                      {"name":"返璞归真",
                       "type":"属性攻击",
                       "power":0,
                       "pp":5,"pp_max":5,
                       "effect":{"proper_up":
                                 {"attack":2,"defense":0,
                                  "special_attack":2,
                                  "special_defense":0,
                                  "speed":0}},},
                      "skill4":
                      {"name":"不灭斗气",
                       "type":"属性攻击",
                       "power":0,
                       "pp":15,"pp_max":15,
                       "effect":{"proper_up":
                                 {"attack":0,"defense":1,
                                  "special_attack":0,
                                  "special_defense":1,
                                  "speed":0}},}})

global_leiyi=Genie("雷伊","电",
                    {"hp":2000,
                        "attack":369,
                        "defense":206,
                        "speed":327,
                        "special_attack":221,
                        "special_defense":210},
                        {"skill1":
                         {"name":"白光刃",
                          "type":"物理攻击",
                          "power":95,
                          "pp":99999,"pp_max":99999,
                          "effect":None},
                          "skill2":
                         {"name":"白光刃",
                          "type":"物理攻击",
                          "power":95,
                          "pp":99999,"pp_max":99999,
                          "effect":None},
                          "skill3":
                         {"name":"白光刃",
                          "type":"物理攻击",
                          "power":95,
                          "pp":99999,"pp_max":99999,
                          "effect":None},
                          "skill4":
                         {"name":"白光刃",
                          "type":"物理攻击",
                          "power":95,
                          "pp":99999,"pp_max":99999,
                          "effect":None}})



class AlphaSeer(gymnasium.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 2
        }
    def __init__(self):

        #盖亚（玩家）与雷伊
        self.gaiya=global_gaiya
        self.leiyi=global_leiyi
        #boss雷伊自带强化+2
        self.leiyi.up_attack=2
        
        
        #当前两只精灵的血量作为state
        self.state = np.array([self.gaiya.hp,self.leiyi.hp])
        self.info = {}
        #步数空间，有6种选择
        self.action_space = spaces.Discrete(6) # 0:skill1, 1:skill2, 2:skill3, 3:skill4, 4:hp,5:pp
        #血量状态空间
        self.size = 2000
        self.observation_space = spaces.Box(np.array([-self.size,-self.size]), np.array([self.size,self.size]))

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        #print(action)
        #盖亚出招（玩家）
        if action==0:
            if self.gaiya.skill_dict['skill1']['pp']>0:
                self.sh=self.gaiya.use_skill(self.leiyi,self.gaiya.skill_dict['skill1'])
                msg = '{} 使用了技能 {}, 造成了{}点伤害, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(self.gaiya.name,
                                                     self.gaiya.skill_dict['skill1']['name'],
                                                     self.sh,
                                                     self.gaiya.name,
                                                    self.gaiya.hp,self.gaiya.max_hp,
                                                     self.leiyi.name,
                                                    self.leiyi.hp,self.leiyi.max_hp)
            else:
                msg = '{} 没有pp了'.format(self.gaiya.skill_dict['skill1']['name'])
        elif action==1:
            if self.gaiya.skill_dict['skill2']['pp']>0:
                self.sh=self.gaiya.use_skill(self.leiyi,self.gaiya.skill_dict['skill2'])
                msg = '{} 使用了技能 {}, 造成了{}点伤害,\n{}当前血量{}/{}, {}当前血量{}/{}'.format(self.gaiya.name,
                                                     self.gaiya.skill_dict['skill2']['name'],
                                                     self.sh,
                                                     self.gaiya.name,
                                                    self.gaiya.hp,self.gaiya.max_hp,
                                                     self.leiyi.name,
                                                    self.leiyi.hp,self.leiyi.max_hp)
            else:
                msg = '{} 没有pp了'.format(self.gaiya.skill_dict['skill1']['name'])
        elif action==2:
            if self.gaiya.skill_dict['skill3']['pp']>0:
                self.sh=self.gaiya.use_skill(self.leiyi,self.gaiya.skill_dict['skill3'])
                msg = '{} 使用了技能 {}, 造成了{}点伤害, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(self.gaiya.name,
                                                     self.gaiya.skill_dict['skill3']['name'],
                                                     self.sh,
                                                     self.gaiya.name,
                                                    self.gaiya.hp,self.gaiya.max_hp,
                                                     self.leiyi.name,
                                                    self.leiyi.hp,self.leiyi.max_hp)
            else:
                msg = '{} 没有pp了'.format(self.gaiya.skill_dict['skill1']['name'])
        elif action==3:
            if self.gaiya.skill_dict['skill4']['pp']>0:
                self.sh=self.gaiya.use_skill(self.leiyi,self.gaiya.skill_dict['skill4'])
                msg = '{} 使用了技能 {}, 造成了{}点伤害, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(self.gaiya.name,
                                                     self.gaiya.skill_dict['skill4']['name'],
                                                     self.sh,
                                                     self.gaiya.name,
                                                    self.gaiya.hp,self.gaiya.max_hp,
                                                     self.leiyi.name,
                                                    self.leiyi.hp,self.leiyi.max_hp)
            else:
                msg = '{} 没有pp了'.format(self.gaiya.skill_dict['skill1']['name'])
        elif action==4:
            self.sh=0
            self.gaiya.hp+=200
            msg = '{} 使用补血, 恢复了200hp, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(self.gaiya.name,
                                                                         self.gaiya.name,
                                                    self.gaiya.hp,self.gaiya.max_hp,
                                                     self.leiyi.name,
                                                    self.leiyi.hp,self.leiyi.max_hp)
        elif action==5:
            self.sh=0
            self.gaiya.skill_dict['skill1']['pp']+=5
            self.gaiya.skill_dict['skill2']['pp']+=5
            self.gaiya.skill_dict['skill3']['pp']+=5
            self.gaiya.skill_dict['skill4']['pp']+=5
            msg = '{} 使用补pp, 恢复了5pp, {}当前血量{}/{}'.format(self.gaiya.name,self.gaiya.name,
                                                    self.gaiya.hp,self.gaiya.max_hp,
                                                     self.leiyi.name,
                                                    self.leiyi.hp,self.leiyi.max_hp)
        
        self.refresh_status()
        #self.pyqt_window.refresh_status()
        
        
        #雷伊出招
        self.sh2=self.leiyi.use_skill(self.gaiya,self.leiyi.skill_dict['skill1'])
        self.refresh_status()
        #self.pyqt_window.refresh_status()
        
        # 结算
        self.state = np.array([self.gaiya.hp,self.leiyi.hp])
        self.state = self.state.astype(np.float32)
        reward = self._get_reward()
        
        #判断游戏是否结束
        terminated = self._get_terminated()
        terminated = bool(terminated)
        
        #判断精灵血量是否超出边界
        truncated = self._get_truncated()
        truncated = bool(truncated)

        #info = {msg}
        info ={}
        return self.state, reward, terminated,truncated, info
    
    def step_info(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        #print(action)
        #盖亚出招（玩家）
        if action==0:
            if self.gaiya.skill_dict['skill1']['pp']>0:
                self.sh=self.gaiya.use_skill(self.leiyi,self.gaiya.skill_dict['skill1'])
                
        elif action==1:
            if self.gaiya.skill_dict['skill2']['pp']>0:
                self.sh=self.gaiya.use_skill(self.leiyi,self.gaiya.skill_dict['skill2'])
                
        elif action==2:
            if self.gaiya.skill_dict['skill3']['pp']>0:
                self.sh=self.gaiya.use_skill(self.leiyi,self.gaiya.skill_dict['skill3'])
                
        elif action==3:
            if self.gaiya.skill_dict['skill4']['pp']>0:
                self.sh=self.gaiya.use_skill(self.leiyi,self.gaiya.skill_dict['skill4'])

        elif action==4:
            self.sh=0
            self.gaiya.hp+=200

        elif action==5:
            self.sh=0
            self.gaiya.skill_dict['skill1']['pp']+=5
            self.gaiya.skill_dict['skill2']['pp']+=5
            self.gaiya.skill_dict['skill3']['pp']+=5
            self.gaiya.skill_dict['skill4']['pp']+=5
        
        self.refresh_status()
        #self.pyqt_window.refresh_status()
        self.state = np.array([self.gaiya.hp,self.leiyi.hp])
        self.state = self.state.astype(np.float32)
        
        #如果打死了，立即结算
        if self._get_terminated():
            reward = self._get_reward()
            #判断游戏是否结束
            terminated = self._get_terminated()
            terminated = bool(terminated)

            #判断精灵血量是否超出边界
            truncated = self._get_truncated()
            truncated = bool(truncated)
            info = '游戏结束'
            return self.state, reward, terminated,truncated, info
        
        
        #雷伊出招
        self.sh2=self.leiyi.use_skill(self.gaiya,self.leiyi.skill_dict['skill1'])
        self.refresh_status()
        
        if action==0:
            msg= '{} 使用了技能 {}, 造成了{}点伤害, {} 使用了技能 {}, 造成了{}点伤害, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(
                self.gaiya.name,
                self.gaiya.skill_dict['skill1']['name'],
                self.sh,
                self.leiyi.name,
                self.leiyi.skill_dict['skill1']['name'],
                self.sh2,
                self.gaiya.name,
                self.gaiya.hp,self.gaiya.max_hp,
                self.leiyi.name,
                self.leiyi.hp,self.leiyi.max_hp)
        elif action==1:
            msg = '{} 使用了技能 {}, 造成了{}点伤害, {} 使用了技能 {}, 造成了{}点伤害, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(
                self.gaiya.name,
                self.gaiya.skill_dict['skill2']['name'],
                self.sh,
                self.leiyi.name,
                self.leiyi.skill_dict['skill1']['name'],
                self.sh2,
                self.gaiya.name,
                self.gaiya.hp,self.gaiya.max_hp,
                self.leiyi.name,
                self.leiyi.hp,self.leiyi.max_hp)
        elif action==2:
            msg = '{} 使用了技能 {}, 造成了{}点伤害, {} 使用了技能 {}, 造成了{}点伤害, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(
                self.gaiya.name,
                self.gaiya.skill_dict['skill3']['name'],
                self.sh,
                self.leiyi.name,
                self.leiyi.skill_dict['skill1']['name'],
                self.sh2,
                self.gaiya.name,
                self.gaiya.hp,self.gaiya.max_hp,
                self.leiyi.name,
                self.leiyi.hp,self.leiyi.max_hp)
            
        elif action==3:
            msg = '{} 使用了技能 {}, 造成了{}点伤害, {} 使用了技能 {}, 造成了{}点伤害, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(
                self.gaiya.name,
                self.gaiya.skill_dict['skill4']['name'],
                self.sh,
                self.leiyi.name,
                self.leiyi.skill_dict['skill1']['name'],
                self.sh2,
                self.gaiya.name,
                self.gaiya.hp,self.gaiya.max_hp,
                self.leiyi.name,
                self.leiyi.hp,self.leiyi.max_hp)
            
        elif action==4:
            msg = '{} 使用补血, 恢复了200hp, {} 使用了技能 {}, 造成了{}点伤害, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(
                self.gaiya.name,
                self.leiyi.name,
                self.leiyi.skill_dict['skill1']['name'],
                self.sh2,
                self.gaiya.name,
                self.gaiya.hp,self.gaiya.max_hp,
                self.leiyi.name,
                self.leiyi.hp,self.leiyi.max_hp)
            
        elif action==5:
            msg = '{} 使用补pp, 恢复了5pp, {} 使用了技能 {}, 造成了{}点伤害, \n{}当前血量{}/{}, {}当前血量{}/{}'.format(
                self.gaiya.name,
                self.leiyi.name,
                self.leiyi.skill_dict['skill1']['name'],
                self.sh2,
                self.gaiya.name,
                self.gaiya.hp,self.gaiya.max_hp,
                self.leiyi.name,
                self.leiyi.hp,self.leiyi.max_hp)
            
        
        # 结算
        self.state = np.array([self.gaiya.hp,self.leiyi.hp])
        self.state = self.state.astype(np.float32)
        reward = self._get_reward()
        
        #判断游戏是否结束
        terminated = self._get_terminated()
        terminated = bool(terminated)
        
        #判断精灵血量是否超出边界
        truncated = self._get_truncated()
        truncated = bool(truncated)

        info = msg
        #info ={}
        return self.state, reward, terminated,truncated, info
        
    
    def _get_reward(self):
        
        if self.gaiya.hp<=0:
            #如果己方阵亡
            return -2000
        elif self.gaiya.hp>=0 and self.leiyi.hp<=0:
            #如果对方阵亡
            return 10000
        elif self.gaiya.hp>0 and self.leiyi.hp>0:
            #如果双方都活着，那么根据当前造成的伤害返回奖励
            #print(self.sh+100)
            if self.gaiya.hp<=self.gaiya.max_hp//2:
                return self.gaiya.hp+self.sh//2-self.sh2
            else:
                return self.gaiya.hp//1.5+self.sh-self.sh2
        
    def reset(self,seed=None):
        
        #游戏重载，血量恢复最大值
        self.gaiya.hp=self.gaiya.max_hp
        self.leiyi.hp=self.leiyi.max_hp
        
        for skill in self.gaiya.skill_dict.keys():
            self.gaiya.skill_dict[skill]['pp']=self.gaiya.skill_dict[skill]['pp_max']
        for skill in self.leiyi.skill_dict.keys():
            self.leiyi.skill_dict[skill]['pp']=self.leiyi.skill_dict[skill]['pp_max']
        
        #强化等级恢复最大值
        self.gaiya.up_attack=0
        self.gaiya.up_defense=0
        self.gaiya.up_special_attack=0
        self.gaiya.up_special_defense=0
        self.gaiya.up_speed=0

        self.leiyi.up_attack=2
        self.leiyi.up_defense=0
        self.leiyi.up_special_attack=0
        self.leiyi.up_special_defense=0
        self.leiyi.up_speed=0

        #状态恢复起始空间
        self.state = np.array([self.gaiya.hp,self.leiyi.hp])
        self.state = self.state.astype(np.float32)
        #
        self.counts = 0
        self.info = {}
        return self.state,self.info
    
    def render(self, mode='human'):
        print(self.state)
        
    
    def _get_terminated(self):
        x,y = self.state
        if x<=0:
            self.gaiya.hp=0
        if y<=0:
            self.leiyi.hp=0
        if x<=0 or y<=0:
            return True
        else:
            return False
        
    def _get_truncated(self):
        x,y = self.state
        return x<-self.size or x>self.size or y<-self.size or y>self.size

    def refresh_status(self):

        #判断生命值是否超过最大值
        if self.leiyi.hp>self.leiyi.max_hp:
            self.leiyi.hp=self.leiyi.max_hp
        if self.gaiya.hp>self.gaiya.max_hp:
            self.gaiya.hp=self.gaiya.max_hp

        #判断强化是否超过最大值
        if self.leiyi.up_attack>=6:
            self.leiyi.up_attack=6
        if self.leiyi.up_defense>=6:
            self.leiyi.up_defense=6
        if self.leiyi.up_special_attack>=6:
            self.leiyi.up_special_attack=6
        if self.leiyi.up_special_defense>=6:
            self.leiyi.up_special_defense=6
        if self.leiyi.up_speed>=6:
            self.leiyi.up_speed=6

        if self.gaiya.up_attack>=6:
            self.gaiya.up_attack=6
        if self.gaiya.up_defense>=6:
            self.gaiya.up_defense=6
        if self.gaiya.up_special_attack>=6:
            self.gaiya.up_special_attack=6
        if self.gaiya.up_special_defense>=6:
            self.gaiya.up_special_defense=6
        if self.gaiya.up_speed>=6:
            self.gaiya.up_speed=6


        
        #判断技能pp是否超过最大值，是否小于0
        for skill in self.gaiya.skill_dict.keys():
            if self.gaiya.skill_dict[skill]['pp']>self.gaiya.skill_dict[skill]['pp_max']:
                self.gaiya.skill_dict[skill]['pp']=self.gaiya.skill_dict[skill]['pp_max']
        for skill in self.leiyi.skill_dict.keys():
            if self.leiyi.skill_dict[skill]['pp']>self.leiyi.skill_dict[skill]['pp_max']:
                self.leiyi.skill_dict[skill]['pp']=self.leiyi.skill_dict[skill]['pp_max']
        


class Example(QMainWindow):
 
    def __init__(self):
        super().__init__()
 
        self.initUI()
 
 
    def initUI(self):

        self.genie_1=global_gaiya
        self.genie_2=global_leiyi



        #盖亚
        lbl1 = QLabel(self)
        lbl1.resize(200, 400)
        pixmap1 = QPixmap('img/gaiye1.png')
        pixmap1=pixmap1.scaled(pixmap1.width()/3,pixmap1.height()/3)
        lbl1.setPixmap(pixmap1)
        lbl1.move(10, 0)

        #血条
        self.progressBar1 = QProgressBar(self)
        self.progressBar1.setGeometry(30, 40, 200, 50)
        self.progressBar1.setValue(self.genie_1.hp/self.genie_1.max_hp*100)
        self.hp_lbl1=QLabel(self)
        self.hp_lbl1.setText(f"{self.genie_1.hp}/{self.genie_1.max_hp}")
        self.hp_lbl1.move(30+200-50, 28)
        self.hp_lbl1.resize(200, 50)

        #强化等级
        self.up_level1=QLabel(self)
        self.up_level1.setText(f"攻击+{self.genie_1.up_attack}\n防御+{self.genie_1.up_defense}\n特攻+{self.genie_1.up_special_attack}\n特防+{self.genie_1.up_special_defense}\n速度+{self.genie_1.up_speed}")
        self.up_level1.move(200, 50)
        self.up_level1.resize(200, 200)

        #雷伊
        lbl2 = QLabel(self)
        lbl2.resize(200, 400)
        pixmap2 = QPixmap('img/leiyi1.png')
        pixmap2=pixmap2.scaled(pixmap2.width()/4,pixmap2.height()/4)
        pixmap2=pixmap2.transformed(QTransform().scale(-1, 1))
        lbl2.setPixmap(pixmap2)
        lbl2.move(400, 0)

        #血条
        self.progressBar2 = QProgressBar(self)
        self.progressBar2.setGeometry(400, 40, 200, 50)
        self.progressBar2.setValue(self.genie_2.hp/self.genie_2.max_hp*100)
        self.hp_lbl2=QLabel(self)
        self.hp_lbl2.setText(f"{self.genie_2.hp}/{self.genie_2.max_hp}")
        self.hp_lbl2.move(600-50, 28)
        self.hp_lbl2.resize(200, 50)

        #强化等级
        self.up_level2=QLabel(self)
        self.up_level2.setText(f"攻击+{self.genie_2.up_attack}\n防御+{self.genie_2.up_defense}\n特攻+{self.genie_2.up_special_attack}\n特防+{self.genie_2.up_special_defense}\n速度+{self.genie_2.up_speed}")
        self.up_level2.move(400, 50)
        self.up_level2.resize(200, 200)


        #技能按钮
        self.btn_dict={}
 
        self.btn1 = QPushButton(f"日月皆伤\n威力:140 {self.genie_1.skill1['pp']}/{self.genie_1.skill1['pp_max']}", self)
        self.btn1.resize(120, 60)
        self.btn1.setStyleSheet("text-align: left;")
        self.btn1.move(200, 300)
        self.btn_dict['日月皆伤']=self.btn1
 
        self.btn2 = QPushButton(f"石破天惊\n威力:150 {self.genie_1.skill2['pp']}/{self.genie_1.skill2['pp_max']}", self)
        self.btn2.resize(120, 60)
        self.btn2.setStyleSheet("text-align: left;")
        self.btn2.move(330, 300)
        self.btn_dict['石破天惊']=self.btn2

        self.btn3 = QPushButton(f"返璞归真\n威力:0 {self.genie_1.skill3['pp']}/{self.genie_1.skill3['pp_max']}", self)
        self.btn3.resize(120, 60)
        self.btn3.setStyleSheet("text-align: left;")
        self.btn3.move(200, 360)
        self.btn_dict['返璞归真']=self.btn3
 
        self.btn4 = QPushButton(f"不灭斗气\n威力:0 {self.genie_1.skill4['pp']}/{self.genie_1.skill4['pp_max']}", self)
        self.btn4.resize(120, 60)
        self.btn4.setStyleSheet("text-align: left;")
        self.btn4.move(330, 360)
        self.btn_dict['不灭斗气']=self.btn4
 
        self.btn1.clicked.connect(self.buttonClicked)
        self.btn2.clicked.connect(self.buttonClicked)
        self.btn3.clicked.connect(self.buttonClicked)
        self.btn4.clicked.connect(self.buttonClicked)

        hp_btn=QPushButton("补血\n",self)
        hp_btn.resize(120, 60)
        hp_btn.setStyleSheet("text-align: left;")
        hp_btn.move(600, 300)
        hp_btn.clicked.connect(self.buttonClicked)

        pp_btn=QPushButton("补pp\n",self)
        pp_btn.resize(120, 60)
        pp_btn.setStyleSheet("text-align: left;")
        pp_btn.move(730, 300)
        pp_btn.clicked.connect(self.buttonClicked)

        self.button = QPushButton('开始\n', self)
        self.button.resize(120, 60)
        pp_btn.setStyleSheet("text-align: left;")
        self.button.move(730, 360)
        self.button.clicked.connect(self.buttonClicked)

        self.ai_btn = QPushButton('AlphaSeer\n', self)
        self.ai_btn.resize(120, 60)
        pp_btn.setStyleSheet("text-align: left;")
        self.ai_btn.move(600, 360)
        self.ai_btn.clicked.connect(self.ai_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showtime)  # 这个通过调用槽函数来刷新时间
        self.timer.start(10)
        self.worker_thread = WorkerThread(self)


        self.statusBar()
        self.timer = None
        self.progress = 0

        # 创建一个滚动区域，显示对战信息
        central_widget = QWidget(self)
        scroll_area = QScrollArea(self)
        central_widget.setLayout(QVBoxLayout())
        central_widget.layout().addWidget(scroll_area)
        central_widget.move(700, 50)
        central_widget.resize(300, 200)

        self.pk_label=QLabel(self)
        self.pk_label.setText("盖亚 vs 雷伊")
        self.pk_label.setStyleSheet("text-align: left;")
        self.pk_label.move(800, 0)
        self.pk_label.resize(200, 10000)
        self.pk_label.setWordWrap(True)
        self.pk_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(self.pk_label)


        logo = QLabel(self)
        logo.resize(400, 200)
        pixmap_logo = QPixmap('img/logo.png')
        pixmap_logo=pixmap_logo.scaled(pixmap_logo.width()/10,pixmap_logo.height()/10)
        logo.setPixmap(pixmap_logo)
        logo.move(720, -72)
 
        self.setGeometry(200, 200, 1000, 480)
        self.setWindowTitle('AlphaSeer')
        self.show()

    def buttonClicked(self):
 
        sender = self.sender()
        btn_name=sender.text().split("\n")[0]

        if btn_name=='开始':
            self.genie_1.hp=self.genie_1.max_hp
            self.genie_2.hp=self.genie_2.max_hp
            self.genie_1.up_attack=0
            self.genie_1.up_defense=0
            self.genie_1.up_special_attack=0
            self.genie_1.up_special_defense=0
            self.genie_1.up_speed=0

            self.genie_2.up_attack=2
            self.genie_2.up_defense=0
            self.genie_2.up_special_attack=0
            self.genie_2.up_special_defense=0
            self.genie_2.up_speed=0

            for skill in self.genie_1.skill_dict.keys():
                self.genie_1.skill_dict[skill]['pp']=self.genie_1.skill_dict[skill]['pp_max']
            for skill in self.genie_2.skill_dict.keys():
                self.genie_2.skill_dict[skill]['pp']=self.genie_2.skill_dict[skill]['pp_max']
            self.refresh_status()
            self.pk_label.setText("盖亚 vs 雷伊")
            return

        if self.game_over_determine():
            return

        #盖亚环节
       
        for skill in self.genie_1.skill_dict.keys():
            if self.genie_1.skill_dict[skill]['name']==btn_name:
                if self.genie_1.skill_dict[skill]['pp']<=0:
                    return
                sh1=self.genie_1.use_skill(self.genie_2,self.genie_1.skill_dict[skill])
                self.game_over_determine()
                self.refresh_status()

                msg = '{} 使用了技能 {}, 造成了{}点伤害'.format(self.genie_1.name,
                                                     btn_name,
                                                     sh1)
                self.statusBar().showMessage(msg)
                self.pk_label.setText(self.pk_label.text()+"\n"+msg)
                sender.setText(f"{btn_name}\n威力:{self.genie_1.skill_dict[skill]['power']} {self.genie_1.skill_dict[skill]['pp']}/{self.genie_1.skill_dict[skill]['pp_max']}")
                break
            if btn_name=='补血':
                self.genie_1.hp+=200
                self.game_over_determine()
                self.refresh_status()
                msg = '{} 使用了 {}, 恢复了{}点生命值'.format(self.genie_1.name,
                                                     btn_name,
                                                     200)
                self.statusBar().showMessage(msg)
                self.pk_label.setText(self.pk_label.text()+"\n"+msg)
                break
            if btn_name=='补pp':
                for skill in self.genie_1.skill_dict.keys():
                    self.genie_1.skill_dict[skill]['pp']+=10
                self.game_over_determine()
            
                self.refresh_status()
                msg = '{} 使用了 {}, 恢复了pp'.format(self.genie_1.name,
                                                     btn_name)
                self.statusBar().showMessage(msg)
                self.pk_label.setText(self.pk_label.text()+"\n"+msg)
                break
            
        
        #雷伊环节
        for skill in self.genie_2.skill_dict.keys():
            if self.genie_2.skill_dict[skill]['name']=='白光刃':
                sh2=self.genie_2.use_skill(self.genie_1,self.genie_2.skill_dict[skill])
                self.game_over_determine()
                self.refresh_status()
                msg = '{} 使用了技能 {}, 造成了{}点伤害'.format(self.genie_2.name,
                                                     '白光刃',
                                                     sh2)
                self.statusBar().showMessage(msg)
                self.pk_label.setText(self.pk_label.text()+"\n"+msg)
                break

    
    def refresh_status(self):

        #判断生命值是否超过最大值
        if self.genie_1.hp>self.genie_1.max_hp:
            self.genie_1.hp=self.genie_1.max_hp
        if self.genie_2.hp>self.genie_2.max_hp:
            self.genie_2.hp=self.genie_2.max_hp

        #判断强化是否超过最大值
        if self.genie_1.up_attack>=6:
            self.genie_1.up_attack=6
        if self.genie_1.up_defense>=6:
            self.genie_1.up_defense=6
        if self.genie_1.up_special_attack>=6:
            self.genie_1.up_special_attack=6
        if self.genie_1.up_special_defense>=6:
            self.genie_1.up_special_defense=6
        if self.genie_1.up_speed>=6:
            self.genie_1.up_speed=6

        if self.genie_2.up_attack>=6:
            self.genie_2.up_attack=6
        if self.genie_2.up_defense>=6:
            self.genie_2.up_defense=6
        if self.genie_2.up_special_attack>=6:
            self.genie_2.up_special_attack=6
        if self.genie_2.up_special_defense>=6:
            self.genie_2.up_special_defense=6
        if self.genie_2.up_speed>=6:
            self.genie_2.up_speed=6


        
        #判断技能pp是否超过最大值，是否小于0
        for skill in self.genie_1.skill_dict.keys():
            if self.genie_1.skill_dict[skill]['pp']>self.genie_1.skill_dict[skill]['pp_max']:
                self.genie_1.skill_dict[skill]['pp']=self.genie_1.skill_dict[skill]['pp_max']
            if self.genie_1.skill_dict[skill]['pp']<=0:
                self.btn_dict[self.genie_1.skill_dict[skill]['name']].setEnabled(False)
            else:
                self.btn_dict[self.genie_1.skill_dict[skill]['name']].setEnabled(True)
        for skill in self.genie_2.skill_dict.keys():
            if self.genie_2.skill_dict[skill]['pp']>self.genie_2.skill_dict[skill]['pp_max']:
                self.genie_2.skill_dict[skill]['pp']=self.genie_2.skill_dict[skill]['pp_max']
            

        #刷新强化状态
        self.up_level1.setText(f"攻击+{self.genie_1.up_attack}\n防御+{self.genie_1.up_defense}\n特攻+{self.genie_1.up_special_attack}\n特防+{self.genie_1.up_special_defense}\n速度+{self.genie_1.up_speed}")
        self.up_level2.setText(f"攻击+{self.genie_2.up_attack}\n防御+{self.genie_2.up_defense}\n特攻+{self.genie_2.up_special_attack}\n特防+{self.genie_2.up_special_defense}\n速度+{self.genie_2.up_speed}")
    
        #刷新血量
        self.progressBar1.setValue(self.genie_1.hp/self.genie_1.max_hp*100)
        self.progressBar2.setValue(self.genie_2.hp/self.genie_2.max_hp*100)
        self.hp_lbl1.setText(f"{self.genie_1.hp}/{self.genie_1.max_hp}")
        self.hp_lbl2.setText(f"{self.genie_2.hp}/{self.genie_2.max_hp}")

        #刷新技能pp
        self.btn1.setText(f"日月皆伤\n威力:140 {self.genie_1.skill1['pp']}/{self.genie_1.skill1['pp_max']}")
        self.btn2.setText(f"石破天惊\n威力:150 {self.genie_1.skill2['pp']}/{self.genie_1.skill2['pp_max']}")
        self.btn3.setText(f"返璞归真\n威力:0 {self.genie_1.skill3['pp']}/{self.genie_1.skill3['pp_max']}")
        self.btn4.setText(f"不灭斗气\n威力:0 {self.genie_1.skill4['pp']}/{self.genie_1.skill4['pp_max']}")
        #print(self.gaiya.skill1['pp'])

    def game_over_determine(self):
        if self.genie_1.hp <=0:
            self.genie_1.hp=0
            msg="{}阵亡".format(self.genie_1.name)
            self.statusBar().showMessage(msg)
            self.pk_label.setText(self.pk_label.text()+"\n"+msg)
            return True
        elif self.genie_2.hp <=0:
            self.genie_2.hp=0
            msg="{}阵亡".format(self.genie_2.name)
            self.statusBar().showMessage(msg)
            self.pk_label.setText(self.pk_label.text()+"\n"+msg)
            return True
        else:
            return False
        
    def ai_button(self):
        #启动AlphaSeer
        self.worker_thread.start()
        
    def showtime(self):
        self.refresh_status()
            

        
        
from PyQt6.QtCore import QThread, QTimer
class WorkerThread(QThread):
    def __init__(self,pyqt_window):
        super().__init__()
        self.pyqt_window=pyqt_window

    def run(self):
        # 长时间运行的任务
        from stable_baselines3 import DQN

        # 创建环境（请确保此处的环境配置与训练时的环境配置一致）
        env = AlphaSeer()

        # 创建已经训练好的DQN模型并加载训练好的权重
        trained_model = DQN.load("DQN_Seer")

        # 在环境中使用模型进行预测
        obs = env.reset()  # 重置环境状态
        done = False
        k=0
        while not done:
            if k==0:
                obs=obs[0]
            action, _ = trained_model.predict(obs)  # 使用模型预测动作
            
            obs, reward, done, _,info = env.step_info(action.reshape(-1)[0])  # 执行动作并获取新的状态、奖励和终止信息
            self.pyqt_window.pk_label.setText(self.pyqt_window.pk_label.text()+"\n"+info)
            self.pyqt_window.statusBar().showMessage(info)
            #刷新强化状态
            self.pyqt_window.up_level1.setText(f"攻击+{self.pyqt_window.genie_1.up_attack}\n防御+{self.pyqt_window.genie_1.up_defense}\n特攻+{self.pyqt_window.genie_1.up_special_attack}\n特防+{self.pyqt_window.genie_1.up_special_defense}\n速度+{self.pyqt_window.genie_1.up_speed}")
            self.pyqt_window.up_level2.setText(f"攻击+{self.pyqt_window.genie_2.up_attack}\n防御+{self.pyqt_window.genie_2.up_defense}\n特攻+{self.pyqt_window.genie_2.up_special_attack}\n特防+{self.pyqt_window.genie_2.up_special_defense}\n速度+{self.pyqt_window.genie_2.up_speed}")
            time.sleep(0.75)
            #刷新血量
            self.pyqt_window.progressBar1.setValue(self.pyqt_window.genie_1.hp/self.pyqt_window.genie_1.max_hp*100)
            self.pyqt_window.progressBar2.setValue(self.pyqt_window.genie_2.hp/self.pyqt_window.genie_2.max_hp*100)
            self.pyqt_window.hp_lbl1.setText(f"{self.pyqt_window.genie_1.hp}/{self.pyqt_window.genie_1.max_hp}")
            self.pyqt_window.hp_lbl2.setText(f"{self.pyqt_window.genie_2.hp}/{self.pyqt_window.genie_2.max_hp}")

            #刷新技能pp
            self.pyqt_window.btn1.setText(f"日月皆伤\n威力:140 {self.pyqt_window.genie_1.skill1['pp']}/{self.pyqt_window.genie_1.skill1['pp_max']}")
            self.pyqt_window.btn2.setText(f"石破天惊\n威力:150 {self.pyqt_window.genie_1.skill2['pp']}/{self.pyqt_window.genie_1.skill2['pp_max']}")
            self.pyqt_window.btn3.setText(f"返璞归真\n威力:0 {self.pyqt_window.genie_1.skill3['pp']}/{self.pyqt_window.genie_1.skill3['pp_max']}")
            self.pyqt_window.btn4.setText(f"不灭斗气\n威力:0 {self.pyqt_window.genie_1.skill4['pp']}/{self.pyqt_window.genie_1.skill4['pp_max']}")
            
            #self.pyqt_window.refresh_status()
            #time.sleep(1)
            print(reward,info)
            k+=1

def main():
 
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())
 
 
if __name__ == '__main__':
    main()
         
        
        
