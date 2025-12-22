from tkinter import *
from tkinter import ttk, messagebox
import crawler
import calculator
import format_utils
from models import CollapsiblePane

class Torn_BS_Helper():
    def __init__(self):
        self.root = Tk()
        self.root.title("Torn-BS-Helper")
        self.root.config(background="white")
        self.root.geometry("600x800")

        self.digit_validation = self.root.register(format_utils.validate_digit_input)
        self.numeric_entry_formatters = []
        ttk.Style().configure("TRadiobutton", background="white")
        ttk.Style().configure("TCheckbutton", background="white")
        ttk.Style().configure("TSpinbox", disabledbackground="white")

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
        
        self.stock_name_dict = {
            "1":"TSB","4":"LAG","5":"IOU","6":"GRN","7":"THS","9":"TCT",
            "10":"CNC","12":"TMI","15":"FHG","16":"SYM","17":"LSC","18":"PRN",
            "19":"EWM","24":"MUN","32":"ASS","35":"PTS"
        }
        self.stock_divids = {"1": 50000000, "4": "368", "5": 12000000,
            "6": 4000000, "7": "365", "9": 1000000,
            "10": 80000000, "12": 25000000, "15": "367",
            "16": "370", "17": "369", "18": "366", 
            "19": "364", "24": "818", "32": "817"}

        self.item_value = {}
        self.API_KEY = StringVar()
        self.bank_period = StringVar(value="3m")
        self.bank_num = IntVar(value=2000000000)
        self.bank_merits = IntVar(value=0)
        self.TCI = BooleanVar(value=False)
        self.bank_rate = {}
        self.salary = IntVar(value=0)
        self.others = IntVar(value=0)
        self.stock_dict = {}
        self.STR = IntVar(value=10)
        self.DEF = IntVar(value=10)
        self.SPD = IntVar(value=10)
        self.DEX = IntVar(value=10)
        self.income_yearly = 0
        self.pts_value = 0
        self.energy_perks = 0

        self.set_tutorial()
        self.set_api()
        self.set_stats()
        self.set_BS()
        self.set_calculator()

    def set_default(self):
        self.bank_period.set("3m")
        self.bank_num.set(2000000000)
        self.bank_merits.set(0)
        self.TCI.set(False)
        self.salary.set(0)
        self.others.set(0)
        self.STR.set(10)
        self.DEF.set(10)
        self.SPD.set(10)
        self.DEX.set(10)
        self.income_yearly = 0
        for i in self.stock_name_dict.keys():
            self.stock_dict[i][0].set(False)
            self.stock_dict[i][1].set(0)

    def _on_frame_configure(self, event=None):
        """更新滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event=None):
        """调整内部框架的宽度以适应Canvas"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def _on_mousewheel(self, event):
        """鼠标滚轮事件"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _stock_box_generator(self, father, i, name):
        benefit_div = Frame(father, background="white")
        ttk.Checkbutton(benefit_div, text=name, width=7, variable=self.stock_dict[i][0], takefocus=0).grid(column=0, row=0, sticky="w")
        Label(benefit_div, text="bb数量：  ",background="white", width=10).grid(column=1, row=0)
        ttk.Spinbox(benefit_div, from_=0, to=999, increment=1, state="readonly", width=5, textvariable=self.stock_dict[i][1]).grid(column=2, row=0)
        return benefit_div
    
    def _bs_box_generator(self, father, name, stats, col, row):
        inner_BS_box = Frame(father, background="white", padx=10, pady=5)
        Label(inner_BS_box, text=name, background="white",width=10).grid(column=col, row=row)
        stats_entry = Entry(
            inner_BS_box,
            validate="key",
            validatecommand=(self.digit_validation, "%P", "%S", "%d"),
            highlightbackground="grey",
            highlightthickness=1,
            invalidcommand=self.wrong,
            width=15,
            relief="flat",
            highlightcolor="grey",
        )
        stats_entry.grid(column=col, row=row+1)
        self._register_numeric_entry(stats_entry, stats)
        inner_BS_box.grid(column=col, row=row//2)

    def _energy_box_generator(self, father, energy, num):
        if energy == 150:
            effective_energy = energy
        else:
            effective_energy = round(energy * (1+int(self.energy_perks) / 100))
        bs_gain = int(effective_energy * num * 40000)
        gain_text = format_utils.format_number(bs_gain)
        e_div = CollapsiblePane(father, expanded_text=f"{energy}E: 每年额外增长{gain_text} [折叠]", collapsed_text=f"{energy}E: 每年额外增长{gain_text} [展开]")
        e_div.pack(padx=10, pady=5,fill="both")
        Label(e_div.content, text=f"使用{format_utils.format_number(num)}个{energy}E物品（等效{format_utils.format_number(effective_energy)}E)").pack()
        Label(e_div.content, text=f"多用{format_utils.format_number(int(effective_energy*num))}E").pack()

    def _SE_box_generator(self, father, num, stats, name, stats_name, col, row):
        bs_gain = int(stats * pow(1.01, num))
        text = (
            f"每年使用{format_utils.format_number(num)}个{name}\n"
            f"{stats_name}增长{format_utils.format_number(bs_gain)}"
        )
        Label(father, text=text, borderwidth=5, background="white", highlightcolor="grey", highlightthickness=2, highlightbackground="grey", width=25).grid(row=row, column=col, padx=10, pady=5)

    def _register_numeric_entry(self, entry_widget, variable):
        formatter = format_utils.NumericEntryFormatter(entry_widget, variable)
        self.numeric_entry_formatters.append(formatter)

    def wrong(self):
        messagebox.showwarning("错误","请输入数字")

    def set_api(self):  # API key输入框
        apikey = LabelFrame(self.inner_frame, text="API key", background="white")
        apikey.pack(fill="both", padx=10, pady=5)
        
        api_input_div = Frame(apikey, bg="white")
        api_label = Label(api_input_div, text="请输入您的API key (需要Limited Access):  ", background="white")
        api_label.grid(column=0, row=0)
        
        api_input = Entry(api_input_div, textvariable=self.API_KEY, relief="flat", highlightbackground="grey",
                          highlightcolor="grey", highlightthickness=1)
        api_input.grid(column=1, row=0)
        api_input_div.pack(padx=10, pady=5)
        
        def crawl():
            try:
                self.set_default()
                return crawler.crawlers(self, self.API_KEY.get())
            except Exception as e:
                messagebox.showerror("错误", e)

        ttk.Button(apikey, text="运行", command=crawl, takefocus=0).pack(pady=5)

    def set_stats(self):  # 属性填写框
        stats_input_div = LabelFrame(self.inner_frame, text="收入统计区", background="white")
        stats_input_div.pack(fill="both", padx=10, pady=5)

        # 银行部分
        bank_div = LabelFrame(stats_input_div, text="银行解锁及储蓄情况", background="white")
        bank_inner_div = Frame(bank_div, background="white")

        bank_num_div = Frame(bank_inner_div, background="white")
        Label(bank_num_div, text="储蓄额：", background="white").pack(anchor="w")
        bank_amount_entry = Entry(
            bank_num_div,
            validate="key",
            validatecommand=(self.digit_validation, "%P", "%S", "%d"),
            relief="flat",
            highlightcolor="grey",
            invalidcommand=self.wrong,
            width=20,
            highlightthickness=1,
            highlightbackground="grey",
        )
        bank_amount_entry.pack()
        self._register_numeric_entry(bank_amount_entry, self.bank_num)

        bank_time_div = Frame(bank_inner_div, background="white")
        periods = [
            ("1 week", "1w"),
            ("2 weeks", "2w"), 
            ("1 month", "1m"),
            ("2 months", "2m"),
            ("3 months", "3m")
        ]
        
        for text, value in periods:
            ttk.Radiobutton(bank_time_div, text=text, variable=self.bank_period, 
                       value=value, takefocus=0).pack(anchor="w")
        
        bank_benefit_div = LabelFrame(bank_inner_div, text="增益情况", background="white")
        TCI_label = Label(bank_benefit_div, text="是否有TCI  ", background="white")
        TCI_label.grid(column=0, row=0)
        
        TCI_input = ttk.Checkbutton(bank_benefit_div, variable=self.TCI, takefocus=0)
        TCI_input.grid(column=1, row=0, pady=10)
        
        Label(bank_benefit_div, background="white", text="merits数量: ").grid(column=0, row=1)
        merits_input = ttk.Spinbox(bank_benefit_div, from_=0, to=10, 
                              increment=1, state="readonly", width=10, textvariable=self.bank_merits)
        merits_input.grid(column=0, row=2, columnspan=2)
        
        bank_benefit_div.grid(column=2, row=0, sticky="ns", padx=10)
        bank_num_div.grid(column=0, row=0, padx=10)
        bank_time_div.grid(column=1, row=0, padx=10)
        bank_inner_div.pack(pady=10)
        bank_div.pack(fill="x", padx=5, pady=5)

        # 股票部分
        stock_div = LabelFrame(stats_input_div, text="分红股收益情况 (TCC和HRG的收益有随机性，建议自己填写在月收入; 如不勾选则不计算收入)", background="white")
        stock_inner_div = Frame(stock_div, background="white")
        
        for i in self.stock_name_dict.keys():
            self.stock_dict[i]=(BooleanVar(value=False), IntVar(value=0))
            tmp = self._stock_box_generator(stock_inner_div, i, self.stock_name_dict[i])
            tmp.pack(anchor="w", padx=10, pady=2)
        
        stock_inner_div.pack(pady=5)
        stock_div.pack(fill="x", padx=5, pady=5)

        # 工作部分
        job_div = LabelFrame(stats_input_div, text="工作收益情况 (系统公司默认不爬取，你可以自己填进去)", background="white")
        job_inner_div = Frame(job_div, background="white")
        Label(job_inner_div, text="工作日收入: ",background="white").grid(column=0,row=0)
        
        job_income = Entry(
            job_inner_div,
            validate="key",
            validatecommand=(self.digit_validation, "%P", "%S", "%d"),
            highlightcolor="grey",
            relief="flat",
            invalidcommand=self.wrong,
            highlightbackground="grey",
            highlightthickness=1,
        )
        job_income.grid(column=1,row=0)
        self._register_numeric_entry(job_income, self.salary)

        job_inner_div.pack(pady=5)
        job_div.pack(fill="x", padx=5, pady=5)

        # 其余部分
        other_div = LabelFrame(stats_input_div, text="其余收益情况（e.g.Crimes, OC, virus, mug）需自行填写，按31d计", background="white")
        other_inner_div = Frame(other_div, background="white")
        Label(other_inner_div, text="其余月收入: ",background="white").grid(column=0,row=0)


        other_income = Entry(
            other_inner_div,
            validate="key",
            validatecommand=(self.digit_validation, "%P", "%S", "%d"),
            highlightcolor="grey",
            relief="flat",
            invalidcommand=self.wrong,
            highlightbackground="grey",
            highlightthickness=1,
        )
        other_income.grid(column=1,row=0)
        self._register_numeric_entry(other_income, self.others)

        other_inner_div.pack(pady=5)
        other_div.pack(fill="x", padx=5, pady=5)

    def set_BS(self):
        BS = LabelFrame(self.inner_frame, text="BS", background="white")
        BS.pack(fill="both", padx=10, pady=5)

        BS_inner_div = Frame(BS, background="white")
        BS_inner_div.pack()
        self._bs_box_generator(BS_inner_div, "STR", self.STR, 0, 0)
        self._bs_box_generator(BS_inner_div, "DEF", self.DEF, 1, 0)
        self._bs_box_generator(BS_inner_div, "SPD", self.SPD, 0, 2)
        self._bs_box_generator(BS_inner_div, "DEX", self.DEX, 1, 2)

    def set_calculator(self):
        Frame(self.inner_frame, height=2, background="black").pack(fill="x")
        Label(self.inner_frame, text="确认上述内容无误后，点击按钮开始计算", background="white", font=("TkDefaultFont", 10, "bold")).pack()
        def start_calculate():
            for i in self.result_div.winfo_children():
                i.destroy()
            self.set_income_result()
            self.set_energy_result()
            self.set_SE_result()
        ttk.Button(self.inner_frame, text="开始计算", command=start_calculate, takefocus=0).pack()
    
        self.result_div = LabelFrame(self.inner_frame, text="计算结果", background="white")
        self.result_div.pack(fill="both", padx=10, pady=5)
        
    def set_income_result(self):
        bank_income = calculator.calculate_bank(self.TCI.get(), self.bank_merits.get(), self.bank_num.get(), self.bank_rate[self.bank_period.get()])
        stock_income = 0
        for i, j in self.stock_dict.items():
            available = j[0].get()
            num = j[1].get()
            if available and num and i!="35":
                divid = self.stock_divids[i]
                if isinstance(divid, int):
                    stock_income += calculator.calculate_stocks(divid*num, 31)
                else:
                    divid = self.item_value[divid]
                    stock_income += calculator.calculate_stocks(divid*num, 7)
            if i == "35" and num:
                divid = 100 * self.pts_value
                stock_income += calculator.calculate_stocks(divid*num, 7)
        other_income = calculator.calculate_others(self.others.get())
        self.income_yearly = int(bank_income + stock_income*365 + other_income*365 + self.salary.get()*365)
        total_income_text = format_utils.format_number(self.income_yearly)
        profit_div = CollapsiblePane(
            self.result_div,
            expanded_text=f"年收入: {total_income_text} [折叠]",
            collapsed_text=f"年收入: {total_income_text} [展开]",
        )
        profit_div.pack(fill="both", padx=10, pady=5)
        bank_div = Frame(profit_div.content, background="white")
        Label(bank_div, text="银行年收入: ").grid(column=0, row=0)
        Label(bank_div, text=format_utils.format_number(int(bank_income))).grid(column=1, row=0)
        bank_div.pack()

        stocks_div = Frame(profit_div.content, background="white")
        Label(stocks_div, text="股票年收入: ").grid(column=0, row=0)
        Label(stocks_div, text=format_utils.format_number(int(stock_income*365))).grid(column=1, row=0)
        stocks_div.pack()

        salary_div = Frame(profit_div.content, background="white")
        Label(salary_div, text="工作年收入: ").grid(column=0, row=0)
        Label(salary_div, text=format_utils.format_number(int(self.salary.get()*365))).grid(column=1, row=0)
        salary_div.pack()
        
        other_div = Frame(profit_div.content, background="white")
        Label(other_div, text="其他年收入: ").grid(column=0, row=0)
        Label(other_div, text=format_utils.format_number(int(other_income)*365)).grid(column=1, row=0)
        other_div.pack()

    def set_energy_result(self):
        separator = Frame(self.result_div, bg="white")
        Frame(separator, height=1, bg="grey").pack(side="left", fill="x", expand=True, pady=5)
        Label(separator, text=f"按照10k E-40m BS计算，帮派饮料加成{self.energy_perks}%", bg="white").pack(side="left", pady=5, padx=5)
        Frame(separator, height=1, bg="grey").pack(side="left", fill="x", expand=True, pady=5)
        separator.pack(fill="both")
        five_e_nums = min(12*365, self.income_yearly//self.item_value["985"])
        ten_e_nums = min(12*365, self.income_yearly//self.item_value["986"])
        fifteen_e_nums = min(12*365, self.income_yearly//self.item_value["987"])
        twenty_e_nums = min(12*365, self.income_yearly//min(self.item_value["530"], self.item_value["553"]))
        twentyfive_e_nums = min(12*365, self.income_yearly//min(self.item_value["532"], self.item_value["554"]))
        thirty_e_nums = min(12*365, self.income_yearly//min(self.item_value["533"], self.item_value["555"]))
        FHC_nums = min(4*365, self.income_yearly//self.item_value["367"])
        self._energy_box_generator(self.result_div, 5, five_e_nums)
        self._energy_box_generator(self.result_div, 10, ten_e_nums)
        self._energy_box_generator(self.result_div, 15, fifteen_e_nums)
        self._energy_box_generator(self.result_div, 20, twenty_e_nums)
        self._energy_box_generator(self.result_div, 25, twentyfive_e_nums)
        self._energy_box_generator(self.result_div, 30, thirty_e_nums)
        self._energy_box_generator(self.result_div, 150, FHC_nums)

    def set_SE_result(self):
        separator = Frame(self.result_div, bg="white")
        Frame(separator, height=1, bg="grey").pack(side="left", fill="x", expand=True, pady=5)
        Label(separator, text="SE使用情况", bg="white").pack(side="left", pady=5, padx=5)
        Frame(separator, height=1, bg="grey").pack(side="left", fill="x", expand=True, pady=5)
        separator.pack(fill="both")
        SE_div = Frame(self.result_div, bg="white")
        SE_inner_div = Frame(SE_div, bg="white")
        DEF_num = min(4*365, self.income_yearly//self.item_value["330"])
        DEX_num = min(4*365, self.income_yearly//self.item_value["106"])
        STR_num = min(4*365, self.income_yearly//self.item_value["331"])
        SPD_num = min(4*365, self.income_yearly//self.item_value["329"])
        self._SE_box_generator(SE_inner_div, STR_num, self.STR.get(), "哑铃", "STR",0, 0)
        self._SE_box_generator(SE_inner_div, DEF_num, self.DEF.get(), "拳套", "DEF",1, 0)
        self._SE_box_generator(SE_inner_div, SPD_num, self.SPD.get(), "滑板", "SPD",0, 1)
        self._SE_box_generator(SE_inner_div, DEX_num, self.DEX.get(), "降落伞", "DEX",1, 1)
        SE_inner_div.pack()
        SE_div.pack(fill="both", padx=10, pady=5)
        
    def set_tutorial(self):
        tutorial = CollapsiblePane(self.inner_frame, expanded_text="收起", collapsed_text="使用指南", is_expanded=True)
        tutorial.pack(fill="both", padx=10, pady=5)
        Label(tutorial.content, text="从settings->API keys中复制一个级别至少为Limited Access的key到最上方文本框中\n点击运行，等待数据爬取结束\n随后按需修改/添加数值，点击最下方计算开始计算").pack()

if __name__ == "__main__":
    app = Torn_BS_Helper()
    app.root.mainloop()