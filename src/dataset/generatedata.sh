#!/usr/bin/env bash

echo "Running generation script"
python ./generate_dataset.py

echo " data summary script"

python ./datasummary.py

if [ ${outputdir} ]
    then
        outputdir="${outputdir}/output";
else
    outputdir="./output/"
fi

if [ ${s3bucket} ]
    then
    echo "copying output to s3 bucket ${s3bucket}"
    aws s3 cp ${outputdir}/output.csv.gz ${s3bucket}/dgadataset/ --quiet
fi
