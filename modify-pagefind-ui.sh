#!/bin/bash

# Path to the pagefind-ui.js file
FILE="_site/pagefind/pagefind-ui.js"

# Original expression to find
ORIGINAL_EXPRESSION='placeholder:"Search",clear_search:"Clear"'

# Replacement expression
NEW_EXPRESSION='placeholder:"can\'t steer unless already moving",clear_search:"infoBAG"'

# Use sed to perform the replacement, escaping special characters in the new expression
sed -i "s/$ORIGINAL_EXPRESSION/$(echo "$NEW_EXPRESSION" | sed 's/[\&/]/\\&/g')/g" "$FILE"

echo "Replacement complete."
