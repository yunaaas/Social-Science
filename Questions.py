import random

from questions_human import *

from questions_economy import *

from questions_policy import *

from questions_law import *

from questions_sociology import *

from SQL import *

sql = SQL()

class Questions:  
    def __init__(self, mode = 0, complexity = "", question = {}, asnwer = {}):  
        self._mode = mode  
        self._complexity = complexity
        self._question = question
        self._answer = asnwer

    def get_mode(self):  
        return self._mode  

    def set_mode(self, a):  
        self._mode = a
    
    
    def get_complexity(self):
        return self._complexity
    
    def set_complexuty(self, a):
        self._complexity = a


    def get_question(self, id):
        return self._question[f"{id}"]
    
    def get_answer(self, id):
        return self._answer[f"{id}"]
    
    
    def set_question(self, id):
        result = sql.search_in_table(id)
        cloud = None
        if (result[0][14] == 1) and (self._complexity == 1):
            cloud = random.choice(human_easy_question_list).split("-")

        if (result[0][14] == 1) and (self._complexity == 2):
            cloud = random.choice(human_hard_question_list).split("-")

        if (result[0][14] == 2) and (self._complexity == 1):
            cloud = random.choice(economy_easy_question_list).split("-")

        if (result[0][14] == 2) and (self._complexity == 2):
            cloud = random.choice(economy_hard_question_list).split("-")  
        
        if (result[0][14] == 3) and (self._complexity == 1):
            cloud = random.choice(policy_easy_question_list).split("-")

        if (result[0][14] == 3) and (self._complexity == 2):
            cloud = random.choice(policy_hard_question_list).split("-")

        if (result[0][14] == 4) and (self._complexity == 1):
            cloud = random.choice(law_easy_question_list).split("-")

        if (result[0][14] == 4) and (self._complexity == 2):
            cloud = random.choice(law_hard_question_list).split("-")

        if (result[0][14] == 5) and (self._complexity == 1):
            cloud = random.choice(sociology_easy_question_list).split("-")

        if (result[0][14] == 5) and (self._complexity == 2):
            cloud = random.choice(sociology_hard_question_list).split("-")

        sql.change_totals(id, result[0][14])   
        self._question[f"{id}"] = cloud[0].lstrip()
        self._answer[f"{id}"] = cloud[1].rstrip()