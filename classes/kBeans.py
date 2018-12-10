class kBeans:
    def __init__(self, data, k):
        self.data = data
        self.k = k
        # Mr kBeans has many GFs, each one represent the centroid od a cluster.
        # in each iteration of the re-clustering, the centroids will move toward the mean of elements for each cluster.
        # and we compare if the GFs are similar to the previous ones (X_GFs), so we stop the iteration.
        self.GF = []
    
        # max re-clustering repetitions
        self.ENOUGH_THANX = 1000

        self.STOP_IT_NOW = False
        # we have set measurement for checking the similarity of the GFs (centroids)
        self.CLOSE_ENOGUH = 0.000001
        
        # set centroids in the first step of clustering, this could be random or whatever we want.
        for i in range(0, k):
            self.GF.append(data.iloc[i*101])

        # keep the previous centroids (X_GFs) to check when they are almost stable 
        self.X_GF = [[] for i in range(k)] 

        self.iterations = 0
        
        self.labels_ = []
        
    def fit(self):
        while not self.STOP_IT_NOW:
            self.iterations += 1

            clusters = [[] for i in range(self.k)]

            # assign data points to clusters
            clusters = self.dist(clusters)

            # recalculate centroids
            index = 0
            for cluster in clusters:
                self.X_GF[index] = self.GF[index]
                self.GF[index] = np.mean(cluster, axis=0).tolist()
                index += 1
            if self.allSame():
                self.STOP_IT_NOW = True

        
        ii = 0
        clusterDisct = {}
        for cluster in clusters:
            clusterDisct[ii] = cluster
            ii +=1

        
                      
    # Calculates the distance between each data point and every centroids:      
    def dist(self, clusters):
        self.labels_ = []
        for ind, x in self.data.iterrows():  
            # Find nearest centroid (GF) and attach to its cluster.
            mu_index = min([(i[0], distance.euclidean(x,self.GF[i[0]])) \
                                for i in enumerate(self.GF)], key=lambda t:t[1])[0]
            try:
                clusters[mu_index].append(x)
            except KeyError:
                clusters[mu_index] = [x]
            
            # labels_ will return list of data points represtend by the number of cluster they belong to
            self.labels_.append(mu_index)

      
        for cluster in clusters:
            if not cluster:
                cluster.append(data[np.random.randint(0, len(data), size=1)].flatten().tolist())

        return clusters
    
        # check if GFs are similar to the X_GFs (centroids are stable over the this iteration)
    def allSame(self):

        if self.iterations > self.ENOUGH_THANX:
            return True
        if np.sum(np.subtract(self.GF, self.X_GF)/self.X_GF *100.0) <= self.CLOSE_ENOGUH:
            return True
        return False