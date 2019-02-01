# Open input.txt in read mode to read line by line
#Output output.txt

op = open("output.txt","w")
with open('input.txt') as ip:
    for line in ip:
        state = tuple(line.strip().split(","))
        if state[1] == "Dirty":
            op.write("Suck"+"\n")
        elif state[0] == "A":
            op.write("Right"+"\n")
        elif state[0] == "B":
            op.write("Left"+"\n")

op.close()