from tkinter import messagebox
import mysql.connector 
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from random import randint


import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="sqluser",
  password="password",
  database="rock_paper_scissor_db"
)
cursor = db.cursor()

def login():
 global login_screen
 login_screen = Tk()
 login_screen.title("Login")
 login_screen.geometry("1200x1200")
 login_screen.configure(background="#9b59b6")
 
 username_label = Label(login_screen,font=150, text="Username * ",bg="#9b59b6")
 username_entry = Text(login_screen,height=2,width=30,wrap=NONE,font=30)
 password_label = Label(login_screen,font=150,text="Password * ",bg="#9b59b6")
 password_entry = Entry(login_screen,width=30,font=30, show="*")

 username_label.place(x=150,y=130)
 username_entry.place(x=300,y=120)
 password_label.place(x=150,y=250)
 password_entry.place(x=300,y=240) 
 
 #new user
 def register_user():
  # check if username and password fields are not empty
  uid=username_entry.get("1.0", "end-1c")
  if not(username_entry.get("1.0", "end-1c")) or not (password_entry.get()):
    messagebox.showerror("Error", "Username and password fields cannot be empty.")
  else:
    # check if user already exists in the database
            cursor.execute("SELECT * FROM user WHERE user_id = %s", (username_entry.get("1.0", "end-1c"),))
            result = cursor.fetchone()
            if result:
                messagebox.showerror("Error", "Username already exists.")
            else:
                # insert data into the database
                cursor.execute("INSERT INTO user (user_id, password) VALUES (%s, %s)",
                               (username_entry.get("1.0", "end-1c"), password_entry.get()))
                db.commit()
                messagebox.showinfo("Success", "Registration successful.")
                startgame(uid)

#Existing user
 def login_user():
  # check if username and password fields are not empty
  uid=username_entry.get("1.0", "end-1c")
  if not(username_entry.get("1.0", "end-1c")) or not (password_entry.get()):
    messagebox.showerror("Error", "Username and password fields cannot be empty.")
  else:
    # check if user exists in the database
    cursor.execute("SELECT * FROM user WHERE user_id = %s AND password = %s",
                   (username_entry.get("1.0", "end-1c"), password_entry.get()))
    user = cursor.fetchone()
    if user is not None:
      messagebox.showinfo("Success", "Login successful.")
      startgame(uid)
    else:
      messagebox.showerror("Error", "Invalid username or password.")
    db.commit()  
    
 # register and login buttons    
 register_button = Button(login_screen, text="Register", width=10, height=1, bg="#ffffff", fg="red", font=20, command=register_user).place(x=250,y=400)
 login_button = Button(login_screen, text="Login", width=10, height=1, bg="#ffffff", fg="red", font=20, command=login_user).place(x=400,y=400) 

 def startgame(uid):
  login_screen.destroy()
  root = Tk()
  root.title("Rock Paper Scissor")
  root.configure(background="#9b59b6")
  root.geometry("1500x1500")
  db = mysql.connector.connect(
  host="localhost",
  user="sqluser",
  password="password",
  database="rock_paper_scissor_db"
  )
  cursor = db.cursor()
  cursor.execute("SELECT score FROM user WHERE user_id=%s", (uid,))
  user_score = cursor.fetchone()[0]

  #picture
  rock_img= ImageTk.PhotoImage(Image.open("rock_user.png"))
  paper_img= ImageTk.PhotoImage(Image.open("paper_user.png"))
  scissor_img= ImageTk.PhotoImage(Image.open("scissor_user.png"))
  rock_img_comp= ImageTk.PhotoImage(Image.open("rock.png"))
  paper_img_comp= ImageTk.PhotoImage(Image.open("paper.png"))
  scissor_img_comp= ImageTk.PhotoImage(Image.open("scissor.png"))
  happy_user=ImageTk.PhotoImage(Image.open("happy_user.png"))
  sad_user=ImageTk.PhotoImage(Image.open("sad_user.png"))
  happy_comp=ImageTk.PhotoImage(Image.open("happy_comp.png"))
  sad_comp=ImageTk.PhotoImage(Image.open("sad_comp.png"))


#insert picture
  user_pic=Label(root,image=happy_user,bg="#9b59b6")
  comp_pic=Label(root,image=happy_comp,bg="#9b59b6")
  user_label=Label(root,image=paper_img,bg="#9b59b6")
  comp_label=Label(root,image=paper_img_comp,bg="#9b59b6")
  comp_label.grid(row=1,column=1)
  user_label.grid(row=1,column=5)
  user_pic.grid(row=0,column=5)
  comp_pic.grid(row=0,column=1)

