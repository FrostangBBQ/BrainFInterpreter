class BFArray(): #Run BrainF Code
    
    def __init__(self):
        import msvcrt
        import sys
        self.values = [0] #array
        self.pointer = 0 #pointer
        self.cap = 255 #max array value
        self.floor = 0 #min array value
        self.getch = msvcrt.getch
        self.stdout = sys.stdout
    
    def dump(self): #Print the Current array
        print(end="\nDump: ")
        for i in range(len(self.values)):
            if i == self.pointer:
                print("[" + str(self.values[i]) + "]", end = " ")
            else:
                print(self.values[i], end=" ")
        print()

    def moveRight(self): #Move pointer to the right
        if self.pointer == 0 and self.values[0] == 0:
            self.pointer -= 1
            del self.values[0] #clean up leading 0s
        self.pointer += 1
        if self.pointer == len(self.values):
            self.values = self.values + [0]
    
    def moveLeft(self): #move pointer to the left
        if self.pointer == len(self.values) - 1 and self.values[-1] == 0:
            del self.values[-1] #clean up trailing 0s
        if self.pointer == 0:
            self.values = [0] + self.values
        else:
            self.pointer -= 1
    
    def output(self): #print ASCII char for current value
        print(end=chr(self.values[self.pointer]))
        self.stdout.flush()

    def input(self): #input single char to ASCII value
        char = self.getch()
        char = ord(char)

        if char == 13:
            char = 10
        
        print(end=chr(char))
        self.stdout.flush()
        
        self.values[self.pointer] = char

    def increment(self): #increase current value by 1
        pointer = self.pointer
        if self.values[pointer] == self.cap:
            self.values[pointer] = self.floor #wrap if at limits
        else:
            self.values[pointer] += 1

    def decrement(self): #decrease current value by 1
        pointer = self.pointer
        if self.values[pointer] == self.floor:
            self.values[pointer] = self.cap #wrap if at limits
        else:
            self.values[pointer] -= 1

    def fileToCode(self, file, dumpCode=False): #convert file to readable code
        #open file
        try:
            with open(file, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("Error: File Not Found")
            return ""
        
        #convert to text
        fileText = "".join(lines)

        #convert from text to code
        return self.textToCode(fileText, dumpCode)

    def textToCode(self, text, dumpCode=False): #convert text to readable code
        validChars = "<>.,+-[]#%"
        code = ""
        for i in text:
            if i in validChars:
                code += i
        
        if dumpCode:
            print(code)
        
        return code

    def run(self, code, breakMode = False): #run code
        current = 0
        while current < len(code):
            instruction = code[current]
            if breakMode:
                print(end=instruction)

            if instruction == "[": #if/loop statements
                open = 1
                if self.values[self.pointer] == 0:
                    while open != 0: #match brackets
                        current += 1
                        if code[current] == "[":
                            open += 1
                        elif code[current] == "]":
                            open -= 1
            elif instruction == "]": #if/loop statments
                close = 1
                if self.values[self.pointer] != 0:
                    while close != 0: #match brackets
                        current -= 1
                        if code[current] == "]":
                            close += 1
                        elif code[current] == "[":
                            close -= 1
            elif instruction == "%": #toggle break mode
                if breakMode:
                    print("\nEND BREAK MODE [%]")
                    breakMode = False
                else:
                    print("\nBREAK MODE [%]")
                    breakMode = True
            else: #execute instructions
                self.execute(instruction)

            if breakMode:
                self.dump()
                input()

            current += 1

    def execute(self, command): #execute instructions
        if command == ">":
            self.moveRight()
        elif command == "<":
            self.moveLeft()
        elif command == ".":
            self.output()
        elif command == ",":
            self.input()
        elif command == "+":
            self.increment()
        elif command == "-":
            self.decrement()
        elif command == "#":
            self.dump()


#_______CODE STARTS HERE_______

FILE_PATH = "C:/Users/Joe Bowen/Desktop/CODE/BrainF/"

FILE = "hello.bf"
INSTRUCTIONS = ""
DUMP_INSTRUCTIONS = False

bf = BFArray()

if FILE != "":
    code = bf.fileToCode(FILE_PATH + FILE, DUMP_INSTRUCTIONS)
elif INSTRUCTIONS != "":
    code = bf.textToCode(INSTRUCTIONS, DUMP_INSTRUCTIONS)
else:
    file = input("---BrainF Interpreter---\nFile: ")
    code = bf.fileToCode(FILE_PATH + file, DUMP_INSTRUCTIONS)
    print("---Program START---\n")

bf.run(code)