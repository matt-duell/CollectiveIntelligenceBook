from math import sqrt,pow

#returns a distance based similarity score for person 1 and person 2 using the ecludian distance to calculate similarity.
# 1 = same preferences
# 0 = nothing in common
# somewhere in between will give an idea how much is in common / how much is not in common
def sim_distance(prefs,person1,person2):
	#Keep track of the shared items
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1
	#return 0 if there are no commonalities
	if len(si)==0: 
		return 0

	#Add up the suares of all the differences
	sum_of_squares=sum([	pow(prefs[person1][item]-prefs[person2][item],2) for item in si	])

	#return difference. adding 1 to ensure a div by 0 is avoided
	return 1/(1+sqrt(sum_of_squares))
	
#Returns the similarity score for person 1 and person 2 using the Pearson Correlation coefficient.
#	http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
#	Returns a value between -1 and 1
#	1 = exact same rating for every item considered (positive correlation)
#	0 = no correlation
#	-1 = negative correlation
def sim_pearson(prefs,p1,p2):
	#Keep track of shared items
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item]=1
	n = len(si)

	#return 0 if there are no commonalities
	if n==0: 
		return 0
	
	#Add up the preferences for each user separately
	sum1= sum([ prefs[p1][item] for item in si ])
	sum2= sum([ prefs[p2][item] for item in si ])

	#add up the squares for each user separately

	sum1Sq = sum([ pow(prefs[p1][item],2) for item in si])	
	sum2Sq = sum([ pow(prefs[p2][item],2) for item in si])
		
	#sum up the products
	prodSum = sum([	prefs[p1][item] * prefs[p2][item] for item in si ])

	#Calculate the pearson score
	num = prodSum-(sum1*sum2/n)
	den = sqrt(	(sum1Sq - pow(sum1,2)/n ) * ( sum2Sq - pow(sum2,2)/n )	)
	if den==0: return 0
	r = num/den

	return r
	
#Returns the best matches for person from the prefs dictionary.  i.e. returns the other person who is the most similar to the selected person
def topMatches (prefs,person,n=5,similarity=sim_pearson):
	scores= [ (similarity(prefs,person,other), other) for other in prefs if other!=person]

	scores.sort()
	scores.reverse()
	return scores[0:n]
		

#A dictionary of movie critics and their ratings on a small set of movies
critics={
	'Lisa Rose': {'Lady in the Water': 2.5,'Snakes on a Plane':3.5,'Just My Luck':3.0,'Superman Returns': 3.5,'You,Me and Dupree':2.5,'The Night Listener':3.0},
	'Gene Seymour': {'Lady in the Water': 3.0,'Snakes on a Plane':3.5,'Just My Luck':1.5,'Superman Returns': 5.0,'You,Me and Dupree':3.5,'The Night Listener':3.0},
	'Michael Phillips': {'Lady in the Water': 2.5,'Snakes on a Plane':3.0,'Superman Returns': 3.5,'The Night Listener':4.0},
	'Claudia Puig': {'Snakes on a Plane':3.5,'Just My Luck':3.0,'Superman Returns': 4.0,'You,Me and Dupree':2.5,'The Night Listener':4.5},
	'Mick LaSalle': {'Lady in the Water': 3.0,'Snakes on a Plane':4.0,'Just My Luck':2.0,'Superman Returns': 3.0,'You,Me and Dupree':2.0,'The Night Listener':3.0},
	'Jack Matthews': {'Lady in the Water': 3.0,'Snakes on a Plane':4.0,'Superman Returns': 5.0,'You,Me and Dupree':3.5,'The Night Listener':3.0},
	'Toby': {'Snakes on a Plane':4.5,'Superman Returns': 4.0,'You,Me and Dupree':1.0}
	}