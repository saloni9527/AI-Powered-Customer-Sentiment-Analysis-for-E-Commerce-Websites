import matplotlib.pyplot as plt

def show_chart(sentiments):

    labels = ["Positive","Negative","Neutral"]

    values = [

        sentiments.count("Positive"),

        sentiments.count("Negative"),

        sentiments.count("Neutral")

    ]

    plt.bar(labels,values)

    plt.title("Customer Sentiment Analysis")

    plt.show()