import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline

TRAINING_PERCENT = 0.6 #60%
FEATURE_TAGS = ['first_letter', 
				'first_2_letters',
				'first_half',
				'last_half',
				'last_2_letters',
				'last_letter',
				 'length_of_name']
#print(FEATURE_TAGS)

def DT_features(given_name):
	#test_given_name = ['corette', 'corey', 'cori', 'corinne', 'william', 'mason', 'jacob', 'zorro'] #small test
	features_list = []
	name_features = [given_name[0], given_name[:2], given_name[:len(given_name)/2], given_name[len(given_name)/2:], given_name[-2:], given_name[-1:], len(given_name)]
	#[['z', 'zo', 'zo', 'rro', 'ro', 'o', 5], ['z', 'zo', 'zo', 'rro', 'ro', 'o', 5]]
	features_list = dict(zip(FEATURE_TAGS, name_features))
	return features_list

def determine_gender(name, pipeline):
	#return male/female for a given name
	return pipeline.predict(DT_features([name]))#[0]

if __name__ == '__main__':
	gender_names_data = pd.read_csv('names_gender.csv')
	gender_names_data = gender_names_data.as_matrix()[1:, :]
	print(len(gender_names_data))

	gender_y = gender_names_data[:, 1]

	DT_features = np.vectorize(DT_features)
	names_x = DT_features(gender_names_data[:, 0]) # generate new list/list array with additional features

	#shuffle to create train/test data
	from sklearn.utils import shuffle
	names_x, gender_y = shuffle(names_x, gender_y)

	x_train = names_x[:int(TRAINING_PERCENT * len(names_x))]
	x_test = names_x[int(TRAINING_PERCENT * len(names_x)):]
	y_train = gender_y[:int(TRAINING_PERCENT * len(gender_y))]
	y_test = gender_y[int(TRAINING_PERCENT * len(gender_y)):]

	#classifier
	#TODO: update with better model for testing (currently ~85% on testing, ~99% on training)
	#TOD: shrink dataset to run faster
	vectorizer = DictVectorizer()
	dtc = DecisionTreeClassifier()
	pipeline = Pipeline([('dict', vectorizer), ('dtc', dtc)])
	pipeline.fit(x_train, y_train)

	#Accuracy
	print("Accuracy on training: {0}".format(pipeline.score(x_train, y_train)))
	print("Accuracy on testing: {0}".format(pipeline.score(x_test, y_test)))

	#testing on novel names
	test_name = "Dejah"
	print("The name '{0}' is most likely {1}".format(test_name, determine_gender(test_name, pipeline)))
