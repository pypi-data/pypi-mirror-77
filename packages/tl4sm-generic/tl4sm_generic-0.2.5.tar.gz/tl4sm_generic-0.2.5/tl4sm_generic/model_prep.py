from prepare_data import split_dataset
from numpy import array, stack
from pandas import read_csv, DataFrame
from pathlib import Path
from keras.models import load_model, clone_model
import time
from matplotlib import pyplot as plt
from keras import optimizers
from prepare_data import to_supervised
from keras.utils import to_categorical
from numpy import argmax
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, classification_report




#function to bin data and return dataframe
def bin_data(dataset, med, high):
    dataset['bin'] = 0
    dataset['bin'][(dataset['intSpeed'] < high) & (dataset['intSpeed'] > med)] = 1
    dataset['bin'][(dataset['intSpeed'] >= high)] = 2
    return dataset

#function to view the training history of each model
def view_loss(history, exp_num):
    plt.plot(history.history['loss'],label='Train')
    plt.plot(history.history['val_loss'],label='Val')
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()
    plt.savefig('../Plots/loss-history'+str(exp_num)+'.png')
    plt.show()
    
#function to view the training history of each model
def view_acc(history, exp_num):
    plt.close()
    plt.plot(history.history['acc'],label='Accuracy')
    plt.plot(history.history['loss'],label='Loss')
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()
    plt.savefig('../Plots/loss-history'+str(exp_num)+'.png')
    plt.show()


# make a forecast
def forecast(model, history, n_input):
    # flatten data
    data = array(history)
    data = data.reshape((data.shape[0]*data.shape[1], data.shape[2]))
    # retrieve last observations for input data
    input_x = data[-n_input:, :]
    # reshape into [samples, timesteps, features]
    input_x = input_x.reshape((1, input_x.shape[0], input_x.shape[1]))
    # forecast the next week
    yhat = model.predict(input_x, verbose=0)
    # we only want the vector forecast
    yhat = yhat[0]
    return yhat


#function to evaluate the model
def evaluate_model(model, train, test, tr_time, n_input, source, exp_num):
    # history is a list of training data
    history = [x for x in train]
    # walk-forward validation over each timestep
    predictions = list()
    for i in range(len(test)):
        # predict the timestep
        yhat_sequence = forecast(model, history, n_input)
        # store the predictions
        predictions.append(yhat_sequence)
        # get real observation and add to history for predicting the next timestep
        history.append(test[i, :])
    # evaluate predictions days for each timestep
    predictions = array(predictions)
    test1 = test[:, :, -1]
    YPred = argmax(predictions.reshape(predictions.shape[0], (predictions.shape[1]*predictions.shape[2])), out=None, axis=1)
    YPred = YPred.reshape(YPred.shape[0], 1)
    df = stack((YPred, test1))
    df = df.transpose()
    df = df.reshape(df.shape[1], 2)
    DataFrame(df).to_csv('../Results/2DConvLSTMAE_TL_'+str(exp_num)+'.csv')
    cm = confusion_matrix(test1, YPred)
    print(cm)
    f1 = f1_score(test1, YPred, average='weighted')
    acc = accuracy_score(test1, YPred)
    print(classification_report(test1, YPred))
    return f1, acc, tr_time, f1, acc, tr_time

