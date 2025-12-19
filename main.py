from tkinter import *
from tkinter import ttk

class Torn_BS_Helper():
    def __init__(self):
        self.root = Tk()
        self.root.title("Torn-BS-Helper")
        self.root.config(background="white")
        self.root.geometry("500x500")

        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=1)
        
        self.canvas = Canvas(main_frame, bg="white")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        
        v_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=RIGHT, fill=Y)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set)
        
        self.inner_frame = Frame(self.canvas, bg="white")
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.API_KEY = None
        self.bank_period = None

        self.set_api()
        self.set_stats()
        self.set_test_tool()
    
    def _on_frame_configure(self, event=None):
        """更新滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event=None):
        """调整内部框架的宽度以适应Canvas"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def _on_mousewheel(self, event):
        """鼠标滚轮事件"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _stock_box_generator(self, father, name):
        benefit_div = Frame(father, background="white")
        Checkbutton(benefit_div, text=name, background="white", width=10, anchor="w").grid(column=0, row=0, sticky="w")
        Label(benefit_div, text="bb数量：  ",background="white", width=10).grid(column=1, row=0)
        Spinbox(benefit_div, background="white", from_=0, to=999, increment=1, state="readonly", readonlybackground="white", width=5).grid(column=2, row=0)
        return benefit_div

    def set_api(self):  # API key输入框
        apikey = LabelFrame(self.inner_frame, text="API key", background="white")
        apikey.pack(fill="both", padx=10, pady=5)
        
        api_input_div = Frame(apikey, bg="white")
        api_label = Label(api_input_div, text="请输入您的API key:  ", background="white")
        api_label.grid(column=0, row=0)
        
        api_input = Entry(api_input_div)
        api_input.grid(column=1, row=0)
        api_input_div.pack(padx=10, pady=5)
        
        def get_api():
            self.API_KEY = api_input.get()
            print(f"API Key set: {self.API_KEY}")
        
        Button(apikey, text="运行", command=get_api).pack(pady=5)

    def set_stats(self):  # 属性填写框
        stats_input_div = LabelFrame(self.inner_frame, text="收入统计区", background="white")
        stats_input_div.pack(fill="both", padx=10, pady=5)

        # 银行部分
        bank_div = LabelFrame(stats_input_div, text="银行解锁及储蓄情况", background="white")
        bank_inner_div = Frame(bank_div, background="white")
        bank_time_div = Frame(bank_inner_div, background="white")
        
        self.bank_period = StringVar()
        periods = [
            ("1 week", "1w"),
            ("2 weeks", "2w"), 
            ("1 month", "1m"),
            ("2 months", "2m"),
            ("3 months", "3m")
        ]
        
        for text, value in periods:
            Radiobutton(bank_time_div, text=text, variable=self.bank_period, 
                       value=value, background="white").pack(anchor="w")
        
        bank_benefit_div = LabelFrame(bank_inner_div, text="增益情况", background="white")
        TCI_label = Label(bank_benefit_div, text="是否有TCI  ", background="white")
        TCI_label.grid(column=0, row=0)
        
        TCI_input = Checkbutton(bank_benefit_div, background="white")
        TCI_input.grid(column=1, row=0, pady=10)
        
        Label(bank_benefit_div, background="white", text="merits数量: ").grid(column=0, row=1)
        merits_input = Spinbox(bank_benefit_div, background="white", from_=0, to=10, 
                              increment=1, state="readonly", readonlybackground="white", width=10)
        merits_input.grid(column=0, row=2, columnspan=2)
        
        bank_benefit_div.grid(column=1, row=0, sticky="ns", padx=10)
        bank_time_div.grid(column=0, row=0, padx=10)
        bank_inner_div.pack(pady=10)
        bank_div.pack(fill="x", padx=5, pady=5)

        # 股票部分
        stock_div = LabelFrame(stats_input_div, text="分红股收益情况", background="white")
        stock_inner_div = Frame(stock_div, background="white")
        
        stock_name_dict = {
            "1":"TSB","4":"LAG","5":"IOU","6":"GRN","7":"THS","9":"TCT",
            "10":"CNC","12":"TMI","15":"FHG","16":"SYM","17":"LSC","18":"PRN",
            "19":"EWM","22":"HRG","24":"MUN","31":"TCC","32":"ASS","35":"PTS"
        }
        
        for i in stock_name_dict.values():
            tmp = self._stock_box_generator(stock_inner_div, i)
            tmp.pack(anchor="w", padx=10, pady=2)
        
        stock_inner_div.pack(pady=5)
        stock_div.pack(fill="x", padx=5, pady=5)

        # 工作部分
        job_div = LabelFrame(stats_input_div, text="工作收益情况", background="white")
        job_inner_div = Frame(job_div, background="white")
        Label(job_inner_div, text="工作日收入: ",background="white").grid(column=0,row=0)
        
        def vld():
            if job_income.get().isdigit():
                print("数字，符合要求")
                return True
            else:
                print("不是数字，不符合要求")
                return False
        
        def wrong():
            print("输入不符合要求，调用invalidcommand")
        job_income = Entry(job_inner_div, validate="focusout", validatecommand=vld, invalidcommand=wrong)
        job_income.grid(column=1,row=0)

        job_inner_div.pack(pady=5)
        job_div.pack(fill="x", padx=5, pady=5)

        # 其余部分
        other_div = LabelFrame(stats_input_div, text="其余收益情况（e.g.Crimes, OC, virus）", background="white")
        other_inner_div = Frame(other_div, background="white")
        Label(other_inner_div, text="工作日收入: ",background="white").grid(column=0,row=0)
        
        def vld():
            if other_income.get().isdigit():
                print("数字，符合要求")
                return True
            else:
                print("不是数字，不符合要求")
                return False
        
        def wrong():
            print("输入不符合要求，调用invalidcommand")
        other_income = Entry(other_inner_div, validate="focusout", validatecommand=vld, invalidcommand=wrong)
        other_income.grid(column=1,row=0)

        other_inner_div.pack(pady=5)
        other_div.pack(fill="x", padx=5, pady=5)

    def set_test_tool(self):
        def test_tool():
            print(f"Bank period: {self.bank_period.get()}")
            print(f"API Key: {self.API_KEY}")
        
        test_button = Button(self.inner_frame, text="测试", command=test_tool)
        test_button.pack(pady=10)

if __name__ == "__main__":
    app = Torn_BS_Helper()
    app.root.mainloop()