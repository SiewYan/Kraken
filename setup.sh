# Where does stuff come from

myRoot=/home/cmsprod
pkgRoot=/home/cmsprod/Tools

# Other packages needed
source $pkgRoot/Dools/setup.sh
source $pkgRoot/FiBS/setup.sh
source $pkgRoot/T2Tools/setup.sh paus paus
# bad fix but needed so curl works with cmsweb
source /cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/curl/7.47.1/etc/profile.d/init.sh
source /cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/openssl/1.0.2d/etc/profile.d/init.sh

# Kraken parameters (edit as needed)

# for the agents
export KRAKEN_USER=cmsprod
export KRAKEN_GROUP=zh

# user for submit (can be different from Tier-3)
export KRAKEN_BASE=$pkgRoot/Kraken
export KRAKEN_WORK=$myRoot/cms/jobs
export KRAKEN_SCRIPT=releaseKraken.sh
export KRAKEN_EXE=cmsRun
export KRAKEN_CMSSW=$myRoot/cms/cmssw
export KRAKEN_REMOTE_USER=paus

export KRAKEN_SE_BASE=/cms/store/user/paus
export KRAKEN_CATALOG_INPUT=/home/cmsprod/catalog/t2mit
export KRAKEN_CATALOG_OUTPUT=/home/cmsprod/catalog/t2mit
export KRAKEN_TMP_PREFIX='tmp_0_'

export PATH=${PATH}:${KRAKEN_BASE}/bin
export PYTHONPATH=${PYTHONPATH}:${KRAKEN_BASE}/python