#scores
  playerScore=Label(root,text=0,font=100,bg="#9b59b6",fg="white")
  computerScore=Label(root,text=0,font=100,bg="#9b59b6",fg="white")
  computerScore.grid(row=1,column=2)
  playerScore.grid(row=1,column=3)
  highestScore=Label(root, text=f"highest score:{user_score}",font=100,bg="#9b59b6",fg="yellow")
  highestScore.place(x=1200,y=100)

#indicators
  user_indicator=Label(root,font=50,text="USER",bg="#9b59b6",fg="white")
  comp_indicator=Label(root,font=50,text="COMPUTER",bg="#9b59b6",fg="white")
  user_indicator.config(padx=80, pady=80)
  comp_indicator.config(padx=80, pady=80)
  user_indicator.grid(row=0,column=3)
  comp_indicator.grid(row=0,column=2)
  highest_score_indicater=Label(root,font=60,text="HIGHEST SCORE:",bg="#9b59b6",fg="black")
  highest_score_indicater.place(x=1150,y=100)

#messages
  msg=Label(root,font=50,bg="#9b59b6",fg="white")    # text="YOU LOOSE"
  msg.place(x=718,y=803)
  
#buttons
  rock=Button(root,width=20,height=2,text="ROCK",bg="#FF3E4D",fg="black",command=lambda:updateChoice("rock"),activeforeground='red',font=("bold")).place(x=200,y=600)
  paper=Button(root,width=20,height=2,text="PAPER",bg="#FAD02E",fg="black",command=lambda:updateChoice("paper"),activeforeground='red',font=("bold")).place(x=430,y=600)
  scissor=Button(root,width=20,height=2,text="SCISSOR",bg="#0ABDE3",fg="black",command=lambda:updateChoice("scissor"),activeforeground='red',font=("bold")).place(x=660,y=600)
  end=Button(root,width=15,height=1,text="ENDGAME",bg="#c73866",fg="white",command=lambda:end_game(int(playerScore.cget("text"))),activeforeground='red',font=("bold")).place(x=1150,y=150)
  
#end game
  def end_game(x):
    sq="SELECT score FROM user WHERE user_id = %s"
    values = (uid,)
    cursor.execute(sq,values)
    result = cursor.fetchone()
    highest_score = result[0]
    if(int(highest_score) < int(x)):
       sq = "UPDATE user SET score = %s WHERE user_id = %s" 
       values = (x, uid)
       cursor.execute(sq,values)
       messagebox.showinfo("Success", "Highest score updated")
    else:
       messagebox.showinfo("Try again", "Best luck next time")
    db.commit()
    db.close()
    exit()
    root.destroy()  
    
#update message
  def updateMessage(x):
    msg['text']=x

#update user score
  def updateUserScore():
    score=int(playerScore["text"])
    score += 1
    playerScore["text"]=str(score)

#update computer score
  def updateCompScore():
    score=int(computerScore["text"])
    score += 1
    computerScore["text"]=str(score)

#update user and computer pictures
  def updatePicture(x):
    if x==1:
        comp_pic.configure(image=sad_comp)
        user_pic.configure(image=happy_user)
    elif x==0:
        comp_pic.configure(image=happy_comp)
        user_pic.configure(image=sad_user)
    else:
        comp_pic.configure(image=happy_comp)
        user_pic.configure(image=happy_user)


#check winner
  def checkWin(player,computer):
    x=2
    if player==computer:
        updateMessage("It's a tie!!!")
    elif player== "rock":
        if computer=="paper":
            updateMessage("You loose")
            updateCompScore()
            x=0
        else:     
            updateMessage("You Win")
            updateUserScore()
            x=1
    elif player=="paper":
        if computer=="scissor":
            updateMessage("You loose")
            updateCompScore()
            x=0
        else:
            updateMessage("You Win")
            updateUserScore()
            x=1
    elif player=="scissor":
        if computer=="rock":
            updateMessage("You loose")
            updateCompScore()   
            x=0   
        else:
            updateMessage("You Win")
            updateUserScore()       
            x=1
    else:
        pass  
    updatePicture(x)                    


#update choices
  choices=["rock","paper","scissor"]

  def updateChoice(x):

 #for computer
    compChoice=choices[randint(0,2)]

    if compChoice=="rock":
        comp_label.configure(image=rock_img_comp)
    elif compChoice=="paper":
        comp_label.configure(image=paper_img_comp)
    else:
        comp_label.configure(image=scissor_img_comp)      

 #for user
    if(x=="rock"):
        user_label.configure(image=rock_img)
    elif x=="paper":
        user_label.configure(image=paper_img)
    else:   
        user_label.configure(image=scissor_img)    
    checkWin(x,compChoice)    


#buttons

  root.mainloop()
 login_screen.mainloop()
login() 