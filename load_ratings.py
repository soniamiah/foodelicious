import sys, os
import pandas as pd
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dproj.settings")

import django
django.setup()
from django.contrib.auth.models import User
from blog.models import Rating, User
import matplotlib.pyplot as plt

def save_rating(rate_row):
    rate= Rating()
    rate.id = rate_row[0]
    rate.recipe = rate_row[1]
    rate.rating = rate_row[2]
    rate.user = User.objects.get(id=rate_row[3])
    rate.save()

if __name__ == "__main__":

    # Check number of arguments (including the command name)
    if len(sys.argv) == 2:
        print ("Reading from file" + str(sys.argv[1]))
        rating_df = pd.read_csv(sys.argv[1])
        print(rating_df.describe())
        ratings= pd.DataFrame(rating_df.groupby('recipe')['rating'].mean())
        print (ratings.head())
        ratings['number_of_ratings']= rating_df.groupby('recipe')['rating'].count()
        print (ratings.head())
        plot= ratings['rating'].hist(bins=50)
        plt.show(plot)
        #print (rating_df)


        '''# apply save_review_from_row to each review in the data frame
        rating_df.apply(
            save_rating,
            axis=1
        )

        print ("There are {} reviews in DB".format(Rating.objects.count()))

    else:
        print ("Please, provide Reviews file path")
'''
