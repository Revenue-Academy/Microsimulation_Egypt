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

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

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
        self.data_filename = "dataegyptallsectors.csv"
        self.weights_filename = "cit_weights_egypt.csv"
        self.policy_filename = "current_law_policy_cit_egypt.json"
        self.records_vars_filename = "records_variables_egypt.json"
        self.growfactors_filename = self.sub_directory+"/"+"growfactors_egypt.csv"    
        self.benchmark_filename = "tax_incentives_benchmark.json"        
        self.total_revenue_text1 = ""
        self.reform_revenue_text1 = ""
        self.reform_filename = "egypt_reform.json"

        self.fontStyle = tkfont.Font(family="Helvetica", size="10")
        self.fontStyle_sub_title = tkfont.Font(family="Helvetica", size="14", weight="bold")         
        self.fontStyle_title = tkfont.Font(family="Helvetica", size="18", weight="bold")
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)        
        self.text_font = ('Arial', '10')
                
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
           
        
        '''Creating a Label for Tax Microsimulation Model'''

        self.root_title=Label(text="EGYPT CIT Microsimulation Model",
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
        """
        self.entry_growfactors_filename = Entry(width=30, font = self.fontStyle)
        self.entry_growfactors_filename.place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_4_y, anchor = "e")
        self.entry_growfactors_filename.insert(END, self.policy_filename)
        self.button_growfactors_filename = ttk.Button(text = "Change Growfactors File", style='my.TButton', command=self.input_growfactors_filename)
        self.button_growfactors_filename.place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_4_y, anchor = "w")
        """        
        
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
        self.block_widget_dict[1][1].current(1)
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

        self.num_reforms += 1
        self.button_add_reform = ttk.Button(text="+", style='my.TButton', command=self.create_policy_widgets, width=2)
        self.button_add_reform.place(relx = self.button_add_reform_x, rely = self.block_2_entry_1_1_y, anchor = "w") 

        '''Create a Button for deleting a reform '''

        self.button_delete_reform = ttk.Button(text="del", style='my.TButton', command=self.delete_policy_widgets, width=2)
        self.button_delete_reform.place(relx = self.button_del_reform_x, rely = self.block_2_entry_1_1_y, anchor = "w") 

        '''Create a Button to Reset policy reform selection'''

        self.button_clear_reform = ttk.Button(text="Reset", style='my.TButton', command=self.reset_policy_widgets, width=6)
        self.button_clear_reform.place(relx = self.button_clear_reform_x, rely = self.block_2_entry_1_1_y, anchor = "w")

        
        '''Create a Button for Generating Revenue under Reform using command function 'apply_policy_change'''

        self.button_generate_revenue_policy = ttk.Button(text = "Generate Revenue under Reform", style='my.TButton', command=self.apply_policy_change)
        self.button_2_pos_y = (self.block_2_entry_1_1_y+(self.num_reforms-1)*(self.entry_entry_gap_y)) +self.entry_button_gap
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
        
        '''Insert a Logo in Frame'''

        #self.image=Image.open("Egypt_logo.png")
        #self.image=Image.open("WB_logo2.jpg")
        self.image=Image.open('egypt_flag.jpg')
        basewidth = 400
        wpercent = (basewidth/float(self.image.size[0]))
        hsize = int((float(self.image.size[1])*float(wpercent)))
        self.image_resized = self.image.resize((basewidth,hsize), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image_resized)
        self.pic = Label(image=self.img)
        self.pic.place(relx = 0.65, rely = 0.2, anchor = "nw")
                
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

    def create_policy_widgets(self):
   
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
        
               
        self.num_reforms += 1
        self.button_2_pos_y = (self.block_2_entry_1_1_y+(self.num_reforms-1)*(self.entry_entry_gap_y))+self.entry_button_gap        
        self.button_generate_revenue_policy.place(relx = self.button_1_pos_x,
                                            rely = self.button_2_pos_y, anchor = "w")

        
    '''THIS METHOD RESETS THE POLICY WIDGET TO DEFAULT'''
    '''EACH NEW REFORM WIDGET block_widget_dict[self.num_reforms][1][2][3] IS destroyed '''
    '''SELF.NUM_REFORMS IS SET TO DEFAULT VALUE OF 1 '''

    def reset_policy_widgets(self):
        for num in range(2, self.num_reforms):
            self.block_widget_dict[num][1].destroy()
            self.block_widget_dict[num][2].destroy()
            self.block_widget_dict[num][3].destroy()
        self.num_reforms=1
        self.button_2_pos_y = (self.block_2_entry_1_1_y+(self.num_reforms)*(self.entry_entry_gap_y))+self.entry_button_gap 
        self.button_generate_revenue_policy.place(relx = self.button_1_pos_x, rely = self.button_2_pos_y, anchor = "w")
    
    
    def delete_policy_widgets(self):
        num = self.num_reforms - 1
        print(num)
        if num == 1:
            showinfo("Warning", "cannot delete")
        else:
            self.block_widget_dict[num][1].destroy()
            self.block_widget_dict[num][2].destroy()
            self.block_widget_dict[num][3].destroy()
                

    
    def popup_window(self):
        window = tk.Toplevel()

        label = tk.Label(window, text="Hello World!")
        label.pack(fill='x', padx=50, pady=5)

        button_close = tk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close.pack(fill='x')

    def popup_showinfo(self):
        showinfo("ShowInfo", "Hello World!")
    

    def generate_total_revenues(self):
        
               
        self.selected_year=2024
        
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
        window.geometry("600x500+140+140")
        label = tk.Label(window, text="Results")
        label.place(relx = 0.50, rely = 0.05)
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)        
        button_close1 = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close1.place(relx = 0.50, rely = 0.90)
        
        ''' Dump_vars is a list of dump variables which is all the read and calculated variables generated using the function
            read_calc_variables '''

        dump_vars = self.read_calc_variables()
        #dump_vars = ['Taxpayer_ID', 'Revenues', 'Tax_base', 'citax']
        
        
        y_add_space = 0.07
        df=pd.DataFrame()
        i=0
        for year in range(2020, 2025):
            calc1.advance_to_year(year)    
        # Produce DataFrame of results using cross-section
            calc1.calc_all()
            weighted_citax1 = calc1.weighted_total('citax')
            citax_collection1 = weighted_citax1.sum()
            citax_collection_billions1 = citax_collection1/10**9
            citax_collection_str1 = '{0:.2f}'.format(citax_collection_billions1)
            print('\n\n\n')
            print('TAX COLLECTION FOR THE YEAR: ', year)
            print("The CIT Collection in billions is: ", citax_collection_str1)
            dumpdf = calc1.dataframe(dump_vars)
            dumpdf.to_csv('egypt_results_'+ str(year) + '.csv', index=False, float_format='%.0f')
            df['citax'+str(year)] = dumpdf.groupby(dumpdf['Sector'])[['citax']].sum()
            total_revenue_text = "TAX COLLECTION FOR THE YEAR - " + str(year) + " is: " + str(citax_collection_str1) + " bn EGP"
            revenue_label = Label(window, text=total_revenue_text, font=self.fontStyle)
            revenue_label.place(relx = 0.05, rely = 0.20 + y_add_space*i, anchor = "w")        
            i +=1
        
        df = df/10**6
        df = df.rename(index={0.0:"Hotels", 1.0:"Banks", 2.0:"Oil&Gas", 3.0:"Gen Bus"})

        cmap = plt.cm.tab10
        colors = cmap(np.arange(len(df)) % cmap.N)
        ax = df['citax2020'].plot(kind='bar', use_index=True, y='citax2020', 
                            legend=False, rot=90,
                            figsize=(8,8), color=colors)
        ax.set_xlabel('Sectors')
        ax.set_title('CIT Collection (in million EGP) by Sector (2020)', fontweight="bold")
        plt.show()
        #pic_filename1 = 'CIT Collection by Sector (2020).png' 
        #plt.savefig(pic_filename1)
        
        

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
        years.sort()
        years = [int(x) for x in years]
        return years, ref
    
    def apply_policy_change(self):
        
        for num in range(1, self.num_reforms):
            self.block_selected_dict[num]['selected_item']= self.block_widget_dict[num][1].get()
            self.block_selected_dict[num]['selected_value']= self.block_widget_dict[num][3].get()
            self.block_selected_dict[num]['selected_year']= self.block_widget_dict[num][2].get()
        
        #print(self.block_selected_dict)
        
        recs = Records(data=self.data_filename, weights=self.weights_filename)
        
              
        print("data_filename: ", self.data_filename)
        print("weights_filename: ", self.weights_filename)
        
        assert isinstance(recs, Records)
        assert recs.current_year == 2020

        # create Policy object containing current-law policy
        pol = Policy(DEFAULTS_FILENAME=self.policy_filename)
        
        # specify Calculator objects for current-law policy
        calc1 = Calculator(policy=pol, records=recs, verbose=False)
        assert isinstance(calc1, Calculator)
        assert calc1.current_year == 2020

        np.seterr(divide='ignore', invalid='ignore')
        
        pol2 = Policy(DEFAULTS_FILENAME=self.policy_filename)
        
        years, self.reform=self.read_reform_dict(self.block_selected_dict)
        print("reform dictionary: ",self.reform) 
        #reform = Calculator.read_json_param_objects('app01_reform.json', None)
        pol2.implement_reform(self.reform['policy'])
        
        calc2 = Calculator(policy=pol2, records=recs, verbose=False)
        # popup window for the Results
        window = tk.Toplevel()
        window.geometry("600x500+140+140")
        label = tk.Label(window, text="Results", font=self.fontStyle)
        label.place(relx = 0.05, rely = 0.14)
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)         
        button_close = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close.place(relx = 0.50, rely = 0.90)
        

        
        total_revenue_text={}
        reform_revenue_text={}
        revenue_dict={}
        revenue_amount_dict = {}
        num = 1
        #for year in range(years[0], years[-1]+1):            
        for year in range(2020, 2024):  
            calc1.advance_to_year(year)        
            calc2.advance_to_year(year)
            # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
            #       so we can continue to use pol and recs in this script without any
            #       concern about side effects from Calculator method calls on calc1.
    
            # Produce DataFrame of results using cross-section
            calc1.calc_all()
            weighted_citax1 = calc1.weighted_total('citax')
                    
            citax_collection_billions1 = weighted_citax1/10**9
            
            citax_collection_str1 = '{0:.2f}'.format(citax_collection_billions1)
            
            print('\n\n\n')
            print('TAX COLLECTION FOR THE YEAR - 2020\n')
            
            print("The CIT Collection in billions is: ", citax_collection_str1)
            
            total_revenue_text[year] = "TAX COLLECTION UNDER CURRENT LAW FOR THE YEAR - " + str(year)+" : "+str(citax_collection_str1)+" bn EGP"
            #self.l6.config(text=total_revenue_text1)
            #self.l6.place(relx = 0.1, rely = 0.7+(num-1)*0.1, anchor = "w")
            # Produce DataFrame of results using cross-section
            calc2.calc_all()
            
            weighted_citax2 = calc2.weighted_total('citax')
            
            citax_collection_billions2 = weighted_citax2/10**9
            
            citax_collection_str2 = '{0:.2f}'.format(citax_collection_billions2)
            
            print('\n\n\n')
            print('TAX COLLECTION FOR THE YEAR UNDER REFORM - 2020\n')
            
            print("The CIT Collection in billions is: ", citax_collection_str2)
            
            reform_revenue_text[year] = "TAX COLLECTION UNDER REFORM FOR THE YEAR - " + str(year)+"           : "+str(citax_collection_str2)+" bn "
           
            #df1, df2 = calc1.distribution_tables(calc2, 'weighted_deciles')
            #print(df1, df2)     

            revenue_dict[year]={}
            revenue_amount_dict[year]={}
            revenue_dict[year]['current_law']={}
            revenue_amount_dict[year]['current_law']={}
            revenue_dict[year]['current_law']['Label'] = Label(window, text=total_revenue_text[year], font=self.fontStyle)
            revenue_dict[year]['current_law']['Label'].place(relx = 0.05, rely = 0.1+(num-1)*0.15, anchor = "w")
            revenue_amount_dict[year]['current_law']['amount'] = citax_collection_str1
            #self.l6=Label(text=self.total_revenue_text1)
            #self.l6.place(relx = 0.4, rely = 0.1, anchor = "w")
            revenue_dict[year]['reform']={}
            revenue_amount_dict[year]['reform']={}         
            revenue_dict[year]['reform']['Label'] = Label(window, text=reform_revenue_text[year], font=self.fontStyle)
            revenue_dict[year]['reform']['Label'].place(relx = 0.05, rely = 0.15+(num-1)*0.15, anchor = "w")            
            revenue_amount_dict[year]['reform']['amount'] = citax_collection_str2
            #self.l7=Label(text=self.reform_revenue_text1)
            #self.l7.place(relx = 0.4, rely = 0.15, anchor = "w")        
            num += 1
        
        #print(revenue_amount_dict)
        df_revenue_proj = pd.DataFrame(revenue_amount_dict)
        df_revenue_proj = df_revenue_proj.T
        df_revenue_proj['Current Law'] = df_revenue_proj['current_law'].apply(pd.Series)
        df_revenue_proj['Reform'] = df_revenue_proj['reform'].apply(pd.Series)
        df_revenue_proj = df_revenue_proj.drop(['current_law', 'reform'], axis=1)
        df_revenue_proj['Current Law'] = pd.to_numeric(df_revenue_proj['Current Law'])
        df_revenue_proj['Reform'] = pd.to_numeric(df_revenue_proj['Reform'])
        print("Revenues\n", df_revenue_proj)
        ax = df_revenue_proj.plot(y=["Current Law", "Reform"], kind="bar", rot=0,
                            figsize=(8,8))
        ax.set_ylabel('(billion )')
        ax.set_xlabel('')
        ax.set_title('CIT Revenue - Current Law vs. Reforms', fontweight="bold")
        pic_filename2 = 'CIT - Current Law and Reforms.png'
        plt.savefig(pic_filename2)
        
        img1 = Image.open(pic_filename2)
        img2 = img1.resize((500, 500), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(img2)
        self.pic.configure(image=img3)
        self.pic.image = img3

        #df1, df2 = calc1.distribution_tables(calc2, 'weighted_deciles')
        #print(df1, df2)
        

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
        dump_vars = ['Taxpayer_ID', 'Net_accounting_profit', 'Total_taxable_profit', \
                    'Donations_Govt', 'Donations_allowed', 'Investment_incentive', \
                    'Net_taxable_profit', 'Tax_base', 'Net_tax_base', 'citax']
        #for year in range(years[0], years[-1]+1):            
        for year in range(2020, 2024):  
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
        
        img1 = Image.open(pic_filename3)
        img2 = img1.resize((500, 500), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(img2)
        self.pic.configure(image=img3)
        self.pic.image = img3
    
    
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
        policy_options_list = []
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
        self.block_selected_dict[num]['selected_item']= self.block_widget_dict[num][1].get()
        self.block_selected_dict[num]['selected_value']= self.current_law_policy['_'+ self.selected_item]['value'][0]
        self.block_selected_dict[num]['selected_year']= self.current_law_policy['_'+ self.selected_item]['row_label'][0]
        
        self.block_widget_dict[num][3].delete(0, END)
        self.block_widget_dict[num][3].insert(END, self.selected_value)
        self.block_widget_dict[num][2].delete(0, END)
        self.block_widget_dict[num][2].insert(END, self.selected_year)

        for num in range(1, self.num_reforms):        
            self.block_selected_dict[num]['selected_value']= self.block_widget_dict[num][3].get()
            self.block_selected_dict[num]['selected_year']= self.block_widget_dict[num][2].get()
        
        print(self.block_selected_dict)
        return
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
