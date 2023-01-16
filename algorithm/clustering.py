
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

# --------------- Datasceince libraries -----------

from sklearn.datasets import make_blobs
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from scipy.spatial import distance


from algorithm.match import normalise


def cluster(keys, names, corpus):

	# > initialise TF-IDF vectorizer, removing stopwords (again)
	# > object used to find TF-IDF values of the items in corpus

	vectorizer = TfidfVectorizer(
		lowercase = True,
		max_df = 0.7,
		min_df = 2,
		#ngram_range = (1, 3),
		# max_features = 100,
		stop_words="english",
	)

	# > recieve the vectors, 
	vectors = vectorizer.fit_transform(corpus)
	feature_names = vectorizer.get_feature_names()

	# > itialising step to get keywords, used for visualising and identifying
	# clusters
	dense = vectors.todense()
	denselist = dense.tolist()

	# --- Used to get keywords of each cluster ----------------------#

	all_keywords = []

	for description in denselist:
		x = 0
		keywords = []
		for word in description:
			if word > 0:
				keywords.append(feature_names[x])
			x = x + 1
		
		all_keywords.append(keywords)
			
	# print(all_keywords[0])
	# ---------------------------------------------------------------#

	# > k-value for the kmeans object
	true_k = 3

	# > initialising kmeans model
	model = KMeans(
		n_clusters = true_k, 
		init="k-means++", 
		max_iter=100, 
		n_init=1
	)

	# > combining vectors into model
	model.fit(vectors)

	# order_centroids = model.cluster_centers_.argsort()[:, ::-1]
	# terms = vectorizer.get_feature_names()

	# dimesnions
	# print(len(vectors.toarray()))

	# for i in range(true_k):
	# 	print("Cluster",i,"\n")
		
	# 	for ind in order_centroids[i, :10]:
	# 		print(terms[ind])
	# 	print("\n")
			
	# --------- Finding Disatnce - getting COORD -------------------#

	kmean_indices = model.fit_predict(vectors)

	# reduce dimensionality using Principle Componenet Analysis
	pca = PCA(n_components = 2)
	scatter_plot_points = pca.fit_transform(vectors.toarray())

	# ------------------- Helper code for visualising ----------------#

	colors = ["r", "b", "y", "c", 'm']

	x_axis = [o[0] for o in scatter_plot_points]
	y_axis = [o[1] for o in scatter_plot_points]

	fig, ax = plt.subplots(figsize=(5, 5))

	ax.scatter(x_axis, y_axis, c=[colors[d] for d in kmean_indices])

	coord = {}

	for i, txt in enumerate(names):
		ax.annotate(txt, (x_axis[i], y_axis[i]))
		
		coord[txt] = [x_axis[i], y_axis[i]]

	# > uncomment, run = recieve cluster image (appendix in dissertation)
	#fig.savefig('cluster.png')

	# ------------------------------------------------------# 

	# > talent first point, due to index in corpus
	talent = scatter_plot_points[0]

	# > initalise list to store all distances from Events to Talent
	dst_from_tal = []

	# > calculate distance, add to dst_from_tal
	for i in range(len(scatter_plot_points)):
		dst = distance.euclidean(talent, scatter_plot_points[i])
		dst_from_tal.append([keys[i], names[i], dst])

	# > create dataframe, slice first row, sort values by closeness (and therefor similarity)
	df = pd.DataFrame(data=dst_from_tal, columns=["ID", "Venue", "Dst"]).iloc[1:]
	df = df.sort_values(by="Dst", ascending=True)

	# > recieve first 4, this is a limitation that is discussed in the evaluation of the dissertation
	df = df.iloc[:4]

	return(df)

	#return df

# >>>>> Unused normalisation code - last minute problems resulted in its removal
# >>>>> with more time, this would be improved 
# arr = []

# 	# > for each value add to array
# 	for val in df["Dst"].values.tolist():
# 		arr.append(val)

# 	arr_total = 0  
# 	norm_arr = []

# 	for val in arr:
# 		arr_total += val

# 	for val2 in arr:
# 		norm_arr.append(val2/arr_total)

# 	df['Normalised'] = norm_arr

# 	#print(df)#, arr_total, total)



	

