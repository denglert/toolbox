#!/bin/bash

# - Utility script
replaceAllOccurrences()
{
	if [ "$#" -ne 2 ];
	then
		echo "Usage:"
		echo "replaceAllOccurrences string_to_be_replace new_string"
	else

	OLD=$1
	NEW=$2

	echo "Replacing ${OLD} with ${NEW}"

	# - Rename files
	#find . -depth -name "*${OLD}*" -exec bash -c "for f; do base=${f##*/}; mv -- $f ${f%/*}/${base//${OLD}/${NEW}}; done" _ {} +

	# - First rename directories specifically
	find . -depth -type d -not -path "*/.git/*" -iname "*${OLD}*"  -exec rename "s@${OLD}@${NEW}@g" {} +

	# - 
	find . -depth -not -path "*/.git/*" -name "*${OLD}*" -exec rename "${OLD}" "${NEW}" '{}' \;

	# - Replace within contents of the file
	find . -type f -not -path "*/.git/*" -exec sed -i "s/${OLD}/${NEW}/g" {} +
	fi
}
