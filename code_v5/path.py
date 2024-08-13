import matplotlib.pyplot as plt
import sklearn.metrics as metrics
ENV = "DEV"
PATH = "C:/Users/NicolasBocage/Documents/projet/test/"
PATH_TO_CACHE = PATH+"cache/"
PARTICIPANT_URL = PATH_TO_CACHE+"participants/"
PATH_TO_DATASETS = PATH_TO_CACHE+"datasets/"

directory_encode= "2021_2023_attele_bis" #"2020_2023" # "short_for_dev" 
DATASET="2020_2024_bis"#"reduced"
DATASET_TEST= "2020_2024_test_bis"# "2024_test" #"short_dev_test"#

def div_time(date,delay=0):
    nombre_de_mois_par_div=1
    year=int(date[4:8])
    div=int(int(date[2:4])/nombre_de_mois_par_div)+delay
    while div<1:
        year=year-1
        div=int(div+(12/nombre_de_mois_par_div))
    return str(year)+str(div)


def plot_ROC(y_test, probs):
    # Plot ROC Curve
    fpr, tpr, _ = metrics.roc_curve(y_test, probs)
    roc_auc = metrics.auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()

# Function to display probabilities
def display_prob(probabilities, y_test):
    res = [[0, 0] for _ in range(100)]
    for i in range(len(probabilities)):
        if int(probabilities[i] * 100) in range(100):
            if y_test[i] == 1:
                res[int(probabilities[i] * 100)][0] += 1
            else:
                res[int(probabilities[i] * 100)][1] += 1

    i = 0.5
    x = []
    y = []
    for r in res:
        if r[0] + r[1] > 10:
            x.append(i)
            y.append(r[0] / (r[0] + r[1]))
        i += 1
    plt.plot(x, y)
    plt.plot(x,[a/100 for a in x],color='orange')
    plt.show()

# Function to plot probabilities
def plotProbas(pred):
    winner_proba = [res * 100 for res in pred]
    plt.hist(winner_proba, bins=[i for i in range(100)])
    plt.show()

# import pandas as pd
# df=pd.read_csv(PATH+directory_encode+'/X_test.csv')
# print(df.iloc[:, 133])
