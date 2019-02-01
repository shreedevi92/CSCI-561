import time
from copy import deepcopy
class AssignApplicants:

        def __init__(self):
            self.bed_nos = 0
            self.parking_slot_nos = 0
            self.lahsa_chosen_num_of_applicants = 0
            self.spla_chosen_num_of_applicants = 0
            self.lahsa_chosen_applicants = []
            self.spla_chosen_applicants = []
            self.total_num_of_applicants = 0
            self.total_applicants_list = []
            self.spla_appl_list = []
            self.lahsa_appl_list = []  
            self.lahsa_week_slots = [0,0,0,0,0,0,0]
            self.spla_week_slots = [0,0,0,0,0,0,0]
            self.spla_efficiency = 0
            self.lahsa_efficiency = 0
            self.spla_days_dict = {}
            self.spla_days_desc_dict = {}
            self.spla_days_asc_dict = {}
            self.common_appl_list = []
            self.common_appl_dict = {}
            self.greedy_apid = 0
            self.greedy_spla_eff = 0


        def parse_applicants(self, fip):
            line_num = 0
            lahsa_end_line = 0
            spla_end_line = 0
            with open(fip) as ip:
                for line in ip:
                    line_num += 1
                    if line_num == 1 :
                        self.bed_nos = int(line.strip())
                    elif line_num == 2:
                        self.parking_slot_nos = int(line.strip())
                    elif line_num == 3:
                        self.lahsa_chosen_num_of_applicants = int(line.strip())
                        lahsa_end_line = 4 + self.lahsa_chosen_num_of_applicants
                    elif line_num > 3 and line_num < lahsa_end_line :
                        self.lahsa_chosen_applicants.append(line.strip())
                    elif line_num == lahsa_end_line:
                        self.spla_chosen_num_of_applicants = int(line.strip())
                        spla_end_line = lahsa_end_line + self.spla_chosen_num_of_applicants + 1
                    elif line_num > lahsa_end_line and line_num < spla_end_line:  
                        self.spla_chosen_applicants.append(line.strip())
                    elif line_num == spla_end_line:
                        self.total_num_of_applicants = int(line.strip())
                    else:    
                        self.total_applicants_list.append(line.strip())
                

            for appl in self.total_applicants_list:
                if(appl[0:5]) in self.spla_chosen_applicants:
                    appl_days = map(int,appl[13:])
                    self.spla_week_slots = [self.spla_week_slots[i] + appl_days[i] for i in range(len(self.spla_week_slots))]
                    self.spla_efficiency += sum(appl_days)
                    continue
                
                if(appl[0:5]) in self.lahsa_chosen_applicants:
                    appl_days = map(int,appl[13:])
                    self.lahsa_week_slots = [self.lahsa_week_slots[i]+appl_days[i] for i in range(len(self.lahsa_week_slots))]
                    self.lahsa_efficiency += sum(appl_days)
                    continue
                
                if appl[5] == "F" and int(appl[6:9]) > 17 and appl[9] == "N":
                    self.lahsa_appl_list.append(appl)
                    appl_days = map(int,appl[13:])


                if appl[10] == "N" and appl[11] == "Y" and appl[12] == "Y":
                    self.spla_appl_list.append(appl)
                    appl_days = map(int,appl[13:])
                    self.spla_days_dict[appl] = sum(appl_days)

            self.lahsa_appl_list = sorted(self.lahsa_appl_list, key=lambda x: int(x[0:5]))
            self.spla_appl_list = sorted(self.spla_appl_list, key=lambda x: int(x[0:5]))

            print("LAHSA satisfying applicants:" + str(self.lahsa_appl_list))
            print("SPLA satisfying applicants:" + str(self.spla_appl_list))
            #print (self.lahsa_week_slots)
            #print (self.spla_week_slots)

        def build_game_tree(self,spla_list,lahsa_list,player,spla_week,lahsa_week):
            spla_eff = 0
            lahsa_eff = 0
            node = -1
            triplet = []
            if player==1:
                 for i in range(len(spla_list)):

                     spla_appl = spla_list[i]
                     flag = 0
                     exceed = 0
                     applicant = spla_appl[13:]
                     for l in range(len(applicant)):
                        if spla_week[l] + int(applicant[l]) > self.parking_slot_nos:
                            exceed = 1
                            break
                     if exceed == 1:
                         spla_eff = sum(spla_week)
                         lahsa_eff = sum(lahsa_week)
                         continue
                     appl_days = map(int,applicant)
                     spla_week = [spla_week[i] + appl_days[i] for i in range(len(spla_week))]
                     
                     if spla_appl in lahsa_list:
                        flag += 1
                        indexLahsa = lahsa_list.index(spla_appl)
                        lahsa_list.remove(spla_appl)
                    
                     indexSpla = spla_list.index(spla_appl)
                     spla_list.remove(spla_appl)

                     if lahsa_list:
                        triplet = self.build_game_tree(spla_list,lahsa_list, 0, spla_week,lahsa_week)
                        if spla_list and triplet[2]== -1:
                            triplet = self.build_game_tree(spla_list,lahsa_list, 1, spla_week,lahsa_week)
                     elif spla_list:
                        triplet = self.build_game_tree(spla_list,lahsa_list, 1 , spla_week,lahsa_week)     
                     elif not spla_list and not lahsa_list:
                         spla_eff = sum(spla_week)
                         lahsa_eff = sum(lahsa_week)
                         node = spla_appl[0:5] 
                     if triplet and triplet[0]>spla_eff:
                         spla_eff = triplet[0]
                         lahsa_eff = triplet [1]
                         node = spla_appl[0:5]

                     if flag > 0:
                        lahsa_list.insert(indexLahsa,spla_appl) 
                     spla_list.insert(indexSpla,spla_appl)
                     spla_week = [spla_week[i] - appl_days[i] for i in range(len(spla_week))]                     

            elif player==0:
                 for i in range(len(lahsa_list)):
                     lahsa_appl = lahsa_list[i]
                     flag = 0
                     exceed = 0
                     applicant = lahsa_appl[13:]
                     for l in range(len(applicant)):
                        if lahsa_week[l] + int(applicant[l]) > self.bed_nos:
                            exceed = 1
                            break
                     if exceed == 1:
                         spla_eff = sum(spla_week)
                         lahsa_eff = sum(lahsa_week)
                         continue
                     appl_days = map(int,applicant)
                     lahsa_week = [lahsa_week[i] + appl_days[i] for i in range(len(lahsa_week))]
                     
                     #print lahsa_eff
                     if lahsa_appl in spla_list:
                        flag += 1
                        indexSpla = spla_list.index(lahsa_appl)
                        spla_list.remove(lahsa_appl)
                    
                     indexLahsa = lahsa_list.index(lahsa_appl)
                     lahsa_list.remove(lahsa_appl)

                     if spla_list:
                        triplet = self.build_game_tree(spla_list,lahsa_list, 1, spla_week,lahsa_week)
                        if lahsa_list and triplet[2]== -1:
                            triplet = self.build_game_tree(spla_list,lahsa_list, 0, spla_week,lahsa_week) 
                     elif lahsa_list:
                        triplet = self.build_game_tree(spla_list,lahsa_list, 0, spla_week,lahsa_week)   
                     elif not spla_list and not lahsa_list:
                          spla_eff = sum(spla_week)
                          lahsa_eff = sum(lahsa_week)
                          node = lahsa_appl[0:5] 

                     if triplet and triplet[1]>lahsa_eff:
                         spla_eff = triplet[0]
                         lahsa_eff = triplet [1]
                         node = lahsa_appl[0:5]

                     if flag > 0:
                        spla_list.insert(indexSpla,lahsa_appl)  
                     lahsa_list.insert(indexLahsa,lahsa_appl)
                     lahsa_week = [lahsa_week[i] - appl_days[i] for i in range(len(lahsa_week))]

            return [spla_eff, lahsa_eff, node]


        def greedy(self):

            self.common_appl_list = list(set(self.spla_appl_list).intersection(self.lahsa_appl_list))
            self.spla_days_desc_dict = sorted(self.spla_days_dict.items(), key=lambda x:x[1], reverse=True)
            self.spla_days_asc_dict = sorted(self.spla_days_dict.items(), key=lambda x:x[1])
            for a in self.common_appl_list:
                appl_days = map(int,a[13:])
                self.common_appl_dict[a] = sum(appl_days)

            #descending order
            for i in range(len(self.spla_days_desc_dict)):
                spla_week = self.spla_week_slots
                efficiency_pool=[]
                applicant_pool={}
                k = list(self.spla_days_desc_dict)[i]
                applicant = k[0][13:]
                exceed = 0
                for l in range(len(applicant)):
                        if spla_week[l] + int(applicant[l]) > self.parking_slot_nos:
                            exceed = 1
                            break
                if exceed == 1:
                    continue
                applicant_pool[k[0]]=k[1]
                efficiency_pool.append(k[1])
                for j in range(i+1,len(self.spla_days_desc_dict)):
                    exceed = 0
                    a = list(self.spla_days_desc_dict)[j]
                    appl = a[0][13:]
                    for l in range(len(appl)):
                        if spla_week[l] + int(appl[l]) > self.parking_slot_nos:
                            exceed = 1
                            break
                    if exceed == 1:
                        continue
                    applicant_pool[a[0]]=a[1]
                    efficiency_pool.append(a[1])
                
                if sum(efficiency_pool) >= self.greedy_spla_eff:
                    self.greedy_spla_eff = sum(efficiency_pool)
                    d = {x:applicant_pool[x] for x in applicant_pool if x in self.common_appl_dict}
                    if d:
                        d = sorted(d.items(), key=lambda x:x[1], reverse=True)
                        self.greedy_apid = list(d)[0][0][0:5]
                        for i in range((len(d))-1):
                            if list(d)[i][1]==list(d)[i+1][1]:
                                self.greedy_apid = list(d)[i+1][0][0:5]
                    else:
                        self.greedy_apid = k[0][0:5]
             
            #ascending order
            for i in range(len(self.spla_days_asc_dict)):
                spla_week = self.spla_week_slots
                efficiency_pool=[]
                applicant_pool={}
                k = list(self.spla_days_asc_dict)[i]
                applicant = k[0][13:]
                exceed = 0
                for l in range(len(applicant)):
                        if spla_week[l] + int(applicant[l]) > self.parking_slot_nos:
                            exceed = 1
                            break
                if exceed == 1:
                    continue
                applicant_pool[k[0]]=k[1]
                efficiency_pool.append(k[1])
                for j in range(i+1,len(self.spla_days_asc_dict)):
                    exceed = 0
                    a = list(self.spla_days_asc_dict)[j]
                    appl = a[0][13:]
                    for l in range(len(appl)):
                        if spla_week[l] + int(appl[l]) > self.parking_slot_nos:
                            exceed = 1
                            break
                    if exceed == 1:
                        continue
                    applicant_pool[a[0]]=a[1]
                    efficiency_pool.append(a[1])
                
                if sum(efficiency_pool) >= self.greedy_spla_eff:
                    self.greedy_spla_eff = sum(efficiency_pool)
                    d = {x:applicant_pool[x] for x in applicant_pool if x in self.common_appl_dict}
                    if d:
                        d = sorted(d.items(), key=lambda x:x[1], reverse=True)
                        self.greedy_apid = list(d)[0][0][0:5]
                        for i in range((len(d))-1):
                            if list(d)[i][1]==list(d)[i+1][1]:
                                self.greedy_apid = list(d)[i+1][0][0:5]
                    else:
                        x = sorted(applicant_pool.items(), key=lambda x:x[1], reverse=True)
                        self.greedy_apid = list(x)[0][0][0:5]
                        for i in range((len(x))-1):
                            if list(x)[i][1]==list(x)[i+1][1]:
                                self.greedy_apid = list(x)[i+1][0][0:5]


            # all possibilities desc
            for i in range(len(self.spla_days_desc_dict)):
                spla_week = self.spla_week_slots
                efficiency_pool=[]
                applicant_pool={}
                k = list(self.spla_days_desc_dict)[i]
                applicant = k[0][13:]
                exceed = 0
                for l in range(len(applicant)):
                        if spla_week[l] + int(applicant[l]) > self.parking_slot_nos:
                            exceed = 1
                            break
                if exceed == 1:
                    continue
                applicant_pool[k[0]]=k[1]
                efficiency_pool.append(k[1])
                temp_dict=deepcopy(self.spla_days_desc_dict)
                del temp_dict[i]
                for j in range(len(temp_dict)):
                    exceed = 0
                    a = list(temp_dict)[j]
                    appl = a[0][13:]
                    for l in range(len(appl)):
                        if spla_week[l] + int(appl[l]) > self.parking_slot_nos:
                            exceed = 1
                            break
                    if exceed == 1:
                        continue
                    applicant_pool[a[0]] = a[1]
                    efficiency_pool.append(a[1])

                if sum(efficiency_pool) >= self.greedy_spla_eff:
                    self.greedy_spla_eff = sum(efficiency_pool)
                    d = {x:applicant_pool[x] for x in applicant_pool if x in self.common_appl_dict}
                    if d:
                        d = sorted(d.items(), key=lambda x:x[1], reverse=True)
                        self.greedy_apid = list(d)[0][0][0:5]
                        for i in range((len(d))-1):
                            if list(d)[i][1]==list(d)[i+1][1]:
                                self.greedy_apid = list(d)[i+1][0][0:5]
                    else:
                        self.greedy_apid = k[0][0:5]


            # all possibilities asc
            for i in range(len(self.spla_days_asc_dict)):
                spla_week = self.spla_week_slots
                efficiency_pool=[]
                applicant_pool={}
                k = list(self.spla_days_asc_dict)[i]
                applicant = k[0][13:]
                exceed = 0
                for l in range(len(applicant)):
                        if spla_week[l] + int(applicant[l]) > self.parking_slot_nos:
                            exceed = 1
                            break
                if exceed == 1:
                    continue
                applicant_pool[k[0]]=k[1]
                efficiency_pool.append(k[1])
                temp_dict=deepcopy(self.spla_days_asc_dict)
                del temp_dict[i]
                for j in range(len(temp_dict)):
                    exceed = 0
                    a = list(temp_dict)[j]
                    appl = a[0][13:]
                    for l in range(len(appl)):
                        if spla_week[l] + int(appl[l]) > self.parking_slot_nos:
                            exceed = 1
                            break
                    if exceed == 1:
                        continue
                    applicant_pool[a[0]] = a[1]
                    efficiency_pool.append(a[1])
                
                if sum(efficiency_pool) >= self.greedy_spla_eff:
                    self.greedy_spla_eff = sum(efficiency_pool)
                    d = {x:applicant_pool[x] for x in applicant_pool if x in self.common_appl_dict}
                    if d:
                        d = sorted(d.items(), key=lambda x:x[1], reverse=True)
                        self.greedy_apid = list(d)[0][0][0:5]
                        for i in range((len(d))-1):
                            if list(d)[i][1]==list(d)[i+1][1]:
                                self.greedy_apid = list(d)[i+1][0][0:5]
                            else:
                                break      
                    else:
                        x = sorted(applicant_pool.items(), key=lambda x:x[1], reverse=True)
                        self.greedy_apid = list(x)[0][0][0:5]
                        for i in range((len(x))-1):
                            if list(x)[i][1]==list(x)[i+1][1]:
                                self.greedy_apid = list(x)[i+1][0][0:5]
            return
        
        def call_game_tree(self):
            if (len(self.spla_appl_list)+len(self.lahsa_appl_list))>12 or (self.bed_nos > 10) or (self.parking_slot_nos >10):
                self.greedy()
                print self.greedy_apid
                print self.greedy_spla_eff+self.spla_efficiency
                op = open("output.txt","w")
                op.write(str(self.greedy_apid))
            else:
                start_time = time.time()
                triplet = self.build_game_tree(self.spla_appl_list,self.lahsa_appl_list,1,self.spla_week_slots, self.lahsa_week_slots)
                print triplet
                print("--- %s seconds ---" % (time.time() - start_time))
                op = open("output.txt","w")
                if(triplet[2] == -1):
                    op.write("0")
                else:
                    op.write(str(triplet[2]))


homeless = AssignApplicants()
homeless.parse_applicants("input.txt")
homeless.call_game_tree()