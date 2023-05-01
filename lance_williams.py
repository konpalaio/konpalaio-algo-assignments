import sys
#For each element calculate all posible distances and find the minimun
def MinimunDistance(clusters,methodology,cluster_history_dictionary):
    smallest_distance = 9999999
    u_index = -1
    v_index = -1
    for u in range (0, len(clusters) - 1):
        for v in range (u + 1, len(clusters)):
            if len(clusters[u]) == 1 and len(clusters[v]) == 1 :
                distance = abs(clusters[u][0] - clusters[v][0])
            else:
                if len(clusters[u]) != 1:
                    cluster_t = cluster_history_dictionary[str(clusters[u])][0]
                    cluster_s = cluster_history_dictionary[str(clusters[u])][1]
                    cluster_u = clusters[v]
                else:
                    cluster_t = cluster_history_dictionary[str(clusters[v])][0]
                    cluster_s = cluster_history_dictionary[str(clusters[v])][1]
                    cluster_u = clusters[u]
                if methodology == "single":
                    ai = 0.5
                    aj = 0.5
                    c = -0.5
                    dist_tu = 100000
                    for i in cluster_t:
                        for j in cluster_u:
                            if abs(i-j) < dist_tu:
                                dist_tu = abs(i-j)
                    dist_su = 100000
                    for i in cluster_s:
                        for j in cluster_u:
                            if abs(i-j) < dist_su:
                                dist_su = abs(i-j)
                    distance = ai*dist_tu + aj*dist_su + c*abs(dist_tu - dist_su)
                elif methodology == "complete":
                    ai = 0.5
                    aj = 0.5
                    c = 0.5
                    dist_tu = -1
                    for i in cluster_t:
                        for j in cluster_u:
                            if abs(i-j) > dist_tu:
                                dist_tu = abs(i-j)
                    dist_su = -1
                    for i in cluster_s:
                        for j in cluster_u:
                            if abs(i-j) > dist_su:
                                dist_su = abs(i-j)
                    distance = ai*dist_tu + aj*dist_su + c*abs(dist_tu - dist_su)   
                elif methodology == "average":
                    ai = len(cluster_t)/(len(cluster_t)+len(cluster_s))
                    aj = len(cluster_s)/(len(cluster_t)+len(cluster_s))
                    dist_tu = 0
                    for i in cluster_t:
                        for j in cluster_u:
                            dist_tu += abs(i-j)/(len(cluster_t)*len(cluster_u))
                    dist_su = 0
                    for i in cluster_s:
                        for j in cluster_u:
                            dist_su += abs(i-j)/(len(cluster_s)*len(cluster_u))
                    distance = ai*dist_tu + aj*dist_su  
            if distance < smallest_distance:
                smallest_distance = distance
                u_index = u
                v_index = v       
    return u_index, v_index, smallest_distance


methodology = sys.argv[1]
txt = sys.argv[2]
with open(txt) as f:
    numbers = sorted([int(num) for line in f.read().splitlines() for num in line.split()])
clusters = [[num] for num in numbers]
cluster_history_dictionary = {}
while len(clusters) > 1 :
    u_index, v_index, distance = MinimunDistance(clusters, methodology,cluster_history_dictionary)
    cluster_one = clusters[u_index]
    cluster_two = clusters[v_index]
    print("({})({}) {} {}".format(' '.join(map(str, cluster_one)), ' '.join(map(str, cluster_two)), round(float(distance), 2), len(cluster_one) + len(cluster_two)))
    cluster_u = cluster_one + cluster_two
    clusters.append(cluster_u)
    clusters.remove(cluster_one)
    clusters.remove(cluster_two)
    # This cluster dictionary will always now the past state of cluster so we can use the t,s that derive from u as stated in the algorithm
    cluster_history_dictionary.update({str(clusters[len(clusters)-1]):[cluster_one,cluster_two]})
