from merge_opti import MergedDF

'''Filtering of signals'''

def FinalStrategy(df_M30, df_M15, df_M5, strategies_by_timeframe, extracted_params):

    '''Mix of strategies, middle and short terms, some specifically for 
    buy or others for sell signals.'''

    df = MergedDF(df_M30, df_M15, df_M5, extracted_params)

    ## Extract the strategies used

    m5_strat = list(strategies_by_timeframe['M5'])
    m15_strat = list(strategies_by_timeframe['M15'])
    m30_strat = list(strategies_by_timeframe['M30'])

    ################## SIGNAL LOGIC ####################

    ############ Check each timeframe ############

    df['final_signal_M30'] = 0
    df['final_sl_M30']=0
    df['final_tp_M30']=0
    df['final_signal_M15'] = 0
    df['final_sl_M15']=0
    df['final_tp_M15']=0
    df['final_signal_M5'] = 0
    df['final_sl_M5']=0
    df['final_tp_M5']=0
        
    # Check the M30

    for i in range(len(df)):
        if set(m30_strat) == {'ST', 'DI', 'CE'}:
            row = df.iloc[i]
            signals =[int(row['signal_M30_1']), int(row['signal_M30_2']), int(row['signal_M30_3'])]
            sls = [row['sl_M30_1'],row['sl_M30_2'], row['sl_M30_3']]
            tps = [row['tp_M30_1'],row['tp_M30_2'], row['tp_M30_3']]
                            
            # Check if all signals are the same
            if len(set(signals)) == 1:
                df.loc[row.name, 'final_signal_M30'] = signals[0]
                df.loc[row.name, 'final_sl_M30']=sls[0]
                df.loc[row.name, 'final_tp_M30']=tps[0]

            # Check if 2 of the 3 signals are the same and one of them is 0
            elif len(set(signals)) == 2 and signals.count(0) == 1:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M30'] = non_zero_signal
                df.loc[row.name, 'final_sl_M30'] = non_zero_sl
                df.loc[row.name, 'final_tp_M30'] = non_zero_tp

            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals.count(0) == 2:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M30'] = non_zero_signal
                df.loc[row.name, 'final_sl_M30'] = non_zero_sl
                df.loc[row.name, 'final_tp_M30'] = non_zero_tp

            else:
                df.loc[row.name, 'final_signal_M30'] = 0
                df.loc[row.name, 'final_sl_M30']=0
                df.loc[row.name, 'final_tp_M30']=0

        elif set(m30_strat) == {'ST', 'DI'}:
            row = df.iloc[i]
            signals = [int(row['signal_M30_1']), int(row['signal_M30_2'])]
            sls = [row['sl_M30_1'], row['sl_M30_2']]
            tps = [row['tp_M30_1'], row['tp_M30_2']]
                    
            # Check if all signals are the same
            if len(set(signals)) == 1:
                df.loc[row.name, 'final_signal_M30'] = signals[0]
                df.loc[row.name, 'final_sl_M30']=sls[0]
                df.loc[row.name, 'final_tp_M30']=tps[0]
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals.count(0) == 1:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M30'] = non_zero_signal
                df.loc[row.name, 'final_sl_M30'] = non_zero_sl
                df.loc[row.name, 'final_tp_M30'] = non_zero_tp
                
            else:
                df.loc[row.name, 'final_signal_M30'] = 0
                df.loc[row.name, 'final_sl_M30'] = 0
                df.loc[row.name, 'final_tp_M30'] = 0

        elif set(m30_strat) == {'CE', 'DI'}:
            row = df.iloc[i]
            signals = [int(row['signal_M30_1']), int(row['signal_M30_3'])]
            sls = [row['sl_M30_1'], row['sl_M30_3']]
            tps = [row['tp_M30_1'], row['tp_M30_3']]
                    
            # Check if all signals are the same
            if len(set(signals)) == 1:
                df.loc[row.name, 'final_signal_M30'] = signals[0]
                df.loc[row.name, 'final_sl_M30']=sls[0]
                df.loc[row.name, 'final_tp_M30']=tps[0]
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals.count(0) == 1:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M30'] = non_zero_signal
                df.loc[row.name, 'final_sl_M30'] = non_zero_sl
                df.loc[row.name, 'final_tp_M30'] = non_zero_tp
                
            else:
                df.loc[row.name, 'final_signal_M30'] = 0
                df.loc[row.name, 'final_sl_M30'] = 0
                df.loc[row.name, 'final_tp_M30'] = 0

        elif set(m30_strat) == {'CE', 'ST'}:
            row = df.iloc[i]
            signals = [int(row['signal_M30_2']), int(row['signal_M30_3'])]
            sls = [row['sl_M30_2'], row['sl_M30_3']]
            tps = [row['tp_M30_2'], row['tp_M30_3']]
                    
            # Check if all signals are the same
            if len(set(signals)) == 1:
                df.loc[row.name, 'final_signal_M30'] = signals[0]
                df.loc[row.name, 'final_sl_M30']=sls[0]
                df.loc[row.name, 'final_tp_M30']=tps[0]
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals.count(0) == 1:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M30'] = non_zero_signal
                df.loc[row.name, 'final_sl_M30'] = non_zero_sl
                df.loc[row.name, 'final_tp_M30'] = non_zero_tp
                
            else:
                df.loc[row.name, 'final_signal_M30'] = 0
                df.loc[row.name, 'final_sl_M30'] = 0
                df.loc[row.name, 'final_tp_M30'] = 0

        elif set(m30_strat) == {'DI'}:
            row = df.iloc[i]
            signals = int(row['signal_M30_1'])
            sls = row['sl_M30_1']
            tps = row['tp_M30_1']
                                       
            # Check if all signals are the same
            if signals == 1:
                df.loc[row.name, 'final_signal_M30'] = 1
                df.loc[row.name, 'final_sl_M30']=sls
                df.loc[row.name, 'final_tp_M30']=tps
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals == -1:
                df.loc[row.name, 'final_signal_M30'] = -1
                df.loc[row.name, 'final_sl_M30']=sls
                df.loc[row.name, 'final_tp_M30']=tps

            else:
                df.loc[row.name, 'final_signal_M30'] = 0
                df.loc[row.name, 'final_sl_M30'] = 0
                df.loc[row.name, 'final_tp_M30'] = 0
        
        elif set(m30_strat) == {'ST'}:
            row = df.iloc[i]
            signals = int(row['signal_M30_2'])
            sls = row['sl_M30_2']
            tps = row['tp_M30_2']
                                       
            # Check if all signals are the same
            if signals == 1:
                df.loc[row.name, 'final_signal_M30'] = 1
                df.loc[row.name, 'final_sl_M30']=sls
                df.loc[row.name, 'final_tp_M30']=tps
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals == -1:
                df.loc[row.name, 'final_signal_M30'] = -1
                df.loc[row.name, 'final_sl_M30']=sls
                df.loc[row.name, 'final_tp_M30']=tps

            else:
                df.loc[row.name, 'final_signal_M30'] = 0
                df.loc[row.name, 'final_sl_M30'] = 0
                df.loc[row.name, 'final_tp_M30'] = 0

        elif set(m30_strat) == {'CE'}:
            row = df.iloc[i]
            signals = int(row['signal_M30_3'])
            sls = row['sl_M30_3']
            tps = row['tp_M30_3']
                                        
            # Check if all signals are the same
            if signals == 1:
                df.loc[row.name, 'final_signal_M30'] = 1
                df.loc[row.name, 'final_sl_M30']=sls
                df.loc[row.name, 'final_tp_M30']=tps
                            
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals == -1:
                df.loc[row.name, 'final_signal_M30'] = -1
                df.loc[row.name, 'final_sl_M30']=sls
                df.loc[row.name, 'final_tp_M30']=tps

            else:
                df.loc[row.name, 'final_signal_M30'] = 0
                df.loc[row.name, 'final_sl_M30'] = 0
                df.loc[row.name, 'final_tp_M30'] = 0
            
    # Check the M15

    for i in range(len(df)):
        if set(m15_strat) == {'ST', 'DI', 'CE'}:
            row = df.iloc[i]
            signals =[int(row['signal_M15_1']),int(row['signal_M15_2']), int(row['signal_M15_3'])]
            sls = [row['sl_M15_1'],row['sl_M15_2'], row['sl_M15_3']]
            tps = [row['tp_M15_1'],row['tp_M15_2'], row['tp_M15_3']]
                        
            # Check if all signals are the same
            if len(set(signals)) == 1:
                df.loc[row.name, 'final_signal_M15'] = signals[0]
                df.loc[row.name, 'final_sl_M15']=sls[0]
                df.loc[row.name, 'final_tp_M15']=tps[0]

            # Check if 2 of the 3 signals are the same and one of them is 0
            elif len(set(signals)) == 2 and signals.count(0) == 1:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M15'] = non_zero_signal
                df.loc[row.name, 'final_sl_M15'] = non_zero_sl
                df.loc[row.name, 'final_tp_M15'] = non_zero_tp

            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals.count(0) == 2:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M15'] = non_zero_signal
                df.loc[row.name, 'final_sl_M15'] = non_zero_sl
                df.loc[row.name, 'final_tp_M15'] = non_zero_tp

            else:
                df.loc[row.name, 'final_signal_M15'] = 0
                df.loc[row.name, 'final_sl_M15']=0
                df.loc[row.name, 'final_tp_M15']=0

        elif set(m15_strat) == {'ST', 'DI'}:
            row = df.iloc[i]
            signals = [int(row['signal_M15_1']), int(row['signal_M15_2'])]
            sls = [row['sl_M15_1'], row['sl_M15_2']]
            tps = [row['tp_M15_1'], row['tp_M15_2']]
                    
            # Check if all signals are the same
            if len(set(signals)) == 1:
                df.loc[row.name, 'final_signal_M15'] = signals[0]
                df.loc[row.name, 'final_sl_M15']=sls[0]
                df.loc[row.name, 'final_tp_M15']=tps[0]
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals.count(0) == 1:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M15'] = non_zero_signal
                df.loc[row.name, 'final_sl_M15'] = non_zero_sl
                df.loc[row.name, 'final_tp_M15'] = non_zero_tp
                
            else:
                df.loc[row.name, 'final_signal_M15'] = 0
                df.loc[row.name, 'final_sl_M15'] = 0
                df.loc[row.name, 'final_tp_M15'] = 0

        elif set(m15_strat) == {'DI', 'CE'}:
            row = df.iloc[i]
            signals = [int(row['signal_M15_1']), int(row['signal_M15_3'])]
            sls = [row['sl_M15_1'], row['sl_M15_3']]
            tps = [row['tp_M15_1'], row['tp_M15_3']]
                    
            # Check if all signals are the same
            if len(set(signals)) == 1:
                df.loc[row.name, 'final_signal_M15'] = signals[0]
                df.loc[row.name, 'final_sl_M15']=sls[0]
                df.loc[row.name, 'final_tp_M15']=tps[0]
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals.count(0) == 1:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M15'] = non_zero_signal
                df.loc[row.name, 'final_sl_M15'] = non_zero_sl
                df.loc[row.name, 'final_tp_M15'] = non_zero_tp
                
            else:
                df.loc[row.name, 'final_signal_M15'] = 0
                df.loc[row.name, 'final_sl_M15'] = 0
                df.loc[row.name, 'final_tp_M15'] = 0

        elif set(m15_strat) == {'ST', 'CE'}:
            row = df.iloc[i]
            signals = [int(row['signal_M15_2']), int(row['signal_M15_3'])]
            sls = [row['sl_M15_2'], row['sl_M15_3']]
            tps = [row['tp_M15_2'], row['tp_M15_3']]
                    
            # Check if all signals are the same
            if len(set(signals)) == 1:
                df.loc[row.name, 'final_signal_M15'] = signals[0]
                df.loc[row.name, 'final_sl_M15']=sls[0]
                df.loc[row.name, 'final_tp_M15']=tps[0]
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals.count(0) == 1:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M15'] = non_zero_signal
                df.loc[row.name, 'final_sl_M15'] = non_zero_sl
                df.loc[row.name, 'final_tp_M15'] = non_zero_tp
                
            else:
                df.loc[row.name, 'final_signal_M15'] = 0
                df.loc[row.name, 'final_sl_M15'] = 0
                df.loc[row.name, 'final_tp_M15'] = 0

        elif set(m15_strat) == {'DI'}:
            row = df.iloc[i]
            signals = int(row['signal_M15_1'])
            sls = row['sl_M15_1']
            tps = row['tp_M15_1']
                                       
            # Check if all signals are the same
            if signals == 1:
                df.loc[row.name, 'final_signal_M15'] = 1
                df.loc[row.name, 'final_sl_M15']=sls
                df.loc[row.name, 'final_tp_M15']=tps
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals == -1:
                df.loc[row.name, 'final_signal_M15'] = -1
                df.loc[row.name, 'final_sl_M15']=sls
                df.loc[row.name, 'final_tp_M15']=tps

            else:
                df.loc[row.name, 'final_signal_M15'] = 0
                df.loc[row.name, 'final_sl_M15'] = 0
                df.loc[row.name, 'final_tp_M15'] = 0
        
        elif set(m15_strat) == {'ST'}:
            row = df.iloc[i]
            signals = int(row['signal_M15_2'])
            sls = row['sl_M15_2']
            tps = row['tp_M15_2']
                                       
            # Check if all signals are the same
            if signals == 1:
                df.loc[row.name, 'final_signal_M15'] = 1
                df.loc[row.name, 'final_sl_M15']=sls
                df.loc[row.name, 'final_tp_M15']=tps
                        
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals == -1:
                df.loc[row.name, 'final_signal_M15'] = -1
                df.loc[row.name, 'final_sl_M15']=sls
                df.loc[row.name, 'final_tp_M15']=tps

            else:
                df.loc[row.name, 'final_signal_M15'] = 0
                df.loc[row.name, 'final_sl_M15'] = 0
                df.loc[row.name, 'final_tp_M15'] = 0

        elif set(m15_strat) == {'CE'}:
            row = df.iloc[i]
            signals = int(row['signal_M15_3'])
            sls = row['sl_M15_3']
            tps = row['tp_M15_3']
                                            
            # Check if all signals are the same
            if signals == 1:
                df.loc[row.name, 'final_signal_M15'] = 1
                df.loc[row.name, 'final_sl_M15']=sls
                df.loc[row.name, 'final_tp_M15']=tps
                                
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals == -1:
                df.loc[row.name, 'final_signal_M15'] = -1
                df.loc[row.name, 'final_sl_M15']=sls
                df.loc[row.name, 'final_tp_M15']=tps

            else:
                df.loc[row.name, 'final_signal_M15'] = 0
                df.loc[row.name, 'final_sl_M15'] = 0
                df.loc[row.name, 'final_tp_M15'] = 0

    # Check the M5

    for i in range(len(df)):
        if set(m5_strat) == {'ST', 'CE'}:
            row = df.iloc[i]
            signals = [int(row['signal_M5_2']), int(row['signal_M5_3'])]
            sls = [row['sl_M5_2'], row['sl_M5_3']]
            tps = [row['tp_M5_2'], row['tp_M5_3']]
                            
            # Check if all signals are the same
            if len(set(signals)) == 1:
                df.loc[row.name, 'final_signal_M5'] = signals[0]
                df.loc[row.name, 'final_sl_M5']=sls[0]
                df.loc[row.name, 'final_tp_M5']=tps[0]
                                
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals.count(0) == 1:
                non_zero_signal = [x for x in signals if x != 0][0]
                non_zero_sl=[x for x in sls if x != 0][0]
                non_zero_tp=[x for x in tps if x != 0][0]
                df.loc[row.name, 'final_signal_M5'] = non_zero_signal
                df.loc[row.name, 'final_sl_M5'] = non_zero_sl
                df.loc[row.name, 'final_tp_M5'] = non_zero_tp
                        
            else:
                df.loc[row.name, 'final_signal_M15'] = 0
                df.loc[row.name, 'final_sl_M15'] = 0
                df.loc[row.name, 'final_tp_M15'] = 0

        elif set(m5_strat) == {'CE'}:
            row = df.iloc[i]
            signals = int(row['signal_M5_3'])
            sls = row['sl_M5_3']
            tps = row['tp_M5_3']
                                        
            # Check if all signals are the same
            if signals == 1:
                df.loc[row.name, 'final_signal_M5'] = 1
                df.loc[row.name, 'final_sl_M5']=sls
                df.loc[row.name, 'final_tp_M5']=tps
                            
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals == -1:
                df.loc[row.name, 'final_signal_M5'] = -1
                df.loc[row.name, 'final_sl_M5']=sls
                df.loc[row.name, 'final_tp_M5']=tps

            else:
                df.loc[row.name, 'final_signal_M5'] = 0
                df.loc[row.name, 'final_sl_M5'] = 0
                df.loc[row.name, 'final_tp_M5'] = 0

        elif set(m5_strat) == {'ST'}:
            row = df.iloc[i]
            signals = int(row['signal_M5_2'])
            sls = row['sl_M5_2']
            tps = row['tp_M5_2']
                                        
            # Check if all signals are the same
            if signals == 1:
                df.loc[row.name, 'final_signal_M5'] = 1
                df.loc[row.name, 'final_sl_M5']=sls
                df.loc[row.name, 'final_tp_M5']=tps
                            
            # Check if one of the 3 signals is 1 or -1 and four of them are 0
            elif signals == -1:
                df.loc[row.name, 'final_signal_M5'] = -1
                df.loc[row.name, 'final_sl_M5']=sls
                df.loc[row.name, 'final_tp_M5']=tps

            else:
                df.loc[row.name, 'final_signal_M5'] = 0
                df.loc[row.name, 'final_sl_M5'] = 0
                df.loc[row.name, 'final_tp_M5'] = 0
    
    return df