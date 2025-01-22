import random
import time
from colorama import Fore
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#tests if valid to make integer, if not, tries again and prompts user to enter different value.
def makeInteger(name: str, value) -> int:
  while value != int:
    try:
      value = int(value)
    except:
      print('Please set ' + str(name) + 'to an integer.')
    else:
      print(str(name) + ' successfully set to: ' + str(value))
      break
  return value


def chooseRandomQuestionType() -> str:
  #list of all types of questions, and their chance of being called.
  lQuestionTypes = [{
      'q': '+',
      '%': 0.1
  }, {
      'q': '-',
      '%': 0.1
  }, {
      'q': '*',
      '%': 0.6
  }, {
      'q': '/',
      '%': 0.2
  }]
  foo = random.random()
  #the question type that causes the sum to be greater than the random float, becomes the returned question type.
  for i in lQuestionTypes:
    foo -= i['%']
    if foo <= 0:
      foo = i['q']
      break
    return foo

#yep
def solve(question: list) -> int:
  opperator = question[2]
  if opperator == '+':
    return (question[0] + question[1])
  elif opperator == '-':
    return (question[0] - question[1])
  elif opperator == '*':
    return (question[0] * question[1])
  elif opperator == '/':
    return (question[0] / question[1])
  else:
    raise Exception('invalid opperator, of name: ' + str(opperator))

def defaultMode():
  min = makeInteger("minimum", input("minimum: "))
  max = makeInteger('maximum', input("maximum: "))
  while True:
    #generates random question
    question = [
        random.randint(min, max),
        random.randint(min, max),
        chooseRandomQuestionType()
    ]
    question.append(solve(question))
    if chooseRandomQuestionType:
      print('Solve: ' + str(question[0]) + str(question[2]) + str(question[1]))
    if input('>>') == str(question[3]):
      print(Fore.GREEN + 'Welldone! The correct answer is indeed: ' +
            str(question[3]) + Fore.RESET)
    else:
      print('your such a failure... the correct answer is actually: ' +
            str(question[3]))

def get_avg(history: list) -> int:
  foo = 0
  #sum list
  for i in history:
    foo+=i
  #divide by length of list
  return int(foo/len(history))

def choose_rand_for_trainingMode(questions):
  foo = random.random()*10
  foo2 = foo
  while isinstance(foo, int) == False:
    #the question type that causes the sum to be greater than the random float, becomes the returned question type.
    for i in questions:
      foo -= 1-get_avg(questions[i]['history'])
      if foo <= 0:
        foo = i
        break
    if foo == foo2:
      print(Fore.BLUE+'Well done!!! You have proven mastery, feel free to try again')
      exit()
  return foo

def trainingMode():
  #questions = {1:['history':[ten 0s]], 2:['hist... up to 9}
  questions = {i+1:{'history':[0 for i in range(10)]} for i in range(9)}
  
  while True:
    input('Continue')
    cls()
    question = [choose_rand_for_trainingMode(questions),choose_rand_for_trainingMode(questions)]
    print(str(question[0])+'*'+str(question[1]))
    #starts timing player
    stopwatch_start = time.time()
    if input('>>') == str(question[0]*question[1]):
      for i in range(2):
        #makes sure both numbers are not equal. If they are, then the attempt is only stored once.
        if i == 1 and questions[int(question[1])] == questions[int(question[0])]:
          break
        #removes oldest known attempt, and adds new attempt representing now.
        del questions[int(question[i])]['history'][0]
        questions[int(question[i])]['history'].append(1-(time.time()-stopwatch_start)/5)
        #Basicly just makes sure that if you get it correct, you don't get a 0 score, and if you excel, you get bonus.
        if questions[int(question[i])]['history'][-1] < 0:
          questions[int(question[i])]['history'][-1] = 0.01
        elif questions[int(question[i])]['history'][-1] > 0.8:
          print(Fore.BLUE + "welldone!! you succeeded in " + str(time.time()-stopwatch_start) + " seconds! You will get significantly less of these numbers.")
        #second number isn't as important
        if i == 1:
          questions[int(question[i])]['history'][-1] *= 0.5
        #sends data
        ##print(questions[int(question[i])]['history'])
      #sends message to player that they succeeded.
      print(Fore.GREEN + 'correct' + Fore.RESET)
    else:
      for i in range(1):
        #updates history with the player's utter failure,
        del questions[int(question[i])]['history'][0]
        questions[int(question[i])]['history'].append(0)
        #before telling the player that they are an utter failure.
        print('wrong')
    
      

print('MODES:\n  default\n  training')
if input('>>') in 'training':
  #mode that keeps track of player time, and success rates, to decide which types of numbers they need more practice with. It eventually decides if the player is proficient enough to stop getting those numbers, until they have proved mastery on all numbers, and the player is rewarded with a 'congratulations!' kinda thing.
  trainingMode()
else:
  #random questions, of which use many different types of opperators.
  defaultMode()