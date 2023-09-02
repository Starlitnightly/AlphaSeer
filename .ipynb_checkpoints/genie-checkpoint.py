import random
class Genie(object):

    def __init__(self,name,element,proper_dict,skill_dict) -> None:
        #精灵名字
        self.name=name
        #精灵元素
        self.element=element

        #精灵属性
        self.hp=proper_dict["hp"]
        self.max_hp=proper_dict["hp"]
        self.attack=proper_dict["attack"]
        self.defense=proper_dict["defense"]
        self.speed=proper_dict["speed"]
        self.special_attack=proper_dict["special_attack"]
        self.special_defense=proper_dict["special_defense"]
        
        #精灵强化
        self.up_attack=0
        self.up_defense=0
        self.up_speed=0
        self.up_special_attack=0
        self.up_special_defense=0

        #精灵技能
        self.skill_dict=skill_dict
        self.skill1=skill_dict["skill1"]
        self.skill2=skill_dict["skill2"]
        self.skill3=skill_dict["skill3"]
        self.skill4=skill_dict["skill4"]
        pass

    def use_skill(self,goal,skill):

        if skill['type']=='物理攻击':
            #(0.84×攻击方攻击/防御方防御×技能威力+2)×克制系数×本系加成1.5×(217/255～1)
            #random 217-255
            random_shanghai=random.randint(217,255)/255
            kezhi=1
            shanghai=(0.84*(self.attack*(self.up_attack*0.5+1))/(goal.defense*(goal.up_defense*0.5+1))*skill['power']+2)*1.5*random_shanghai*kezhi
        elif skill['type']=='特殊攻击':
            random_shanghai=random.randint(217,255)/255
            kezhi=1
            shanghai=(0.84*(self.special_attack*(self.up_special_attack*0.5+1))/(goal.special_defense*(goal.up_special_defense*0.5+1))*skill['power']+2)*1.5*random_shanghai*kezhi
        elif skill['type']=='属性攻击': 
            shanghai=0
        
        skill['pp']-=1
        
        if skill['effect']!=None:
            if 'proper_up' in skill['effect'].keys():
                self.up_attack+=skill['effect']['proper_up']['attack']
                self.up_defense+=skill['effect']['proper_up']['defense']
                self.up_special_attack+=skill['effect']['proper_up']['special_attack']
                self.up_special_defense+=skill['effect']['proper_up']['special_defense']
                self.up_speed+=skill['effect']['proper_up']['speed']
            elif 'up_disappear' in skill['effect'].keys():
                goal.up_attack=0
                goal.up_defense=0
                goal.up_special_attack=0
                goal.up_special_defense=0
                goal.up_speed=0
            
        goal.hp-=int(shanghai)
        return int(shanghai)
        
    