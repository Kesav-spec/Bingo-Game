import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class GraphPlot:
    def __init__(self,bingo_data_cdf,full_house_data_cdf,bingo_data_raw,full_house_data_raw):
        self.bingo_table_cdf = bingo_data_cdf
        self.full_house_table_cdf = full_house_data_cdf
        self.bingo_data_raw = bingo_data_raw
        self.full_house_data_raw = full_house_data_raw

    
    def do_np_transform(self):

        bingo_array = np.array(self.bingo_table_cdf)
        full_house_array = np.array(self.full_house_table_cdf)


        if bingo_array.ndim == 0:
            bingo_array = np.array([bingo_array])
        if full_house_array.ndim == 0:
            full_house_array = np.array([full_house_array])

        bingo_df = pd.DataFrame(bingo_array)
        fullhouse_df = pd.DataFrame(full_house_array)

        
        bingo_df_mean = bingo_df.mean(axis=0)
        full_house_df_mean = fullhouse_df.mean(axis=0)

        bingo_df_std = bingo_df.std(axis=0)
        full_house_std = fullhouse_df.std(axis = 0)

        bingo_df_std_UL = bingo_df_std + bingo_df_mean
        bingo_df_std_LL = bingo_df_mean - bingo_df_std

        full_house_std_UL = full_house_df_mean + full_house_std
        full_house_std_LL = full_house_df_mean - full_house_std

        bingo_df_max = bingo_df.max(axis=0)
        full_house_df_max = fullhouse_df.max(axis=0)

        bingo_df_min = bingo_df.min(axis=0)
        full_house_df_min = fullhouse_df.min(axis=0)
        range_ = [i for i in range(len(bingo_df_mean))]

        fig,ax = plt.subplots()

        ax.plot(range_,bingo_df_mean,label="Bingo",color="blue")
        ax.plot(range_,bingo_df_max,linestyle='--',color="skyblue",linewidth=1)
        ax.plot(range_,bingo_df_min,linestyle='--',color="skyblue",linewidth=1)
        

        ax.plot(range_,bingo_df_std_UL,color="skyblue")
        ax.plot(range_,bingo_df_std_LL,color="skyblue")


        ax.plot(range_,full_house_df_mean, label="Full-House",color="orange")
        ax.plot(range_,full_house_df_max,linestyle='--', color="orange",linewidth=1)
        ax.plot(range_,full_house_df_min,linestyle='--', color="orange",linewidth=1)
        ax.plot(range_,full_house_std_LL,color="orange")
        ax.plot(range_,full_house_std_UL,color="orange")
        
        plt.xlabel("# Numbers Called")
        plt.ylabel("# Winners")
        ax.legend()
        plt.fill_between(x=range_,y1=bingo_df_std_UL,y2=bingo_df_mean,alpha=0.1,color="skyblue")
        plt.fill_between(x=range_,y1=bingo_df_std_LL,y2=bingo_df_mean,alpha=0.1,color="skyblue")
        plt.fill_between(x=range_,y1=full_house_std_LL,y2=full_house_df_mean,alpha=0.1,color="orange")
        plt.fill_between(x=range_,y1=full_house_std_UL,y2=full_house_df_mean,alpha=0.1,color="orange")
        plt.savefig(fname="./CDF_Graph",dpi=100)
        plt.legend()

    def draw_details(self,bingo_df,fullhouse_df,numbers_called):
        # Median
        bingo_median = bingo_df.median(axis=0) 
        fullhouse_median = fullhouse_df.median(axis=0)

        # Skewness
        bingo_skew = bingo_df.skew(axis=0)
        fullhouse_skew = fullhouse_df.skew(axis=0) 

        # Percentiles 
        bingo_perc = bingo_df.quantile([0.25,0.75])
        fullhouse_perc = fullhouse_df.quantile([0.25,0.75])

        # Kurtosis
        bingo_kurtosis = bingo_df.kurt(axis=0) 
        fullhouse_kurtosis = fullhouse_df.kurt(axis=0)

        b_df = pd.DataFrame(columns=['Numbers Called','Median','25th Percentile','75th Percentile','Skew','Kurtosis'])
        b_df['Numbers Called'] = numbers_called
        b_df['Median'] = bingo_median
        b_df['Skew'] = bingo_skew
        b_df['Kurtosis'] = bingo_kurtosis
        b_df['25th Percentile'] = bingo_perc.loc[0.25]
        b_df['75th Percentile'] = bingo_perc.loc[0.75]

        f_df = pd.DataFrame(columns=['Numbers Called','Median','25th Percentile','75th Percentile','Skew','Kurtosis'])
        f_df['Numbers Called'] = numbers_called
        f_df['Median'] = fullhouse_median
        f_df['Skew'] = fullhouse_skew
        f_df['Kurtosis'] = fullhouse_kurtosis
        f_df['25th Percentile'] = fullhouse_perc.loc[0.25]
        f_df['75th Percentile'] = fullhouse_perc.loc[0.75]

        b_df.to_html('./Bingo_Details.html',index=False)
        f_df.to_html('./Full_house_Details.html', index=False)


        

        
    def plot_histogram(self):
        bingo_array_raw = np.array(self.bingo_data_raw)
        full_house_array_raw = np.array(self.full_house_data_raw)

        if bingo_array_raw.ndim == 0:
            bingo_array_raw = np.array([bingo_array_raw])
        if full_house_array_raw.ndim == 0:
            full_house_array_raw = np.array([full_house_array_raw])

        bingo_df_raw = pd.DataFrame(bingo_array_raw)
        full_house_df_raw = pd.DataFrame(full_house_array_raw)

        bing_df_mean_raw = bingo_df_raw.mean(axis=0)
        full_house_df_mean_raw = full_house_df_raw.mean(axis=0)


        range_ = [i+1 for i in range(len(bing_df_mean_raw))]

        fig, ax = plt.subplots()

        ax.bar(range_,bing_df_mean_raw,width=1,edgecolor='black')
        #plt.bar(range_,full_house_df_mean_raw,width=1,edgecolor='black',color='skyblue')
        plt.xlabel("Numbers Called")
        plt.ylabel("Bingo encountered")
        plt.savefig("./Histogram.png")

        self.draw_details(bingo_df_raw,full_house_df_raw,range_)