#function to evaluate the model
def evaluate_model_reuse(train, test, n_input, batch_size, lr, source, exp_num, epochs, model_name, data_percent, n_out, batch_norm=True, plot=False):
    #prepare data
    train_x, train_y = to_supervised(train, n_input, step_size=1, n_out=1, is_y=True)
    # define model
    model = load_model(model_name)
    model = clone_model(model)
    model.build()
    opt = optimizers.Adam()
    model.compile(loss='categorical_crossentropy', metrics = ['acc'], optimizer=opt)
    #model.summary()    
    model.load_weights(model_name)
    #data percentage
    train_ind = int(round(len(train_x)*(data_percent)))
    train_x = train_x[-train_ind:, :]
    train_y = train_y[-train_ind:, :]
    # reshape output into [samples, timesteps, features]
    train_y = train_y.reshape((train_y.shape[0], train_y.shape[1], 1)) 
    train_y =to_categorical(train_y)
    #record time
    tic = time.time()
    # fit network
    history = model.fit(train_x, train_y, epochs=epochs, shuffle=False, batch_size=batch_size, verbose=2) 
    #record time
    toc = time.time()
    totTime = toc-tic
    #model.load_weights('../Models/best_weights_TL.hdf5')
    model.save('../Models/model_TL_'+str(exp_num)+'.h5')
    if plot:
        view_loss(history, str(exp_num))
    # history is a list of training data
    history = [x for x in train]
    # walk-forward validation over each timestep
    predictions = list()
    for i in range(len(test)):
        # predict the timestep
        yhat_sequence = forecast(model, history, n_input)
        # store the predictions
        predictions.append(yhat_sequence)
        # get real observation and add to history for predicting the next timestep
        history.append(test[i, :])
    # evaluate predictions days for each timestep
    predictions = array(predictions)
    test1 = test[:, :, -1]
    YPred = argmax(predictions.reshape(predictions.shape[0], (predictions.shape[1]*predictions.shape[2])), out=None, axis=1)
    YPred = YPred.reshape(YPred.shape[0], 1)
    df = stack((YPred, test1))
    df = df.transpose()
    df = df.reshape(df.shape[1], 2)
    DataFrame(df).to_csv('../Results/'+str(model_name)+'_TL_'+str(exp_num)+'.csv')
    cm = confusion_matrix(test1, YPred)
    print(cm)
    f1 = f1_score(test1, YPred, average='weighted')
    acc = accuracy_score(test1, YPred)
    print(classification_report(test1, YPred))    
    return f1, acc, totTime

#function to evaluate the model
def evaluate_model_tl(train, test, n_input, batch_size, lr, source, exp_num, epochs, model_name, data_percent, n_layers, n_out, batch_norm=False, plot=False):
    # load pretrained model
    model = load_model(model_name)
    #prepare data
    train_x, train_y = to_supervised(train, n_input, step_size=1, n_out=1, is_y=True)
    #data percentage
    train_ind = int(round(len(train_x)*(data_percent)))
    train_x = train_x[-train_ind:, :]
    train_y = train_y[-train_ind:, :]
    # reshape output into [samples, timesteps, features]
    train_y = train_y.reshape((train_y.shape[0], train_y.shape[1], 1))
    train_y =to_categorical(train_y)
    # fix the layers as indicated by the papameter 'layers'
    for layer in model.layers[:-n_layers]:
        layer.trainable = False
    #check trainable status of individual layers
    for layer in model.layers:
        print(layer, layer.trainable)                       
    opt = optimizers.Adam(lr=lr)
    model.compile(loss='categorical_crossentropy', metrics=['acc'], optimizer=opt)
    #model.summary()
    #record time
    tic = time.time()
    # fit network
    history = model.fit(train_x, train_y, epochs=epochs, shuffle=False, batch_size=batch_size, verbose=2) 
    #record time
    toc = time.time()
    totTime = toc-tic
    #model.load_weights('../Models/best_weights_TL.hdf5')
    model.save('../Models/model_TL_'+str(exp_num)+'.h5')
    if plot:
        view_acc(history, str(exp_num))
    
    history = [x for x in train]
    # walk-forward validation over each timestep
    predictions = list()
    for i in range(len(test)):
        # predict the timestep
        yhat_sequence = forecast(model, history, n_input)
        # store the predictions
        predictions.append(yhat_sequence)
        # get real observation and add to history for predicting the next timestep
        history.append(test[i, :])
    # evaluate predictions days for each timestep
    predictions = array(predictions)
    test1 = test[:, :, -1]
    YPred = argmax(predictions.reshape(predictions.shape[0], (predictions.shape[1]*predictions.shape[2])), out=None, axis=1)
    YPred = YPred.reshape(YPred.shape[0], 1)
    df = stack((YPred, test1))
    df = df.transpose()
    df = df.reshape(df.shape[1], 2)
    DataFrame(df).to_csv('../Results/'+str(model_name)+'_TL_'+str(exp_num)+'.csv')
    cm = confusion_matrix(test1, YPred)
    print(cm)
    f1 = f1_score(test1, YPred, average='weighted')
    acc = accuracy_score(test1, YPred)
    print(classification_report(test1, YPred))     
    return f1, acc, totTime


