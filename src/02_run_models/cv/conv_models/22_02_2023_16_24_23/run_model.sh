#!/bin/bash

notebook=$1
sbatch <<EOT
#!/bin/bash

#SBATCH --partition=compute
#SBATCH --account=uo1075
#SBATCH --nodes=1
#SBATCH --time=08:00:00
#SBATCH --job-name $notebook
#SBATCH --error ${notebook}.err
#SBATCH --output ${notebook}.out

source activate CNN
jupyter nbconvert --to notebook --execute $notebook

exit 0
EOT



