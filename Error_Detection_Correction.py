class Cluster:
    def __init__(self, fileName):
        self.fileName = fileName
    def clusterFun(self):
        try:
            clusters, threshold = self.read_clusters_from_file(self.fileName)

            # Identify errors in all clusters
            identified_errors = []
            for i, cluster in enumerate(clusters):
                dominant_strand = max(cluster, key=cluster.count)
                error_candidates = [strand for strand in cluster if strand != dominant_strand]
                error_rate = len(error_candidates) / len(cluster)
                if error_rate > threshold:
                    identified_errors.append((i, error_candidates))

            flag = -1

            # Output clusters to a file
            output_filename = self.fileName[:-4]+'_output.txt'
            print(output_filename)
            with open(output_filename, 'w') as output_file:
                # Print the identified errors
                for cluster_index, error_candidates in identified_errors:
                    output_file.write(f"\nCluster {cluster_index} has the following error candidates:\n")
                    for error_strand in error_candidates:
                        output_file.write(''.join(error_strand) + '\n')
                        flag = 1
                    output_file.write('\n')

                if flag == -1:
                    output_file.write("No errors were identified.\n")
                else:
                    # Correct identified errors in all clusters
                    corrected_clusters = self.correct_errors_in_clusters(clusters, threshold)

                    # Print the corrected clusters to the file
                    for i, corrected_cluster in enumerate(corrected_clusters):
                        output_file.write(f"\nCluster {i + 1} after error correction:\n")
                        for corrected_strand in corrected_cluster:
                            output_file.write(''.join(corrected_strand) + '\n')
                        output_file.write('\n')

            print(f"Output written to {output_filename}.")
            return 1
        except:
            return 0

    # Function to identify errors and correct them in each cluster
    def correct_errors_in_cluster(self,cluster, threshold=0.5):
        dominant_strand = max(cluster, key=cluster.count)
        corrected_cluster = []

        for strand in cluster:
            errors = 0
            corrected_strand = []

            # Compare each bit in the strand with the dominant strand
            for i in range(len(strand)):
                if strand[i] != dominant_strand[i]:
                    errors += 1
                    corrected_strand.append(dominant_strand[i])
                else:
                    corrected_strand.append(strand[i])

            # If the error rate is above the threshold, correct the strand
            if errors / len(strand) > threshold:
                corrected_cluster.append(corrected_strand)
            else:
                corrected_cluster.append(strand)

        return corrected_cluster

    # Function to identify errors and correct them in all clusters
    def correct_errors_in_clusters(self,clusters, threshold=0.5):
        corrected_clusters = []

        for cluster in clusters:
            corrected_cluster = self.correct_errors_in_cluster(cluster, threshold)
            corrected_clusters.append(corrected_cluster)

        return corrected_clusters

    # Function to read clusters from a file
    def read_clusters_from_file(self,filename):
        with open(filename, 'r') as file:
            clusters = []
            num_clusters = int(file.readline().strip())
            for i in range(num_clusters):
                cluster = []
                num_strands = int(file.readline().strip())

                for j in range(num_strands):
                    strand_input = file.readline().strip()
                    cluster.append(list(strand_input))

                clusters.append(cluster)

            # Read dominance property threshold from the last line
            threshold = float(file.readline().strip())

        return clusters, threshold

