from Data import MergedDF

def Porte(symbol, timeframe):

    '''Mix of strategies, middle and short terms, some specifically for 
    buy or others for sell signals.'''

    df = MergedDF(symbol, timeframe)

    ################## SIGNAL LOGIC ####################

    if timeframe == 'M30':
        if symbol == 'EURUSD':
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = [int(row['signal_1']), int(row['signal_2']), int(row['signal_3'])]
                sls = [row['sl_1'], row['sl_2'], row['sl_3']]
                tps_1 = [row['tp_1_1'], row['tp_2_1'], row['tp_3_1']]
                tps_2 = [row['tp_1_2'], row['tp_2_2'], row['tp_3_2']]
                tps_3 = [row['tp_1_3'], row['tp_2_3'], row['tp_3_3']]
                tps_4 = [row['tp_1_4'], row['tp_2_4'], row['tp_3_4']]
                tps_5 = [row['tp_1_5'], row['tp_2_5'], row['tp_3_5']]
                
                # Check if all signals are the same
                if len(set(signals)) == 1:
                    df.loc[row.name, 'final_signal'] = signals[0]
                    df.loc[row.name, 'sl'] = sls[0]
                    df.loc[row.name, 'tp_1'] = tps_1[0]
                    df.loc[row.name, 'tp_2'] = tps_2[0]
                    df.loc[row.name, 'tp_3'] = tps_3[0]
                    df.loc[row.name, 'tp_4'] = tps_4[0]
                    df.loc[row.name, 'tp_5'] = tps_5[0]

                elif len(set(signals)) == 2 and signals.count(0) == 1:
                    non_zero_signal = [x for x in signals if x != 0][0]
                    non_zero_sl=[x for x in sls if x != 0][0]
                    non_zero_tp_1=[x for x in tps_1 if x != 0][0]
                    non_zero_tp_2=[x for x in tps_2 if x != 0][0]
                    non_zero_tp_3=[x for x in tps_3 if x != 0][0]
                    non_zero_tp_4=[x for x in tps_4 if x != 0][0]
                    non_zero_tp_5=[x for x in tps_5 if x != 0][0]
                    df.loc[row.name, 'final_signal'] = non_zero_signal
                    df.loc[row.name, 'sl'] = non_zero_sl
                    df.loc[row.name, 'tp_1'] = non_zero_tp_1
                    df.loc[row.name, 'tp_2'] = non_zero_tp_2
                    df.loc[row.name, 'tp_3'] = non_zero_tp_3
                    df.loc[row.name, 'tp_4'] = non_zero_tp_4
                    df.loc[row.name, 'tp_5'] = non_zero_tp_5
                        
                # Check if one of the 2 signals is 1 or -1 and four of them are 0
                elif signals.count(0) == 2:
                    non_zero_signal = [x for x in signals if x != 0][0]
                    non_zero_sl=[x for x in sls if x != 0][0]
                    non_zero_tp_1=[x for x in tps_1 if x != 0][0]
                    non_zero_tp_2=[x for x in tps_2 if x != 0][0]
                    non_zero_tp_3=[x for x in tps_3 if x != 0][0]
                    non_zero_tp_4=[x for x in tps_4 if x != 0][0]
                    non_zero_tp_5=[x for x in tps_5 if x != 0][0]
                    df.loc[row.name, 'final_signal'] = non_zero_signal
                    df.loc[row.name, 'sl'] = non_zero_sl
                    df.loc[row.name, 'tp_1'] = non_zero_tp_1
                    df.loc[row.name, 'tp_2'] = non_zero_tp_2
                    df.loc[row.name, 'tp_3'] = non_zero_tp_3
                    df.loc[row.name, 'tp_4'] = non_zero_tp_4
                    df.loc[row.name, 'tp_5'] = non_zero_tp_5

                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0
                    
        elif symbol == 'TEST':
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = int(row['signal_3'])
                sls = row['sl_3']
                tps_1 = row['tp_3_1']
                tps_2 = row['tp_3_2']
                tps_3 = row['tp_3_3']
                tps_4 = row['tp_3_4']
                tps_5 = row['tp_3_5']

                # Check if all signals are the same
                if signals == 1:
                    df.loc[row.name, 'final_signal'] = 1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5

                # Check if one of the 2 signals is 1 or -1 and four of them are 0
                elif signals == -1:
                    df.loc[row.name, 'final_signal'] = -1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5
                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0
        
        elif symbol == 'TEST':
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = int(row['signal_2'])
                sls = row['sl_2']
                tps_1 = row['tp_2_1']
                tps_2 = row['tp_2_2']
                tps_3 = row['tp_2_3']
                tps_4 = row['tp_2_4']
                tps_5 = row['tp_2_5']

                # Check if all signals are the same
                if signals == 1:
                    df.loc[row.name, 'final_signal'] = 1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5

                # Check if one of the 2 signals is 1 or -1 and four of them are 0
                elif signals == -1:
                    df.loc[row.name, 'final_signal'] = -1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5
                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0

        elif symbol == 'TEST':
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = [int(row['signal_2']), int(row['signal_3'])]
                sls = [row['sl_2'], row['sl_3']]
                tps_1 = [row['tp_2_1'], row['tp_3_1']]
                tps_2 = [row['tp_2_2'], row['tp_3_2']]
                tps_3 = [row['tp_2_3'], row['tp_3_3']]
                tps_4 = [row['tp_2_4'], row['tp_3_4']]
                tps_5 = [row['tp_2_5'], row['tp_3_5']]

                # Check if all signals are the same
                if len(set(signals)) == 1:
                    df.loc[row.name, 'final_signal'] = signals[0]
                    df.loc[row.name, 'sl'] = sls[0]
                    df.loc[row.name, 'tp_1'] = tps_1[0]
                    df.loc[row.name, 'tp_2'] = tps_2[0]
                    df.loc[row.name, 'tp_3'] = tps_3[0]
                    df.loc[row.name, 'tp_4'] = tps_4[0]
                    df.loc[row.name, 'tp_5'] = tps_5[0]

                # Check if one of the 2 signals is 1 or -1 and four of them are 0
                elif signals.count(0) == 1:
                    non_zero_signal = [x for x in signals if x != 0][0]
                    non_zero_sl=[x for x in sls if x != 0][0]
                    non_zero_tp_1=[x for x in tps_1 if x != 0][0]
                    non_zero_tp_2=[x for x in tps_2 if x != 0][0]
                    non_zero_tp_3=[x for x in tps_3 if x != 0][0]
                    non_zero_tp_4=[x for x in tps_4 if x != 0][0]
                    non_zero_tp_5=[x for x in tps_5 if x != 0][0]
                    df.loc[row.name, 'final_signal'] = non_zero_signal
                    df.loc[row.name, 'sl'] = non_zero_sl
                    df.loc[row.name, 'tp_1'] = non_zero_tp_1
                    df.loc[row.name, 'tp_2'] = non_zero_tp_2
                    df.loc[row.name, 'tp_3'] = non_zero_tp_3
                    df.loc[row.name, 'tp_4'] = non_zero_tp_4
                    df.loc[row.name, 'tp_5'] = non_zero_tp_5

                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0

    elif timeframe == 'M15':
        if symbol in ['EURUSD', 'GBPUSD']:
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = [int(row['signal_1']), int(row['signal_2']), int(row['signal_3'])]
                sls = [row['sl_1'], row['sl_2'], row['sl_3']]
                tps_1 = [row['tp_1_1'], row['tp_2_1'], row['tp_3_1']]
                tps_2 = [row['tp_1_2'], row['tp_2_2'], row['tp_3_2']]
                tps_3 = [row['tp_1_3'], row['tp_2_3'], row['tp_3_3']]
                tps_4 = [row['tp_1_4'], row['tp_2_4'], row['tp_3_4']]
                tps_5 = [row['tp_1_5'], row['tp_2_5'], row['tp_3_5']]
                
                # Check if all signals are the same
                if len(set(signals)) == 1:
                    df.loc[row.name, 'final_signal'] = signals[0]
                    df.loc[row.name, 'sl'] = sls[0]
                    df.loc[row.name, 'tp_1'] = tps_1[0]
                    df.loc[row.name, 'tp_2'] = tps_2[0]
                    df.loc[row.name, 'tp_3'] = tps_3[0]
                    df.loc[row.name, 'tp_4'] = tps_4[0]
                    df.loc[row.name, 'tp_5'] = tps_5[0]

                elif len(set(signals)) == 2 and signals.count(0) == 1:
                    non_zero_signal = [x for x in signals if x != 0][0]
                    non_zero_sl=[x for x in sls if x != 0][0]
                    non_zero_tp_1=[x for x in tps_1 if x != 0][0]
                    non_zero_tp_2=[x for x in tps_2 if x != 0][0]
                    non_zero_tp_3=[x for x in tps_3 if x != 0][0]
                    non_zero_tp_4=[x for x in tps_4 if x != 0][0]
                    non_zero_tp_5=[x for x in tps_5 if x != 0][0]
                    df.loc[row.name, 'final_signal'] = non_zero_signal
                    df.loc[row.name, 'sl'] = non_zero_sl
                    df.loc[row.name, 'tp_1'] = non_zero_tp_1
                    df.loc[row.name, 'tp_2'] = non_zero_tp_2
                    df.loc[row.name, 'tp_3'] = non_zero_tp_3
                    df.loc[row.name, 'tp_4'] = non_zero_tp_4
                    df.loc[row.name, 'tp_5'] = non_zero_tp_5
                        
                # Check if one of the 2 signals is 1 or -1 and four of them are 0
                elif signals.count(0) == 2:
                    non_zero_signal = [x for x in signals if x != 0][0]
                    non_zero_sl=[x for x in sls if x != 0][0]
                    non_zero_tp_1=[x for x in tps_1 if x != 0][0]
                    non_zero_tp_2=[x for x in tps_2 if x != 0][0]
                    non_zero_tp_3=[x for x in tps_3 if x != 0][0]
                    non_zero_tp_4=[x for x in tps_4 if x != 0][0]
                    non_zero_tp_5=[x for x in tps_5 if x != 0][0]
                    df.loc[row.name, 'final_signal'] = non_zero_signal
                    df.loc[row.name, 'sl'] = non_zero_sl
                    df.loc[row.name, 'tp_1'] = non_zero_tp_1
                    df.loc[row.name, 'tp_2'] = non_zero_tp_2
                    df.loc[row.name, 'tp_3'] = non_zero_tp_3
                    df.loc[row.name, 'tp_4'] = non_zero_tp_4
                    df.loc[row.name, 'tp_5'] = non_zero_tp_5

                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0

        elif symbol == 'TEST':
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = int(row['signal_3'])
                sls = row['sl_3']
                tps_1 = row['tp_3_1']
                tps_2 = row['tp_3_2']
                tps_3 = row['tp_3_3']
                tps_4 = row['tp_3_4']
                tps_5 = row['tp_3_5']

                # Check if all signals are the same
                if signals == 1:
                    df.loc[row.name, 'final_signal'] = 1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5

                # Check if one of the 2 signals is 1 or -1 and four of them are 0
                elif signals == -1:
                    df.loc[row.name, 'final_signal'] = -1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5
                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0

        elif symbol in ['TEST', 'TEST']:
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = [int(row['signal_2']), int(row['signal_3'])]
                sls = [row['sl_2'], row['sl_3']]
                tps_1 = [row['tp_2_1'], row['tp_3_1']]
                tps_2 = [row['tp_2_2'], row['tp_3_2']]
                tps_3 = [row['tp_2_3'], row['tp_3_3']]
                tps_4 = [row['tp_2_4'], row['tp_3_4']]
                tps_5 = [row['tp_2_5'], row['tp_3_5']]

                # Check if all signals are the same
                if len(set(signals)) == 1:
                    df.loc[row.name, 'final_signal'] = signals[0]
                    df.loc[row.name, 'sl'] = sls[0]
                    df.loc[row.name, 'tp_1'] = tps_1[0]
                    df.loc[row.name, 'tp_2'] = tps_2[0]
                    df.loc[row.name, 'tp_3'] = tps_3[0]
                    df.loc[row.name, 'tp_4'] = tps_4[0]
                    df.loc[row.name, 'tp_5'] = tps_5[0]

                # Check if one of the 2 signals is 1 or -1 and four of them are 0
                elif signals.count(0) == 1:
                    non_zero_signal = [x for x in signals if x != 0][0]
                    non_zero_sl=[x for x in sls if x != 0][0]
                    non_zero_tp_1=[x for x in tps_1 if x != 0][0]
                    non_zero_tp_2=[x for x in tps_2 if x != 0][0]
                    non_zero_tp_3=[x for x in tps_3 if x != 0][0]
                    non_zero_tp_4=[x for x in tps_4 if x != 0][0]
                    non_zero_tp_5=[x for x in tps_5 if x != 0][0]
                    df.loc[row.name, 'final_signal'] = non_zero_signal
                    df.loc[row.name, 'sl'] = non_zero_sl
                    df.loc[row.name, 'tp_1'] = non_zero_tp_1
                    df.loc[row.name, 'tp_2'] = non_zero_tp_2
                    df.loc[row.name, 'tp_3'] = non_zero_tp_3
                    df.loc[row.name, 'tp_4'] = non_zero_tp_4
                    df.loc[row.name, 'tp_5'] = non_zero_tp_5

                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0

        elif symbol == 'TEST':
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = [int(row['signal_3']), int(row['signal_1'])]
                sls = [row['sl_3'], row['sl_1']]
                tps_1 = [row['tp_3_1'], row['tp_1_1']]
                tps_2 = [row['tp_3_2'], row['tp_1_2']]
                tps_3 = [row['tp_3_3'], row['tp_1_3']]
                tps_4 = [row['tp_3_4'], row['tp_1_4']]
                tps_5 = [row['tp_3_5'], row['tp_1_5']]

                # Check if all signals are the same
                if len(set(signals)) == 1:
                    df.loc[row.name, 'final_signal'] = signals[0]
                    df.loc[row.name, 'sl'] = sls[0]
                    df.loc[row.name, 'tp_1'] = tps_1[0]
                    df.loc[row.name, 'tp_2'] = tps_2[0]
                    df.loc[row.name, 'tp_3'] = tps_3[0]
                    df.loc[row.name, 'tp_4'] = tps_4[0]
                    df.loc[row.name, 'tp_5'] = tps_5[0]

                # Check if one of the 2 signals is 1 or -1 and four of them are 0
                elif signals.count(0) == 1:
                    non_zero_signal = [x for x in signals if x != 0][0]
                    non_zero_sl=[x for x in sls if x != 0][0]
                    non_zero_tp_1=[x for x in tps_1 if x != 0][0]
                    non_zero_tp_2=[x for x in tps_2 if x != 0][0]
                    non_zero_tp_3=[x for x in tps_3 if x != 0][0]
                    non_zero_tp_4=[x for x in tps_4 if x != 0][0]
                    non_zero_tp_5=[x for x in tps_5 if x != 0][0]
                    df.loc[row.name, 'final_signal'] = non_zero_signal
                    df.loc[row.name, 'sl'] = non_zero_sl
                    df.loc[row.name, 'tp_1'] = non_zero_tp_1
                    df.loc[row.name, 'tp_2'] = non_zero_tp_2
                    df.loc[row.name, 'tp_3'] = non_zero_tp_3
                    df.loc[row.name, 'tp_4'] = non_zero_tp_4
                    df.loc[row.name, 'tp_5'] = non_zero_tp_5

                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0
        
    elif timeframe == 'M5':
        if symbol in ['TEST','TEST', 'TEST']:
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = int(row['signal_2'])
                sls = row['sl_2']
                tps_1 = row['tp_2_1']
                tps_2 = row['tp_2_2']
                tps_3 = row['tp_2_3']
                tps_4 = row['tp_2_4']
                tps_5 = row['tp_2_5']
                    
                # Check if all signals are the same
                if signals == 1:
                    df.loc[row.name, 'final_signal'] = 1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5
                    
                elif signals == -1:
                    df.loc[row.name, 'final_signal'] = -1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5
                            
                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0
        
        elif symbol in ['EURUSD', 'GBPUSD']:
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = [int(row['signal_3']), int(row['signal_2'])]
                sls = [row['sl_3'], row['sl_2']]
                tps_1 = [row['tp_3_1'], row['tp_2_1']]
                tps_2 = [row['tp_3_2'], row['tp_2_2']]
                tps_3 = [row['tp_3_3'], row['tp_2_3']]
                tps_4 = [row['tp_3_4'], row['tp_2_4']]
                tps_5 = [row['tp_3_5'], row['tp_2_5']]

                # Check if all signals are the same
                if len(set(signals)) == 1:
                    df.loc[row.name, 'final_signal'] = signals[0]
                    df.loc[row.name, 'sl'] = sls[0]
                    df.loc[row.name, 'tp_1'] = tps_1[0]
                    df.loc[row.name, 'tp_2'] = tps_2[0]
                    df.loc[row.name, 'tp_3'] = tps_3[0]
                    df.loc[row.name, 'tp_4'] = tps_4[0]
                    df.loc[row.name, 'tp_5'] = tps_5[0]

                # Check if one of the 2 signals is 1 or -1 and four of them are 0
                elif signals.count(0) == 1:
                    non_zero_signal = [x for x in signals if x != 0][0]
                    non_zero_sl=[x for x in sls if x != 0][0]
                    non_zero_tp_1=[x for x in tps_1 if x != 0][0]
                    non_zero_tp_2=[x for x in tps_2 if x != 0][0]
                    non_zero_tp_3=[x for x in tps_3 if x != 0][0]
                    non_zero_tp_4=[x for x in tps_4 if x != 0][0]
                    non_zero_tp_5=[x for x in tps_5 if x != 0][0]
                    df.loc[row.name, 'final_signal'] = non_zero_signal
                    df.loc[row.name, 'sl'] = non_zero_sl
                    df.loc[row.name, 'tp_1'] = non_zero_tp_1
                    df.loc[row.name, 'tp_2'] = non_zero_tp_2
                    df.loc[row.name, 'tp_3'] = non_zero_tp_3
                    df.loc[row.name, 'tp_4'] = non_zero_tp_4
                    df.loc[row.name, 'tp_5'] = non_zero_tp_5

                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0

        elif symbol in ['TEST', 'TEST']:
            df['final_signal'] = 0
            df['sl']=0
            df['tp_1']=0
            df['tp_2']=0
            df['tp_3']=0
            df['tp_4']=0
            df['tp_5']=0

            for i in range(len(df)):
                row = df.iloc[i]
                signals = int(row['signal_3'])
                sls = row['sl_3']
                tps_1 = row['tp_3_1']
                tps_2 = row['tp_3_2']
                tps_3 = row['tp_3_3']
                tps_4 = row['tp_3_4']
                tps_5 = row['tp_3_5']
        
                # Check if all signals are the same
                if signals == 1:
                    df.loc[row.name, 'final_signal'] = 1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5
                    
                elif signals == -1:
                    df.loc[row.name, 'final_signal'] = -1
                    df.loc[row.name, 'sl'] = sls
                    df.loc[row.name, 'tp_1'] = tps_1
                    df.loc[row.name, 'tp_2'] = tps_2
                    df.loc[row.name, 'tp_3'] = tps_3
                    df.loc[row.name, 'tp_4'] = tps_4
                    df.loc[row.name, 'tp_5'] = tps_5
                            
                else:
                    df.loc[row.name, 'final_signal'] = 0
                    df.loc[row.name, 'sl'] = 0
                    df.loc[row.name, 'tp_1'] = 0
                    df.loc[row.name, 'tp_2'] = 0
                    df.loc[row.name, 'tp_3'] = 0
                    df.loc[row.name, 'tp_4'] = 0
                    df.loc[row.name, 'tp_5'] = 0

    signal = df['final_signal'].iloc[-1]
    close = df['Close'].iloc[-1]
    sl = df['sl'].iloc[-1]
    tp_1 = df['tp_1'].iloc[-1]
    tp_2 = df['tp_2'].iloc[-1]
    tp_3 = df['tp_3'].iloc[-1]
    tp_4 = df['tp_4'].iloc[-1]
    tp_5 = df['tp_5'].iloc[-1]
        
    return signal, close, sl, tp_1, tp_2, tp_3, tp_4, tp_5