# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 21:27:09 2020

@author: wb305167
"""

import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter.messagebox import showinfo

from tkinter import filedialog
from turtle import color

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import seaborn as sns

from taxcalc import *

from PIL import Image,ImageTk

'''
CREATE APPLICATION AS A SUBCLASS OF CLASS 'FRAME' - IT IS A BIG CONTAINER WHICH CONTAINS WIDGETS FOR ENTERING DATA, WEIGHTS, POLICY FILE
BUTTONS FOR COMPUTING TAX UNDER CURRENT LAW, UNDER REFORM AND CALCULATING TAX EXPENDITURE

'''

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.number = 0
        self.widgets = []
        self.grid()
        
        #self.createWidgets()
        
        self.reform={}
        self.selected_item = ""
        self.selected_value = ""
        self.selected_year = 2020
        self.sub_directory = "taxcalc"
        self.data_filename = "bigdata_temp_withdepr.csv"
        self.weights_filename = "bigcit_weights_egypt.csv"
        self.policy_filename = "current_law_policy_cit_egypt.json"
        self.records_vars_filename = "records_variables_egypt.json"
        self.growfactors_filename = self.sub_directory+"/"+"growfactors_egypt.csv"    
        self.benchmark_filename = "tax_incentives_benchmark.json"        
        self.total_revenue_text1 = ""
        self.reform_revenue_text1 = ""
        #self.reform_filename = "egypt_reform.json"

        self.fontStyle = tkfont.Font(family="Helvetica", size="12")
        self.fontStyle_sub_title = tkfont.Font(family="Helvetica", size="14", weight="bold")         
        self.fontStyle_title = tkfont.Font(family="Helvetica", size="18", weight="bold")
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)        
        self.text_font = ('Arial', '12')
        self.insert_image('world_bank.png')      
        # positions
        
        self.title_pos_x = 0.5
        self.title_pos_y = 0.0
        
        self.block_1_title_pos_x = 0.15
        self.block_1_title_pos_y = 0.1
        self.block_title_entry_gap_y = 0.05
        self.block_entry_entry_gap_y = 0.05
        self.block_1_entry_x = 0.2
        self.entry_entry_gap_y = 0.03
        self.block_1_entry_1_y = (self.block_1_title_pos_y+self.block_title_entry_gap_y)
        self.block_1_entry_2_y = (self.block_1_entry_1_y+self.block_entry_entry_gap_y)
        self.block_1_entry_3_y = (self.block_1_entry_2_y+self.block_entry_entry_gap_y)
        self.block_1_entry_4_y = (self.block_1_entry_3_y+self.block_entry_entry_gap_y)        
        self.entry_button_gap = 0.02
        self.button_1_pos_x = 0.2
        self.block_block_gap = 0.1

        self.block_1A_title_pos_y = self.block_1_entry_3_y + self.entry_button_gap + self.block_block_gap        
        self.button_1_pos_y = self.block_1A_title_pos_y + self.block_title_entry_gap_y

        self.block_2_entry_1_1_x = 0.03
        self.block_2_title_pos_y = self.button_1_pos_y + self.block_block_gap
        self.text_entry_gap = 0.03
        self.block_2_entry_1_1_y = (self.block_2_title_pos_y+
                                    self.block_title_entry_gap_y+
                                    self.text_entry_gap)
        
        '''Position of combo-box for adding policy reform'''
        self.block_2_combo_entry_gap_x = 0.21
        self.block_2_entry_entry_gap_x = 0.04
        self.block_2_entry_1_2_x = self.block_2_entry_1_1_x + self.block_2_combo_entry_gap_x
        self.block_2_entry_1_3_x = self.block_2_entry_1_2_x + self.block_2_entry_entry_gap_x

        self.block_3_title_pos_x = 0.3
        self.block_3_title_pos_y = self.block_1A_title_pos_y
        self.block_3_entry_x = 0.4
        self.block_3_entry_y = self.block_3_title_pos_y + self.block_title_entry_gap_y      
        self.button_3_pos_x = 0.3  
        self.button_3_pos_y = self.block_3_entry_y + 2*self.entry_button_gap        
             
        self.button_add_reform_x = self.block_2_entry_1_3_x + self.block_2_entry_entry_gap_x + 0.03
        self.button_del_reform_x = self.block_2_entry_1_3_x + self.block_2_entry_entry_gap_x + 0.05
        self.button_clear_reform_x = self.block_2_entry_1_3_x + self.block_2_entry_entry_gap_x + 0.07
        self.button_update_reform_param_x = self.block_2_entry_1_3_x + self.block_2_entry_entry_gap_x + 0.11
           
        
        '''Creating a Label for Tax Microsimulation Model'''

        self.root_title=Label(text="Egypt CIT Microsimulation Model",
                 font = self.fontStyle_title)
        self.root_title.place(relx = self.title_pos_x, rely = self.title_pos_y, anchor = "n")
        
        '''Creating a Label for Data Inputs - for Data File, Weights File and Policy File'''

        self.l1=Label(text="Data Inputs",
                 font = self.fontStyle_sub_title)
        self.l1.place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
        
        '''Creating an input field for Data File'''

        self.entry_data_filename = Entry(width=30, font = self.fontStyle)
        self.entry_data_filename.place(relx = self.block_1_entry_x, 
                                  rely = self.block_1_entry_1_y,
                                  anchor = "e")
        self.entry_data_filename.insert(END, self.data_filename)

        '''Create a button to Change Data File '''
        self.button_data_filename = ttk.Button(text = "Change Data File", style='my.TButton', command=self.input_data_filename)
        self.button_data_filename.place(relx = self.block_1_entry_x,
                                   rely = self.block_1_entry_1_y, anchor = "w")
        #button.place(x=140,y=50)
        
        '''Create an input field for Weight File'''

        self.entry_weights_filename = Entry(width=30, font = self.fontStyle)
        self.entry_weights_filename.place(relx = self.block_1_entry_x,
                                     rely = self.block_1_entry_2_y, anchor = "e")
        self.entry_weights_filename.insert(END, self.weights_filename)

        '''Create a Button to Change Weight File '''
        self.button_weights_filename = ttk.Button(text = "Change Weights File", style='my.TButton', command=self.input_weights_filename)
        self.button_weights_filename.place(relx = self.block_1_entry_x, 
                                      rely = self.block_1_entry_2_y, anchor = "w")
        
        '''Create an input field for Policy File'''
        self.entry_policy_filename = Entry(width=30, font = self.fontStyle)
        self.entry_policy_filename.place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_3_y, anchor = "e")
        self.entry_policy_filename.insert(END, self.policy_filename)

        '''Create a Button to Change Policy File'''

        self.button_policy_filename = ttk.Button(text = "Change Policy File", style='my.TButton', command=self.input_policy_filename)
        self.button_policy_filename.place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_3_y, anchor = "w")
          
        
        '''Create Label for Current Law '''
        
        self.l1A=Label(text="Current Law",
                 font = self.fontStyle_sub_title)
        self.l1A.place(relx = self.block_1_title_pos_x, rely = self.block_1A_title_pos_y, anchor = "w")
        
        '''Create Button to Generate Current Law Total Revenues using the command function 'generate_total_revenues'''

        self.button_generate_revenue_curr_law = ttk.Button(text = "Generate Current Law Total Revenues", style='my.TButton', command=self.generate_total_revenues)
        self.button_generate_revenue_curr_law.place(relx = self.button_1_pos_x, 
                                                 rely = self.button_1_pos_y, anchor = "e")
        
        '''Create Label for Reform '''

        self.l2=Label(text="Reform", font = self.fontStyle_sub_title)
        self.l2.place(relx = self.block_1_title_pos_x, rely = self.block_2_title_pos_y, anchor = "w")
        
        '''Create a Label for Selecting Policy parameter for Policy Reform'''

        self.l3=Label(text="Select Policy Parameter: ", font = self.fontStyle)
        self.l3.place(relx = self.block_2_entry_1_1_x, 
                 rely = self.block_2_entry_1_1_y-self.text_entry_gap, anchor = "w")
        
        '''Creating a menu of Policy Parameters using a Function 'policy_options' which returns list of policy params from current law policy '''

        self.current_law_policy, self.policy_options_list = self.policy_options()
        #self.policy_options_list.remove('gst_rate')
        self.block_widget_dict = {}
        self.block_selected_dict = {}
        self.num_reforms = 1
        
        '''Creating a combobox to allow menu of policy params to display and choose one param at a time'''

        self.block_widget_dict[1] = {}
        self.block_selected_dict[1] = {}
        self.block_widget_dict[1][1] = ttk.Combobox(value=self.policy_options_list, font=self.text_font, name=str(self.num_reforms))
        #self.block_widget_dict[1][1].current(0)
        self.block_widget_dict[1][1].place(relx = self.block_2_entry_1_1_x, 
                        rely = self.block_2_entry_1_1_y, anchor = "w", width=300)
        
        self.block_widget_dict[1][1].bind("<<ComboboxSelected>>", self.show_policy_selection)
        
        '''Create a Label for Year to be entered for Reform '''

        self.l4=Label(text="Year: ", font = self.fontStyle)
        self.l4.place(relx = self.block_2_entry_1_2_x, 
                 rely = self.block_2_entry_1_1_y-self.text_entry_gap, anchor = "w")
        self.block_widget_dict[1][2] = Entry(width=6, font = self.fontStyle)
        self.block_widget_dict[1][2].place(relx = self.block_2_entry_1_2_x, rely = self.block_2_entry_1_1_y, anchor = "w")
        
        '''Create a Label for Value of Policy Param chosen for Reform '''

        self.l5=Label(text="Value: ", font = self.fontStyle)
        self.l5.place(relx = self.block_2_entry_1_3_x, 
                 rely = self.block_2_entry_1_1_y-self.text_entry_gap, anchor = "w")
        self.block_widget_dict[1][3] = Entry(width=10, font = self.fontStyle)
        self.block_widget_dict[1][3].place(relx = self.block_2_entry_1_3_x, rely = self.block_2_entry_1_1_y, anchor = "w")
        
        '''Create a Button for adding Policy Params to reform '''

        #self.num_reforms += 1
        self.button_add_reform = ttk.Button(text="+", style='my.TButton', command=self.create_policy_widgets, width=2)
        self.button_add_reform.place(relx = self.button_add_reform_x, rely = self.block_2_entry_1_1_y, anchor = "w") 

        '''Create a Button for deleting a reform '''

        self.button_delete_reform = ttk.Button(text="-", style='my.TButton', command=self.delete_policy_widgets, width=2)
        self.button_delete_reform.place(relx = self.button_del_reform_x, rely = self.block_2_entry_1_1_y, anchor = "w") 

        '''Create a Button to Reset policy reform selection'''

        self.button_clear_reform = ttk.Button(text="Reset", style='my.TButton', command=self.reset_policy_widgets, width=6)
        self.button_clear_reform.place(relx = self.button_clear_reform_x, rely = self.block_2_entry_1_1_y, anchor = "w")
        #self.button_clear_reform.bind('<Button-7>', self.reset_policy_widgets)
        
        '''Create a Button for Generating Revenue under Reform using command function 'apply_policy_change'''

        self.button_generate_revenue_policy = ttk.Button(text = "Generate Revenue under Reform", style='my.TButton', command=self.apply_policy_change)
        self.button_2_pos_y = (self.block_2_entry_1_1_y+(self.num_reforms)*(self.entry_entry_gap_y+0.05)) +self.entry_button_gap
        self.button_generate_revenue_policy.place(relx = self.button_1_pos_x,
                                                    rely = self.button_2_pos_y, anchor = "w")


        
        '''Create Label for Tax Expenditure'''

        self.l3A=Label(text="Tax Expenditures",
                 font = self.fontStyle_sub_title)
        self.l3A.place(relx = self.block_3_title_pos_x, rely = self.block_3_title_pos_y, anchor = "w")

        self.entry_benchmark_filename = Entry(width=30, font = self.fontStyle)
        self.entry_benchmark_filename.place(relx = self.block_3_entry_x, 
                                  rely = self.block_3_entry_y,
                                  anchor = "e")
        self.entry_benchmark_filename.insert(END, self.benchmark_filename)
        
        '''Create Button for changing Benchmark file for Tax Expenditure'''

        self.button_benchmark_filename = ttk.Button(text = "Change Benchmark File", style='my.TButton', command=self.input_benchmark_filename)
        self.button_benchmark_filename.place(relx = self.block_3_entry_x,
                                   rely = self.block_3_entry_y, anchor = "w")    

        '''Create Button for calculating Tax Expenditure using Benchmark File '''    

        self.button_generate_tax_expenditures = ttk.Button(text = "Generate Tax Expenditures", style='my.TButton', command=self.generate_tax_expenditures)
        self.button_generate_tax_expenditures.place(relx = self.button_3_pos_x, 
                                                 rely = self.button_3_pos_y, anchor = "w")        
        
           
        '''
        ---------------------------------------------------------------------------------------------------------------------------------------------------------
        END OF MAIN CLASS INIT METHOD OF CLASS APPLICATION
        ----------------------------------------------------------------------------------------------------------------------------------------------------------
        '''
        
        '''
        CREATE NEW METHODS OF CLASS 'APPLICATION' TO BE CALLED IN INIT METHOD
        '''
        
       
    '''THIS METHOD ADDS POLICY WIDGETS WHEN '+' BUTTON IS CLICKED TO ADD MORE THAN ONE REFORM '''
    '''IT FILLS THE NEW POLICY REFORM VALUES WITH DEFAULT VALUES USING 'show_policy_selection' function'''
    '''THEN IT ALLOWS USER TO FILL NEW VALUES OF YEAR AND VALUE OF REFORM PARAM IN THE INPUT FIELDS'''

    def insert_image(self, pic_file):
        self.image=Image.open('egypt_flag.jpg')
        #self.image=Image.open(pic_file)
        basewidth = 400
        wpercent = (basewidth/float(self.image.size[0]))
        hsize = int((float(self.image.size[1])*float(wpercent)))
        self.image_resized = self.image.resize((basewidth,hsize), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image_resized)
        self.pic = Label(image=self.img)
        self.pic.place(relx = 0.65, rely = 0.2, anchor = "nw")

    def create_policy_widgets(self):
        self.num_reforms += 1
        self.block_widget_dict[self.num_reforms] = {}
        self.block_selected_dict[self.num_reforms] = {}
        self.block_widget_dict[self.num_reforms][1] = ttk.Combobox(value=self.policy_options_list, font=self.text_font, name=str(self.num_reforms))
        self.block_widget_dict[self.num_reforms][1].current(1)
        self.block_widget_dict[self.num_reforms][1].place(relx = self.block_2_entry_1_1_x, 
                        rely = (self.block_2_entry_1_1_y+
                                (self.num_reforms-1)*(self.entry_entry_gap_y)), anchor = "w", width=300)
        self.block_widget_dict[self.num_reforms][1].bind("<<ComboboxSelected>>", self.show_policy_selection)

        self.block_widget_dict[self.num_reforms][2] = Entry(width=6, font=self.fontStyle)
        self.block_widget_dict[self.num_reforms][2].place(relx = self.block_2_entry_1_2_x,
                                                          rely = (self.block_2_entry_1_1_y+
                                (self.num_reforms-1)*(self.entry_entry_gap_y)), anchor = "w")

        self.block_widget_dict[self.num_reforms][3] = Entry(width=14, font=self.fontStyle)
        self.block_widget_dict[self.num_reforms][3].place(relx = self.block_2_entry_1_3_x,
                                                          rely = (self.block_2_entry_1_1_y+
                                (self.num_reforms-1)*(self.entry_entry_gap_y)), anchor = "w")
        
        self.button_2_pos_y = (self.block_2_entry_1_1_y+(self.num_reforms)*(self.entry_entry_gap_y))+self.entry_button_gap        
        self.button_generate_revenue_policy.place(relx = self.button_1_pos_x,
                                            rely = self.button_2_pos_y, anchor = "w")

        
    '''THIS METHOD RESETS THE POLICY WIDGET TO DEFAULT'''
    '''EACH NEW REFORM WIDGET block_widget_dict[self.num_reforms][1][2][3] IS destroyed '''
    '''SELF.NUM_REFORMS IS SET TO DEFAULT VALUE OF 1 '''

    def reset_policy_widgets(self):
        for num in range(2, self.num_reforms+1):
            self.block_widget_dict[num][1].destroy()
            self.block_widget_dict[num][2].destroy()
            self.block_widget_dict[num][3].destroy()
        self.num_reforms=1
        self.block_widget_dict[1][3].delete(0, END)
        self.block_widget_dict[1][2].delete(0, END)
        self.button_2_pos_y = (self.block_2_entry_1_1_y+(self.num_reforms)*(self.entry_entry_gap_y))+self.entry_button_gap 
        self.button_generate_revenue_policy.place(relx = self.button_1_pos_x, rely = self.button_2_pos_y, anchor = "w")
                

    def delete_policy_widgets(self):
        num = self.num_reforms 
        print(num)
        if num < 2:
            showinfo("Warning", "cannot delete")
            self.num_reforms += 1                   # increase num_reforms by 1 so that it doesnt reduce to zero in the next step when it is reduced by 1
        else:
            self.block_widget_dict[num][1].destroy()
            self.block_widget_dict[num][2].destroy()
            self.block_widget_dict[num][3].destroy()
        self.num_reforms -= 1    
        self.button_2_pos_y = (self.block_2_entry_1_1_y+(self.num_reforms)*(self.entry_entry_gap_y))+self.entry_button_gap 
        self.button_generate_revenue_policy.place(relx = self.button_1_pos_x, rely = self.button_2_pos_y, anchor = "w")
    


    def popup_results_window(self, pic_file):
        window = tk.Toplevel()
        window.geometry("600x500+140+140")
        self.image=Image.open(pic_file)
        basewidth = 400
        wpercent = (basewidth/float(self.image.size[0]))
        hsize = int((float(self.image.size[1])*float(wpercent)))
        self.image_resized = self.image.resize((basewidth,hsize), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image_resized)
        self.pic = tk.Label(window, image=self.img)
        #label = tk.Label(window, text=results)
        self.pic.place(relx = 0.50, rely = 0.05)
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)        
        button_close1 = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close1.place(relx = 0.50, rely = 0.90)
        

    def popup_showinfo(self):
        showinfo("ShowInfo", "Hello World!")
    

    def generate_total_revenues(self):
        
               
        self.selected_year=2030
        
        # create Records object containing egypt data, weights and growfactors file 
        recs = Records(data=self.data_filename, weights=self.weights_filename, gfactors=GrowFactors(growfactors_filename=self.growfactors_filename))
        
        # create a Policy object as an instance of Policy class
        pol = Policy(DEFAULTS_FILENAME=self.policy_filename)
        
        # specify Calculator objects for current-law policy
        calc1 = Calculator(policy=pol, records=recs, verbose=False)
        
        # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
        #       so we can continue to use pol and recs in this script without any
        #       concern about side effects from Calculator method calls on calc1.
        
        assert isinstance(calc1, Calculator)
        assert calc1.current_year == 2020
        
        np.seterr(divide='ignore', invalid='ignore')

        # popup window for the Results
        window = tk.Toplevel()
        window.geometry("900x700+140+140")
        label = tk.Label(window, text="Results", font=self.fontStyle_title)
        label.place(relx = 0.50, rely = 0.05)
        #Create Treeview widgets for output window
        style = ttk.Style()
        style.theme_use("default")
        style.configure("mystyle.Treeview", rowheight=30, bd=0, font=('Calibri', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 10,'bold')) # Modify the font of the headings
        
        tree = ttk.Treeview(window, columns=(1, 2, 3, 4, 5, 6, 7), padding=10, show='headings', height=10, style="mystyle.Treeview")
        tree.column(1, width=100, anchor=CENTER)
        tree.heading(1, text="Year")
        tree.column(2, width=100, anchor=CENTER)
        tree.heading(2, text="Net acc profit")
        tree.column(3, width=100, anchor=CENTER)
        tree.heading(3, text="Tax depr")
        tree.column(4, width=100, anchor=CENTER)
        tree.heading(4, text="Donations")
        tree.column(5, width=100, anchor=CENTER)
        tree.heading(5, text="Used Loss")
        tree.column(6, width=100, anchor=CENTER)
        tree.heading(6, text="Net tax liability(bn EGP)")
        tree.column(7, width=100, anchor=CENTER)
        tree.heading(7, text="% Change")
        tree.place(relx = 0.1, rely = 0.15)


        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)        
        button_close1 = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close1.place(relx = 0.50, rely = 0.90)
        
        ''' Dump_vars is a list of dump variables which is all the read and calculated variables generated using the function read_calc_variables '''

        dump_vars = self.read_calc_variables()
        #dump_vars = ['Taxpayer_ID', 'Revenues', 'Tax_base', 'citax']
        wt_cit = []  
        year_list = []     
        y_add_space = 0.07
        df=pd.DataFrame()
        df1=pd.DataFrame()
        total_revenue_text_dict={}
        start_year = 2020
        end_year = 2030
        i=0
        for year in range(start_year, end_year):
            calc1.advance_to_year(year)    
            calc1.calc_all()
            wt_accounting_profit = round(calc1.weighted_total('Net_accounting_profit')/10**9, 2)
            wt_tax_depr = round(calc1.weighted_total('Tax_depr')/10**9, 2)
            wt_donations = round(calc1.weighted_total('Donations_allowed')/10**9, 2)
            wt_used_loss = round(calc1.weighted_total('Used_loss_total')/10**9, 2)
            weighted_citax1 = calc1.weighted_total('citax')
            weighted_citax1_bn = round(weighted_citax1/10**9, 2)
            wt_cit += [weighted_citax1_bn]
            year_list += [year]
            citax_collection1 = weighted_citax1.sum()
            citax_collection_billions1 = citax_collection1/10**9
            citax_collection_str1 = '{0:.2f}'.format(citax_collection_billions1)
            print('\n\n\n')
            print('TAX COLLECTION FOR THE YEAR: ', year)
            print("The CIT Collection in billions is: ", citax_collection_str1)
            dumpdf1 = calc1.dataframe(dump_vars)
            dumpdf1.to_csv('egypt_results_'+ str(year) + '.csv', index=False, float_format='%.0f')
            dumpdf = calc1.weighted_dataframe(dump_vars)
            if i == 0:
                pct_change = 0
            else:
                pct_change = round((wt_cit[i] - wt_cit[i-1])*100/(wt_cit[i-1]),2)
            pct_change = str(pct_change) + " %"            
            
            tree.insert('', 'end', text="1", values=(str(year), str(wt_accounting_profit), 
                        str(wt_tax_depr), str(wt_donations), str(wt_used_loss),  str(weighted_citax1_bn), pct_change))
            
            dumpdf['Sector'] = dumpdf1['Sector']
            df['citax'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['citax']].sum()
            df['Donations_allowed'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['Donations_allowed']].sum()
            df['Exemptions'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['Exemptions']].sum()
            df['Revenues'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['Revenues']].sum()
            df['Used_loss_total'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['Used_loss_total']].sum()
            df['Add_Bld'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['Add_Bld']].sum()
            df['Add_Intang'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['Add_Intang']].sum()
            df['Add_Mach'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['Add_Mach']].sum()
            df['Add_Others'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['Add_Others']].sum()
            df['Add_Comp'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['Add_Comp']].sum()

            total_revenue_text = "TAX COLLECTION FOR THE YEAR - " + str(year) + " is: " + str(citax_collection_str1) + " bn EGP"
            #revenue_label = Label(window, text=total_revenue_text, font=self.fontStyle)
            #revenue_label.place(relx = 0.05, rely = 0.05 + y_add_space*i, anchor = "w")        
            
            i += 1
        
        df_2020 = pd.read_csv('egypt_results_2020.csv')
        df_2020['weight'] = 2.2
        df_2020['Profit_flag'] = np.where(df_2020['Net_tax_base'] < 0, 'Loss', 'Profit')

        #print the revenue forecast chart
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.plot(year_list, wt_cit, color='r', marker='x')
        plt.title('Corporate tax forecast (in billion EGP)')
        for index in range(len(year_list)):
            ax.text(year_list[index], wt_cit[index], wt_cit[index], size=12)
        plt.show()
        
        #Print the distribution tables by tax liability  
        dist1 = create_distribution_table(df_2020, groupby='weighted_deciles', income_measure='Net_taxable_profit', averages=False, scaling=True)
        dist1.to_csv('dist_table.csv', index=False, float_format='%.0f')
        table1 = dist1.plot(kind='bar', use_index=True, y='citax', legend=False, rot=90, figsize=(8,8))
        table1.set_title('Distribution of CIT liability in Egypt - 2020')
        plt.show()
        
        #Print the distribution tables by Net taxable profit  
        table2 = dist1.plot(kind='bar', use_index=True, y='Net_taxable_profit', legend=False, rot=90, figsize=(8,8))
        table2.set_title('Distribution of Net Taxable profit in Egypt - 2020')
        plt.show()

        #print plot of tax liability by sector
        df = df/10**6
        df = df.rename(index={0.0:"Hotels", 1.0:"Banks", 2.0:"Oil&Gas", 3.0:"Gen Bus"})
        df['Add_assets2020'] = df['Add_Bld2020'] + df['Add_Intang2020'] + df['Add_Mach2020'] + df['Add_Others2020'] + df['Add_Comp2020']
        cmap = plt.cm.tab10
        colors = cmap(np.arange(len(df)) % cmap.N)
        
        ax = df['citax2020'].plot(kind='bar', use_index=True, y='citax2020', 
                            legend=False, rot=90,
                            figsize=(8,8), color=colors)
        ax.set_xlabel('Sectors')
        ax.set_title('CIT Collection (in million EGP) by Sector (2020)', fontweight="bold")
        plt.show()
        pic_filename1 = 'CIT Collection by Sector (2020).png' 
        plt.savefig(pic_filename1)
        
        #Print plot of Donations allowed
        ax1 = df['Donations_allowed2020'].plot(kind='bar', use_index=True, y='Donations_allowed2020', 
                            legend=False, rot=90, figsize=(8,8), color=colors)
        ax1.set_xlabel('Sectors')
        ax1.set_title('Donations allowed as deduction (in million EGP) by Sector (2020)', fontweight="bold")
        plt.show()

        #Print plot of additions to assets
        ax2 = df['Add_assets2020'].plot(kind='bar', use_index=True, y='Add_assets2020', 
                            legend=False, rot=90, figsize=(8,8), color=colors)
        ax2.set_xlabel('Sectors')
        ax2.set_title('Additional Investment in assets (in million EGP) by Sector (2020)', fontweight="bold")
        plt.show()
        
        #Print plot of used loss by sector
        ax3 = df['Used_loss_total2020'].plot(kind='bar', use_index=True, y='Used_loss_total2020', 
                            legend=False, rot=90, figsize=(8,8), color=colors)
        ax3.set_xlabel('Sectors')
        ax3.set_title('Used loss (in million EGP) by Sector (2020)', fontweight="bold")
        plt.show()

        #Print the Net accounting profit, tax depreciation and donations data by Profit & Loss making
        df2020_new = pd.DataFrame()
        df2020_new['Net_acc_profit'] = df_2020['Net_accounting_profit'].groupby(df_2020['Profit_flag']).sum()
        df2020_new['Tax_depr'] = df_2020['Tax_depr'].groupby(df_2020['Profit_flag']).sum()
        df2020_new['Donations'] = df_2020['Donations_allowed'].groupby(df_2020['Profit_flag']).sum()

        df2020_new.plot(kind='bar', subplots=True, figsize=(8,8))
        plt.show()
        
        
    ''' Read the policy reform parameters and their values from the reform menu fields and returns a dictionary of reform '''

    def read_reform_dict(self, block_selected_dict):
        years=[]
        for k in block_selected_dict.keys():
            if (block_selected_dict[k]['selected_year'] not in years):
                years = years + [block_selected_dict[k]['selected_year']]
        ref = {}
        ref['policy']={}
        for year in years:
            policy_dict = {}
            for k in block_selected_dict.keys():
                if block_selected_dict[k]['selected_year']==year:
                    policy_dict['_'+block_selected_dict[k]['selected_item']]=[float(block_selected_dict[k]['selected_value'])]
            ref['policy'][int(year)] = policy_dict
            print(ref)
        years.sort()
        years = [int(x) for x in years]
        return years, ref
    
    def apply_policy_change(self):
        self.block_selected_dict = {}
        print(self.num_reforms)
        for num in range(1, self.num_reforms+1):
            self.block_selected_dict[num]={}
            self.block_selected_dict[num]['selected_item']= self.block_widget_dict[num][1].get()
            self.block_selected_dict[num]['selected_year']= self.block_widget_dict[num][2].get()
            self.block_selected_dict[num]['selected_value']= self.block_widget_dict[num][3].get()
        print(self.block_selected_dict)
        
        recs = Records(data=self.data_filename, weights=self.weights_filename)
        
              
        print("data_filename: ", self.data_filename)
        print("weights_filename: ", self.weights_filename)
        
        assert isinstance(recs, Records)
        assert recs.current_year == 2020

        # create Policy object containing current-law policy
        pol = Policy(DEFAULTS_FILENAME=self.policy_filename)
        
        ''' CURRENT LAW POLICY CALCULATOR '''
        # specify Calculator objects for current-law policy
        calc1 = Calculator(policy=pol, records=recs, verbose=False)
        assert isinstance(calc1, Calculator)
        assert calc1.current_year == 2020

        np.seterr(divide='ignore', invalid='ignore')
        
        #generate policy reform pol2 as instance of Policy class
        pol2 = Policy(DEFAULTS_FILENAME=self.policy_filename)
        self.reform={}
        years, self.reform=self.read_reform_dict(self.block_selected_dict)
        print("reform dictionary: ",self.reform) 
        
        ''' CALCULATOR FOR REFORM '''
        #reform = Calculator.read_json_param_objects('app01_reform.json', None)
        pol2.implement_reform(self.reform['policy'])
        
        calc2 = Calculator(policy=pol2, records=recs, verbose=False)
        # popup window for the Results
        window = tk.Toplevel()
        window.geometry("700x800+140+140")
        label = tk.Label(window, text="Results", font=self.fontStyle_title)
        label.place(relx = 0.5, rely = 0.0, anchor="n")
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("mystyle.Treeview", rowheight=30, bd=0, font=('Calibri', 14)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        
        tree = ttk.Treeview(window, columns=(1, 2, 3, 4), padding=10, show='headings', height=15, style="mystyle.Treeview")
        tree.column(1, width=100, anchor=CENTER)
        tree.heading(1, text="Year")
        tree.column(2, width=150, anchor=CENTER)
        tree.heading(2, text="Current(bn EGP)")
        tree.column(3, width=150, anchor=CENTER)
        tree.heading(3, text="Reform(bn EGP)")
        tree.column(4, width=150, anchor=CENTER)
        tree.heading(4, text="% Change")
        tree.place(relx = 0.07, rely = 0.1)
        

        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)         
        button_close = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close.place(relx = 0.50, rely = 0.90)
        
        '''CREATE EMPTY DICTIONARIES TO RECORD THE TOTAL CIT COLLECTION UNDER CURRENT LAW AND REFORM POLICY FOR VARIOUS YEARS '''
        
        total_revenue_text={}
        reform_revenue_text={}
        revenue_dict={}
        revenue_amount_dict = {}
        num = 1
        start_year = 2020
        end_year = 2030
        for year in range(start_year, end_year):  
            calc1.advance_to_year(year) 
            
            # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
            #       so we can continue to use pol and recs in this script without any
            #       concern about side effects from Calculator method calls on calc1.
    
            calc1.calc_all()
            weighted_citax1 = calc1.weighted_total('citax')
            citax_collection_billions1 = weighted_citax1/10**9
            citax_collection_str1 = '{0:.2f}'.format(citax_collection_billions1)
            revenue_dict[year]={}
            revenue_amount_dict[year]={}
            revenue_dict[year]['current_law']={}
            revenue_amount_dict[year]['current_law']={}
            revenue_amount_dict[year]['current_law']['amount'] = citax_collection_str1

            calc2.advance_to_year(year) 
            calc2.calc_all()
            weighted_citax2 = calc2.weighted_total('citax')
            citax_collection_billions2 = weighted_citax2/10**9
            citax_collection_str2 = '{0:.2f}'.format(citax_collection_billions2)
            revenue_dict[year]['reform']={}
            revenue_amount_dict[year]['reform']={}         
            revenue_amount_dict[year]['reform']['amount'] = citax_collection_str2
            pct_change = (citax_collection_billions2 - citax_collection_billions1)*100/citax_collection_billions1
            pct_change = '{0:.2f}'.format(pct_change) + " %"
            tree.insert('', 'end', text="1", values=(str(year), str(citax_collection_str1), str(citax_collection_str2), pct_change))          
            num += 1
        
        print(revenue_amount_dict)
        df_revenue_proj = pd.DataFrame()
        for keys in revenue_amount_dict.keys():
            dict=revenue_amount_dict[keys]
            df_temp = pd.DataFrame.from_dict(dict, orient='columns')
            df_revenue_proj = pd.concat([df_revenue_proj, df_temp], ignore_index='True').astype(float)
        
        Year = np.arange(start_year, end_year)
        df_revenue_proj.insert(0, 'Year', Year)
        df_revenue_proj = df_revenue_proj.rename(columns={'current_law': 'Current Law', 'reform':'Reform'})
        df_revenue_proj['% Change'] = (df_revenue_proj['Reform'] - df_revenue_proj['Current Law'])/df_revenue_proj['Current Law']
        
        print("Revenues\n", df_revenue_proj)
        
        ax = df_revenue_proj.plot.bar(x='Year', y=["Current Law", "Reform"], rot=0, figsize=(8,8))
        ax.set_ylabel('(billion )')
        ax.set_xlabel('')
        ax.set_title('CIT Revenue - Current Law vs. Reforms', fontweight="bold")
        pic_filename2 = 'CIT - Current Law and Reforms.png'
        plt.savefig(pic_filename2)
        plt.show()
        #img1 = Image.open(pic_filename2)
        #img2 = img1.resize((500, 500), Image.ANTIALIAS)
        #img3 = ImageTk.PhotoImage(img2)
        #self.pic.configure(image=img3)
        #self.pic.image = img3

        
    def generate_tax_expenditures(self):
        
        # create Records object containing pit.csv and pit_weights.csv input data
        recs = Records(data=self.data_filename, weights=self.weights_filename)
        
        # create Policy object containing current-law policy
        pol = Policy()
        
        # specify Calculator objects for current-law policy
        calc1 = Calculator(policy=pol, records=recs, verbose=False)
        assert isinstance(calc1, Calculator)
        assert calc1.current_year == 2020

        np.seterr(divide='ignore', invalid='ignore')

        # Produce DataFrame of results using cross-section
        calc1.calc_all()
        
        dump_vars = ['Taxpayer_ID', 'Net_accounting_profit', 'Total_taxable_profit', \
                    'Donations_Govt', 'Donations_allowed', 'Investment_incentive', \
                    'Net_taxable_profit', 'Tax_base', 'Net_tax_base', 'citax']

        # This is the Overall Tax Expenditures
        pol2 = Policy()
        reform = Calculator.read_json_param_objects(self.benchmark_filename, None)
        pol2.implement_reform(reform['policy'])
        
        calc2 = Calculator(policy=pol2, records=recs, verbose=False)
        # popup window for the Results
        window = tk.Toplevel()
        window.geometry("700x600+140+140")
        label = tk.Label(window, text="Tax Expenditures", font=self.fontStyle_sub_title)
        label.place(relx = 0.40, rely = 0.02)
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)         
        button_close = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close.place(relx = 0.50, rely = 0.90)
        
        total_revenue_text={}
        reform_revenue_text={}
        tax_expenditure_text = {}        
        revenue_dict={}
        revenue_amount_dict = {}
        tax_expenditure = {}
        num = 1
        
        #for year in range(years[0], years[-1]+1):            
        for year in range(2020, 2026):  
            calc1.advance_to_year(year)        
            calc2.advance_to_year(year)
            # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
            #       so we can continue to use pol and recs in this script without any
            #       concern about side effects from Calculator method calls on calc1.
    
            # Produce DataFrame of results using cross-section
            calc1.calc_all()
            
            dumpdf_1 = calc1.dataframe(dump_vars)
            dumpdf_1.to_csv('dumpresults_egypt.csv', index=False, float_format='%.0f')
            
            citax1 = calc1.array('citax')
            weight1 = calc1.array('weight')

            wtd_citax1 = citax1 * weight1
            
            citax_collection1 = wtd_citax1.sum()
            
            citax_collection_billions1 = citax_collection1/10**9
            
            citax_collection_str1 = '{0:.2f}'.format(citax_collection_billions1)
            
            print('\n\n\n')
            print('TAX COLLECTION UNDER CURRENT LAW FOR THE YEAR - '+str(year)+': ', citax_collection_billions1)
            
            total_revenue_text[year] = "TAX COLLECTION UNDER CURRENT LAW FOR THE YEAR - " + str(year)+" : "+str(citax_collection_str1)+" bill "
            #self.l6.config(text=total_revenue_text1)
            #self.l6.place(relx = 0.1, rely = 0.7+(num-1)*0.1, anchor = "w")
            # Produce DataFrame of results using cross-section
            calc2.calc_all()
            
            dumpdf_2 = calc2.dataframe(dump_vars)
            dumpdf_2.to_csv('dumpresults_egypt2.csv', index=False, float_format='%.0f')
            
            citax2 = calc2.array('citax')
            weight2 = calc2.array('weight')
            
            wtd_citax2 = citax2 * weight2
            
            citax_collection2 = wtd_citax2.sum()
            
            citax_collection_billions2 = citax_collection2/10**9
            citax_expenditure_billions = citax_collection_billions2 -  citax_collection_billions1
            citax_collection_str2 = '{0:.2f}'.format(citax_collection_billions2)
            
            citax_expenditure_billions_str = '{0:.5f}'.format(citax_expenditure_billions)
            
            print('\n\n\n')
            print('TAX COLLECTION UNDER BENCHMARK POLICY FOR THE YEAR - '+str(year)+': ', citax_collection_billions2)
                 
            revenue_amount_dict[year]={}
            revenue_amount_dict[year]['current_law']={}            
            revenue_amount_dict[year]['current_law']['amount'] = citax_collection_billions1
            revenue_amount_dict[year]['benchmark']={}
            revenue_amount_dict[year]['benchmark']={}
            revenue_amount_dict[year]['benchmark']['amount'] = citax_collection_billions2
            
            revenue_amount_dict[year]['tax_expenditure']={}
            revenue_amount_dict[year]['tax_expenditure']={}                     
            revenue_amount_dict[year]['tax_expenditure']['amount'] = citax_expenditure_billions    
            
            reform_revenue_text[year] = "TAX COLLECTION UNDER BENCHMARK FOR THE YEAR - " + str(year)+" : "+str(citax_collection_str2)+" bill "

            tax_expenditure_text[year] = "TAX EXPENDITURES FOR THE YEAR - " + str(year)+" : "+citax_expenditure_billions_str+" bill "
            
            revenue_dict[year]={}
            revenue_dict[year]['current_law'] = {}
            revenue_dict[year]['current_law']['Label'] = Label(window, text=total_revenue_text[year], font=self.fontStyle)
            revenue_dict[year]['current_law']['Label'].place(relx = 0.05, rely = 0.1+(num-1)*0.2, anchor = "w") 
            revenue_dict[year]['benchmark'] = {}
            revenue_dict[year]['benchmark']['Label'] = Label(window, text=reform_revenue_text[year], font=self.fontStyle)
            revenue_dict[year]['benchmark']['Label'].place(relx = 0.05, rely = 0.13+(num-1)*0.2, anchor = "w") 
            revenue_dict[year]['tax_expenditure'] = {}
            revenue_dict[year]['tax_expenditure']['Label'] = Label(window, text=tax_expenditure_text[year], font=self.fontStyle)
            revenue_dict[year]['tax_expenditure']['Label'].place(relx = 0.05, rely = 0.16+(num-1)*0.2, anchor = "w")            
            num += 1
        
        #print(revenue_amount_dict)
        df_revenue_proj = pd.DataFrame(revenue_amount_dict)
        df_revenue_proj = df_revenue_proj.T
        df_revenue_proj['Current Law'] = df_revenue_proj['current_law'].apply(pd.Series)
        df_revenue_proj['Benchmark'] = df_revenue_proj['benchmark'].apply(pd.Series)
        df_revenue_proj = df_revenue_proj.drop(['current_law', 'benchmark'], axis=1)
        df_revenue_proj['Current Law'] = pd.to_numeric(df_revenue_proj['Current Law'])
        df_revenue_proj['Benchmark'] = pd.to_numeric(df_revenue_proj['Benchmark'])
        print("Revenue Projections2\n", df_revenue_proj)
        ax = df_revenue_proj.plot(y=["Current Law", "Benchmark"], kind="bar", rot=0,
                            figsize=(8,8))
        ax.set_ylabel('(billion )')
        ax.set_xlabel('')
        ax.set_title('CIT - Tax Collection under Current Law vs. Benchmark', fontweight="bold")
        pic_filename3 = 'CIT - Current Law and Benchmark.png'
        plt.savefig(pic_filename3)
        plt.show()
        

        img1 = Image.open(pic_filename3)
        img2 = img1.resize((500, 500), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(img2)
        #self.pic.configure(image=img3)
        #self.pic.image = img3
    
    
    def newselection1(self, event):
        print('selected1:', event.widget.get())
    
    def newselection2(self, event):
        print('selected2:', event.widget.get())
    
    '''CLASS METHOD WHICH OPENS THE FOLDER IN WHICH FILES ARE STORED ON THE LOCAL COMPUTER TO CHOOSE A DATA FILE'''

    def input_data_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file')
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.data_filename = filename_list[-1]
        self.entry_data_filename.delete(0,END)
        self.entry_data_filename.insert(0,self.data_filename)
    
    def input_weights_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file')
        #print(filez[0])
        #self.master.update()        
        #filename_path = tk.splitlist(filez)[0]
        #filename_list = filename_path.split('/')
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.weights_filename = filename_list[-1]
        self.entry_weights_filename.delete(0,END)
        self.entry_weights_filename.insert(0,self.weights_filename)
    
    def input_policy_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file') 
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.policy_filename = filename_list[-1]
        self.entry_policy_filename.delete(0,END)
        self.entry_policy_filename.insert(0,self.policy_filename)

    def input_benchmark_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file') 
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.benchmark_filename = filename_list[-1]
        self.entry_benchmark_filename.delete(0,END)
        self.entry_benchmark_filename.insert(0,self.benchmark_filename)
               
    
    def policy_options(self):
        self.sub_directory
        self.policy_filename
        with open(self.sub_directory+'/'+self.policy_filename) as f:
            current_law_policy = json.load(f)
        current_law_policy_sorted = dict(sorted(current_law_policy.items()))    
        policy_options_list = ['None selected']
        for k, s in current_law_policy_sorted.items():
            #print(k)
            #print(current_law_policy[k]['description'])
            #policy_option_list = policy_option_list + [current_law_policy[k]['description']]
            policy_options_list = policy_options_list + [k[1:]]
        return (current_law_policy, policy_options_list)
    
    '''This function returns the read and calc variables from json file '''
    '''Used to generate dump variable list '''

    def read_calc_variables(self):
        self.sub_directory
        self.records_vars_filename
        with open(self.sub_directory+'/'+self.records_vars_filename) as f:
            record_vars = json.load(f)
        records_vars_list = []
        for k, s in record_vars.items():
            for items in s.items():
                records_vars_list += items[:1]
        return records_vars_list


    '''This function updates the value of policy param as per changes made in reform '''
    def policy_reform():
        self.reform={}
        self.reform['policy']={}
        self.reform['policy']['_'+self.selected_item]={}
        self.updated_year = self.block_widget_dict[1][2].get()
        self.updated_value = self.block_widget_dict[1][3].get()
        self.reform['policy']['_'+selected_item][self.updated_year]=[self.updated_value]
        print("Reform2: ", self.reform)
    
    '''This function return the value of policy param selected for reform, as per current law policy
        e.g. if cess_rate is selected in the combo box, it will return a json list of 
        {1: {'selected_item': 'cess_rate', 'selected_value': '0.03', 'selected_year': '2017'}}
    '''
        
    def show_policy_selection(self, event):
        active_widget_number = int(str(event.widget)[1:])
        print("active_widget_number: ", active_widget_number)
        num = active_widget_number
        ''' Active widget number is '''

        self.selected_item = self.block_widget_dict[num][1].get()
        self.selected_value = self.current_law_policy['_'+ self.selected_item]['value'][0]
        self.selected_year = self.current_law_policy['_'+ self.selected_item]['row_label'][0]
        self.block_selected_dict[num]['selected_item']= self.selected_item
        self.block_selected_dict[num]['selected_value']= self.current_law_policy['_'+ self.selected_item]['value'][0]
        self.block_selected_dict[num]['selected_year']= self.current_law_policy['_'+ self.selected_item]['row_label'][0]
        
        self.block_widget_dict[num][3].delete(0, END)
        self.block_widget_dict[num][3].insert(END, self.selected_value)
        self.block_widget_dict[num][2].delete(0, END)
        self.block_widget_dict[num][2].insert(END, self.selected_year)
    
        
    # --- main ---
    
 
def main():
    root = tk.Tk()
    root.geometry('1500x600')
    root.title('The World Bank')
    img=Image.open('WB_logo1.png')
    img.save('icon.ico', format='ICO', sizes=[(30,30)])
    root.iconbitmap('icon.ico')
    app = Application(root)
    app.mainloop()


if __name__ == "__main__":
    main()
      
"""
    
    #button(row=6, column=1, sticky = W, pady = (0,25), padx = (0,0))
    root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.master.title("Sample application")
    app.mainloop()
    
 """   
