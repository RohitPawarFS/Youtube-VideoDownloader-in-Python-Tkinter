def VideoUrl():
    DownloadingBarTextLable.configure(text="")
    DownloadnigLabelResult.configure(text="")
    DownloadnigSizeLabelResult.configure(text="")
    DownloadnigLabelTimeLeft.configure(text="")
    video_title.configure(text="")
    video_image.configure(text="")
    Authorresult.configure(text="")
    durationresult.configure(text="")
    ratingresult.configure(text="")
    videoidresult.configure(text="")
    viewcountresult.configure(text="")
    likesresult.configure(text="")
    dislikesresult.configure(text="")

    getdetail = threading.Thread(target=getvideo)
    getdetail.start()
    getdetail = threading.Thread(target=gettitle)                    
    getdetail.start()
    getdetail = threading.Thread(target=getimage)
    getdetail.start()


def gettitle():
    global title
    url = urltext.get()
    data = pafy.new(url)
    title=data.title
    video_title.config(text=title)
    Author=data.author
    Authorresult.config(text=Author)
    duration=data.duration
    durationresult.config(text=duration)
    rating=data.rating
    ratingresult.config(text=rating)
    viewcount=data.viewcount
    viewcountresult.config(text=viewcount)
    videoid=data.videoid
    videoidresult.config(text=videoid)
    likes=data.likes
    likesresult.config(text=likes)
    dislikes=data.dislikes
    dislikesresult.config(text=dislikes)

def getimage():
    global img
    url = urltext.get()
    data = pafy.new(url)
    thumbnail=data.thumb
    response=requests.get(thumbnail)
    img_byte=io.BytesIO(response.content)
    img=Image.open(img_byte)
    img=img.resize((235,235))
    img=ImageTk.PhotoImage(img)
    video_image.config(image=img)

