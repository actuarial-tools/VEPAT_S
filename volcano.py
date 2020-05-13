import json
import pandas as pd
import numpy as np
import math
import plotly.express as px
import plotly.graph_objects as go



class volcano:
    def __init__(self, elc, du, volcano, eldate, filename):
        self.elc = elc
        self.du = du
        self.volcano = volcano
        self.eldate = eldate
        self.filename = filename
        self.volcanoConfigData = self.read_config(self.filename)
        self.dfd = self.table_vpt()
        self.dfd_last = self.table_vpt_last()
        self.df2 = self.table_stat_vpt()
        self.df2_last = self.table_stat_vpt_last()
        # self.erp_cls = self.cal_vpt()
        self.df1 = self.table_phit()
        # self.table_nvp = self.table_near_vent_proc()




    def read_config(self, filename):
        with open(filename) as config_ws:
            config = json.load(config_ws)
        return config

    def inp_para(self):
        inps = {
            "Volcano": self.volcano,
            "Elicitation date": self.eldate,
            "Elicitation Duration (day/s)": self.elc,
            "Elicitation Duration (week/s)": self.du
        }
        return inps

    def base_para(self):
        self.base_para = self.volcanoConfigData['Base parameters']
        return self.base_para


    def table_vpt(self):
        self.dfd = pd.DataFrame(data=self.volcanoConfigData['elicitation_inputs'])
        self.dfd['Error low'] = self.dfd['Best guess'] - self.dfd['Min']
        self.dfd['Error high'] = self.dfd['Max'] - self.dfd['Best guess']
        return self.dfd


    # def load_df(self, df1):
    #     self.df1 = df1


    def table_stat_vpt(self):
        mean_bestG = self.dfd['Best guess'].mean()
        median_bestG = self.dfd['Best guess'].median()
        # qntl_bestG = dfd['Best guess'].quantile(0.84) #84th percentile
        # 84th percentile calculation over a range of columns:
        dfd84 = pd.concat(self.dfd[c] for c in ['Best guess', 'Best guess repeat', 'Min', 'Max']).reset_index(drop=True)
        pcntl_bestG = np.percentile(dfd84.values, 84)

        mean_min = self.dfd['Min'].mean()
        median_min = self.dfd['Min'].median()

        mean_max = self.dfd['Max'].mean()
        median_max = self.dfd['Max'].median()

        d2 = {'Stat': ['Mean', 'Median', '84th percentile'],
              'Best Guess': [mean_bestG, median_bestG, pcntl_bestG],
              'Min': [mean_min, median_min, ""],
              'Max': [mean_max, median_max, ""]}
        self.df2 = pd.DataFrame(data=d2)
        return self.df2


    def table_vpt_last(self):
        self.dfd_last = pd.DataFrame(data=self.volcanoConfigData['elicitation_inputs_last'])
        self.dfd_last['Error low'] = self.dfd_last['Best guess'] - self.dfd_last['Min']
        self.dfd_last['Error high'] = self.dfd_last['Max'] - self.dfd_last['Best guess']
        return self.dfd_last

    def table_stat_vpt_last(self):
        mean_bestGL = self.dfd_last['Best guess'].mean()
        median_bestGL = self.dfd_last['Best guess'].median()
        dfd84L = pd.concat(self.dfd_last[c] for c in ['Best guess', 'Best guess repeat', 'Min', 'Max']).reset_index(drop=True)
        pcntl_bestGL = np.percentile(dfd84L.values, 84)

        mean_minL = self.dfd_last['Min'].mean()
        median_minL = self.dfd_last['Min'].median()

        mean_maxL = self.dfd_last['Max'].mean()
        median_maxL = self.dfd_last['Max'].median()

        d2_lst = {'Stat': ['Mean', 'Median', '84th percentile'],
              'Best Guess': [mean_bestGL, median_bestGL, pcntl_bestGL],
              'Min': [mean_minL, median_minL, ""],
              'Max': [mean_maxL, median_maxL, ""]}
        self.df2_last = pd.DataFrame(data=d2_lst)
        return self.df2_last


    def table_phit(self):
        self.df1 = pd.DataFrame(data=self.volcanoConfigData['phit_inputs'])
        return self.df1


    def elici_plot(self):
        inp1 = self.volcano
        inp2 = self.eldate
        inp3 = int(self.elc)

        if inp3 == 0:
            inp3 = int(self.du)
            inp3 = str(inp3) + " week/s"
        else:
            inp3 = str(inp3) + " day/s"

        x1 = self.dfd['Best guess']
        y1 = self.dfd['Person']
        x_erm = self.dfd['Error low']
        x_erh = self.dfd['Error high']

        #get mean, median, and 84th percentile values
        ymin = self.dfd['Person'].min()
        ymax = self.dfd['Person'].max()
        # xmin = (self.dfd['Best guess'] - self.dfd['Error low']).min()
        # xmax = (self.dfd['Error high'] + self.dfd['Best guess']).max()
        # xmax_last = (self.dfd_last['Best guess'] + self.dfd_last['Error high']).max()
        xmin = self.dfd['Min'].min()
        xmax = self.dfd['Max'].max()
        xmax_last = self.dfd_last['Max'].max()

        # set x range comparing with last elicitaion reuslts
        if xmax < xmax_last:
            xmax = xmax_last
        else:
            xmax = xmax

        if xmin < 0:
            xmin = xmin
        else:
            xmin = 0

        med_ame = self.df2['Best Guess'][1]
        mean1 = self.df2['Best Guess'][0]
        perctil = self.df2['Best Guess'][2]

        trace1 = go.Scatter(
            x=x1,
            y=y1,
            mode='markers',
            marker_symbol='diamond',
            name = "Elicitations",
            error_x=dict(
                type='data',
                symmetric=False,
                array=x_erh,
                arrayminus=x_erm,
                thickness=0.6,
            ))

        trace_median1 = go.Scatter(x=[med_ame, med_ame],
                               y=[0, ymax],
                               mode="lines",
                               line=dict(width=1.5, dash='dot', color="rgba(20,60,200,0.6)"),
                               name="Median"
                               )


        trace_mean = go.Scatter(x=[mean1, mean1],
                                    y=[0, ymax],
                                    mode="lines",
                                    line=dict(width=1.5, dash='dot', color="rgba(26,150,65,0.8)"),
                                    name="Mean"
                                    )

        trace_perctil = go.Scatter(x=[perctil, perctil],
                                   y=[0, ymax],
                                   mode="lines",
                                   line=dict(width=1.5, color="rgba(240,30,65,0.8)"),
                                   name="84th percentile"
                                   )

        data = [trace1, trace_median1, trace_mean, trace_perctil]
        tit = inp1 + " eruption within next " + inp3 + " (" + inp2 + ")"
        layout = go.Layout(
            title=tit,
            xaxis_title="Best guess",
            yaxis_title="Person",
            # paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=go.layout.XAxis(
                dtick=0.1,
                #autorange=True
                range=[xmin, xmax]
            ),
            yaxis=go.layout.YAxis(
                dtick=1,
                #autorange=True
                range=[0, ymax + 0.5]
            )
        )

        fig1 = go.Figure(
            data=data,
            layout=layout
        )
        fig1.update_xaxes(showline=True, linewidth=0.8, linecolor='black', ticks="outside", tickwidth=0.8,
                          tickcolor='black', ticklen=4, mirror=True)
        fig1.update_yaxes(showline=True, linewidth=0.8, linecolor='black', ticks="outside", tickwidth=0.8,
                          tickcolor='black', ticklen=4, mirror=True)

        fig1.show()

    def elici_plot_last(self):
        baseParaLast = self.volcanoConfigData['elicitation_parameters_last']
        inp1 = self.volcano
        inp2 = baseParaLast.get("Elicitation date", "")

        inp3 = int(baseParaLast.get("Elicitation Duration (day/s)", ""))

        if inp3 == 0:
            inp3 = int(baseParaLast.get("Elicitation Duration (week/s)", ""))
            inp3 = str(inp3) + " week/s"
        else:
            inp3 = str(inp3) + " day/s"
        print(inp3)

        x1 = self.dfd_last['Best guess']
        y1 = self.dfd_last['Person']
        x_erm = self.dfd_last['Error low']
        x_erh = self.dfd_last['Error high']

        #get mean, median, and 84th percentile values
        ymin = self.dfd_last['Person'].min()
        ymax = self.dfd_last['Person'].max()
        # xmin = (self.dfd['Best guess'] - self.dfd['Error low']).min()
        # xmax = (self.dfd['Error high'] + self.dfd['Best guess']).max()
        # xmax_last = (self.dfd_last['Best guess'] + self.dfd_last['Error high']).max()
        xmin = self.dfd_last['Min'].min()
        xmax = self.dfd_last['Max'].max()

        if xmin < 0:
            xmin = xmin
        else:
            xmin = 0

        med_ame = self.df2_last['Best Guess'][1]
        mean1 = self.df2_last['Best Guess'][0]
        perctil = self.df2_last['Best Guess'][2]

        trace1 = go.Scatter(
            x=x1,
            y=y1,
            mode='markers',
            marker_symbol='diamond',
            name = "Elicitations",
            error_x=dict(
                type='data',
                symmetric=False,
                array=x_erh,
                arrayminus=x_erm,
                thickness=0.6,
            ))

        trace_median1 = go.Scatter(x=[med_ame, med_ame],
                               y=[0, ymax],
                               mode="lines",
                               line=dict(width=1.5, dash='dot', color="rgba(20,60,200,0.6)"),
                               name="Median"
                               )


        trace_mean = go.Scatter(x=[mean1, mean1],
                                    y=[0, ymax],
                                    mode="lines",
                                    line=dict(width=1.5, dash='dot', color="rgba(26,150,65,0.8)"),
                                    name="Mean"
                                    )

        trace_perctil = go.Scatter(x=[perctil, perctil],
                                   y=[0, ymax],
                                   mode="lines",
                                   line=dict(width=1.5, color="rgba(240,30,65,0.8)"),
                                   name="84th percentile"
                                   )

        data = [trace1, trace_median1, trace_mean, trace_perctil]
        tit = inp1 + " eruption within next " + inp3 + " (" + inp2 + ")"
        layout = go.Layout(
            title=tit,
            xaxis_title="Best guess",
            yaxis_title="Person",
            # paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=go.layout.XAxis(
                dtick=0.1,
                #autorange=True
                range=[xmin, xmax + 0.05]
            ),
            yaxis=go.layout.YAxis(
                dtick=1,
                #autorange=True
                range=[0, ymax + 0.5]
            )
        )

        fig0 = go.Figure(
            data=data,
            layout=layout
        )
        fig0.update_xaxes(showline=True, linewidth=0.8, linecolor='black', ticks="outside", tickwidth=0.8,
                          tickcolor='black', ticklen=4, mirror=True)
        fig0.update_yaxes(showline=True, linewidth=0.8, linecolor='black', ticks="outside", tickwidth=0.8,
                          tickcolor='black', ticklen=4, mirror=True)

        fig0.show()

    def tbl_ballis(self, dct1, lst1, lst2, lst3):
        df_ballp = {'Eruption size': dct1,
                    'P(hourly)': lst1,
                    'Ballistic diameter (m)': lst2,
                    # BRA:Given eruption, # ballistics in reference area
                    'Given eruption, # ballistics in reference area': lst3}
        # 'P(given eruption, death from ballistics)': p_erp_death_ball}
        df_bp = pd.DataFrame(data=df_ballp)

        return df_bp

    def tbl_surge(self, dct1, lst1, lst2, lst3):
        tb1 = {'Eruption size': dct1,
               'P(hourly)': lst1,
               'P(given eruption, exposure to surge)': lst2,
               'P(given exposure, death from surge)': lst3}
        tb1_p = pd.DataFrame(data=tb1)
        tb1_p['P(given eruption, death from surge)'] = tb1_p['P(given eruption, exposure to surge)'] * tb1_p['P(given exposure, death from surge)']
        tb1_p['P(death from surge in hr)'] = tb1_p['P(hourly)'] * tb1_p['P(given eruption, death from surge)']

        return tb1_p

    def risk_dying_cal(self, df2, df3, df1, val):
        if isinstance(df1, pd.DataFrame):  # check if the dataframe is None or not
            val1 = df2.iloc[val]['P(hourly)']
            val2 = df1.iloc[val]['P(given eruption, death from near vent processes)']
            val3 = df2.iloc[val]['P(given eruption, death from ballistics)']
            val4 = df3.iloc[val]['P(given eruption, death from surge)']
            RDE = val1 * (1 - (1 - val2) * (1 - val3) * (1 - val4))  # risk of dying from eruption
        else:
            val1 = df2.iloc[val]['P(hourly)']
            val3 = df2.iloc[val]['P(given eruption, death from ballistics)']
            val4 = df3.iloc[val]['P(given eruption, death from surge)']
            RDE = val1 * (1 - (1 - val3) * (1 - val4))  # risk of dying from eruption
        return RDE















