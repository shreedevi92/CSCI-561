import numpy as np
import time
epsilon = 0.1
discount_factor = 0.9
class SpeedRacer:
        def __init__(self):
            self.grid_size = 0
            self.num_of_cars = 0
            self.num_of_obstacles = 0
            self.loc_of_obstacles = []
            self.start_loc = []
            self.terminal_loc = []
            self.states = []
            self.policies = []
            self.utility = np.dtype('Float64')
            self.reward = np.dtype('Float64')

        def parse_input(self, fip):
            line_num = 0
            obstacles_endline = 0
            start_loc_endline = 0
            terminal_loc_endline = 0

            with open(fip) as ip:
                for line in ip:
                    line_num += 1
                    if line_num == 1 :
                        self.grid_size = int(line.strip())
                    elif line_num == 2:
                        self.num_of_cars = int(line.strip())
                        self.states=[(x,y) for x in range(self.grid_size) for y in range(self.grid_size)]
                    elif line_num == 3:
                        self.num_of_obstacles = int(line.strip())
                        obstacles_endline = 3 + self.num_of_obstacles
                        start_loc_endline = obstacles_endline + self.num_of_cars
                        terminal_loc_endline = start_loc_endline + self.num_of_cars
                    elif line_num > 3 and line_num <= obstacles_endline :
                        obs_x , obs_y = line.strip().split(",")
                        self.loc_of_obstacles.append((int(obs_y), int(obs_x)))
                    elif line_num > obstacles_endline and line_num <= start_loc_endline:
                        start_x, start_y = line.strip().split(",")
                        self.start_loc.append((int(start_y), int(start_x)))
                    elif line_num > start_loc_endline and line_num <=  terminal_loc_endline:
                        end_x, end_y = line.strip().split(",")
                        self.terminal_loc.append((int(end_y), int(end_x)))

            # print(self.loc_of_obstacles)
            # print(self.start_loc)
            # print(self.terminal_loc)
            #print(self.reward)
            # print(self.states)
            # print(self.policies)
        def generate_reward(self,car_num):
            reward = np.full((self.grid_size, self.grid_size), -1.0)
            for o in self.loc_of_obstacles:
                reward[o[0]][o[1]] -= 100

            t_x = self.terminal_loc[car_num][0]
            t_y = self.terminal_loc[car_num][1]
            reward[t_x][t_y] += 100
            
            return reward

        def update_utility(self, reward, car_num):
            north_x, north_y, south_x, south_y, east_x, east_y, west_x, west_y = [-1000] * 8
            temp_utility = reward.copy()
            while True:
                utility = temp_utility.copy()
                diff = 0
                for s in self.states:
                	#calculate co-ordinates of the next grid
                    if s != self.terminal_loc[car_num]:
                        if (s[0]-1) < 0: 
                            north_x = s[0]
                            north_y = s[1]
                        else:
                            north_x = s[0] - 1
                            north_y = s[1]

                        if (s[0]+1) == self.grid_size: 
                            south_x = s[0]
                            south_y = s[1]
                        else:
                            south_x = s[0] + 1
                            south_y = s[1]
                        
                        if (s[1]+1) == self.grid_size: 
                            east_x = s[0]
                            east_y = s[1]
                        else:
                            east_x = s[0]
                            east_y = s[1] + 1

                        if (s[1] - 1) < 0: 
                            west_x = s[0]
                            west_y = s[1]
                        else:
                            west_x = s[0]
                            west_y = s[1] - 1


                        north_utility = 0.7*utility[north_x,north_y] + 0.1*utility[south_x,south_y] + 0.1*utility[east_x,east_y] + 0.1*utility[west_x,west_y]
                        south_utility = 0.1*utility[north_x,north_y] + 0.7*utility[south_x,south_y] + 0.1*utility[east_x,east_y] + 0.1*utility[west_x,west_y]
                        east_utility = 0.1*utility[north_x,north_y] + 0.1*utility[south_x,south_y] + 0.7*utility[east_x,east_y] + 0.1*utility[west_x,west_y]
                        west_utility = 0.1*utility[north_x,north_y] + 0.1*utility[south_x,south_y] + 0.1*utility[east_x,east_y] + 0.7*utility[west_x,west_y]

                      
                        temp_utility[s[0],s[1]] = self.reward[s[0],s[1]] + discount_factor * max([north_utility,south_utility,east_utility,west_utility])
                        diff = max(diff,np.max(np.abs(temp_utility[:,:] - utility[:,:])))

                if diff < epsilon * (1-discount_factor)/discount_factor:
                    break

            return utility   

        def generate_policy(self, utility, car_num):
            policies=[[(0,0) for x in range(self.grid_size)] for y in range(self.grid_size)]
            policies[self.terminal_loc[car_num][0]][self.terminal_loc[car_num][1]] = ('')
            north_x, north_y, south_x, south_y, east_x, east_y, west_x, west_y = [-1000] * 8
            for s in self.states:
            		#calculate co-ordinates of the next grid
                    if s != self.terminal_loc[car_num]:
                        if (s[0]-1) < 0: 
                            north_x = s[0]
                            north_y = s[1]
                        else:
                            north_x = s[0] - 1
                            north_y = s[1]

                        if (s[0]+1) == self.grid_size: 
                            south_x = s[0]
                            south_y = s[1]
                        else:
                            south_x = s[0] + 1
                            south_y = s[1]
                        
                        if (s[1]+1) == self.grid_size: 
                            east_x = s[0]
                            east_y = s[1]
                        else:
                            east_x = s[0]
                            east_y = s[1] + 1

                        if (s[1] - 1) < 0: 
                            west_x = s[0]
                            west_y = s[1]
                        else:
                            west_x = s[0]
                            west_y = s[1] - 1

                        north_utility = 0.7*utility[north_x,north_y] + 0.1*utility[south_x,south_y] + 0.1*utility[east_x,east_y] + 0.1*utility[west_x,west_y]
                        south_utility = 0.1*utility[north_x,north_y] + 0.7*utility[south_x,south_y] + 0.1*utility[east_x,east_y] + 0.1*utility[west_x,west_y]
                        east_utility = 0.1*utility[north_x,north_y] + 0.1*utility[south_x,south_y] + 0.7*utility[east_x,east_y] + 0.1*utility[west_x,west_y]
                        west_utility = 0.1*utility[north_x,north_y] + 0.1*utility[south_x,south_y] + 0.1*utility[east_x,east_y] + 0.7*utility[west_x,west_y]

                       
                        max_direction = np.argmax([north_utility,south_utility,east_utility,west_utility],axis=0)
                        if max_direction == 0:
                            policies[s[0]][s[1]] = (-1,0)
                        elif max_direction == 1:
                            policies[s[0]][s[1]] = (1,0)
                        elif max_direction == 2:
                            policies[s[0]][s[1]] = (0,1)
                        elif max_direction == 3:
                            policies[s[0]][s[1]] = (0,-1)
            
            return policies

        def simulate_move(self):
            output_file = open("output.txt","w")
            for i in range(self.num_of_cars):
                self.reward = self.generate_reward(i)
                #print self.reward
                self.utility = self.update_utility(self.reward, i)
                self.policies = self.generate_policy(self.utility,i)
                #print self.utility
                #print self.policies
                cost_list=[]
                for j in range(10):
                    pos = self.start_loc[i]
                    np.random.seed(j)
                    swerve = np.random.random_sample(1000000) 
                    k=0
                    #print np.finfo(type(swerve[k]))
                    if pos == self.terminal_loc[i]:
                        cost = 100
                    else:
                        cost = 0
                    while pos != self.terminal_loc[i]:
                        move = self.policies[pos[0]][pos[1]] 
                        if swerve[k] > 0.7:
                            if swerve[k] > 0.8:
                                if swerve[k] > 0.9:
                                    # reverse direction
                                    move = tuple([x*-1 for x in move])
                                else:
                                    if(move[1]==0):
                                        move = tuple(x*-1 for x in(reversed(move)))
                                    else:
                                        move = tuple(reversed(move))
                            else:
                                if(move[1]==0):
                                    move = tuple(reversed(move))
                                else:
                                    move = tuple(x*-1 for x in(reversed(move)))
                        new_pos_x = pos[0] + move[0]
                        new_pos_y = pos[1] + move[1]
                        if(new_pos_x>-1) and (new_pos_x<self.grid_size)and ((new_pos_y>-1) and (new_pos_y<self.grid_size)):
                            pos = (pos[0] + move[0], pos[1] + move[1])
                        cost = cost + self.reward[pos[0],pos[1]]
                        k+=1
                    cost_list.append(cost)
                    #print(cost)
                
                final_cost = np.floor(np.mean(cost_list))
                #print(int(final_cost))
                output_file.write(str(int(final_cost))+ "\n")
                
            output_file.close()

racer = SpeedRacer()
start_time = time.time()
racer.parse_input("input.txt")
racer.simulate_move()
print("--- %s seconds ---" % (time.time() - start_time))