def getvideo():
    global streams
    ListBox.delete(0, END)
    url = urltext.get()
    data = pafy.new(url)    
    streams = data.allstreams
    index = 0
    for i in streams:
        du = '{:0.1f}'.format(i.get_filesize()//(1024*1024))
        datas = str(index) + '.'.ljust(10, ' ') + str(i.quality).ljust(20, ' ') + str(i.extension).ljust(10, ' ') + str(i.mediatype) + ' ' + du.rjust(15, ' ') + "MB"
        ListBox.insert(END, datas)
        index += 1



def SelectCursor(evt):
    global downloadindex
    listboxdata = ListBox.get(ListBox.curselection())
    print(listboxdata)
    downloadstream = listboxdata[:3]
    downloadindex = int(''.join(x for x in downloadstream if x.isdigit()))


def DownloadVideo():
    getdata = threading.Thread(target=DownloadVideoData)
    getdata.start()


def DownloadVideoData():
    global downloadindex
    fgr = filedialog.askdirectory()
    DownloadingBarTextLable.configure(text="Downloading.....")
    def mycallback(total, recvd, ratio, rate, eta):
        global total12
        total12 = float('{:.5}'.format(total/(1024*1024)))
        DownloadnigProgressBar.configure(maximum=total12)
        recieved1 = '{:.5} mb'.format(recvd / (1024 * 1024))
        eta1 = '{:.2f} sec'.format(eta)
        DownloadnigSizeLabelResult.configure(text=total12)
        DownloadnigLabelResult.configure(text=recieved1)
        DownloadnigLabelTimeLeft.configure(text=eta1)
        DownloadnigProgressBar['value'] = recvd/(1024*1024)

    streams[downloadindex].download(filepath=fgr, quiet=True, callback=mycallback)
    DownloadingBarTextLable.configure(text="Downloaded")


def ChangeIntroLabelColor():
    ss = random.choice(colors)
    IntroLabel.configure(fg=ss)
    IntroLabel.after(20, ChangeIntroLabelColor)

from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
import random
import threading
import pafy
import io
import requests
from PIL import Image,ImageTk
from pytube import*
from tkinter import ttk

root = Tk()
root.configure(bg='whitesmoke')
root.title("YOUTUBE DOWNLOADER USING PYTHON")
root.geometry('950x700+300+50')
root.resizable(False, False)
root.attributes()




downloadindex = 0
total12 = 0
streams = ""
colors = ['white']


scrollbar = Scrollbar(root)
scrollbar.place(x=910, y=355, height=207, width=20)

IntroLabel = Label(root,text='YOUTUBE DOWNLOADER USING PYTHON',font=("times new roman",18),bg="#262626",fg='white')
IntroLabel.pack(side=TOP,fill=X)

urltext = StringVar()
IntroLabel = Label(root,text='Video URL',font=("times new roman",16),bg="whitesmoke")
IntroLabel.place(x=3,y=50)
UrlEntry = Entry(root, textvariable=urltext, font=('times new roman', 16),bg="lightyellow", width=73)
UrlEntry.place(x=120, y=50)


ListBox = Listbox(root, yscrollcommand=scrollbar.set, width=90, height=9, font=('times new roman', 15),bg="lightyellow",relief='ridge', bd=2, highlightcolor="blue", highlightthickness=2)
ListBox.place(x=2, y=354)
ListBox.bind("<<ListboxSelect>>", SelectCursor)

scrollbar.configure(command=ListBox.yview)


video_title=Label(root,text='Video Title Here',font=("times new roman",17,'bold'),bg='whitesmoke',anchor='w')
video_title.place(x=244,y=121,relwidth=1)
video_image=Label(root,text='Video \nImage',font=("times new roman",15),bg="lightgray",bd=2,relief=RIDGE)
video_image.place(x=4,y=120,width=235,height=235)
Author = Label(root, text='Author or Channel Name:', font=('times new roman', 15), bg='whitesmoke')
Author.place(x=244, y=152)
duration = Label(root, text='Duration: ', font=('times new roman', 15), bg='whitesmoke')
duration.place(x=244, y=183)
rating = Label(root, text='Rating: ', font=('times new roman', 15), bg='whitesmoke')
rating.place(x=244, y=215)
videoid = Label(root, text="Video I'd: ", font=('times new roman', 15), bg='whitesmoke')
videoid.place(x=244, y=245)
viewcount = Label(root, text='View Count: ', font=('times new roman', 15), bg='whitesmoke')
viewcount.place(x=244, y=275)
likes = Label(root, text='Likes: ', font=('times new roman', 15), bg='whitesmoke')
likes.place(x=244, y=305)
dislikes = Label(root, text='Dislikes: ', font=('times new roman', 15), bg='whitesmoke')
dislikes.place(x=544, y=305)
DownloadnigSizeLabel = Label(root, text='Total Size: ', font=('times new roman', 15), bg='whitesmoke')
DownloadnigSizeLabel.place(x=2, y=569)
DownloadnigLabel = Label(root, text='Recieved Size: ', font=('times new roman', 15), bg='whitesmoke')
DownloadnigLabel.place(x=2, y=592)
DownloadnigTime = Label(root, text='Time Left: ', font=('times new roman', 15), bg='whitesmoke')
DownloadnigTime.place(x=2, y=613)



Authorresult = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
Authorresult.place(x=453, y=152)
durationresult = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
durationresult.place(x=331, y=183)
ratingresult = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
ratingresult.place(x=313, y=215)
videoidresult = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
videoidresult.place(x=335, y=245)
viewcountresult = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
viewcountresult.place(x=356, y=275)
likesresult = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
likesresult.place(x=305, y=305)
dislikesresult = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
dislikesresult.place(x=628, y=305)
DownloadnigSizeLabelResult = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
DownloadnigSizeLabelResult.place(x=90, y=569)
DownloadnigLabelResult = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
DownloadnigLabelResult.place(x=125, y=592)
DownloadnigLabelTimeLeft = Label(root, text='', font=('times new roman', 15), bg='whitesmoke')
DownloadnigLabelTimeLeft.place(x=90, y=613)



DownloadingBarTextLable = Label(root, text='Downloading bar', width=20, font=('times new roman', 17), fg='black',bg='whitesmoke')
DownloadingBarTextLable.place(x=435, y=645)

DownloadingProgressBarLabel = Label(root, text='', width=58, font=('times new roman', 17), fg='red', bg='whitesmoke',relief='raised')
DownloadingProgressBarLabel.place(x=2, y=646)


DownloadnigProgressBar = Progressbar(DownloadingProgressBarLabel, orient=HORIZONTAL, value=0, length=100, maximum= total12)
DownloadnigProgressBar.grid(row=0, column=0, ipadx=185, ipady=3)



ClickButton = Button(root, text='Search', font=('times new roman', 16), bg='deep sky blue', fg='black',command=VideoUrl)
ClickButton.place(x=779,y=90,width=150,height=30)
DownloadButton = Button(root, text='Download', font=('times new roman', 16), bg='red', fg='white',activebackground='blue',width=15, command=DownloadVideo)
DownloadButton.place(x=730, y=600)



root.mainloop()