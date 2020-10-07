# GUI Imports
import tkinter as tk
import threading
import sys


# Script Imports
import time
import cv2
import pyautogui as pgui
import numpy as np

# Variables in global scope
sizeX, sizeY = pgui.size()  # Size of screen, used in screenshot function
method = cv2.TM_SQDIFF_NORMED  # Method to use when comparing captures
pgui.PAUSE = 0.05  # PyAutoGUI low delay

dictJailItems = {0:'img/normiefish.png', 1:'img/goldenfish.png', 2:'img/epicfish.png', 3:'img/epiccoin.png',
                 4:'img/lifepotion.png', 5:'img/ruby.png', 6:'img/coin.png', 7:'img/zombieeye.png',
                 8:'img/unicornhorn.png', 9:'img/mermaidhair.png', 10:'img/chip.png', 11:'img/dragonscale.png',
                 12:'img/apple.png', 13:'img/banana.png', 14:'img/wolfskin.png'}

dictJailItemsNames = {0:'Normie fish', 1:'Golden fish', 2:'Epic fish', 3:'Epic Coin', 4:'Life Potion',
                      5:'Ruby', 6:'Coin', 7:'Zombie Eye', 8:'Unicorn Horn',
                      9:'Mermaid Hair', 10:'Chip', 11:'Dragon Scale', 12:'Apple', 13:'Banana', 14:'Wolf Skin'}

dictLootboxes = {0:"img/gotcommon.png", 1:"img/gotuncommon.png", 2:"img/gotrare.png", 3:'img/gotepic.png',
                 4:"img/gotedgy.png"}
dictLootboxesNames = {0:"Common LB", 1:"Uncommon LB", 2:"Rare LB", 3:'Epic LB', 4:"Edgy LB"}

trigger = cv2.imread("img/trigger.png")
jailed = cv2.imread('img/jail.png')
fine = cv2.imread('img/leftjail.png')

minHunts = 15
maxHunts = 25
minHuntInterval = 65
maxHuntInterval = 75
minSessionInterval = 180
maxSessionInterval = 400


def jailTest():
    for x in dictJailItems:
        currentCapture = pgui.screenshot('img/currentCapture.png', region=(0, 0, sizeX, sizeY))
        currentCapture = cv2.cvtColor(np.array(currentCapture), cv2.COLOR_RGB2BGR)
        find = cv2.imread(dictJailItems.get(x))

        result = cv2.matchTemplate(find, currentCapture, method)
        itemConfidence = round((1 - np.amin(result)) * 100, 4)

        if itemConfidence >= 85:
            print('>' + dictJailItemsNames.get(x) + ' found!. \nConf: ' + str(itemConfidence) + '%.')
            time.sleep(0.5)
            pgui.write(str(dictJailItemsNames.get(x)), interval=0.11)
            time.sleep(0.2)
            pgui.press('enter')
            time.sleep(1)
        else:
            print('>' + dictJailItemsNames.get(x) + ' NOT found!. \nConf: ' + str(itemConfidence) + '%.')


def flushScreen():
    print('>Flushing screen with CD')
    time.sleep(2)
    pgui.write('rpg cd', interval=0.09)
    time.sleep(0.1)
    pgui.press('enter')
    time.sleep(2)
    pgui.write('rpg cd', interval=0.13)
    time.sleep(0.1)
    pgui.press('enter')
    time.sleep(2)


def checkForDroppedLb():
    currentCapture = pgui.screenshot('img/currentCapture.png', region=(0, 0, sizeX, sizeY))
    currentCapture = cv2.cvtColor(np.array(currentCapture), cv2.COLOR_RGB2BGR)
    for x in dictLootboxes:
        find = cv2.imread(dictLootboxes.get(x))
        result = cv2.matchTemplate(find, currentCapture, method)
        droppedConfidence = round((1 - np.amin(result)) * 100, 4)
        if droppedConfidence >= 90:
            print('>Dropped ' + dictLootboxesNames.get(x) + '. \nConf: ' + str(droppedConfidence) + '%.')

            # Open dropped lootbox
            pgui.write('rpg open', interval=0.10)
            time.sleep(0.2)
            pgui.press('enter')
            print('>Opened lootbox.')
            time.sleep(1)
            flushScreen()

        else:  # If we didn't drop any lootboxes, print out confidence and end function
            print('>' + dictLootboxesNames.get(x) + ' NOT dropped. \nConf: ' + str(droppedConfidence) + '%.')

