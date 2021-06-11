#!/bin/bash

BASEDIR=$(dirname "$0") # get the directory of this file
BRANCH_NAME=$1

download_dep() { # download git folder using svn
    local dep_proto=$1
    local branch=$2
    if [[ "$branch" == "" ]]; then
        branch="master"
    fi

    folder=${dep_proto//.//} # replace "." with "/"
    dest_folder=$BASEDIR/dep/$folder 

    echo "Downloading dependency for $folder into $dest_folder for branch=$branch"

    if [[ "$branch" == "master" ]]; then
        svn export https://github.com/RyanAngJY/dop_proto_common/trunk/$folder $dest_folder --force
    else
        svn export https://github.com/RyanAngJY/dop_proto_common/branches/$branch/$folder $dest_folder --force
    fi
}

get_config() {
    # Get config from ./dep_proto_common.json file
    # jq is a brew installed library that helps with reading JSON in bash
    # the tr command converts JSON array to bash array by removing angular brackets and commas
    echo $(jq -r '.dep' $BASEDIR/dep_proto_common.json | tr -d '[]," ') 
}

# brew install jq # install required dependency on jq

# Download all deps specified
dep_protos=$(get_config)
for dep_proto in ${dep_protos[@]}; do
    download_dep ${dep_proto} $BRANCH_NAME
done






# ===== This is for downloading the file directly ======
# download_dep() {
#     local dep_proto=$1
#     folder=${dep_proto//.//} # replace "." with "/"
#     filename=$(echo $dep_proto | sed 's/.*\.//') # find the filename (the substring after the last ".")
#     echo $folder
#     echo $filename

#     dest_file=$BASEDIR/dep/$folder/$filename.proto
#     github_link=https://raw.githubusercontent.com/RyanAngJY/dop_proto_common/master/$folder/$filename.proto
    
#     # Pull file from github:
#     curl -o $dest_file -LJ $github_link --create-dirs # create parent dirs locally if don't exist
# }
