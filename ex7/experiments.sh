echo "##############################################################"
echo "\n"
echo "Experiment 1 --k 2 --method KMeans"
python3 my_clustering_universal.py --k 2 --method KMeans
echo "\n"
echo "Experiment 2 --k 3 --method KMeans"
python3 my_clustering_universal.py --k 3 --method KMeans
echo "\n"
echo "Experiment 3 --k 4 --method KMeans"
python3 my_clustering_universal.py --k 4 --method KMeans
echo "##############################################################"
echo "\n"
echo "Experiment 4 --k 2 --method Birch"
python3 my_clustering_universal.py --k 2 --method Birch
echo "\n"
echo "Experiment 5 --k 3 --method Birch"
python3 my_clustering_universal.py --k 3 --method Birch
echo "\n"
echo "Experiment 6 --k 4 --method Birch"
python3 my_clustering_universal.py --k 4 --method Birch
echo "##############################################################"
echo "\n"
echo "Experiment 7 --k 2 --method SpectralClustering"
python3 my_clustering_universal.py --k 2 --method SpectralClustering
echo "\n"
echo "Experiment 8 --k 3 --method SpectralClustering"
python3 my_clustering_universal.py --k 3 --method SpectralClustering
echo "\n"
echo "Experiment 9 --k 4 --method SpectralClustering"
python3 my_clustering_universal.py --k 4 --method SpectralClustering
