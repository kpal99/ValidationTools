#echo "running moreCut.sh"
#source moreCut.sh
#wait
#echo
#echo "running ntuple_split.sh"
#source ntuple_split.sh
#wait
#echo
echo "running all_plots_fnal.sh"
source all_plots_fnal.sh
wait
echo
sed -i "s/0,5)/0,3)/" one_histogram.py
echo
echo "running all_plots_fnal.2.sh"
source all_plots_fnal.2.sh
wait
echo
echo "running all_plots_fnal.2_split.sh"
source all_plots_fnal.2_split.sh
wait
sed -i "s/0,3)/0,5)/" one_histogram.py