### BEGIN SCRIPT CLASS ###
class Script:
    def __init__(self, updateStats=True, huntsDone=0, huntsTowardsGather=0, huntsTowardsAdv=0, huntsTowardsLb=0, huntsTowardsEpic=0, jailcheckAmount=0, jailedAmount=0, currentlyJailed=False):
        self.updateStats = updateStats
        self.currentlyJailed = currentlyJailed

        # Stat counters
        self.huntsDone = huntsDone
        self.huntsTowardsGather = huntsTowardsGather
        self.huntsTowardsAdv = huntsTowardsAdv
        self.huntsTowardsLb = huntsTowardsLb
        self.huntsTowardsEpic = huntsTowardsEpic
        self.jailcheckAmount = jailcheckAmount
        self.jailedAmount = jailedAmount



    # End __main__ function
    # Begin action functions
    def goHunting(self):
        print('>Going hunting!')

        pgui.write('rpg hunt', interval=0.11)
        time.sleep(0.2)
        pgui.press('enter')
        self.huntsDone += 1
        self.huntsTowardsGather += 1
        self.huntsTowardsAdv += 1
        self.huntsTowardsLb += 1
        self.huntsTowardsEpic += 1
        time.sleep(3)

        self.checkForJailcheck()

        time.sleep(0.5)
        print('>Healing after hunt.')
        pgui.write('rpg heal', interval=0.13)
        time.sleep(0.15)
        pgui.press('enter')
        # Heals don't trigger jailcheck, no need to check for it
        time.sleep(1)
        print('>Casting CD just in case we dropped an item as to not interfere with jail check.')
        pgui.write('rpg cd', interval=0.09)
        time.sleep(0.1)
        pgui.press('enter')
        # Checking if we dropped a lootbox while hunting
        checkForDroppedLb()  # This function flushed the screen if we dropped a lootbox

    def goGathering(self):
        if app.shouldGather.get() == 1 and self.huntsTowardsGather == 5:
            print('>Going gathering!')
            self.huntsTowardsGather = 0
            pgui.write(str(app.gatherCommand.get()), interval=0.10)
            time.sleep(0.2)
            pgui.press('enter')
            time.sleep(3)

            self.checkForJailcheck()

            time.sleep(0.5)
            flushScreen()  # Flush screen after gathering

    def goAdventuring(self):
        if app.shouldAdv.get() == 1 and self.huntsTowardsAdv == 20:
            print('>Going adventuring!')
            self.huntsTowardsAdv = 0
            pgui.write('rpg adv', interval=0.13)
            time.sleep(0.2)
            pgui.press('enter')
            time.sleep(3)

            self.checkForJailcheck()

            time.sleep(0.5)
            print('>Healing after adventure.')
            pgui.write('rpg heal', interval=0.13)
            time.sleep(0.15)
            pgui.press('enter')

            checkForDroppedLb()  # If we dropped a lootbox, open it and flush screen

    def goLootbox(self):
        if app.shouldLb.get() == 1 and self.huntsTowardsLb == 20:
            print('>Buying Edgy Lootbox!')
            self.huntsTowardsLb = 0
            pgui.write('rpg buy ed lb', interval=0.11)
            time.sleep(0.3)
            pgui.press('enter')
            time.sleep(2)

            pgui.write('rpg open', interval=0.22)
            time.sleep(0.3)
            pgui.press('enter')
            time.sleep(2)

            flushScreen()  # Flush screen after attempt to buy ED Lootbox

    def goEpic(self):
        if app.shouldEpic.get() == 1 and self.huntsTowardsEpic == 20:
            print('>Going on Epic Quest!')
            self.huntsTowardsEpic = 0
            pgui.write('rpg epic quest', interval=0.15)
            time.sleep(0.3)
            pgui.press('enter')
            time.sleep(2)

            pgui.write(str(app.epicWave.get()), interval=0.21)
            time.sleep(0.3)
            pgui.press('enter')
            time.sleep(2)

            print('>Healing after Epic Quest.')
            pgui.write('rpg heal', interval=0.21)
            time.sleep(0.3)
            pgui.press('enter')
            time.sleep(2)

    # Begin other functions

    def checkForJailcheck(self):
        time.sleep(1)
        currentCapture = pgui.screenshot('img/currentCapture.png', region=(0, 0, sizeX, sizeY))
        currentCapture = cv2.cvtColor(np.array(currentCapture), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(trigger, currentCapture, method)
        jailcheckConfidence = round((1 - np.amin(result)) * 100, 4)

        if jailcheckConfidence >= 85:
            print('>We were prompted by Anti-AFK! \nConf: ' + str(jailcheckConfidence) + '%.')
            self.jailcheckAmount += 1
            time.sleep(1)

            print('>Begin jail test function.')
            jailTest()

            flushScreen()  # Flushing screen after answering jailTest

        else:
            print('>No jailcheck detected. \nConf: ' + str(jailcheckConfidence) + '%.')

    def areWeJailed(self):
        currentCapture = pgui.screenshot('img/currentCapture.png', region=(0, 0, sizeX, sizeY))
        currentCapture = cv2.cvtColor(np.array(currentCapture), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(jailed, currentCapture, method)
        JailedConfidence = round((1 - np.amin(result)) * 100, 4)

        if JailedConfidence >= 85:
            print('>We are in JAIL. \nConf: ' + str(JailedConfidence) + '%.')
            self.currentlyJailed = True
            self.jailedAmount += 1
            time.sleep(1)
            print('>Attempting escape.')
            pgui.write('rpg jail', interval=0.11)
            time.sleep(0.2)
            pgui.press('enter')
            time.sleep(2)
            pgui.write('protest', interval=0.11)
            time.sleep(0.2)
            pgui.press('enter')
            time.sleep(3)

            # Once we type protest, we will be prompted again for a jailcheck
            jailTest()

            time.sleep(2)

            # Confirmation we left jail!
            currentCapture = pgui.screenshot('img/currentCapture.png', region=(0, 0, sizeX, sizeY))
            currentCapture = cv2.cvtColor(np.array(currentCapture), cv2.COLOR_RGB2BGR)
            result = cv2.matchTemplate(fine, currentCapture, method)
            fineConfidence = round((1 - np.amin(result)) * 100, 4)
            if fineConfidence >= 90:
                self.currentlyJailed = False
                print('>Got out of jail successfully.\n')
                print('Conf: ' + str(fineConfidence) + '%.')
            else:
                print('>Could not get out of jail. \nHalting script.')
                time.sleep(86400)
                app.master.quit()


        else:
            print('>We are NOT jailed. \nConf: ' + str(JailedConfidence) + '%.')

    # Begin RUN function
    def run(self):
        print('>Beginning in 3 seconds. \nAlt-Tab to Discord NOW.')
        time.sleep(3)

        while(True):
            if not self.currentlyJailed:
                numberOfHuntsInRow = np.random.randint(minHunts, maxHunts)
                print('>Hunting ' + str(numberOfHuntsInRow) + ' times before stopping for a while.')

                for y in range(numberOfHuntsInRow):
                    self.areWeJailed()

                    self.goHunting()
                    self.goGathering()
                    self.goAdventuring()
                    self.goLootbox()
                    self.goEpic()

                    intervalBetweenHunts = np.random.randint(minHuntInterval, maxHuntInterval)
                    print('>Wait ' + str(intervalBetweenHunts) + ' seconds for next hunt.')
                    time.sleep(intervalBetweenHunts)

                invervalBetweenSessions = np.random.randint(minSessionInterval, maxSessionInterval)
                print('>Wait ' + str(invervalBetweenSessions) + ' seconds for next session.')
                time.sleep(invervalBetweenSessions)


script = Script()

### BEGIN GUI CLASS ###
# Configure GUI size, resizeability, name and icon
root = tk.Tk()
root.title("AutoRPG")
root.iconbitmap('icon.ico')
root.geometry("300x700")
root.minsize(150, 300)
root.maxsize(300, 700)
root.resizable(1, 1)

class Window:
    def __init__(self, master, isStarted=0, newMessage=False):
        self.master = master

        # Cross function variables go here
        self.isStarted = isStarted
        self.newMessage = newMessage

        self.shouldGather = tk.IntVar()
        self.shouldAdv = tk.IntVar()
        self.shouldLb = tk.IntVar()
        self.shouldEpic = tk.IntVar()
        self.gatherCommand = tk.StringVar()
        self.epicWave = tk.StringVar()

        # Here we should also define and call functions that keep on updating, like hideEntries, updateStats and updateConsole
        # GUI Builder function (long ass function)
        def BuildGUI():
            # Top frame (Header and start button)
            self.topFrame = tk.Frame(master, bg='#32353B')
            self.topFrame.pack(fill='both')

            # Header
            self.headerImg = tk.PhotoImage(file='imggui/header.png')
            self.header = tk.Label(self.topFrame, image=self.headerImg, bg='#32353B')
            self.header.pack(pady=5)

            # StartButton
            self.startButtonImg = tk.PhotoImage(file='imggui/start.png')
            self.startButton = tk.Button(self.topFrame, command=self.startScript, image=self.startButtonImg,
                                         borderwidth=0, bg='#32353B')
            self.startButton.pack(pady=10)

            # Input frame (Checkbuttons and entries)
            self.inputFrame = tk.Frame(master, bg='#32353B')
            self.inputFrame.pack(fill='both')

            # Left input frame (GREEN, checkbuttons)
            self.leftInputFrame = tk.Frame(self.inputFrame, bg='#32353B')
            self.leftInputFrame.pack(side='left')

            # Gathering checkbutton
            self.gatherCheckbutton = tk.Checkbutton(self.leftInputFrame, text='Gather', variable=self.shouldGather,
                                                    bg='#32353B', fg='white', selectcolor='black')
            self.gatherCheckbutton.pack(anchor='w', padx=15)
            # Adventure checkbutton
            self.advCheckbutton = tk.Checkbutton(self.leftInputFrame, text='Adventure', variable=self.shouldAdv,
                                                 bg='#32353B', fg='white', selectcolor='black')
            self.advCheckbutton.pack(anchor='w', padx=15)
            # Lootbox checkbutton
            self.lbCheckbutton = tk.Checkbutton(self.leftInputFrame, text='Edgy Lootbox', variable=self.shouldLb,
                                                bg='#32353B', fg='white', selectcolor='black')
            self.lbCheckbutton.pack(anchor='w', padx=15)
            # Epic Quest checkbutton
            self.epicCheckbutton = tk.Checkbutton(self.leftInputFrame, text='Epic Quest', variable=self.shouldEpic,
                                                  bg='#32353B', fg='white', selectcolor='black')
            self.epicCheckbutton.pack(anchor='w', padx=15)

            # Right input frame contains 2 extra frames
            self.rightInputFrame = tk.Frame(self.inputFrame, bg='#32353B')
            self.rightInputFrame.pack(anchor='nw', side='left', fill='both')

            self.gatherFrame = tk.Frame(self.rightInputFrame, bg='#32353B')
            self.gatherFrame.pack(anchor='nw', side='top', fill='both')

            self.epicFrame = tk.Frame(self.rightInputFrame, bg='#32353B')
            self.epicFrame.pack(anchor='sw', side='bottom', fill='both')

            # Gather command label
            self.gatherLabel = tk.Label(self.gatherFrame, text='Command:', bg='#32353B', fg='white')
            self.gatherLabel.pack(anchor='nw', side='left', pady=1)
            # Gather command entry
            self.gatherEntry = tk.Entry(self.gatherFrame, bg='#979FAF', fg='white', textvariable=self.gatherCommand, width=15, disabledbackground='#2F3136', disabledforeground='white')
            self.gatherEntry.pack(anchor='ne', side='left', pady=1)

            # Wave command label
            self.waveLabel = tk.Label(self.epicFrame, text='Epic Quest wave:', bg='#32353B', fg='white')
            self.waveLabel.pack(anchor='nw', side='left', pady=1)
            # Wave command entry
            self.waveEntry = tk.Entry(self.epicFrame, bg='#979FAF', fg='white', textvariable=self.epicWave, width=4, disabledbackground='#2F3136', disabledforeground='white')
            self.waveEntry.pack(anchor='ne', side='left', pady=1)

            # Console frame
            self.consoleFrame = tk.Frame(self.master, bg='#32353B')
            self.consoleFrame.pack(fill='both')
            # Console window
            self.ConsoleRegion = tk.LabelFrame(self.consoleFrame, text="Console", height=300, bg='#32353B', fg='white')
            self.ConsoleRegion.pack(padx=10, pady=5, fill='both')
            # Console text widget and scrollbar
            self.scrollbar = tk.Scrollbar(self.ConsoleRegion)
            self.consoleText = tk.Text(self.ConsoleRegion, state='disabled', fg='white', bg='#1A1F28', wrap='word', height=18, width=32, yscrollcommand=self.scrollbar.set)
            self.consoleText.pack(side='left')
            self.scrollbar.config(command=self.consoleText.yview)
            self.scrollbar.pack(side='left', fill='y')


            # Statistics frame
            self.statsFrame = tk.Frame(self.master, bg='#32353B', height=112)
            self.statsFrame.pack(fill='both')
            # Statistics window
            self.statsRegion = tk.LabelFrame(self.statsFrame, text="Statistics", height=112, bg='#32353B', fg='white')
            self.statsRegion.pack(padx=10, pady=5, fill='both')
            # Statistics text widget
            self.statsText = tk.Text(self.statsRegion, state='disabled', fg='white', bg='#1A1F28', wrap='word', height=5)
            self.statsText.pack()

            # Bottom frame (Kill button)
            self.bottomFrame = tk.Frame(master, bg='#32353B')
            self.bottomFrame.pack(fill='both')

            self.killButtonImg = tk.PhotoImage(file='imggui/kill.png')
            self.killButton = tk.Button(self.bottomFrame, command=self.master.destroy, image=self.killButtonImg,
                                        borderwidth=0, bg='#32353B')
            self.killButton.pack(pady=20)

        BuildGUI()

        # Keep updating Entries GUI in case gather/epicquest commands are ticked off
        def hideEntries():
            if self.shouldGather.get() == 1 and self.isStarted == 0:
                self.gatherEntry.configure(state='normal')
            else:
                self.gatherEntry.configure(state='disabled')

            if self.shouldEpic.get() == 1 and self.isStarted == 0:
                self.waveEntry.configure(state='normal')
            else:
                self.waveEntry.configure(state='disabled')

            # Keep on updating
            root.after(20, hideEntries)

        hideEntries()


        # Keep updating Statistics GUI
        def updateStats():
            self.statsText.config(state='normal')
            self.statsText.delete('1.0', '2.0')
            self.statsText.insert('1.0', str(script.huntsDone) + ' hunts done since epoch.                     ')

            self.statsText.delete('2.0', '3.0')
            self.statsText.insert('1.0', str(script.huntsTowardsGather) + '/5 hunts towards next gather.                  ')

            self.statsText.delete('3.0', '4.0')
            self.statsText.insert('1.0', str(script.huntsTowardsAdv) + '/20 hunts towards next adv/lb/q.                  ')

            self.statsText.delete('4.0', '5.0')
            self.statsText.insert('1.0', str(script.jailcheckAmount) + ' jail checks prompted.                     ')

            self.statsText.delete('5.0', '6.0')
            self.statsText.insert('1.0', str(script.jailedAmount) + ' times(s) jailed.                  ')
            self.statsText.config(state='disabled')

            # Keep on updating
            root.after(20, updateStats)

        updateStats()



    ### End __init__ function

    # Here we define functions that are called once or in events, like pressing buttons
    # StartButton function
    def startScript(self):
        self.isStarted = 1
        # Begin new thread for running the script
        self.t1 = threading.Thread(target=script.run, daemon=True)
        self.t1.start()

        # Lock any changes to configurations
        self.runningButtonImg = tk.PhotoImage(file='imggui/running.png')
        self.startButton.configure(state='disabled', image=self.runningButtonImg, disabledforeground='#D8798E')

        self.gatherCheckbutton.configure(state='disabled')
        self.advCheckbutton.configure(state='disabled')
        self.lbCheckbutton.configure(state='disabled')
        self.epicCheckbutton.configure(state='disabled')
        self.waveEntry.configure(state='disabled')
        self.gatherEntry.configure(state='disabled')



# Initialize Window object as app
app = Window(root)


# Logic functions

# Redirecting print output to GUI console (FINALLY!)
def redirector(inputStr):
    app.consoleText.config(state='normal')
    app.consoleText.insert(tk.INSERT, inputStr)
    app.consoleText.see(tk.END)
    app.consoleText.config(state='disabled')


sys.stdout.write = redirector  # Whenever sys.stdout.write is called, redirector is called.
print('>Detected system resolution: ' + str(sizeX) + 'x' + str(sizeY) + '.')

# Mainloop
root.mainloop()