def perform_experiment(model, resFile, file_name, n_test, model_, n_out, verbose, med, high):
    #load experimental config from csv file
    df_exp = read_csv(resFile, header=0)
    #create result dataframe lists
    f1_list, train_time, acc_list = list(), list(), list()
    #iterate through rows and take parameters specified
    for index, row in df_exp.iterrows():
        #Experiment Number
        exp_num = row['Exp. Number']
        #Layer
        n_layer = int(row['Layer'])
        #Lookback
        n_input = int(row['Inputs'])
        #Epochs
        epochs = int(row['Epochs'])
        #Batch Size
        batch_size= int(row['Batch'])
        #Source
        source = int(row['Source'])
        #Target
        target = int(row['Target'])
        #TL type
        tl_type = str(row['TL type'])
        #Data Percent
        data_percent = float(row['Data Percent'])
        #Learning Rate
        lr = float(row['LR'])
        #Source Model Name
        model_name = model_+str(source)+'.h5'        
        # load the new file
        dataset = read_csv(file_name+str(target)+'.csv', header=0, index_col=0)
        #fill NANs
        dataset = dataset.fillna(method='ffill')
        #bin data
        dataset = bin_data(dataset, med, high)
        # split into train and test
        train, test = split_dataset(dataset.values, n_test)        
        #run experiments
        #check if model exists then do TL
        if Path(model_+str(source)+'.h5').is_file():
            print('============= Model Training with TL ===============')
            print('Source', source, 'Target', target)
            print('Data Percent', data_percent)
            print('_____________________________________________________')
            #evaluate model on TL if model does not exist
            if tl_type == 'reuse':
                print('Performing TL')
                score, accuracy, trainTime = evaluate_model_reuse(train, test, n_input, batch_size, lr, source, exp_num, epochs, model_name, data_percent, n_out, batch_norm=False, plot=False)
            elif tl_type == 'fine-tune':
                print('Fine-tuning')
                score, accuracy, trainTime = evaluate_model_tl(train, test, n_input, batch_size, lr, source, exp_num, epochs, model_name, data_percent, n_layer, n_out)
            elif tl_type == 'None':
                print('============= Model Training without TL ===============')
                print('Source', source, 'Target', target)
                print('Data Percent', data_percent)
                score, accuracy, trainTime, _, _, _ = evaluate_model(model, train, test, n_input, source, exp_num)
        else:
            print('============= Model Training without TL ===============')
            print('Source', source, 'Target', target)
            print('Data Percent', data_percent)
            score, accuracy, trainTime, f1_base, acc_base, tr_time_base = evaluate_model(model, train, test, n_input, source, exp_num)
        #append scores
        f1_list.append(array(score).reshape(1,))
        acc_list.append(array(accuracy).reshape(1,))
        train_time.append(array(trainTime).reshape(1,))
        df_res = stack((f1_list, acc_list, train_time)).transpose().reshape(len(train_time),3)
        df_res = DataFrame(df_res, columns = ['F1_Score', 'Accuracy_Score', 'Train Time'])
        #write to original experiment config
        df_exp['F1_Score'], df_exp['Accuracy_Score'], df_exp['Train Time'] = df_res['F1_Score'], df_res['Accuracy_Score'], df_res['Train Time']
        #output to experiment result file
        df_exp.to_csv(resFile, index=False)