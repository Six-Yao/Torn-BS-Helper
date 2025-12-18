from tkinter import *
from api import *

global API_KEY

def set_api():
    global API_KEY
    apikey = LabelFrame(root, text="API key",background="white")
    apikey.pack(fill="both")
    api_input_div = Frame(apikey)
    api_label = Label(api_input_div, text="请输入您的API key:  ", background="white")
    api_label.grid(column=0,row=0)
    api_input = Entry(api_input_div)
    api_input.grid(column=1,row=0)
    api_input_div.pack()
    def get_api():
        API_KEY = api_input.get()
    api_button = Button(apikey, text="运行", command=get_api)
    api_button.pack()

if __name__ == "__main__":
    root = Tk()
    root.title("Torn-BS-Helper")
    root.config(background="white")
    root.geometry("500x500") # 设置大小，不够了记得来调
    set_api()
    def test_tool():
        print(API_KEY)
    test_button = Button(root, text="测试", command=test_tool)
    test_button.pack()
    mainloop()