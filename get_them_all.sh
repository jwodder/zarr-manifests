#!/bin/bash

set -eu

set -x

rm -rf  times manifests
mkdir -p times manifests

# needs config
#s3cmd -c ~/.s3cfg-dandi-backup ls s3://dandiarchive/zarr/ \
#	| while read _ zarr; do
#	z=${zarr%*/}
#	z=${z##*/}

p=s3://dandiarchive/zarr
aws --no-sign-request s3 ls $p/ \
	| while read _ zarr; do
	z=${zarr%*/}
	time ./list_bucket_prefix_versionids.py $p/$zarr > manifests/$z.json 2>times/$z.out
	break
done
