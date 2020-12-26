BASEDIR=$(dirname "$0") # get the directory of this file

download_dep() {
    local proto_dep=$1
    folder=${proto_dep//.//} # replace "." with "/"
    filename=$(echo $proto_dep | sed 's/.*\.//') # find the filename (the substring after the last ".")
    echo $folder
    echo $filename

    dest_file=$BASEDIR/dep/$folder/$filename.proto
    github_link=https://raw.githubusercontent.com/RyanAngJY/dop_proto_common/master/$folder/$filename.proto
    
    # Pull file from github:
    curl -o $dest_file -LJ $github_link --create-dirs # create parent dirs locally if don't exist
}

get_config() {
    # Get config from ./dep_proto_common.json file
    # jq is a brew installed library that helps with reading JSON in bash
    # the tr command converts JSON array to bash array by removing angular brackets and commas
    echo $(jq -r '.dep' $BASEDIR/dep_proto_common.json | tr -d '[]," ') 
}

# brew install jq # install required dependency on jq

# Download all deps specified
proto_deps=$(get_config)
for proto_dep in ${proto_deps[@]}; do
    download_dep ${proto_dep}
done
